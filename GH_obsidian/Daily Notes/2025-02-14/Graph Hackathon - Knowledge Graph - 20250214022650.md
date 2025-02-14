### **Adjusting Social Unit Impact Calculation**

We will modify the calculation so that **one unit of childcare frees up to 6 workers, and one unit of transportation frees up to 4 workers.**

This means that instead of unlocking **only 1 worker per unit of labor**, each social unit type will have **different efficiency rates**.

---

### **📂 Updating `filter_workers.py` to Use New Labor Efficiency**

📄 **File:** `backend/api/filter_workers.py`

```python
@app.route("/api/social_unit_impact", methods=["GET"])
def social_unit_impact():
    """
    Simulates adding a unit of labor to social support (e.g., childcare, transportation)
    and calculates how many workers would become available.
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

        # Step 2: Group workers by type of need
        need_counts = {}
        workers_per_need = {}
        for worker_id, name, need in workers_with_needs:
            if need not in need_counts:
                need_counts[need] = 0
                workers_per_need[need] = []
            need_counts[need] += 1
            workers_per_need[need].append({"id": worker_id, "name": name})

        # Step 3: Define labor efficiency (how many workers can be freed per unit)
        labor_efficiency = {
            "Childcare": 6,
            "Transportation": 4,
            "Remote Work": 3,
            "Flexible Hours": 5  # Example, can be adjusted
        }

        # Step 4: Calculate impact based on efficiency
        impact_analysis = {}
        for need, count in need_counts.items():
            freed_workers = min(count, labor_efficiency.get(need, 1))  # Default to 1 if need is unknown
            impact_analysis[need] = {
                "workers_unlocked": freed_workers,
                "remaining_workers": count - freed_workers,
                "affected_workers": workers_per_need[need][:freed_workers]  # Show which workers are freed
            }

        conn.close()

        return jsonify({"social_unit_impact": impact_analysis}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

---

### **📂 Updating the Frontend to Reflect New Labor Units**

📄 **File:** `frontend/forms/social_unit_impact.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Social Unit Impact</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Simulating Social Unit Labor Injection</h2>
        <button onclick="fetchSocialUnitImpact()">Calculate Impact</button>

        <h2>Impact Results</h2>
        <table border="1" id="impactTable">
            <thead>
                <tr>
                    <th>Need</th>
                    <th>Workers Unlocked</th>
                    <th>Remaining Workers</th>
                    <th>Freed Workers</th>
                </tr>
            </thead>
            <tbody>
                <!-- Impact results will be inserted here -->
            </tbody>
        </table>
    </div>

    <script>
        async function fetchSocialUnitImpact() {
            let response = await fetch("http://127.0.0.1:5007/api/social_unit_impact");
            let data = await response.json();
            console.log("✅ API Response:", data);

            let tableBody = document.getElementById("impactTable").querySelector("tbody");
            tableBody.innerHTML = "";

            for (let need in data.social_unit_impact) {
                let entry = data.social_unit_impact[need];
                let freedWorkers = entry.affected_workers.map(worker => worker.name).join(", ");

                let row = `<tr>
                    <td>${need}</td>
                    <td>${entry.workers_unlocked}</td>
                    <td>${entry.remaining_workers}</td>
                    <td>${freedWorkers}</td>
                </tr>`;
                tableBody.innerHTML += row;
            }
        }
    </script>
</body>
</html>
```

---

### **🚀 Steps to Run the Updated Simulation**

1️⃣ **Restart the API**

```sh
python backend/api/filter_workers.py
```

2️⃣ **Visit the Frontend**

```
http://127.0.0.1:5500/forms/social_unit_impact.html
```

3️⃣ **Click the button to calculate impact.**

---

### **🔍 Expected Output**

|**Need**|**Workers Unlocked**|**Remaining Workers**|**Freed Workers**|
|---|---|---|---|
|Childcare|6|3|Alice, Bob, Eve, Joe, Mike, Sarah|
|Transportation|4|2|David, Chris, Laura, Steve|
|Remote Work|3|1|Mark, Tom, Jane|

**Interpretation:**

- Childcare had **9 workers in need**, so **1 unit freed 6**.
- Transportation had **6 workers in need**, so **1 unit freed 4**.
- Remote Work had **4 workers in need**, so **1 unit freed 3**.

---

### **🚀 Next Steps**

1. **Allow users to input multiple labor units for testing scalability.**
2. **Incorporate real-world thresholds for labor needs.**
3. **Ensure freed workers move into the "Available for Work" category automatically.**

This should now accurately model how **social unit intervention unlocks more labor capacity.** Let me know if you need further adjustments! 🚀🔥