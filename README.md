# Veri-Scholars
The rise of fake degrees and forged academic certificates poses a serious threat to the credibility of higher education, job markets, and government schemes. Manual verification methods are slow, inconsistent, and vulnerable to corruption. To ensure academic integrity and public trust, there is a pressing need for a secure, scalable, and automated system that can detect and prevent the misuse of fraudulent certificates.

Objectives
1. Provide a smart, reliable, and fast verification system for certificates.  
2. Ensure security, scalability, and transparency in validation.  
3. Enable employers, institutions, and government agencies to easily verify academic records.
 
Our Solution
We are building a smart, scalable, and secure Fake Degree/Certificate Recognition System tailored for higher education institutions in Jharkhand, with the ability to scale nationwide. The platform combines AI, OCR, and blockchain technologies to provide a seamless and trustworthy way to validate academic credentials.

Tech Stack  
1. Frontend: HTML, CSS, JavaScript, jQuery  
2. Backend: Python (Flask)  
3. Database: SQLite  
4. Other Tools: REST APIs

Core Features
1. Upload & Verify: Employers, institutions, and agencies can upload or input certificate details (PDFs, scans, or digital copies).
2. AI + OCR Extraction: Automatically extracts key details (student name, roll number, marks, certificate ID) from uploaded documents.
3. Database Cross-Verification: Matches extracted data against verified institutional records to detect mismatches or inconsistencies.
4. Forgery Detection: Identifies tampered photos, fake seals, forged signatures, duplicate IDs, and cloned certificates.
5. Blockchain / Digital Watermarking: Ensures newly issued certificates are tamper-proof and easily verifiable.
6. Institution Integration Module: Allows universities and colleges to bulk-upload or sync certificate records in real time.
7. Admin Dashboard: For state departments to monitor verifications, flag suspicious activity, and generate forgery trend reports.
8. Alerts & Notifications: Immediate alerts for invalid or forged entries.
9. Data Privacy & Security: Implements strict access control and encryption to protect sensitive student data.

Impact & Benefits
1. Protects academic integrity and institutional reputation.
2. Speeds up verification for jobs, admissions, and government schemes.
3. Prevents fraud by ensuring only authentic credentials are accepted.
4. Builds trust between students, institutions, employers, and government bodies.
5. Supports Digital India goals by enabling a transparent and future-proof education ecosystem.

Target Users
1. Employers & HR departments
2. Universities & colleges
3. Scholarship agencies
4. Admission offices
5. Government departments

Project Structure

├── frontend/         # HTML, CSS, JS files
├── backend/          # Flask server and routes
├── database/         # SQLite DB schema and migrations
├── static/           # Assets (images, stylesheets, scripts)
├── templates/        # Jinja2 templates for Flask
├── app.py            # Main Flask entry point
├── requirements.txt  # Dependencies
└── README.md         # Documentation

Team Members
1. Akash Biswas - Backend and AI/ML model development
2. Arav Gupta - Backend and AI/ML model development
3. H M Pranav - FrontEnd 
4. Dhritiiraaj Bharali - Security & Data Protection
5. Aditi Agarwal - Web Design (UI/UX)
6. Hrishikesh Shetty - App Development (Frontend)

Future Scope
1. Blockchain-based certificate storage.
2. Integration with DigiLocker / UGC / AICTE databases.
3. AI-powered fraud detection.
4. Mobile application for on-the-go verification.

Scalability
While initially focused on Jharkhand institutions, the system is designed for pan-India adoption, making it a long-term solution for nationwide academic fraud prevention.

Getting Started  
Prerequisites  
- Install [Python 3.x](https://www.python.org/downloads/)  
- Install Flask:  
  ```bash
  pip install flask

This project was built as part of Smart India Hackathon 2025, under the problem statement:
“Authenticity Validator for Academia”
