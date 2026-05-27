# database.py
from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, Float
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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class VerificationLog(Base):
    __tablename__ = 'verification_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    endpoint_used = Column(String, nullable=False) # 'manual' or 'upload' or 'api'
    cert_id_searched = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    status_result = Column(String, nullable=False) # 'success' or 'failed'
    confidence_score = Column(Float, nullable=True)

class SecurityAlert(Base):
    __tablename__ = 'security_alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    severity = Column(String, nullable=False) # 'High', 'Medium', 'Low'
    cert_id_used = Column(String, nullable=True)
    risk_factor = Column(String, nullable=False) # e.g. "Hash Tampering"
    ip_address = Column(String, nullable=True)   # Source IP of the request
    user_agent = Column(String, nullable=True)   # Browser/client user-agent string

# --- Create SQLite engine and table ---
engine = create_engine(
    "sqlite:///certificates.db",
    connect_args={"check_same_thread": False},  # helps with Flask multithreading
    echo=False
)
Base.metadata.create_all(engine)

# --- Create session ---
Session = sessionmaker(bind=engine)
session = scoped_session(Session)

# --- Initialize database only when run directly ---
if __name__ == "__main__":
    # Clear old data
    session.query(Certificate).delete()
    session.query(VerificationLog).delete()
    session.query(SecurityAlert).delete()
    session.commit()

    # Preload database with the required Gold standard demo certificate
    predefined_certificates = [
        {
            "certificate_id": "JHK-2025-CS-042",
            "name": "Aditi Sharma",
            "roll_number": "2021CS042",
            "institution": "Birla Institute of Technology, Mesra",
            "course": "B.Tech Computer Science",
            "year": "2025",
            "doc_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" # Example hash
        },
        {
            "certificate_id": "JHK-2024-ME-109",
            "name": "Rohan Das",
            "roll_number": "2020ME109",
            "institution": "NIT Jamshedpur",
            "course": "B.Tech Mechanical Engineering",
            "year": "2024",
            "doc_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
        }
    ]

    for cert_data in predefined_certificates:
        if not session.query(Certificate).filter_by(certificate_id=cert_data["certificate_id"]).first():
            cert = Certificate(**cert_data)
            session.add(cert)
            
    # Add some dummy verification logs
    dummy_logs = [
        VerificationLog(endpoint_used='api', cert_id_searched='JHK-2024-ME-109', ip_address='10.0.0.8', status_result='success', confidence_score=99.9),
        VerificationLog(endpoint_used='manual', cert_id_searched='FAKE-ID-999', ip_address='45.22.10.1', status_result='failed', confidence_score=0.0)
    ]
    session.add_all(dummy_logs)

    # Add a dummy alert
    dummy_alert = SecurityAlert(severity='High', cert_id_used='UNKNOWN-123', risk_factor='Invalid issuing authority structure')
    session.add(dummy_alert)

    session.commit()
    print("✅ Database initialized with extended schema and demo data.")
