### **Fixing "Capable but Not Available" Issue**

If the **"Capable but Not Available"** category is still **empty**, it means that every worker with the necessary skills is also available in the `worker_availability` table, which is **incorrect**.

We need to:

1. **Ensure some workers with skills are NOT in the `worker_availability` table.**
2. **Modify the filtering logic to correctly detect "capable but not available" workers.**
3. **Verify that the database contains the expected data.**
4. **Confirm the frontend correctly displays results.**

---

### **🛠 Step 1: Manually Check for Capable But Unavailable Workers**

Run the following **SQL query** to check if any skilled workers are missing from `worker_availability`.

#### **Run in SQLite**

```sh
sqlite3 database/jobs/jobs.db
```

Then, execute:

```sql
SELECT DISTINCT users.id, users.name, skills.name 
FROM users
JOIN user_skills ON users.id = user_skills.user_id
JOIN skills ON user_skills.skill_id = skills.id
WHERE users.id NOT IN (
    SELECT DISTINCT user_id FROM worker_availability
);
```

#### **Expected Output**

A list of workers who **have at least one skill required for a job but are NOT in the worker_availability table.**  
If this list is **empty**, it means every skilled worker is also available, which is why **"Capable but Not Available"** is empty.

---

### **🛠 Step 2: Fix the Data if No Workers Are Unavailable**

If the above query **returns no results**, we need to **manually ensure** some workers are **NOT available**.

📄 **Modify `populate_db.py` to remove availability for some workers**

```python
# Ensure at least 10 workers have NO availability
workers_with_no_availability = random.sample(range(1, 51), 10)  # Pick 10 workers to have no shifts
cursor.executemany("DELETE FROM worker_availability WHERE user_id = ?", [(wid,) for wid in workers_with_no_availability])

conn.commit()
conn.close()
print("✅ Large-scale sample data inserted, ensuring 10+ workers are NOT available.")
```

Then **rerun the population script**:

```sh
python database/setup/reset_db.py
python database/setup/populate_db.py
```

**Run the SQL query again to verify that some skilled workers have no availability.**

---

### **🛠 Step 3: Modify the Filtering Logic to Ensure Correct Categorization**

📄 **File:** `backend/api/filter_workers.py`

```python
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

        # Step 2: Find all workers who have the required skills
        cursor.execute(f"""
            SELECT DISTINCT users.id, users.name FROM users
            JOIN user_skills ON users.id = user_skills.user_id
            WHERE user_skills.skill_id IN ({','.join(['?']*len(required_skills))})
        """, required_skills)
        skilled_workers = {row[0]: row[1] for row in cursor.fetchall()}  # {user_id: name}

        # Step 3: Find workers who ARE available
        cursor.execute("SELECT DISTINCT user_id FROM worker_availability")
        available_workers = {row[0] for row in cursor.fetchall()}  # Set of available worker IDs

        # Step 4: Find workers who have special needs
        cursor.execute("SELECT DISTINCT user_id FROM worker_needs")
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
                capable_not_available.append({"id": worker_id, "name": name})  # 🔥 Ensure this gets populated

        print(f"✅ Available (No Req): {len(available_no_reqs)}")
        print(f"🔶 Available (With Req): {len(available_with_reqs)}")
        print(f"❌ Capable But Not Available: {len(capable_not_available)}")  # Debugging output

        return jsonify({
            "available_no_reqs": available_no_reqs,
            "available_with_reqs": available_with_reqs,
            "capable_not_available": capable_not_available
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### **🛠 Step 4: Restart and Debug**

1️⃣ Restart the API:

```sh
python backend/api/filter_workers.py
```

2️⃣ Check **terminal logs** for:

```sh
❌ Capable But Not Available: X  (Should be >0)
```

3️⃣ If it’s **still 0**, rerun the SQL query:

```sql
SELECT * FROM worker_availability WHERE user_id NOT IN (SELECT DISTINCT user_id FROM worker_availability);
```

4️⃣ If it **returns workers**, but they **aren't appearing in the API response**, add this debug line inside the loop:

```python
print(f"🔍 Worker {worker_id} ({name}) should be in 'Capable but Not Available'")
```

Then **check API logs** after querying a job.

---

### **🛠 Step 5: Verify Frontend is Displaying Results**

📄 **File:** `frontend/forms/filter_workers.html`

```html
<script>
    document.getElementById("filterForm").onsubmit = async function(e) {
        e.preventDefault();
        let formData = new FormData(e.target);
        let jobId = formData.get("job_id");

        let response = await fetch(`http://127.0.0.1:5007/api/filter_workers?job_id=${jobId}`);
        let data = await response.json();

        console.log("✅ API Response:", data);  // 🔥 Debugging output in browser console

        updateTable("availableNoReqs", data.available_no_reqs);
        updateTable("availableWithReqs", data.available_with_reqs);
        updateTable("capableNotAvailable", data.capable_not_available);
    };

    function updateTable(tableId, data) {
        let tableBody = document.getElementById(tableId).querySelector("tbody");
        tableBody.innerHTML = "";
        if (!data.length) {
            console.warn(`⚠️ No data for ${tableId}`);  // Debugging output
        }
        data.forEach(worker => {
            let row = `<tr><td>${worker.id}</td><td>${worker.name}</td></tr>`;
            tableBody.innerHTML += row;
        });
    }
</script>
```

---

### **🚀 Final Checklist**

- ✅ **Ensure 10+ workers have NO availability** (run the SQL query above).
- ✅ **Confirm `"❌ Capable But Not Available"` appears in API logs** (from `filter_workers.py`).
- ✅ **Check the browser console for API responses** (ensure the frontend receives correct data).

---

### **🚀 Now "Capable but Not Available" should be correctly populated.**

Let me know if anything else needs fixing! 🚀🔥