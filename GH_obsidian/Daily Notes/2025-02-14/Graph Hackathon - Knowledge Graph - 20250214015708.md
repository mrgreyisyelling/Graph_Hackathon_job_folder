### **Debugging the "Capable but Not Available" Category Not Appearing**

If no workers are appearing in the **"Capable but Not Available"** category, it means that all skilled workers **are either available or have needs**—which is unlikely with our randomized dataset.

---

### **🔍 Steps to Debug**

We'll follow these steps:

1. **Manually check if "capable but not available" workers exist in the database.**
2. **Debug the filtering logic in `filter_workers.py`.**
3. **Verify that the frontend is displaying all returned data.**

---

### **Step 1: Manually Check for Capable but Unavailable Workers**

Run the following SQL query in **SQLite** to check for workers with skills but no availability.

```sh
sqlite3 database/jobs/jobs.db
```

Then, run:

```sql
SELECT DISTINCT users.id, users.name, skills.name 
FROM users
JOIN user_skills ON users.id = user_skills.user_id
JOIN skills ON user_skills.skill_id = skills.id
WHERE users.id NOT IN (
    SELECT DISTINCT user_id FROM worker_availability
);
```

**Expected Output:**  
A list of workers who have at least **one skill required for a job but are NOT in the `worker_availability` table.**  
If this list is **empty**, we need to adjust our dataset.

---

### **Step 2: Fix Data if No Workers Are Unavailable**

If **no workers** were returned from the above query, we need to ensure that **some workers have no availability**.

#### **Modify the `populate_db.py` script to leave some workers without availability**

Add this after inserting `worker_availability`:

📄 **File:** `database/setup/populate_db.py`

```python
# Ensure at least 10 workers have NO availability
workers_with_no_availability = random.sample(range(1, 51), 10)  # Pick 10 workers to have no shifts
cursor.executemany("DELETE FROM worker_availability WHERE user_id = ?", [(wid,) for wid in workers_with_no_availability])
```

Then **rerun the population script**:

```sh
python database/setup/reset_db.py
python database/setup/populate_db.py
```

Now, rerun the SQL query to **ensure that some workers are actually missing from the availability table**.

---

### **Step 3: Debug the Filtering Logic in `filter_workers.py`**

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

        # Step 2: Find workers with required skills
        cursor.execute(f"""
            SELECT DISTINCT users.id, users.name FROM users
            JOIN user_skills ON users.id = user_skills.user_id
            WHERE user_skills.skill_id IN ({','.join(['?']*len(required_skills))})
        """, required_skills)
        skilled_workers = {row[0]: row[1] for row in cursor.fetchall()}  # {user_id: name}

        # Step 3: Find workers' availability
        cursor.execute("SELECT DISTINCT user_id FROM worker_availability")
        available_workers = {row[0] for row in cursor.fetchall()}  # Set of available worker IDs

        # Step 4: Find workers with special needs
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
                capable_not_available.append({"id": worker_id, "name": name})  # 🔥 Ensure this category gets populated

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

**Then restart the filtering API:**

```sh
python backend/api/filter_workers.py
```

Check **logs in the terminal** when making requests. If `❌ Capable But Not Available: 0` appears, we need to fix the dataset.

---

### **Step 4: Verify the Frontend is Displaying Results**

If the backend **correctly categorizes** workers but the **frontend is still empty**, update the script in `filter_workers.html` to log responses.

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
        data.forEach(worker => {
            let row = `<tr><td>${worker.id}</td><td>${worker.name}</td></tr>`;
            tableBody.innerHTML += row;
        });
    }
</script>
```

**Then:**

4. Open your browser’s **Developer Tools (`F12` → Console tab)**
5. Check the logs for `"✅ API Response:"` to ensure `capable_not_available` is populated.

---

### **Final Checklist**

- ✅ **Ensure 10+ workers have NO availability** (run the SQL query above).
- ✅ **Confirm `"❌ Capable But Not Available"` appears in API logs** (from `filter_workers.py`).
- ✅ **Check the browser console for API responses** (ensure the frontend receives correct data).

---

### **🚀 Once these fixes are applied, the third category should now populate correctly!**

Let me know if you need further debugging! 🚀🔥