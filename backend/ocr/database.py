# database.py
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import datetime

# --- Base and Table ---
Base = declarative_base()

class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    certificate_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    roll_number = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    course = Column(String, nullable=True)
    year = Column(String, nullable=True)
    doc_hash = Column(String, nullable=True) # SHA-256 hash of the valid doc
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

class VerificationLog(Base):
    __tablename__ = 'verification_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    endpoint_used = Column(String, nullable=False) # 'manual' or 'upload' or 'api'
    cert_id_searched = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    status_result = Column(String, nullable=False) # 'success' or 'failed'
    confidence_score = Column(Float, nullable=True)

class SecurityAlert(Base):
    __tablename__ = 'security_alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    severity = Column(String, nullable=False) # 'High', 'Medium', 'Low'
    cert_id_used = Column(String, nullable=True)
    risk_factor = Column(String, nullable=False) # e.g. "Hash Tampering"
    ip_address = Column(String, nullable=True)   # Source IP of the request
    user_agent = Column(String, nullable=True)   # Browser/client user-agent string

import os

# --- Create Database Engine ---
# Use PostgreSQL if DATABASE_URL is set (Production), otherwise fallback to SQLite (Local)
database_url = os.environ.get("DATABASE_URL", "sqlite:///certificates.db")

# Fix for older Heroku/Render Postgres URIs that use 'postgres://' instead of 'postgresql://'
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# SQLite needs specific connect_args for multithreading in Flask
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(
    database_url,
    connect_args=connect_args,
    echo=False
)
Base.metadata.create_all(engine)

# --- Create session ---
Session = sessionmaker(bind=engine)
session = scoped_session(Session)

# --- Auto-seed Database with Predefined Demo Certificates ---
predefined_certificates = [
    {
        "certificate_id": "JHK-2025-CS-042",
        "name": "Aditi Sharma",
        "roll_number": "2021CS042",
        "institution": "Birla Institute of Technology, Mesra",
        "course": "B.Tech Computer Science",
        "year": "2025",
        "doc_hash": "c55469d41f0b3b1675f0b669e8dac2aa12c52baf26cae56bb963e8a4fcd23594"
    },
    {
        "certificate_id": "JHK-2024-ME-109",
        "name": "Rohan Das",
        "roll_number": "2020ME109",
        "institution": "NIT Jamshedpur",
        "course": "B.Tech Mechanical Engineering",
        "year": "2024",
        "doc_hash": "d9f73f855a81bd78e0ef8e982d41c0b677adfcf328222fad9739e7fb0495d3c9"
    },
    {
        "certificate_id": "JHK-2025-EE-201",
        "name": "Priya Patel",
        "roll_number": "2021EE201",
        "institution": "IIT (ISM) Dhanbad",
        "course": "B.Tech Electrical Engineering",
        "year": "2025",
        "doc_hash": "d924f44d51238c8b87ca3f1180d8a1c8708444526629678df9a68913cc51ee13"
    },
    {
        "certificate_id": "JHK-2023-EC-304",
        "name": "Vikram Singh",
        "roll_number": "2019EC304",
        "institution": "Ranchi University",
        "course": "B.Sc Electronics",
        "year": "2023",
        "doc_hash": "26e2dd2930451d556301dcf74019e7f9d4f11ac6888cae6d9c62eb48e37a6a2e"
    }
]

# Ensure we auto-seed or update hashes of predefined certificates
try:
    for cert_data in predefined_certificates:
        existing = session.query(Certificate).filter_by(certificate_id=cert_data["certificate_id"]).first()
        if existing:
            # Synchronize doc_hash and other details to match latest compiled demo files
            if existing.doc_hash != cert_data["doc_hash"]:
                existing.doc_hash = cert_data["doc_hash"]
        else:
            cert = Certificate(**cert_data)
            session.add(cert)
    session.commit()
    print("✅ Database successfully seeded and synchronized with demo certificates.")
except Exception as e:
    session.rollback()
    print("⚠️ Database seeding skipped or failed:", e)

# Keep the main run block for manual script resets if needed
if __name__ == "__main__":
    session.query(Certificate).delete()
    session.query(VerificationLog).delete()
    session.query(SecurityAlert).delete()
    session.commit()
    for cert_data in predefined_certificates:
        cert = Certificate(**cert_data)
        session.add(cert)
    session.commit()
    print("✅ Database explicitly reset and seeded.")
