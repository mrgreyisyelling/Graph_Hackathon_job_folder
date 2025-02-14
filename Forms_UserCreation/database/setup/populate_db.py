import sqlite3

DB_PATH = "database/jobs/jobs.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Insert sample users (workers)
cursor.executemany("""
INSERT INTO users (name) VALUES (?)
""", [
    ("Alice",),
    ("Bob",),
    ("Charlie",),
    ("David",),
    ("Eve",),
    ("Frank",),
    ("Grace",),
    ("Hannah",),
    ("Isaac",),
    ("Jack",)
])

# Insert sample jobs
cursor.executemany("""
INSERT INTO jobs (title, description) VALUES (?, ?)
""", [
    ("Software Engineer", "Develop software using Python."),
    ("Data Analyst", "Analyze data and generate reports."),
    ("Construction Worker", "Work on construction sites."),
    ("Plumber", "Fix plumbing issues."),
    ("Web Developer", "Develop web applications with JavaScript."),
    ("Childcare Provider", "Take care of children of workers.")
])

# Insert worker skills
cursor.executemany("""
INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)
""", [
    (1, 1), (1, 2),  # Alice knows Python, Data Analysis
    (2, 3),  # Bob knows Carpentry
    (3, 4),  # Charlie knows Plumbing
    (4, 5),  # David knows JavaScript
    (5, 6),  # Eve knows Graphic Design
    (6, 1), (6, 2),  # Frank knows Python, Data Analysis
    (7, 3), (7, 4),  # Grace knows Carpentry, Plumbing
    (8, 5),  # Hannah knows JavaScript
    (9, 6)   # Isaac knows Graphic Design
])

# Insert job requirements
cursor.executemany("""
INSERT INTO job_requirements (job_id, skill_id) VALUES (?, ?)
""", [
    (1, 1),  # Software Engineer requires Python
    (2, 2),  # Data Analyst requires Data Analysis
    (3, 3),  # Construction Worker requires Carpentry
    (4, 4),  # Plumber requires Plumbing
    (5, 5)   # Web Developer requires JavaScript
])

# Insert worker needs (Childcare, Transportation)
cursor.executemany("""
INSERT INTO worker_needs (user_id, need) VALUES (?, ?)
""", [
    (1, "Childcare"), (2, "Childcare"), (3, "Childcare"),
    (4, "Transportation"), (5, "Childcare"), (6, "Childcare"),
    (7, "Transportation"), (8, "Childcare"), (9, "Transportation")
])

# Insert worker availability
cursor.executemany("""
INSERT INTO worker_availability (user_id, available) VALUES (?, ?)
""", [
    (1, 1), (2, 1), (3, 1),
    (4, 1), (5, 1), (6, 1),
    (7, 1), (8, 1), (9, 1), (10, 1)
])

conn.commit()
conn.close()

print("✅ Sample data inserted into the database.")
