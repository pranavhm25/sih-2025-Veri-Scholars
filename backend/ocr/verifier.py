# verifier.py
import hashlib
from OCRProcessor import OCRProcessor
from database import session, Certificate, VerificationLog, SecurityAlert
from flask import request

class CertificateVerifier:
    def __init__(self, session):
        self.session = session

    def _get_client_ip(self):
        try:
            return request.remote_addr
        except:
            return "127.0.0.1"

    def _log_verification(self, endpoint, cert_id, status, score):
        ip = self._get_client_ip()
        log = VerificationLog(endpoint_used=endpoint, cert_id_searched=cert_id, ip_address=ip, status_result=status, confidence_score=score)
        self.session.add(log)
        self.session.commit()
    
    def _log_alert(self, cert_id, risk_factor, severity="High"):
        alert = SecurityAlert(severity=severity, cert_id_used=cert_id, risk_factor=risk_factor)
        self.session.add(alert)
        self.session.commit()

    def _compute_hash(self, file_stream):
        # We need to read the stream, compute hash, then reset stream
        file_stream.seek(0)
        sha256 = hashlib.sha256()
        for chunk in iter(lambda: file_stream.read(4096), b""):
            sha256.update(chunk)
        file_stream.seek(0)
        return sha256.hexdigest()

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

    def verify_manual(self, cert_id, name):
        """
        Verify manually entered details against DB.
        """
        cert = self.session.query(Certificate).filter_by(certificate_id=cert_id).first()
        if not cert:
            self._log_verification('manual', cert_id, 'failed', 0.0)
            self._log_alert(cert_id, "Certificate ID not found")
            return False, "Certificate ID not found in database", [], {"certificate_id": cert_id, "name": name}
        
        # Simple name check (case-insensitive)
        if name.lower() not in cert.name.lower() and cert.name.lower() not in name.lower():
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

        # Step 5: Name check
        ext_name = extracted_data.get("name", "")
        if ext_name and ext_name.lower() not in cert.name.lower() and cert.name.lower() not in ext_name.lower():
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

