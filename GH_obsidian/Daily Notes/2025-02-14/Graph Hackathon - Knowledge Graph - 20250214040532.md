![[Pasted image 20250214160616.png]]### **🛠 Next Steps: Display Workforce & Support Calculations**

Now that **everything is working**, we need to go back to the **original workforce breakdown** and show:

1️⃣ **People freely available for work**  
2️⃣ **People available but need transportation or childcare**  
3️⃣ **People capable but unavailable**  
4️⃣ **Number of workers providing support (childcare & transportation)**  
5️⃣ **Total net benefit (extra workers unlocked by support)**

---

### **🛠 Step 1: Modify `generate_childcare_jobs.py` to Return More Data**

We need the API to calculate and return:

- **Freely available workers**
- **Available workers with needs**
- **Workers capable but unavailable**
- **Workers assigned to support (childcare/transportation)**
- **Total net benefit (unlocked workforce)**

📂 **File:** `backend/api/generate_childcare_jobs.py`

```python
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DB_PATH = "Forms_UserCreation/database/jobs/jobs.db"

@app.route("/api/workforce_summary", methods=["GET"])
def workforce_summary():
    """
    Summarizes workforce distribution:
    - Freely available workers
    - Available workers with childcare/transportation needs
    - Capable but unavailable workers
    - Support workers (childcare/transportation)
    - Net benefit (unlocked workforce)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Step 1: Freely available workers (No job, no support needed)
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE id NOT IN (SELECT user_id FROM worker_needs)
            AND job_id IS NULL;
        """)
        freely_available = cursor.fetchone()[0]

        # Step 2: Available but need childcare/transportation
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            JOIN worker_needs ON users.id = worker_needs.user_id
            WHERE job_id IS NULL;
        """)
        available_with_needs = cursor.fetchone()[0]

        # Step 3: Capable but unavailable (Have required skills but already working)
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            JOIN user_skills ON users.id = user_skills.user_id
            WHERE job_id IS NOT NULL;
        """)
        capable_but_unavailable = cursor.fetchone()[0]

        # Step 4: Support workers (Assigned to childcare/transportation jobs)
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE job_id IN (SELECT id FROM jobs WHERE title = 'Childcare Provider' OR title = 'Transportation Provider');
        """)
        support_workers = cursor.fetchone()[0]

        # Step 5: Net benefit (Total extra workers unlocked)
        UNLOCKED_RATIO_CHILDCARE = 5
        UNLOCKED_RATIO_TRANSPORTATION = 4

        unlocked_workers = (support_workers // 2) * UNLOCKED_RATIO_CHILDCARE + (support_workers // 2) * UNLOCKED_RATIO_TRANSPORTATION

        conn.close()

        return jsonify({
            "freely_available": freely_available,
            "available_with_needs": available_with_needs,
            "capable_but_unavailable": capable_but_unavailable,
            "support_workers": support_workers,
            "total_unlocked_workers": unlocked_workers
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5008)
```

---

### **🛠 Step 2: Update Frontend (`generate_childcare_jobs.html`)**

We need to **display** these values on the HTML page.

📂 **File:** `frontend/forms/generate_childcare_jobs.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Workforce Summary</title>
    <script>
        async function fetchWorkforceSummary() {
            try {
                console.log("🔄 Fetching workforce summary...");
                let response = await fetch("http://127.0.0.1:5008/api/workforce_summary");

                if (!response.ok) {
                    console.error("❌ API request failed:", response.statusText);
                    return;
                }

                let data = await response.json();
                console.log("✅ API Response:", data);

                document.getElementById("freelyAvailable").innerText = data.freely_available;
                document.getElementById("availableWithNeeds").innerText = data.available_with_needs;
                document.getElementById("capableButUnavailable").innerText = data.capable_but_unavailable;
                document.getElementById("supportWorkers").innerText = data.support_workers;
                document.getElementById("totalUnlocked").innerText = data.total_unlocked_workers;

            } catch (error) {
                console.error("❌ Error fetching API:", error);
            }
        }
    </script>
</head>
<body>
    <div>
        <h2>Workforce Summary</h2>
        <button onclick="fetchWorkforceSummary()">Update Workforce Data</button>

        <p><strong>Freely Available Workers:</strong> <span id="freelyAvailable">-</span></p>
        <p><strong>Available but Need Support:</strong> <span id="availableWithNeeds">-</span></p>
        <p><strong>Capable but Unavailable:</strong> <span id="capableButUnavailable">-</span></p>
        <p><strong>Support Workers (Childcare/Transportation):</strong> <span id="supportWorkers">-</span></p>
        <p><strong>Total Workers Unlocked by Support:</strong> <span id="totalUnlocked">-</span></p>
    </div>
</body>
</html>
```

---

### **🛠 Step 3: Restart Everything & Test**

1. **Restart Flask API**
    
    ```sh
    python backend/api/generate_childcare_jobs.py
    ```
    
2. **Open the API manually**
    
    ```
    http://127.0.0.1:5008/api/workforce_summary
    ```
    
    Expected JSON:
    
    ```json
    {
        "freely_available": 10,
        "available_with_needs": 8,
        "capable_but_unavailable": 15,
        "support_workers": 6,
        "total_unlocked_workers": 24
    }
    ```
    
3. **Click the button on the HTML page** (`http://127.0.0.1:5500/forms/generate_childcare_jobs.html`)

✅ **Numbers should appear on the page!**

---

### **🚀 Summary**

✅ **API now calculates workforce summary.**  
✅ **Frontend dynamically displays workforce stats.**  
✅ **Now we can analyze how many workers need support and the net gain!**

🔥 **Try this now and let me know what needs adjusting!** 🚀