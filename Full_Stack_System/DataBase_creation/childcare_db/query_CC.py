import sqlite3

conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM childcare_facilities LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()