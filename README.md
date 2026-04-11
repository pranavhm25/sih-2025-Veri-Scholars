# Veri-Scholars
The rise of fake degrees and forged academic certificates poses a serious threat to the credibility of higher education, job markets, and government schemes. Manual verification methods are slow, inconsistent, and vulnerable to corruption. To ensure academic integrity and public trust, there is a pressing need for a secure, scalable, and automated system that can detect and prevent the misuse of fraudulent certificates.

![Veri-Scholars Preview](frontend/preview.png)

---

## Objectives
1. Provide a smart, reliable, and fast verification system for certificates.  
2. Ensure security, scalability, and transparency in validation using cryptographic hashes.  
3. Enable employers, institutions, and government agencies to easily verify academic records.
 
## Our Solution
Built for SIH 2025 (Problem Statement 25029), **Veri-Scholars** is a smart, scalable, and secure Fake Degree Verification System tailored for higher education institutions in Jharkhand. The platform combines AI-driven OCR extraction with cryptographic verification to provide a seamless and trustworthy way to validate academic credentials.

## Premium Tech Stack  
1. **Frontend**: HTML5, CSS3 (Glassmorphism & Gradients), Vanilla JavaScript, Chart.js (Analytics)
2. **Backend**: Python (Flask REST API)
3. **AI / ML**: pytesseract (OCR), OpenCV (Image Preprocessing), SentenceTransformers (Entity Matching)
4. **Database**: SQLite with SQLAlchemy ORM
5. **Security**: SHA-256 Cryptographic Document Hashing

## Core Features
1. **Upload & Verify**: Drag-and-drop interface for employers/agencies to test scanned certificates against absolute truth parameters.
2. **AI Extractor**: Automatically pulls key details (student name, roll number, marks, certificate ID) from unstructured document uploads.
3. **QR Code Simulator**: Mock interface demonstrating instant verification capability of printed QR markers on degrees.
4. **Anomaly Dashboard**: Comprehensive metrics via Chart.js displaying forgery trends, volume trackers, and real-time security alerts.
5. **Role-Based Access**: Specialized portals for institutions to bulk-upload immutable records securely.

## Getting Started (Demo Mode)

The frontend overhaul can be entirely previewed without running the backend! We've included a highly realistic simulation mode.

1. Open `frontend/index.html` in your favorite modern browser.
2. On the **Verify** tab, try entering the ID `JHK-2025-CS-042` and the name `Aditi Sharma` to see a successful AI verification.
3. Enter any random string for a failed anomaly detection example.
4. Log into the Institution Portal by clicking "Use Demo Account".

## Getting Started (Backend API)
*Prerequisites*: Python 3.8+ and Tesseract-OCR installed on your system.

```bash
# 1. Navigate to the OCR backend folder
cd backend/ocr

# 2. Install dependencies
pip install -r requirements.txt
# (Dependencies include Flask, PyTesseract, OpenCV-python, sentence-transformers, SQLAlchemy)

# 3. Initialise the database
python database.py

# 4. Run the API Layer
python app.py
```

## Team Members
* Akash Biswas - Backend and AI/ML model development
* Arav Gupta - Backend and AI/ML model development
* H M Pranav - Frontend 
* Dhritiiraaj Bharali - Security & Data Protection
* Aditi Agarwal - Web Design (UI/UX)
* Hrishikesh Shetty - App Development (Frontend)

---

*Powered by the Department of Higher & Technical Education, Jharkhand*
