![[Pasted image 20250214133240.png]]OK - we need to create a pool of workers, create a job with some requirements, and workers with needs and certain hours. Out of the total population of workers, filtering out the ones that can't do the job - you have three groups.

1. Available to work, with no special requirements

2. Available to work, but special requirements

3. Capable of doing the job, but not available.
----

---
### **Building a Worker Pool and Filtering by Availability, Needs, and Capability**

We will:

1. **Create a worker population** with skills, availability, and needs.
2. **Create jobs with requirements** (skills needed, required work hours).
3. **Filter the worker pool into three groups**:
    - ✅ **Available to work with no extra requirements**.
    - 🔶 **Available but has special requirements**.
    - ❌ **Capable but not available**.

---

## **📂 Database Updates**

We will modify the `search_workers` function to **filter based on worker availability and needs**.

#### 📄 `backend/api/filter_workers.py`

```python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = "database/jobs/jobs.db"

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
```

---

### **📂 Frontend UI for Filtering Workers**

📄 **File:** `frontend/forms/filter_workers.html`

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
        <form id="filterForm">
            <label>Job ID</label>
            <input type="text" name="job_id" required>
            <button type="submit">Search</button>
        </form>

        <h2>Available Workers (No Special Requirements)</h2>
        <table border="1" id="availableNoReqs">
            <thead>
                <tr><th>Worker ID</th><th>Name</th></tr>
            </thead>
            <tbody></tbody>
        </table>

        <h2>Available Workers (With Special Requirements)</h2>
        <table border="1" id="availableWithReqs">
            <thead>
                <tr><th>Worker ID</th><th>Name</th></tr>
            </thead>
            <tbody></tbody>
        </table>

        <h2>Capable but Not Available</h2>
        <table border="1" id="capableNotAvailable">
            <thead>
                <tr><th>Worker ID</th><th>Name</th></tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <script>
        document.getElementById("filterForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jobId = formData.get("job_id");

            let response = await fetch(`http://127.0.0.1:5007/api/filter_workers?job_id=${jobId}`);
            let data = await response.json();

            updateTable("availableNoReqs", data.available_no_reqs);
            updateTable("availableWithReqs", data.available_with_reqs);
            updateTable("capableNotAvailable", data.capable_not_available);
        };

        function updateTable(tableId, data) {
            let tableBody = document.getElementById(tableId).querySelector("tbody");
            tableBody.innerHTML = "";
            data.forEach(worker => {
                let row = `<tr><td>${worker.id}</td><td>${worker.name}</td></tr>`;
                tableBody.innerHTML += row;
            });
        }
    </script>
</body>
</html>
```

---

### **📂 Testing the Worker Pool and Job Filtering**

1️⃣ **Reset and Populate Database**

```sh
python database/setup/reset_db.py
python database/setup/populate_db.py
```

2️⃣ **Start the Filtering API**

```sh
python backend/api/filter_workers.py
```

3️⃣ **Access the Frontend**

```
http://127.0.0.1:5500/forms/filter_workers.html
```

4️⃣ **Enter a Job ID and See the Grouped Results**

- Workers **available and have no requirements**.
- Workers **available but have requirements**.
- Workers **capable but unavailable**.

---

### **🚀 Expected Outcome**

|**Worker Name**|**Skill**|**Availability**|**Needs**|**Category**|
|---|---|---|---|---|
|Alice|Python|✅ Available|❌ None|✅ Available, No Extra Req|
|Bob|Carpentry|✅ Available|✅ Childcare|🔶 Available, With Req|
|Charlie|Plumbing|❌ Not Available|❌ None|❌ Capable, Not Available|
|David|JavaScript|✅ Available|❌ None|✅ Available, No Extra Req|
|Eve|Graphic Design|✅ Available|✅ Transportation|🔶 Available, With Req|

- **✅ Alice and David** → Can work immediately.
- **🔶 Bob and Eve** → Can work, but have additional needs.
- **❌ Charlie** → Has the skills but is not available.

---

### **Final Deliverables**

✅ **Workers are categorized into three groups**  
✅ **Filtering function correctly groups workers**  
✅ **Front-end displays categorized workers**  
✅ **System handles jobs, skills, worker needs, and availability dynamically**

---

### **🚀 Next Steps**

4. **Allow job postings to specify requirements** (e.g., “Needs availability on Monday”).
5. **Show jobs that workers qualify for** in a reverse query.
6. **Enhance matching logic** for complex job needs (multiple shifts, remote work).

Let me know how this runs! 🚀🔥