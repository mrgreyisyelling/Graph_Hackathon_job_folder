import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS  # 🔥 Import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # 🔥 Allow CORS for all /api/* endpoints

DB_PATH = "Forms_UserCreation/database/jobs/jobs.db"

@app.route("/api/generate_childcare_jobs", methods=["GET"])
def generate_childcare_jobs():
    """
    Identifies jobs that create childcare needs, assigns childcare jobs to workers who are
    not employable for those jobs, and prioritizes maximizing the overall labor force.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print(f"🔍 Checking database at: {DB_PATH}")

        # Step 1: Identify workers who need childcare
        cursor.execute("""
            SELECT DISTINCT users.id, users.name, users.job_id
            FROM users
            JOIN worker_needs ON users.id = worker_needs.user_id
            WHERE worker_needs.need = 'Childcare'
        """)
        workers_with_childcare_needs = cursor.fetchall()

        print(f"🔍 Workers needing childcare: {workers_with_childcare_needs}")

        # Step 2: Identify all available workers
        cursor.execute("""
            SELECT DISTINCT users.id, users.name
            FROM users
            WHERE users.id NOT IN (SELECT DISTINCT user_id FROM worker_availability)
        """)
        available_workers = cursor.fetchall()

        print(f"✅ Available workers for childcare jobs: {available_workers}")

        if not workers_with_childcare_needs:
            print("⚠️ No workers require childcare!")
            return jsonify({"message": "No workers need childcare."})

        # Step 3: Create childcare jobs
        childcare_jobs_created = []
        childcare_worker_assignments = []
        CHILDCARE_RATIO = 5  # One childcare worker supports 5 needing childcare

        # Calculate how many childcare jobs we need
        childcare_jobs_needed = -(-len(workers_with_childcare_needs) // CHILDCARE_RATIO)

        print(f"📌 Creating {childcare_jobs_needed} childcare jobs...")

        for _ in range(childcare_jobs_needed):
            cursor.execute("INSERT INTO jobs (title, description) VALUES (?, ?)", 
                           ("Childcare Provider", "Provides childcare support."))
            childcare_job_id = cursor.lastrowid
            childcare_jobs_created.append(childcare_job_id)

        print(f"✅ Created childcare jobs: {childcare_jobs_created}")

        # Step 4: Assign available workers to childcare jobs
        print(f"📌 Trying to assign {len(available_workers)} available workers to {len(childcare_jobs_created)} childcare jobs.")

        for childcare_job_id in childcare_jobs_created:
            if available_workers:
                assigned_worker = available_workers.pop(0)
                
                # Update the database to set the worker's job_id
                cursor.execute("""
                    UPDATE users
                    SET job_id = ?
                    WHERE id = ?
                """, (childcare_job_id, assigned_worker[0]))

                childcare_worker_assignments.append({
                    "childcare_job_id": childcare_job_id,
                    "worker_id": assigned_worker[0],
                    "worker_name": assigned_worker[1]
                })
                print(f"✅ Assigned {assigned_worker[1]} (ID: {assigned_worker[0]}) to Childcare Job {childcare_job_id}")

        conn.commit()
        conn.close()

        return jsonify({
            "jobs_created": len(childcare_jobs_created),
            "childcare_worker_assignments": childcare_worker_assignments
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5008)
