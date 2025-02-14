import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

DB_PATH = "database/jobs/jobs.db"

@app.route("/api/generate_childcare_jobs", methods=["GET"])
def generate_childcare_jobs():
    """
    Identifies jobs that create childcare needs, assigns childcare jobs to workers who are
    not employable for those jobs, and prioritizes maximizing the overall labor force.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Step 1: Identify workers who need childcare
        cursor.execute("""
            SELECT DISTINCT users.id, users.name, users.job_id
            FROM users
            JOIN worker_needs ON users.id = worker_needs.user_id
            WHERE worker_needs.need = 'Childcare'
        """)
        workers_with_childcare_needs = cursor.fetchall()  # [(user_id, name, job_id), ...]

        # Step 2: Identify all available workers (who are currently in the labor pool)
        cursor.execute("""
            SELECT DISTINCT users.id, users.name
            FROM users
            LEFT JOIN user_skills ON users.id = user_skills.user_id
            WHERE users.id NOT IN (SELECT DISTINCT user_id FROM worker_availability)
        """)
        available_workers = cursor.fetchall()  # [(user_id, name), ...]

        # Step 3: Group childcare needs by job (to assign proportional childcare jobs)
        job_childcare_needs = {}
        for worker_id, name, job_id in workers_with_childcare_needs:
            if job_id not in job_childcare_needs:
                job_childcare_needs[job_id] = []
            job_childcare_needs[job_id].append({"id": worker_id, "name": name})

        # Step 4: Determine how many childcare jobs are needed
        childcare_jobs_created = []
        childcare_worker_assignments = []
        CHILDCARE_RATIO = 5  # One childcare worker can support 5 workers needing childcare

        for job_id, workers in job_childcare_needs.items():
            num_workers = len(workers)
            childcare_jobs_needed = -(-num_workers // CHILDCARE_RATIO)  # Ceiling division

            # Step 5: Assign childcare jobs to workers who cannot do the primary jobs
            assigned_workers = []
            while childcare_jobs_needed > 0 and available_workers:
                childcare_worker = available_workers.pop(0)  # Pick first available worker
                assigned_workers.append(childcare_worker)
                childcare_jobs_needed -= 1

            # Step 6: Create childcare jobs & record assignments
            for worker in assigned_workers:
                cursor.execute("INSERT INTO jobs (title, description) VALUES (?, ?)", 
                               ("Childcare Provider", f"Provides childcare for job {job_id}"))
                childcare_job_id = cursor.lastrowid  # Get ID of inserted job
                childcare_jobs_created.append(childcare_job_id)
                childcare_worker_assignments.append({
                    "childcare_job_id": childcare_job_id,
                    "worker_id": worker[0],
                    "worker_name": worker[1]
                })

        conn.commit()

        # Step 7: Return response
        return jsonify({
            "jobs_created": len(childcare_jobs_created),
            "childcare_worker_assignments": childcare_worker_assignments
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=5008)
