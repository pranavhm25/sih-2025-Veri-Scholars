import sqlite3

def view_certificates():
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM certificates")
    rows = cursor.fetchall()

    print("\n📜 Stored Certificates:")
    for row in rows:
        print(row)

    conn.close()

# Example usage
if __name__ == "__main__":
    view_certificates()
