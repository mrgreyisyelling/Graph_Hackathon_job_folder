import sqlite3
import os

DB_PATH = "database/jobs/jobs.db"

# Ensure database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old tables
cursor.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS job_requirements;
DROP TABLE IF EXISTS user_skills;
DROP TABLE IF EXISTS worker_needs;
DROP TABLE IF EXISTS worker_availability;
""")


# Create tables
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


conn.commit()
conn.close()

print("✅ Database reset and tables recreated.")