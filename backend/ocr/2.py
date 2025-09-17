import hashlib
import sqlite3

# Function to generate hash
def generate_hash(name, cert_id, details):
    data = f"{name}{cert_id}{details}"
    return hashlib.sha256(data.encode()).hexdigest()

# Function to store certificate
def store_certificate(name, cert_id, details):
    cert_hash = generate_hash(name, cert_id, details)
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()

    # Check if certificate with same cert_id already exists
    cursor.execute("SELECT * FROM certificates WHERE cert_id = ?", (cert_id,))
    if cursor.fetchone():
        print(f"⚠️ Certificate with ID {cert_id} already exists. Skipping insert.")
    else:
        cursor.execute(
            "INSERT INTO certificates (name, cert_id, details, hash) VALUES (?, ?, ?, ?)",
            (name, cert_id, details, cert_hash),
        )
        conn.commit()
        print("✅ Certificate stored with hash:", cert_hash)

    conn.close()

# Example usage
store_certificate("Arav Gupta", "111", "AI Workshop 2025")
store_certificate("Riya Sharma", "124", "Blockchain Seminar 2025")
store_certificate("Arav Gupta", "123", "AI Workshop 2025")  # Duplicate test
