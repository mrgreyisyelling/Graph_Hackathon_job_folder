import sqlite3
import os

DB_PATH = "database/jobs/jobs.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add new tables for worker availability and needs
cursor.executescript("""
CREATE TABLE IF NOT EXISTS worker_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS worker_needs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    need TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ Database updated with worker availability and needs tables.")