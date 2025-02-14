import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = "database/jobs/jobs.db"

@app.route("/api/social_unit_impact", methods=["GET"])
def social_unit_impact():
    """
    Simulates adding social support (e.g., childcare, transportation)
    and calculates:
    - How many labor units are needed to unlock all workers
    - The total number of workers unlocked
    - The ratio of workers unlocked per unit of labor
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Step 1: Get workers in "Available with Requirements" category
        cursor.execute("""
            SELECT DISTINCT users.id, users.name, worker_needs.need
            FROM users
            JOIN worker_needs ON users.id = worker_needs.user_id
            JOIN user_skills ON users.id = user_skills.user_id
            WHERE users.id IN (SELECT DISTINCT user_id FROM worker_availability)
        """)
        workers_with_needs = cursor.fetchall()  # [(id, name, need), ...]

        # Step 2: Group workers by type of need (ignoring flexible hours & remote work)
        tracked_needs = ["Childcare", "Transportation"]
        need_counts = {need: 0 for need in tracked_needs}
        workers_per_need = {need: [] for need in tracked_needs}

        for worker_id, name, need in workers_with_needs:
            if need in tracked_needs:
                need_counts[need] += 1
                workers_per_need[need].append({"id": worker_id, "name": name})

        # Step 3: Define labor efficiency (how many workers can be freed per unit)
        labor_efficiency = {
            "Childcare": 6,
            "Transportation": 4
        }

        # Step 4: Calculate how many labor units are needed and total workers unlocked
        labor_units_needed = 0
        total_workers_unlocked = 0
        impact_analysis = {}

        for need, count in need_counts.items():
            if count > 0:
                units_required = -(-count // labor_efficiency[need])  # Ceiling division
                workers_freed = min(count, units_required * labor_efficiency[need])  # Cap to actual count
                labor_units_needed += units_required
                total_workers_unlocked += workers_freed

                impact_analysis[need] = {
                    "total_workers": count,
                    "labor_units_required": units_required,
                    "workers_freed": workers_per_need[need][:workers_freed]  # Show which workers are freed
                }

        # Step 5: Compute ratio of workers unlocked per labor unit
        unlock_ratio = round(total_workers_unlocked / labor_units_needed, 2) if labor_units_needed > 0 else 0

        conn.close()

        return jsonify({
            "social_unit_impact": impact_analysis,
            "total_labor_units_needed": labor_units_needed,
            "total_workers_unlocked": total_workers_unlocked,
            "unlock_ratio": unlock_ratio
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/filter_workers", methods=["GET"])
def filter_workers():
    try:
        job_id = request.args.get("job_id")
        if not job_id:
            return jsonify({"error": "Missing job_id parameter"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Step 1: Get required skills for the job
        cursor.execute("SELECT skill_id FROM job_requirements WHERE job_id = ?", (job_id,))
        required_skills = [row[0] for row in cursor.fetchall()]
        if not required_skills:
            return jsonify({"message": "No skills required for this job"}), 200

        # Step 2: Find workers with required skills
        cursor.execute(f"""
            SELECT DISTINCT users.id, users.name FROM users
            JOIN user_skills ON users.id = user_skills.user_id
            WHERE user_skills.skill_id IN ({','.join(['?']*len(required_skills))})
        """, required_skills)
        skilled_workers = {row[0]: row[1] for row in cursor.fetchall()}  # {user_id: name}

        # Step 3: Find workers' availability
        cursor.execute("""
            SELECT user_id FROM worker_availability
        """)
        available_workers = {row[0] for row in cursor.fetchall()}  # Set of available worker IDs

        # Step 4: Find workers with special needs
        cursor.execute("""
            SELECT DISTINCT user_id FROM worker_needs
        """)
        workers_with_needs = {row[0] for row in cursor.fetchall()}  # Set of worker IDs with needs

        conn.close()

        # Step 5: Categorize Workers
        available_no_reqs = []
        available_with_reqs = []
        capable_not_available = []

        for worker_id, name in skilled_workers.items():
            if worker_id in available_workers:
                if worker_id in workers_with_needs:
                    available_with_reqs.append({"id": worker_id, "name": name})
                else:
                    available_no_reqs.append({"id": worker_id, "name": name})
            else:
                capable_not_available.append({"id": worker_id, "name": name})

        return jsonify({
            "available_no_reqs": available_no_reqs,
            "available_with_reqs": available_with_reqs,
            "capable_not_available": capable_not_available
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5007)