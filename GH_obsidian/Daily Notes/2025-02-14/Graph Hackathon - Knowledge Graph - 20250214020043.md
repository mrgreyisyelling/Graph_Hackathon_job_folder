![[Pasted image 20250214140212.png]]### **Calculating the Impact of a Social Unit Labor Injection**

Following the **diagram's logic**, we will:

1. **Identify workers in the "Available with Requirements" category**.
2. **Group these workers by the type of requirement (e.g., childcare, transportation)**.
3. **Simulate the effect of injecting one unit of labor into a social unit need** (e.g., providing childcare slots).
4. **Calculate how many workers become fully available as a result**.

---

### **📂 Updating the Worker Pool to Track Social Needs**

We need to modify our database to:

- **Group workers by their needs**.
- **Track how many workers require the same type of support**.
- **Simulate a social unit fulfilling those needs**.

---

### **📄 Modify `filter_workers.py` to Group Workers by Need**

📄 **File:** `backend/api/filter_workers.py`

```python
@app.route("/api/social_unit_impact", methods=["GET"])
def social_unit_impact():
    """
    Simulates adding a unit of labor to social support (e.g., childcare)
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

        # Step 3: Simulate the effect of adding one unit of labor to each social unit need
        impact_analysis = {}
        for need, count in need_counts.items():
            freed_workers = min(count, 1)  # 1 unit of labor can clear at most 1 worker's need
            impact_analysis[need] = {
                "workers_unlocked": freed_workers,
                "remaining_workers": count - freed_workers,
                "affected_workers": workers_per_need[need]
            }

        conn.close()

        return jsonify({"social_unit_impact": impact_analysis}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

---

### **📄 Creating a Frontend UI for Social Unit Impact**

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
                let row = `<tr>
                    <td>${need}</td>
                    <td>${entry.workers_unlocked}</td>
                    <td>${entry.remaining_workers}</td>
                </tr>`;
                tableBody.innerHTML += row;
            }
        }
    </script>
</body>
</html>
```

---

### **🚀 Running the Simulation**

1️⃣ **Start the Social Unit Impact API**

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

|**Need**|**Workers Unlocked**|**Remaining Workers**|
|---|---|---|
|Childcare|1|4|
|Transportation|1|2|
|Flexible Hours|1|3|

- One unit of labor added **unlocks one worker** at a time.
- If we continue adding labor to the social unit, we will unlock more workers.

---

### **🚀 Next Steps**

1. **Allow for scaling** → Instead of **1 unit of labor**, allow input for **X units**.
2. **Refine social unit interventions** → Some problems (e.g., flexible hours) may not need extra labor.
3. **Integrate with actual job matching** → If a worker is **unlocked**, they should immediately move into the available pool.

---

### **🔥 This now models how adding social support increases the labor pool!**

Try it and let me know if any improvements are needed! 🚀