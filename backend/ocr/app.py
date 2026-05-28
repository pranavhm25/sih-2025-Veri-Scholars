# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from verifier import CertificateVerifier
from database import session, VerificationLog, SecurityAlert, Certificate
import pandas as pd
import os
import uuid
import io
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Serve the frontend directory statically
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='/')

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

CORS(app)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize the verifier with the database session
verifier = CertificateVerifier(session)

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

# --- Async Task Queue Setup ---
executor = ThreadPoolExecutor(max_workers=4)
jobs = {}
jobs_lock = threading.Lock()
JOB_TTL_SECONDS = 3600  # 1 hour

def _sweep_stale_jobs():
    """Background daemon that removes jobs older than JOB_TTL_SECONDS every 5 minutes."""
    while True:
        time.sleep(300)  # Run every 5 minutes
        cutoff = time.time() - JOB_TTL_SECONDS
        with jobs_lock:
            stale_ids = [jid for jid, jdata in jobs.items() if jdata.get("created_at", 0) < cutoff]
            for jid in stale_ids:
                del jobs[jid]

_sweeper_thread = threading.Thread(target=_sweep_stale_jobs, daemon=True)
_sweeper_thread.start()

class DummyFileStorage:
    def __init__(self, stream, filename):
        self.stream = stream
        self.filename = filename
        
    def read(self, *args, **kwargs):
        return self.stream.read(*args, **kwargs)

def process_upload_background(job_id, file_bytes, filename):
    try:
        dummy_file = DummyFileStorage(io.BytesIO(file_bytes), filename)
        success, message, anomaly_reasons, extracted_data = verifier.verify_file(dummy_file)
        with jobs_lock:
            jobs[job_id] = {
                "status": "completed",
                "created_at": time.time(),
                "result": {
                    "success": success,
                    "message": message,
                    "anomaly_reasons": anomaly_reasons,
                    "extracted_data": extracted_data
                }
            }
    except Exception as e:
        with jobs_lock:
            jobs[job_id] = {
                "status": "failed",
                "created_at": time.time(),
                "result": {
                    "success": False,
                    "message": f"Server Error: {str(e)}",
                    "anomaly_reasons": [],
                    "extracted_data": {}
                }
            }
    finally:
        # Cleanup the thread-local session for this background thread
        session.remove()

# --- Routes ---

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/verify/manual", methods=["POST"])
@limiter.limit("5 per minute")
def verify_manual():
    data = request.json
    cert_id = data.get('certificate_id')
    name = data.get('name')

    if not cert_id or not name:
        return jsonify({"success": False, "message": "Missing criteria"}), 400

    success, message, anomaly_reasons, extracted_data = verifier.verify_manual(cert_id, name)
    
    return jsonify({
        "success": success,
        "message": message,
        "anomaly_reasons": anomaly_reasons,
        "extracted_data": extracted_data
    }), 200

@app.route("/api/verify/upload", methods=["POST"])
@limiter.limit("5 per minute")
def upload():
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"success": False, "message": f"File type '{ext}' not allowed. Accepted: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    # Validate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)     # Reset to beginning
    if file_size > MAX_FILE_SIZE:
        return jsonify({"success": False, "message": f"File too large ({file_size // (1024*1024)}MB). Maximum is 10MB."}), 400

    try:
        # Read file into memory so it survives the request context
        file_bytes = file.read()
        filename = file.filename
        
        job_id = str(uuid.uuid4())
        with jobs_lock:
            jobs[job_id] = {"status": "processing", "created_at": time.time()}
        
        # Submit to background worker
        executor.submit(process_upload_background, job_id, file_bytes, filename)
        
        return jsonify({
            "success": True,
            "message": "Upload received, processing in background.",
            "job_id": job_id
        }), 202

    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Server Error: {str(e)}",
        }), 500

@app.route("/api/verify/status/<job_id>", methods=["GET"])
def get_job_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return jsonify({"success": False, "message": "Job not found"}), 404
        
        if job["status"] == "processing":
            return jsonify({"status": "processing"}), 200
        
        # Once retrieved, delete the job to free memory.
        result = jobs.pop(job_id)
    return jsonify({"status": result["status"], "result": result["result"]}), 200

@app.route("/api/dashboard/stats", methods=["GET"])
def get_stats():
    # Basic aggregation
    total_logs = session.query(VerificationLog).count()
    success_logs = session.query(VerificationLog).filter_by(status_result='success').count()
    failed_logs = session.query(VerificationLog).filter_by(status_result='failed').count()
    records_issued = session.query(Certificate).count()
    
    # Security metrics
    critical_alerts = session.query(SecurityAlert).filter_by(severity='Critical').count()
    total_alerts = session.query(SecurityAlert).count()

    trust_score = round((success_logs / total_logs * 100), 1) if total_logs > 0 else 100.0

    return jsonify({
        "records_issued": records_issued,
        "total_verifications": total_logs,
        "forged_attempts": failed_logs,
        "trust_score": trust_score,
        "critical_alerts": critical_alerts,
        "total_security_alerts": total_alerts,
    }), 200

@app.route("/api/dashboard/bulk-upload", methods=["POST"])
def bulk_upload():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"success": False, "message": "Only CSV files are supported for bulk upload"}), 400

    try:
        df = pd.read_csv(file)
        # Expected columns
        required_cols = {'certificate_id', 'name', 'institution'}
        if not required_cols.issubset(df.columns):
            return jsonify({"success": False, "message": f"CSV must contain at least: {', '.join(required_cols)}"}), 400

        inserted_count = 0
        for _, row in df.iterrows():
            cert_id = str(row.get('certificate_id')).strip()
            
            # Skip if already exists
            if session.query(Certificate).filter_by(certificate_id=cert_id).first():
                continue

            cert = Certificate(
                certificate_id=cert_id,
                name=str(row.get('name')).strip(),
                roll_number=str(row.get('roll_number', '')).strip(),
                institution=str(row.get('institution')).strip(),
                course=str(row.get('course', '')).strip(),
                year=str(row.get('year', '')).strip(),
                doc_hash=str(row.get('doc_hash', '')).strip() if pd.notna(row.get('doc_hash')) else None
            )
            session.add(cert)
            inserted_count += 1
            
        session.commit()
        return jsonify({
            "success": True, 
            "message": f"Records parsed successfully. Inserted {inserted_count} new certificates.", 
            "inserted_count": inserted_count
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"success": False, "message": f"Failed to process CSV: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
