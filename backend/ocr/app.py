# app.py
from flask import Flask, render_template, request, jsonify
from verifier import CertificateVerifier
from database import session

app = Flask(__name__)

# Initialize the verifier with the database session
verifier = CertificateVerifier(session)

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Check if file part exists
    if "file" not in request.files:
        return jsonify({
            "extracted_data": {"name": None, "certificate_id": None, "institution": None},
            "verification": {"success": False, "message": "No file part in request"}
        }), 200

    file = request.files["file"]
    if file.filename == "":
        return jsonify({
            "extracted_data": {"name": None, "certificate_id": None, "institution": None},
            "verification": {"success": False, "message": "No file selected"}
        }), 200

    try:
        # Run OCR + verification
        success, message, extracted_data = verifier.verify_file(file)

        # Ensure extracted_data is always a dict with required keys
        extracted_data = {
            "name": extracted_data.get("name"),
            "certificate_id": extracted_data.get("certificate_id"),
            "institution": extracted_data.get("institution")
        }

        return jsonify({
            "extracted_data": extracted_data,
            "verification": {
                "success": success,
                "message": message
            }
        }), 200

    except Exception as e:
        # Catch any unexpected errors and return JSON
        return jsonify({
            "extracted_data": {"name": None, "certificate_id": None, "institution": None},
            "verification": {"success": False, "message": f"Error: {str(e)}"}
        }), 200

if __name__ == "__main__":
    app.run(debug=True)
