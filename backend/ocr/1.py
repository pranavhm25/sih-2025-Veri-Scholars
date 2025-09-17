import sqlite3

def init_db():
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS certificates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        cert_id TEXT NOT NULL,
                        details TEXT,
                        hash TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

init_db()
print("✅ Database and table ready!")

