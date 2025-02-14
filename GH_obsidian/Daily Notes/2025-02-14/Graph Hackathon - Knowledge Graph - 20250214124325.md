![[Pasted image 20250214124336.png]]

ok, like users and skills  - we need to create jobs and requirements for those jobs


### **Building the Job and Requirements System**

Similar to **Users & Skills**, we need to:

1. **Create jobs** – Job postings with descriptions.
2. **Create job requirements** – Specific skills, experience, or certifications required for the job.

These will be **stored in SQLite** and later **synchronized with Neo4j**.

---

## **📂 Frontend: Job Forms**

#### 📄 `frontend/forms/create_job.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Job</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Create a Job</h2>
        <form id="jobForm">
            <label>Job Title</label>
            <input type="text" name="job_title" required>

            <label>Job Description</label>
            <textarea name="job_description" required></textarea>

            <button type="submit">Create Job</button>
        </form>

        <h2>Available Jobs</h2>
        <button onclick="fetchJobs()">Refresh Jobs</button>
        <table border="1" id="jobsTable">
            <thead>
                <tr>
                    <th>Job ID</th>
                    <th>Title</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <!-- Jobs will be inserted here dynamically -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("jobForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5004/api/create_job", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchJobs(); // Refresh job list
        };

        async function fetchJobs() {
            let response = await fetch("http://127.0.0.1:5004/api/get_jobs");
            let data = await response.json();

            let tableBody = document.getElementById("jobsTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing rows

            data.jobs.forEach(job => {
                let row = `<tr>
                    <td>${job.id}</td>
                    <td>${job.title}</td>
                    <td>${job.description}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }

        fetchJobs(); // Load jobs on page load
    </script>
</body>
</html>
```

---

#### 📄 `frontend/forms/create_requirements.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Job Requirements</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Assign Requirements to a Job</h2>
        <form id="requirementsForm">
            <label>Job ID</label>
            <input type="text" name="job_id" required>

            <label>Requirement (Skill ID or Other)</label>
            <input type="text" name="requirement" required>

            <button type="submit">Assign Requirement</button>
        </form>

        <h2>Job Requirements</h2>
        <button onclick="fetchRequirements()">Refresh Requirements</button>
        <table border="1" id="requirementsTable">
            <thead>
                <tr>
                    <th>Job ID</th>
                    <th>Requirement</th>
                </tr>
            </thead>
            <tbody>
                <!-- Requirements will be inserted here dynamically -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("requirementsForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5004/api/create_requirement", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchRequirements(); // Refresh requirement list
        };

        async function fetchRequirements() {
            let response = await fetch("http://127.0.0.1:5004/api/get_requirements");
            let data = await response.json();

            let tableBody = document.getElementById("requirementsTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing rows

            data.requirements.forEach(req => {
                let row = `<tr>
                    <td>${req.job_id}</td>
                    <td>${req.requirement}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }

        fetchRequirements(); // Load job requirements on page load
    </script>
</body>
</html>
```

---

## **📂 Backend API**

#### 📄 `backend/api/manage_jobs.py`

```python
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
```

---

### **🚀 Running Everything**

1️⃣ **Start the Job API**

```sh
python backend/api/manage_jobs.py
```

2️⃣ **Visit `create_job.html` and add jobs**

```
http://127.0.0.1:5500/forms/create_job.html
```

3️⃣ **Visit `create_requirements.html` and link requirements**

```
http://127.0.0.1:5500/forms/create_requirements.html
```

4️⃣ **Check the database**

```sh
sqlite3 database/jobs/jobs.db
sqlite> SELECT * FROM jobs;
sqlite> SELECT * FROM job_requirements;
```

🚀 Let me know how it works!