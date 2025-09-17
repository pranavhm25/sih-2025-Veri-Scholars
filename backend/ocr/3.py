import sqlite3

def show_certificates():
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificates")
    rows = cursor.fetchall()
    conn.close()

    print("\n📜 Stored Certificates:")
    for row in rows:
        print(row)

show_certificates()
