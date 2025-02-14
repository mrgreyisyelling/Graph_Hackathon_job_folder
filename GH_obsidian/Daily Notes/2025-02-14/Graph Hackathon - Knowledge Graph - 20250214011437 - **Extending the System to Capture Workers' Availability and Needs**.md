![[Pasted image 20250214131511.png]]### **Extending the System to Capture Workers' Availability and Needs**

We'll enhance the existing structure to:

1. **Allow workers to define their availability** (e.g., hours and days they can work).
2. **Capture specific requirements or preferences** (e.g., childcare, transportation, flexible hours).

This data will help match jobs not only based on skills but also on a worker's personal needs and availability.

---

### **📂 Database Updates**

#### **Extend the `users` table with availability and needs**

We'll add two new tables:

- **`worker_availability`**: Stores the hours and days a worker is available.
- **`worker_needs`**: Captures specific requirements like childcare, flexible hours, etc.

#### 📄 `database/setup/update_db.py`

```python
import sqlite3
import os

DB_PATH = "database/jobs/jobs.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add new tables for worker availability and needs
cursor.executescript("""
CREATE TABLE IF NOT EXISTS worker_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS worker_needs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    need TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ Database updated with worker availability and needs tables.")
```

#### **Run the script to update the database:**

```sh
python database/setup/update_db.py
```

---

### **📂 Frontend: Forms for Workers to Define Availability and Needs**

#### 📄 `frontend/forms/define_availability.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Define Availability</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Define Your Availability</h2>
        <form id="availabilityForm">
            <label>User ID</label>
            <input type="text" name="user_id" required>

            <label>Day of Week</label>
            <select name="day_of_week">
                <option value="Monday">Monday</option>
                <option value="Tuesday">Tuesday</option>
                <option value="Wednesday">Wednesday</option>
                <option value="Thursday">Thursday</option>
                <option value="Friday">Friday</option>
                <option value="Saturday">Saturday</option>
                <option value="Sunday">Sunday</option>
            </select>

            <label>Start Time</label>
            <input type="time" name="start_time" required>

            <label>End Time</label>
            <input type="time" name="end_time" required>

            <button type="submit">Set Availability</button>
        </form>

        <h2>Your Availability</h2>
        <table border="1" id="availabilityTable">
            <thead>
                <tr>
                    <th>Day</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                </tr>
            </thead>
            <tbody>
                <!-- Availability will be inserted here -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("availabilityForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5006/api/set_availability", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchAvailability(jsonData.user_id);
        };

        async function fetchAvailability(user_id) {
            let response = await fetch(`http://127.0.0.1:5006/api/get_availability?user_id=${user_id}`);
            let data = await response.json();

            let tableBody = document.getElementById("availabilityTable").querySelector("tbody");
            tableBody.innerHTML = "";

            data.availability.forEach(item => {
                let row = `<tr>
                    <td>${item.day_of_week}</td>
                    <td>${item.start_time}</td>
                    <td>${item.end_time}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }
    </script>
</body>
</html>
```

---

#### 📄 `frontend/forms/define_needs.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Define Needs</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Define Your Needs</h2>
        <form id="needsForm">
            <label>User ID</label>
            <input type="text" name="user_id" required>

            <label>Need</label>
            <input type="text" name="need" placeholder="e.g., Childcare, Transportation" required>

            <button type="submit">Add Need</button>
        </form>

        <h2>Your Needs</h2>
        <table border="1" id="needsTable">
            <thead>
                <tr>
                    <th>Need</th>
                </tr>
            </thead>
            <tbody>
                <!-- Needs will be inserted here -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("needsForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5006/api/add_need", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchNeeds(jsonData.user_id);
        };

        async function fetchNeeds(user_id) {
            let response = await fetch(`http://127.0.0.1:5006/api/get_needs?user_id=${user_id}`);
            let data = await response.json();

            let tableBody = document.getElementById("needsTable").querySelector("tbody");
            tableBody.innerHTML = "";

            data.needs.forEach(item => {
                let row = `<tr><td>${item.need}</td></tr>`;
                tableBody.innerHTML += row;
            });
        }
    </script>
</body>
</html>
```

---

### **📂 Backend API for Availability and Needs**

#### 📄 `backend/api/manage_availability_needs.py`

```python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = "database/jobs/jobs.db"

@app.route("/api/set_availability", methods=["POST"])
def set_availability():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO worker_availability (user_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
                   (data['user_id'], data['day_of_week'], data['start_time'], data['end_time']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Availability set."})

@app.route("/api/get_availability", methods=["GET"])
def get_availability():
    user_id = request.args.get("user_id")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT day_of_week, start_time, end_time FROM worker_availability WHERE user_id = ?", (user_id,))
    availability = cursor.fetchall()
    conn.close()
    return jsonify({"availability": [{"day_of_week": a[0], "start_time": a[1], "end_time": a[2]} for a in availability]})

@app.route("/api/add_need", methods=["POST"])
def add_need():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO worker_needs (user_id, need) VALUES (?, ?)", (data['user_id'], data['need']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Need added."})

@app.route("/api/get_needs", methods=["GET"])
def get_needs():
    user_id = request.args.get("user_id")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT need FROM worker_needs WHERE user_id = ?", (user_id,))
    needs = cursor.fetchall()
    conn.close()
    return jsonify({"needs": [{"need": n[0]} for n in needs]})

if __name__ == "__main__":
    app.run(debug=True, port=5006)
```

---

### **🚀 Running Everything**

1️⃣ **Update the database:**

```sh
python database/setup/update_db.py
```

2️⃣ **Start the API:**

```sh
python backend/api/manage_availability_needs.py
```

3️⃣ **Test the forms:**

- **Define Availability:** `http://127.0.0.1:5500/forms/define_availability.html`
- **Define Needs:** `http://127.0.0.1:5500/forms/define_needs.html`

---

Let me know if you need any further adjustments or features! 🚀