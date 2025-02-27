import sqlite3
import os

# Define database path
DB_RELATIVE_PATH = "Forms_UserCreation/database/jobs/jobs.db"
DB_PATH = os.path.abspath(DB_RELATIVE_PATH)

# Ensure database exists
if not os.path.exists(DB_PATH):
    print(f"❌ Database not found at {DB_PATH}. Did you run reset_db.py first?")
    exit(1)

# Connect to the database
conn = sqlite3.connect(DB_RELATIVE_PATH)
cursor = conn.cursor()

print(f"📌 Connected to database at: {DB_PATH}")
print("🔄 Populating database with sample data...")

# Insert sample users (workers with jobs)
workers = [
    ("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4), ("Eve", 5),
    ("Frank", 1), ("Grace", 2), ("Hannah", 3), ("Isaac", 4), ("Jack", 5)
]
cursor.executemany("INSERT INTO users (name, job_id) VALUES (?, ?)", workers)
print(f"✅ Inserted {len(workers)} workers with jobs.")

# Insert unassigned workers (who can take childcare jobs)
unassigned_workers = [
    ("Kelly",), ("Sam",), ("Rick",), ("Martha",), ("Nina",),
    ("Leo",), ("Sophie",), ("Chris",), ("Tom",), ("Emma",)
]
cursor.executemany("INSERT INTO users (name) VALUES (?)", unassigned_workers)
print(f"✅ Inserted {len(unassigned_workers)} additional unassigned workers.")

# Insert sample jobs
jobs = [
    ("Software Engineer", "Develop software using Python."),
    ("Data Analyst", "Analyze data and generate reports."),
    ("Construction Worker", "Work on construction sites."),
    ("Plumber", "Fix plumbing issues."),
    ("Web Developer", "Develop web applications with JavaScript."),
    ("Childcare Provider", "Take care of children of workers.")
]
cursor.executemany("INSERT INTO jobs (title, description) VALUES (?, ?)", jobs)
print(f"✅ Inserted {len(jobs)} jobs.")

# Insert worker skills (Avoid duplicates)
user_skills = [
    (1, 1), (1, 2),  # Alice knows Python, Data Analysis
    (2, 3),  # Bob knows Carpentry
    (3, 4),  # Charlie knows Plumbing
    (4, 5),  # David knows JavaScript
    (5, 6),  # Eve knows Graphic Design
    (6, 1), (6, 2),  # Frank knows Python, Data Analysis
    (7, 3), (7, 4),  # Grace knows Carpentry, Plumbing
    (8, 5),  # Hannah knows JavaScript
    (9, 6)   # Isaac knows Graphic Design
]
# Check for duplicates before inserting
cursor.executemany("""
    INSERT OR IGNORE INTO user_skills (user_id, skill_id) VALUES (?, ?)
""", user_skills)
print(f"✅ Inserted {len(user_skills)} user-skill relationships (ignoring duplicates).")

# Insert job requirements
job_requirements = [
    (1, 1),  # Software Engineer requires Python
    (2, 2),  # Data Analyst requires Data Analysis
    (3, 3),  # Construction Worker requires Carpentry
    (4, 4),  # Plumber requires Plumbing
    (5, 5)   # Web Developer requires JavaScript
]
cursor.executemany("INSERT OR IGNORE INTO job_requirements (job_id, skill_id) VALUES (?, ?)", job_requirements)
print(f"✅ Inserted {len(job_requirements)} job requirements.")

# Insert worker needs (Childcare, Transportation)
worker_needs = [
    (1, "Childcare"), (2, "Childcare"), (3, "Childcare"),
    (4, "Transportation"), (5, "Childcare"), (6, "Childcare"),
    (7, "Transportation"), (8, "Childcare"), (9, "Transportation")
]
cursor.executemany("INSERT OR IGNORE INTO worker_needs (user_id, need) VALUES (?, ?)", worker_needs)
print(f"✅ Inserted {len(worker_needs)} worker needs.")

# Insert worker availability
worker_availability = [
    (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
    (11, 1), (12, 1), (13, 1), (14, 1), (15, 1)  # Newly added workers
]
cursor.executemany("INSERT OR IGNORE INTO worker_availability (user_id, available) VALUES (?, ?)", worker_availability)
print(f"✅ Inserted {len(worker_availability)} worker availability records.")

conn.commit()
conn.close()

print("\n🔍 Verifying table population...")

# Reconnect to verify
conn = sqlite3.connect(DB_RELATIVE_PATH)
cursor = conn.cursor()

def check_table(table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"✅ {count} records found in `{table_name}` table.")
    else:
        print(f"❌ No records found in `{table_name}`. Something went wrong.")

tables_to_check = ["users", "jobs", "user_skills", "job_requirements", "worker_needs", "worker_availability"]
for table in tables_to_check:
    check_table(table)

conn.close()

print("\n🎉 Database successfully populated! 🚀")
