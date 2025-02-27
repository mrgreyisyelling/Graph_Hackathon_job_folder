import sqlite3
import os

# Define the correct relative path
DB_RELATIVE_PATH = "Forms_UserCreation/database/jobs/jobs.db"
DB_PATH = os.path.abspath(DB_RELATIVE_PATH)  # Resolve to absolute path for debugging

# Ensure database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

print(f"📌 Using relative path: {DB_RELATIVE_PATH}")
print(f"📌 Resolved absolute path: {DB_PATH}")

# Connect to the database
try:
    conn = sqlite3.connect(DB_RELATIVE_PATH)  # Using relative path for actual connection
    cursor = conn.cursor()
    print("🔄 Connected to database successfully.")
except sqlite3.Error as e:
    print(f"❌ Failed to connect to database: {e}")
    exit(1)

print("🔄 Resetting database...")

# Drop old tables
tables_to_drop = [
    "users", "skills", "jobs", "job_requirements",
    "user_skills", "worker_needs", "worker_availability"
]

for table in tables_to_drop:
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
        print(f"🗑 Dropped table: {table}")
    except sqlite3.Error as e:
        print(f"❌ Failed to drop table {table}: {e}")

# Create tables
print("📌 Creating new tables...")
try:
    cursor.executescript("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        job_id INTEGER,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    );

    CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    );

    CREATE TABLE user_skills (
        user_id INTEGER,
        skill_id INTEGER,
        PRIMARY KEY (user_id, skill_id)
    );

    CREATE TABLE job_requirements (
        job_id INTEGER,
        skill_id INTEGER,
        PRIMARY KEY (job_id, skill_id),
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    );

    CREATE TABLE worker_needs (
        user_id INTEGER,
        need TEXT NOT NULL,
        PRIMARY KEY (user_id, need)
    );

    CREATE TABLE worker_availability (
        user_id INTEGER,
        available INTEGER DEFAULT 1,
        PRIMARY KEY (user_id)
    );
    """)
    print("✅ Tables created successfully.")
except sqlite3.Error as e:
    print(f"❌ Error creating tables: {e}")
    conn.close()
    exit(1)

# Verify table creation
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]
expected_tables = {
    "users", "jobs", "user_skills", "job_requirements", "worker_needs", "worker_availability"
}

print("\n🔍 Verifying table creation...")
for table in expected_tables:
    if table in tables:
        print(f"✅ Table found: {table}")
    else:
        print(f"❌ Missing table: {table}")

if expected_tables.issubset(set(tables)):
    print("\n🎉 All tables created successfully! 🚀")
else:
    print("\n⚠️ Some tables are missing. Check for issues.")

conn.commit()
conn.close()

print("🔄 Database reset process complete.")
