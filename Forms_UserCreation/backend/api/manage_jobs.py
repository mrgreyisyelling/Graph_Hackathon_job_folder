import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set up database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/jobs/jobs.db")

@app.route("/api/create_job", methods=["POST"])
def create_job():
    try:
        data = request.json
        job_title, job_description = data["job_title"], data["job_description"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            );
        """)

        cursor.execute("INSERT INTO jobs (title, description) VALUES (?, ?)", (job_title, job_description))
        conn.commit()
        conn.close()

        return jsonify({"message": "Job created successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get_jobs", methods=["GET"])
def get_jobs():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM jobs")
        jobs = cursor.fetchall()
        conn.close()

        job_list = [{"id": job[0], "title": job[1], "description": job[2]} for job in jobs]
        return jsonify({"jobs": job_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/create_requirement", methods=["POST"])
def create_requirement():
    try:
        data = request.json
        job_id, requirement = data["job_id"], data["requirement"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                requirement TEXT NOT NULL
            );
        """)

        cursor.execute("INSERT INTO job_requirements (job_id, requirement) VALUES (?, ?)", (job_id, requirement))
        conn.commit()
        conn.close()

        return jsonify({"message": "Requirement added to job."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get_requirements", methods=["GET"])
def get_requirements():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT job_id, requirement FROM job_requirements")
        requirements = cursor.fetchall()
        conn.close()

        requirement_list = [{"job_id": req[0], "requirement": req[1]} for req in requirements]
        return jsonify({"requirements": requirement_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5004)
