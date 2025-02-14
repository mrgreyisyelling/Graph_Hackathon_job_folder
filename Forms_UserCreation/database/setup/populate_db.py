import sqlite3
import os

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
    ("Eve",)
])

# Insert sample skills
cursor.executemany("""
INSERT INTO skills (name) VALUES (?)
""", [
    ("Python",),
    ("Data Analysis",),
    ("Carpentry",),
    ("Plumbing",),
    ("JavaScript",),
    ("Graphic Design",)
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
    ("Designer", "Create digital graphics and branding.")
])

# Insert job requirements (skill_id corresponds to the skills table)
cursor.executemany("""
INSERT INTO job_requirements (job_id, skill_id) VALUES (?, ?)
""", [
    (1, 1),  # Software Engineer requires Python
    (2, 2),  # Data Analyst requires Data Analysis
    (3, 3),  # Construction Worker requires Carpentry
    (4, 4),  # Plumber requires Plumbing
    (5, 5),  # Web Developer requires JavaScript
    (6, 6)   # Designer requires Graphic Design
])

# Assign skills to users (simulate skill ownership)
cursor.executemany("""
INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)
""", [
    (1, 1),  # Alice knows Python
    (1, 2),  # Alice also knows Data Analysis
    (2, 3),  # Bob knows Carpentry
    (3, 4),  # Charlie knows Plumbing
    (4, 5),  # David knows JavaScript
    (5, 6)   # Eve knows Graphic Design
])

conn.commit()
conn.close()

print("✅ Sample data inserted into the database.")