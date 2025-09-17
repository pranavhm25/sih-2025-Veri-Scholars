import sqlite3

# Connect to database (will create if not exists)
conn = sqlite3.connect("certificates.db")
cursor = conn.cursor()

# Drop old table (if exists) and create new one with UNIQUE cert_id
cursor.execute("DROP TABLE IF EXISTS certificates;")

cursor.execute("""
CREATE TABLE certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cert_id TEXT NOT NULL UNIQUE,
    details TEXT,
    hash TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ Database setup complete with UNIQUE cert_id constraint")
