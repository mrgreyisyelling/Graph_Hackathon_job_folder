import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "database/jobs/jobs.db"

@app.route("/api/search_workers", methods=["GET"])
def search_workers():
    try:
        job_id = request.args.get("job_id")
        if not job_id:
            return jsonify({"error": "Missing job_id parameter"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Find the required skills for the job
        cursor.execute("SELECT skill_id FROM job_requirements WHERE job_id = ?", (job_id,))
        required_skills = cursor.fetchall()

        if not required_skills:
            return jsonify({"message": "No skills required for this job"}), 200

        skill_ids = [skill[0] for skill in required_skills]

        # Find users who have those skills
        cursor.execute("""
            SELECT DISTINCT users.id, users.name FROM users
            JOIN user_skills ON users.id = user_skills.user_id
            WHERE user_skills.skill_id IN ({})
        """.format(",".join(["?"] * len(skill_ids))), skill_ids)

        workers = cursor.fetchall()
        conn.close()

        worker_list = [{"id": worker[0], "name": worker[1]} for worker in workers]

        return jsonify({"workers": worker_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5005)