import numpy as np
import cv2
import pytesseract
import re
from sentence_transformers import SentenceTransformer, util

class OCRProcessor:
    # Load embedding model once (shared across instances)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    known_institutions = [
        "Ramaiah",
        "IIIT Dharwad",
        "IIIT Bhubaneswar",
        "IISc Bangalore",
        "IIT Bombay",
        "IIT Delhi",
        "NIT Trichy",
        "Delhi University",
        "Anna University"
    ]

    def __init__(self, file_storage):
        self.file = file_storage

    def preprocess(self, img):
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Adaptive threshold
        bw = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        # Noise removal
        kernel = np.ones((1, 1), np.uint8)
        bw = cv2.dilate(bw, kernel, iterations=1)
        bw = cv2.medianBlur(bw, 3)
        # Font thickening
        bw_inv = cv2.bitwise_not(bw)
        bw_inv = cv2.dilate(bw_inv, kernel, iterations=1)
        bw = cv2.bitwise_not(bw_inv)
        return bw

    def extract_name(self, text_clean):
        name_match = re.search(r'NAME[:\- ]*(.*)', text_clean, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            # Remove unwanted characters and normalize spaces
            name = re.sub(r'[^A-Za-z\s]', '', name)
            name = re.sub(r'\s+', ' ', name).strip()
            # Capitalize each word
            name = name.title()
            return name
        return None

    def extract_certificate_id(self, text_clean):
        text_norm = text_clean.upper().replace("O", "0").replace("I", "1").replace(" ", "")
        match = re.search(r'1X\d{4,}', text_norm)
        return match.group(0) if match else None

    def extract_institution(self, text_clean):
        # Try regex first
        inst_match = re.search(r'(INSTITUTION|COLLEGE|UNIVERSITY)[:\- ]*(.*)', text_clean, re.IGNORECASE)
        if inst_match:
            institution = inst_match.group(2).strip()
        else:
            # fallback: first ALL CAPS line
            lines = text_clean.split("\n")
            institution = None
            for line in lines:
                if line.isupper() and len(line) > 5:
                    institution = line.strip()
                    break
        if institution:
            # Clean text
            institution = re.sub(r'[^A-Za-z\s]', ' ', institution)
            institution = re.sub(r'\s+', ' ', institution).strip()
            # Semantic matching with known institutions
            emb_text = self.model.encode(institution, convert_to_tensor=True)
            emb_known = self.model.encode(self.known_institutions, convert_to_tensor=True)
            cos_scores = util.cos_sim(emb_text, emb_known)[0]
            best_idx = cos_scores.argmax()
            if cos_scores[best_idx] > 0.25:  # threshold
                institution = self.known_institutions[best_idx]
            else:
                # capitalize words nicely
                institution = institution.title()
        return institution

    def run(self):
        # Convert FileStorage to OpenCV image
        file_bytes = np.frombuffer(self.file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Preprocess
        processed = self.preprocess(img)

        # OCR
        custom_config = r'--oem 3 --psm 6'
        raw_text = pytesseract.image_to_string(processed, config=custom_config)

        # Clean text
        text_clean = re.sub(r'\n+', '\n', raw_text)
        text_clean = re.sub(r' {2,}', ' ', text_clean)

        # Extract fields
        name = self.extract_name(text_clean)
        certificate_id = self.extract_certificate_id(text_clean)
        institution = self.extract_institution(text_clean)

        return {
            "name": name,
            "certificate_id": certificate_id,
            "institution": institution
        }
