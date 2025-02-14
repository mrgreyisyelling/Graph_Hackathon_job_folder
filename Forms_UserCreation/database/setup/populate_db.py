import sqlite3
import os
import random

DB_PATH = "database/jobs/jobs.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Generate 50 users (workers)
workers = [(f"Worker_{i+1}",) for i in range(50)]
cursor.executemany("INSERT INTO users (name) VALUES (?)", workers)

# Create 10 unique skills
skills = [
    ("Python",), ("Data Analysis",), ("Carpentry",), ("Plumbing",), ("JavaScript",),
    ("Graphic Design",), ("Marketing",), ("Electrical Work",), ("Machine Learning",), ("Customer Service",)
]
cursor.executemany("INSERT INTO skills (name) VALUES (?)", skills)

# Define 5 complex jobs, each requiring multiple skills
jobs = [
    ("Software Engineer", "Develop backend and frontend applications using Python & JavaScript."),
    ("Data Analyst", "Analyze business data, generate reports, and use machine learning."),
    ("Construction Worker", "Handles carpentry, electrical work, and plumbing tasks."),
    ("Digital Marketing Specialist", "Manages marketing campaigns, graphic design, and customer interactions."),
    ("Customer Support Agent", "Handles customer inquiries, requires problem-solving and communication skills.")
]
cursor.executemany("INSERT INTO jobs (title, description) VALUES (?, ?)", jobs)

# Define complex job requirements (each job requires 2-3 skills)
job_requirements = [
    (1, 1), (1, 5), (1, 9),  # Software Engineer → Python, JavaScript, Machine Learning
    (2, 2), (2, 9),  # Data Analyst → Data Analysis, Machine Learning
    (3, 3), (3, 4), (3, 8),  # Construction Worker → Carpentry, Plumbing, Electrical Work
    (4, 6), (4, 7), (4, 10),  # Marketing Specialist → Graphic Design, Marketing, Customer Service
    (5, 10), (5, 2)  # Customer Support → Customer Service, Data Analysis
]
cursor.executemany("INSERT INTO job_requirements (job_id, skill_id) VALUES (?, ?)", job_requirements)

# Randomly assign skills to workers (each worker gets 1-4 skills)
worker_skills = []
for worker_id in range(1, 51):
    num_skills = random.randint(1, 4)
    chosen_skills = random.sample(range(1, 11), num_skills)
    for skill_id in chosen_skills:
        worker_skills.append((worker_id, skill_id))
cursor.executemany("INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)", worker_skills)

# Assign varied worker availability (Randomized schedules)
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
worker_availability = []
for worker_id in range(1, 51):
    num_days_available = random.randint(1, 4)
    chosen_days = random.sample(days_of_week, num_days_available)
    for day in chosen_days:
        start_hour = random.randint(7, 12)  # Start time between 7 AM - 12 PM
        end_hour = start_hour + random.choice([4, 6, 8])  # 4, 6, or 8-hour shifts
        worker_availability.append((worker_id, day, f"{start_hour}:00", f"{end_hour}:00"))
cursor.executemany("INSERT INTO worker_availability (user_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)", worker_availability)

# Assign special needs to ~30% of workers
worker_needs = []
special_needs = ["Childcare", "Transportation", "Remote Work", "Flexible Hours"]
for worker_id in random.sample(range(1, 51), 15):  # Assign needs to 15 workers
    need = random.choice(special_needs)
    worker_needs.append((worker_id, need))
cursor.executemany("INSERT INTO worker_needs (user_id, need) VALUES (?, ?)", worker_needs)

# Ensure at least 10 workers have NO availability
workers_with_no_availability = random.sample(range(1, 51), 10)  # Pick 10 workers to have no shifts
cursor.executemany("DELETE FROM worker_availability WHERE user_id = ?", [(wid,) for wid in workers_with_no_availability])


conn.commit()
conn.close()

print("✅ Large-scale sample data inserted into the database.")
