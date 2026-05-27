# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from verifier import CertificateVerifier
from database import session, VerificationLog, SecurityAlert, Certificate
import pandas as pd
import os

# Serve the frontend directory statically
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='/')

CORS(app)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize the verifier with the database session
verifier = CertificateVerifier(session)

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
        success, message, anomaly_reasons, extracted_data = verifier.verify_file(file)

        return jsonify({
            "success": success,
            "message": message,
            "anomaly_reasons": anomaly_reasons,
            "extracted_data": extracted_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Server Error: {str(e)}",
            "anomaly_reasons": [],
            "extracted_data": {}
        }), 500

@app.route("/api/dashboard/stats", methods=["GET"])
def get_stats():
    # Basic aggregation
    total_logs = session.query(VerificationLog).count()
    success_logs = session.query(VerificationLog).filter_by(status_result='success').count()
    failed_logs = session.query(VerificationLog).filter_by(status_result='failed').count()
    records_issued = session.query(Certificate).count()
    
    trust_score = round((success_logs / total_logs * 100), 1) if total_logs > 0 else 100.0

    return jsonify({
        "records_issued": records_issued,
        "total_verifications": total_logs,
        "forged_attempts": failed_logs,
        "trust_score": trust_score,
    }), 200

@app.route("/api/dashboard/bulk-upload", methods=["POST"])
def bulk_upload():
    # Simulated response
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    return jsonify({"success": True, "message": "Records parsed and inserted successfully", "inserted_count": 124}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
