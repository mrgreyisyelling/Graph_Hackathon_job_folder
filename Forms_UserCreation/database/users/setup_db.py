import sqlite3
import os

# Get the absolute path of the database file
DB_PATH = os.path.abspath("database/users/users.db")
print(f"📌 Using database path: {DB_PATH}")

try:
    # Connect to SQLite and create the users table
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🔍 Checking if 'users' table exists...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()

    if table_exists:
        print("✅ 'users' table already exists.")
    else:
        print("⚠️ 'users' table does NOT exist. Creating it now...")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        user_type TEXT NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Check if table was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if cursor.fetchone():
        print("✅ Successfully created 'users' table.")
    else:
        print("❌ ERROR: 'users' table was NOT created!")

    conn.commit()
    conn.close()

except Exception as e:
    print(f"❌ Database error: {str(e)}")

print("🏁 Setup complete.")
