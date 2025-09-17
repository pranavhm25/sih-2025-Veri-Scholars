# verifier.py
from OCRProcessor import OCRProcessor
from database import session, Certificate

class CertificateVerifier:
    def __init__(self, session):
        self.session = session

    def verify_file(self, file_storage):
        """
        file_storage: the uploaded certificate file (Flask FileStorage)
        """
        # Step 1: Run OCR
        processor = OCRProcessor(file_storage)
        extracted_data = processor.run()  # returns dict with 'certificate_id' and 'name'

        cert_id = extracted_data.get("certificate_id")
        if not cert_id:
            return False, "Certificate ID could not be extracted", extracted_data

        # Step 2: Verify against database (match by certificate_id)
        cert = self.session.query(Certificate).filter_by(certificate_id=cert_id).first()
        if not cert:
            return False, "Certificate ID not found in database", extracted_data
        else:
            return True, f"Certificate verified: {cert.certificate_id}", extracted_data
