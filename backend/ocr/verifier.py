# verifier.py
import hashlib
import hmac
import os
import re
from OCRProcessor import OCRProcessor
from database import session, Certificate, VerificationLog, SecurityAlert
from flask import request

# Secret key for HMAC-SHA256 document hashing.
# In production, set the VERI_HASH_SECRET environment variable.
HASH_SECRET = os.environ.get("VERI_HASH_SECRET", "veri-scholars-dev-key-change-in-production").encode("utf-8")

# --- Input validation constants ---
MAX_CERT_ID_LENGTH = 50
MAX_NAME_LENGTH = 150
CERT_ID_PATTERN = re.compile(r'^[A-Za-z0-9\-\.]+$')  # Alphanumeric, hyphens, dots
NAME_PATTERN = re.compile(r'^[A-Za-z\s\.\-\']+$')     # Letters, spaces, dots, hyphens, apostrophes


class CertificateVerifier:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def _sanitize_cert_id(cert_id):
        """Validate and sanitize certificate ID input."""
        if not cert_id or not isinstance(cert_id, str):
            return None, "Certificate ID is required"
        cert_id = cert_id.strip()
        if len(cert_id) > MAX_CERT_ID_LENGTH:
            return None, f"Certificate ID exceeds maximum length of {MAX_CERT_ID_LENGTH} characters"
        if not CERT_ID_PATTERN.match(cert_id):
            return None, "Certificate ID contains invalid characters"
        return cert_id, None

    @staticmethod
    def _sanitize_name(name):
        """Validate and sanitize name input."""
        if not name or not isinstance(name, str):
            return None, "Name is required"
        name = " ".join(name.strip().split())  # Normalize whitespace
        if len(name) > MAX_NAME_LENGTH:
            return None, f"Name exceeds maximum length of {MAX_NAME_LENGTH} characters"
        if not NAME_PATTERN.match(name):
            return None, "Name contains invalid characters"
        return name, None

    def _get_client_ip(self):
        try:
            # Support reverse-proxy setups (e.g. behind Nginx/Gunicorn)
            if request.headers.get("X-Forwarded-For"):
                return request.headers["X-Forwarded-For"].split(",")[0].strip()
            return request.remote_addr
        except:
            return "127.0.0.1"

    def _get_user_agent(self):
        try:
            return request.headers.get("User-Agent", "Unknown")
        except:
            return "Unknown"

    def _log_verification(self, endpoint, cert_id, status, score):
        ip = self._get_client_ip()
        log = VerificationLog(endpoint_used=endpoint, cert_id_searched=cert_id, ip_address=ip, status_result=status, confidence_score=score)
        self.session.add(log)
        self.session.commit()
    
    def _log_alert(self, cert_id, risk_factor, severity="High"):
        ip = self._get_client_ip()
        user_agent = self._get_user_agent()
        alert = SecurityAlert(
            severity=severity,
            cert_id_used=cert_id,
            risk_factor=risk_factor,
            ip_address=ip,
            user_agent=user_agent
        )
        self.session.add(alert)
        self.session.commit()

    def _compute_hash(self, file_stream):
        """Compute HMAC-SHA256 keyed hash of the document for tamper-proof verification."""
        file_stream.seek(0)
        mac = hmac.new(HASH_SECRET, digestmod=hashlib.sha256)
        for chunk in iter(lambda: file_stream.read(4096), b""):
            mac.update(chunk)
        file_stream.seek(0)
        return mac.hexdigest()

    def _mask_name(self, name):
        """Masks a name for public query (e.g. Aditi Sharma -> A**** S*****)."""
        if not name:
            return "Unknown"
        parts = name.split(" ")
        masked = []
        for p in parts:
            if len(p) > 1:
                masked.append(p[0] + ("*" * (len(p)-1)))
            else:
                masked.append(p)
        return " ".join(masked)

    def _is_fuzzy_match(self, name_a, name_b, threshold=0.8):
        import difflib
        if not name_a or not name_b:
            return False
        # Clean names slightly for comparison (lowercase and strip extra whitespaces)
        clean_a = " ".join(name_a.lower().split())
        clean_b = " ".join(name_b.lower().split())
        
        # Exact substring match
        if clean_a in clean_b or clean_b in clean_a:
            return True
            
        # Fuzzy match
        ratio = difflib.SequenceMatcher(None, clean_a, clean_b).ratio()
        return ratio >= threshold

    def verify_manual(self, cert_id, name):
        """
        Verify manually entered details against DB.
        """
        # Sanitize inputs
        cert_id, id_err = self._sanitize_cert_id(cert_id)
        if id_err:
            self._log_alert(cert_id or "INVALID", f"Input rejected: {id_err}", severity="Medium")
            return False, id_err, ["Invalid input provided"], {}

        name, name_err = self._sanitize_name(name)
        if name_err:
            self._log_alert(cert_id, f"Input rejected: {name_err}", severity="Medium")
            return False, name_err, ["Invalid input provided"], {}

        cert = self.session.query(Certificate).filter_by(certificate_id=cert_id).first()
        if not cert:
            self._log_verification('manual', cert_id, 'failed', 0.0)
            self._log_alert(cert_id, "Certificate ID not found")
            return False, "Certificate ID not found in database", [], {"certificate_id": cert_id, "name": name}
        
        # Fuzzy name check
        if not self._is_fuzzy_match(name, cert.name):
            self._log_verification('manual', cert_id, 'failed', 45.0)
            self._log_alert(cert_id, "Name mismatch")
            return False, "Name mismatch", ["Name entered does not match our records"], {
                "name": name, "certificate_id": cert_id
            }

        self._log_verification('manual', cert_id, 'success', 100.0)
        
        extracted = {
            "name": self._mask_name(cert.name),
            "certificate_id": cert.certificate_id,
            "institution": cert.institution,
            "course": cert.course,
            "year": cert.year,
            "doc_hash": cert.doc_hash
        }
        return True, f"Certificate verified: {cert.certificate_id}", [], extracted


    def verify_file(self, file_storage):
        """
        file_storage: the uploaded certificate file (Flask FileStorage)
        """
        # Step 1: Compute Hash immediately
        doc_hash = self._compute_hash(file_storage.stream)

        # Step 2: Run OCR
        processor = OCRProcessor(file_storage)
        extracted_data = processor.run()  # returns dict with 'certificate_id' and 'name'

        cert_id = extracted_data.get("certificate_id")
        if not cert_id:
            self._log_verification('upload', 'UNKNOWN', 'failed', 10.0)
            return False, "Certificate ID could not be extracted", ["Failed to extract Certificate ID using OCR"], extracted_data

        # Step 3: Verify against database
        cert = self.session.query(Certificate).filter_by(certificate_id=cert_id).first()
        if not cert:
            self._log_verification('upload', cert_id, 'failed', 20.0)
            self._log_alert(cert_id, "Certificate ID not found")
            return False, "Verification Failed", ["Certificate ID not found in database"], extracted_data
        
        anomaly_reasons = []
        score = 99.8

        # Step 4: Cryptographic Hash check
        if cert.doc_hash and cert.doc_hash != doc_hash:
            anomaly_reasons.append("Cryptographic hash mismatch (Document may have been tampered).")
            score -= 50.0
            self._log_alert(cert_id, "Hash Tampering")

        # Step 5: Name check with fuzzy matching
        ext_name = extracted_data.get("name", "")
        if ext_name and not self._is_fuzzy_match(ext_name, cert.name):
            anomaly_reasons.append("Extracted student name does not match database record.")
            score -= 20.0
            self._log_alert(cert_id, "Name Tampering")

        if len(anomaly_reasons) > 0:
            self._log_verification('upload', cert_id, 'failed', score)
            return False, "Verification Failed", anomaly_reasons, extracted_data
        else:
            self._log_verification('upload', cert_id, 'success', score)
            
            # Enrich extracted data with DB stuff for display
            extracted_data["name"] = self._mask_name(cert.name)
            extracted_data["institution"] = cert.institution
            extracted_data["course"] = cert.course
            extracted_data["year"] = cert.year
            extracted_data["doc_hash"] = cert.doc_hash

            return True, f"Certificate verified: {cert.certificate_id}", [], extracted_data

