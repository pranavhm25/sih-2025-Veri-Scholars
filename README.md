<p align="center">
  <img src="frontend/preview.png" alt="Veri-Scholars Preview" width="720" />
</p>

<h1 align="center">🎓 Veri-Scholars</h1>

<p align="center">
  <strong>Authenticity Validator for Academia</strong><br/>
  A smart, scalable, and secure system to detect fake degrees &amp; forged academic certificates.
</p>

<p align="center">
  <a href="https://github.com/pranavhm25/sih-2025-Veri-Scholars/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="MIT License" />
  </a>
  <img src="https://img.shields.io/badge/SIH_2025-Problem_25029-blue?style=for-the-badge" alt="SIH 2025" />
  <img src="https://img.shields.io/badge/python-3.8+-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/status-In_Development-orange?style=for-the-badge" alt="Status" />
</p>

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Core Features](#-core-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Impact & Benefits](#-impact--benefits)
- [Future Roadmap](#-future-roadmap)
- [Team Members](#-team-members)
- [License](#-license)

---

## 🔍 Problem Statement

The rise of fake degrees and forged academic certificates poses a serious threat to the credibility of higher education, job markets, and government schemes. Manual verification methods are slow, inconsistent, and vulnerable to corruption. To ensure academic integrity and public trust, there is a pressing need for a secure, scalable, and automated system that can detect and prevent the misuse of fraudulent certificates.

---

## 💡 Our Solution

Built for **Smart India Hackathon 2025** (Problem Statement **25029**), **Veri-Scholars** is a smart, scalable, and secure Fake Degree Verification System tailored for higher education institutions in Jharkhand. The platform combines **AI-driven OCR extraction** with **cryptographic verification** to provide a seamless and trustworthy way to validate academic credentials.

### Objectives

1. Provide a smart, reliable, and fast verification system for certificates.
2. Ensure security, scalability, and transparency in validation using **cryptographic hashes**.
3. Enable employers, institutions, and government agencies to easily verify academic records.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| **📤 Upload & Verify** | Drag-and-drop interface for employers/agencies to test scanned certificates against verified records. |
| **🤖 AI Extractor (OCR)** | Automatically pulls key details (student name, roll number, marks, certificate ID) from unstructured document uploads using PyTesseract & OpenCV. |
| **📱 QR Code Simulator** | Mock interface demonstrating instant verification capability of printed QR markers on degrees. |
| **📊 Anomaly Dashboard** | Comprehensive metrics via Chart.js — forgery trends, volume trackers, and real-time security alerts. |
| **🔐 Role-Based Access** | Specialized portals for institutions to bulk-upload immutable records securely. |
| **🛡️ SHA-256 Hashing** | Cryptographic document hashing ensures tamper-proof certificate integrity. |

---

## 🛠 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | HTML5 · CSS3 (Glassmorphism & Gradients) · Vanilla JavaScript · Chart.js |
| **Backend** | Python · Flask · Flask-CORS · Flask-Limiter · Gunicorn |
| **AI / ML** | PyTesseract (OCR) · OpenCV (Image Preprocessing) · SentenceTransformers (Entity Matching) |
| **Database** | SQLite · SQLAlchemy ORM |
| **Security** | SHA-256 Cryptographic Document Hashing · Rate Limiting |

---

## 📂 Project Structure

```
sih-2025-Veri-Scholars/
│
├── frontend/                    # Client-side application
│   ├── index.html               # Main SPA entry point
│   ├── style.css                # Global styles (glassmorphism, gradients)
│   ├── script.js                # Client-side logic, navigation & demo mode
│   ├── preview.png              # Project preview screenshot
│   └── flutter.dart             # Flutter prototype reference
│
├── backend/
│   ├── ocr/                     # Flask REST API + AI verification engine
│   │   ├── app.py               # Flask server & route definitions
│   │   ├── OCRProcessor.py      # Tesseract OCR + OpenCV pipeline
│   │   ├── verifier.py          # Certificate verification logic
│   │   ├── database.py          # SQLAlchemy models & DB setup
│   │   ├── wsgi.py              # Gunicorn WSGI entry point
│   │   ├── requirements.txt     # Python dependencies
│   │   ├── certificates.db      # SQLite database
│   │   ├── static/              # Backend-specific static assets
│   │   └── templates/           # Jinja2 templates
│   └── hash/
│       └── certificates.db      # Hash verification database
│
├── flutter.dart                 # Flutter app reference
├── .gitignore
├── LICENSE                      # MIT License
└── README.md
```

---

## 🚀 Getting Started

### Demo Mode (No Backend Required)

The frontend includes a **fully functional simulation mode** — no server needed!

1. **Clone the repository**
   ```bash
   git clone https://github.com/pranavhm25/sih-2025-Veri-Scholars.git
   cd sih-2025-Veri-Scholars
   ```

2. **Open the frontend** in any modern browser
   ```bash
   # Windows
   start frontend/index.html

   # macOS
   open frontend/index.html

   # Linux
   xdg-open frontend/index.html
   ```

3. **Try it out:**
   - Go to the **Verify** tab → enter Certificate ID `JHK-2025-CS-042` and name `Aditi Sharma` for a successful verification.
   - Enter any random string to see anomaly detection in action.
   - Click **"Use Demo Account"** on the Institution Portal to explore the admin dashboard.

### Backend API (Full Mode)

> **Prerequisites:** Python 3.8+ and [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.

```bash
# 1. Navigate to the OCR backend
cd backend/ocr

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialise the database
python database.py

# 4. Start the Flask server
python app.py
```

The API server will start at `http://localhost:5000` and also serve the frontend at the root URL.

---

## 📡 API Reference

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| `GET` | `/` | Serves the frontend SPA | — |
| `POST` | `/api/verify/manual` | Verify a certificate by ID & name | 5/min |
| `POST` | `/api/verify/upload` | Upload & verify a scanned certificate | 5/min |
| `GET` | `/api/dashboard/stats` | Get dashboard statistics (records, verifications, trust score) | — |
| `POST` | `/api/dashboard/bulk-upload` | Bulk upload institutional records | — |

---

## 🎯 Impact & Benefits

- 🛡️ **Protects academic integrity** and institutional reputation.
- ⚡ **Speeds up verification** for jobs, admissions, and government schemes.
- 🚫 **Prevents fraud** by ensuring only authentic credentials are accepted.
- 🤝 **Builds trust** between students, institutions, employers, and government bodies.
- 🇮🇳 **Supports Digital India** goals by enabling a transparent, future-proof education ecosystem.

---

## 🔮 Future Roadmap

- [ ] Blockchain-based immutable certificate storage
- [ ] Integration with **DigiLocker / UGC / AICTE** databases
- [ ] Deep learning–powered advanced fraud detection
- [ ] Mobile application for on-the-go verification
- [ ] Pan-India scaling beyond Jharkhand institutions

---

## 👥 Team Members

| Name | Role |
|------|------|
| **Akash Biswas** | Backend & AI/ML Model Development |
| **Arav Gupta** | Backend & AI/ML Model Development |
| **H M Pranav** | Frontend Development |
| **Dhritiraaj Bharali** | Security & Data Protection |
| **Aditi Agarwal** | Web Design (UI/UX) |
| **Hrishikesh Shetty** | App Development (Frontend) |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for <strong>Smart India Hackathon 2025</strong><br/>
  Problem Statement 25029: <em>"Authenticity Validator for Academia"</em><br/><br/>
  <em>Powered by the Department of Higher & Technical Education, Jharkhand</em>
</p>
