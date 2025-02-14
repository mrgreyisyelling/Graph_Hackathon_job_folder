![[Pasted image 20250214130040.png]]
OK we want to dump the user, skills, jobs and requirements tables, recreate them, and then populate them with Jobs with requirements and a population of people with some of the skill requirements


-----

### **Rebuilding and Populating the Database for Jobs, Requirements, and Workers**

We will:

1. **Delete and recreate the tables** for `users`, `skills`, `jobs`, and `job_requirements`.
2. **Insert sample data**:
    - Jobs with requirements.
    - A population of workers with different skills.
3. **Prepare for querying**: Finding workers for jobs based on skill matches.

---

### **📂 Step 1: Wipe and Rebuild the Database**

📄 **File:** `database/setup/reset_db.py`

```python
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
```

#### **🚀 Run this script to reset the database:**

```sh
python database/setup/reset_db.py
```

---

### **📂 Step 2: Populate the Database with Sample Data**

📄 **File:** `database/setup/populate_db.py`

```python
import sqlite3
import os

DB_PATH = "database/jobs/jobs.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Insert sample users (workers)
cursor.executemany("""
INSERT INTO users (name) VALUES (?)
""", [
    ("Alice",),
    ("Bob",),
    ("Charlie",),
    ("David",),
    ("Eve",)
])

# Insert sample skills
cursor.executemany("""
INSERT INTO skills (name) VALUES (?)
""", [
    ("Python",),
    ("Data Analysis",),
    ("Carpentry",),
    ("Plumbing",),
    ("JavaScript",),
    ("Graphic Design",)
])

# Insert sample jobs
cursor.executemany("""
INSERT INTO jobs (title, description) VALUES (?, ?)
""", [
    ("Software Engineer", "Develop software using Python."),
    ("Data Analyst", "Analyze data and generate reports."),
    ("Construction Worker", "Work on construction sites."),
    ("Plumber", "Fix plumbing issues."),
    ("Web Developer", "Develop web applications with JavaScript."),
    ("Designer", "Create digital graphics and branding.")
])

# Insert job requirements (skill_id corresponds to the skills table)
cursor.executemany("""
INSERT INTO job_requirements (job_id, skill_id) VALUES (?, ?)
""", [
    (1, 1),  # Software Engineer requires Python
    (2, 2),  # Data Analyst requires Data Analysis
    (3, 3),  # Construction Worker requires Carpentry
    (4, 4),  # Plumber requires Plumbing
    (5, 5),  # Web Developer requires JavaScript
    (6, 6)   # Designer requires Graphic Design
])

# Assign skills to users (simulate skill ownership)
cursor.executemany("""
INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)
""", [
    (1, 1),  # Alice knows Python
    (1, 2),  # Alice also knows Data Analysis
    (2, 3),  # Bob knows Carpentry
    (3, 4),  # Charlie knows Plumbing
    (4, 5),  # David knows JavaScript
    (5, 6)   # Eve knows Graphic Design
])

conn.commit()
conn.close()

print("✅ Sample data inserted into the database.")
```

#### **🚀 Run this script to insert sample data:**

```sh
python database/setup/populate_db.py
```

---

### **📂 Step 3: Querying for Workers That Match Job Requirements**

Now that we have jobs, requirements, and users with skills, let's write a query to **find workers for jobs based on skills**.

#### 📄 **File:** `backend/api/search_workers.py`

```python
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
```

#### **🚀 Start the API**

```sh
python backend/api/search_workers.py
```

#### **🧐 Example Query**

To find workers for **job ID 1 (Software Engineer)**:

```
http://127.0.0.1:5005/api/search_workers?job_id=1
```

✅ **Expected Output**

```json
{
  "workers": [
    { "id": 1, "name": "Alice" }
  ]
}
```

Alice is matched because she has the **Python** skill.

---

### **📂 Step 4: Frontend UI for Searching Workers**

📄 **File:** `frontend/forms/search_workers.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Find Workers for a Job</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Search for Workers</h2>
        <form id="searchForm">
            <label>Job ID</label>
            <input type="text" name="job_id" required>
            <button type="submit">Search</button>
        </form>

        <h2>Matching Workers</h2>
        <table border="1" id="workersTable">
            <thead>
                <tr>
                    <th>Worker ID</th>
                    <th>Name</th>
                </tr>
            </thead>
            <tbody>
                <!-- Workers will be inserted here dynamically -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("searchForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch(`http://127.0.0.1:5005/api/search_workers?job_id=${jsonData.job_id}`);
            let data = await response.json();

            let tableBody = document.getElementById("workersTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing rows

            data.workers.forEach(worker => {
                let row = `<tr>
                    <td>${worker.id}</td>
                    <td>${worker.name}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        };
    </script>
</body>
</html>
```

---

### **🚀 Final Steps**

1️⃣ **Run the reset and populate scripts**

```sh
python database/setup/reset_db.py
python database/setup/populate_db.py
```

2️⃣ **Start the Search API**

```sh
python backend/api/search_workers.py
```

3️⃣ **Visit the UI and test searching for workers**

```
http://127.0.0.1:5500/forms/search_workers.html
```

---

Everything should now be functional! **Let me know how it works or if you need tweaks! 🚀**