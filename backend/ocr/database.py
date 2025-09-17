# database.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Base and Table ---
Base = declarative_base()

class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    certificate_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

# --- Create SQLite engine and table ---
engine = create_engine(
    "sqlite:///certificates.db",
    connect_args={"check_same_thread": False},  # helps with Flask multithreading
    echo=False
)
Base.metadata.create_all(engine)

# --- Create session ---
Session = sessionmaker(bind=engine)
session = Session()

# --- Initialize database only when run directly ---
if __name__ == "__main__":
    # Clear old data
    session.query(Certificate).delete()
    session.commit()

    # Preload database with only the ground truth certificate
    predefined_certificates = [
        {"certificate_id": "1X2501049", "name": "John Doe"}
    ]

    for cert_data in predefined_certificates:
        if not session.query(Certificate).filter_by(certificate_id=cert_data["certificate_id"]).first():
            cert = Certificate(**cert_data)
            session.add(cert)
    session.commit()
    print("✅ Database initialized with ground truth certificate")
