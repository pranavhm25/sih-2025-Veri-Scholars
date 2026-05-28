import numpy as np
import cv2
import pytesseract
import re
import difflib

class OCRProcessor:
    known_institutions = [
        # Premier Institutes
        "Birla Institute of Technology, Mesra",
        "IIT (ISM) Dhanbad",
        "NIT Jamshedpur",
        "Central University of Jharkhand",
        "XLRI Jamshedpur",
        # State Universities
        "Ranchi University",
        "Vinoba Bhave University, Hazaribagh",
        "Kolhan University, Chaibasa",
        "Sido Kanhu Murmu University, Dumka",
        "Nilamber Pitamber University, Medininagar",
        # Engineering & Technical Colleges
        "BIT Sindri",
        "University College of Engineering & Technology, Hazaribagh",
        "Cambridge Institute of Technology, Ranchi",
        "Jharkhand Rai University",
        # Other Notable Institutions
        "Birsa Agricultural University, Ranchi",
        "Rajendra Institute of Medical Sciences, Ranchi",
    ]

    def __init__(self, file_storage):
        self.file = file_storage

    def deskew(self, img):
        """Auto-rotates skewed scans of certificates to align them horizontally."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        # Threshold the image
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Get coordinates of all white pixels
        coords = np.column_stack(np.where(thresh > 0))
        if len(coords) == 0:
            return img
            
        # Get the minimum area bounding box
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust the angle correctly
        if angle < -45:
            angle = -(90 + angle)
        elif angle > 45:
            angle = 90 - angle
        else:
            angle = -angle
            
        # If rotation is negligible, return original image
        if abs(angle) < 0.5 or abs(angle) > 25.0:
            return img
            
        # Perform rotation
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def preprocess(self, img):
        # 1. De-skew first to align text lines
        img = self.deskew(img)
        # 2. Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 3. Adaptive threshold
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
        # Match pattern like JHK-2025-CS-042 or JHK-2024-ME-109
        # Looks for 3 or more uppercase letters, a dash, 4 digits, a dash, and some alphanumeric letters/dashes.
        match = re.search(r'([A-Z]{3,}-\d{4}-[A-Z0-9-]+)', text_clean.upper())
        if match:
            # Clean up trailing dashes or spaces if any
            return match.group(1).strip("- ")
            
        # Fallback to the normalized 1X format
        text_norm = text_clean.upper().replace("O", "0").replace("I", "1").replace(" ", "")
        match_fallback = re.search(r'1X\d{4,}', text_norm)
        return match_fallback.group(0) if match_fallback else None

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
            # Fuzzy matching against known institutions using difflib
            best_match = None
            best_ratio = 0.0
            inst_lower = institution.lower()
            for known in self.known_institutions:
                ratio = difflib.SequenceMatcher(None, inst_lower, known.lower()).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = known
            if best_ratio >= 0.45:  # threshold for fuzzy institution matching
                institution = best_match
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
