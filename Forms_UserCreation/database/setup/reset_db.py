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
""")

# Recreate tables
cursor.executescript("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE job_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL
);

CREATE TABLE user_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ Database reset and tables recreated.")