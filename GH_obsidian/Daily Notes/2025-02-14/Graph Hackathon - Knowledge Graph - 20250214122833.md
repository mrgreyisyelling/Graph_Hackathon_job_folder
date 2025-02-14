![[Pasted image 20250214122834.png]]


### **Building the Skills System**

We will create two forms:

1. **Skill Creation Form** → Adds new skills to the system.
2. **Skill Association Form** → Links a skill to a user.

These will be stored in **SQLite** and later **synchronized with Neo4j**.

---

## **📂 Frontend: Skill Forms**

#### 📄 `frontend/forms/create_skill.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Skill</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Create a Skill</h2>
        <form id="skillForm">
            <label>Skill Name</label>
            <input type="text" name="skill_name" required>
            <button type="submit">Create Skill</button>
        </form>

        <h2>Available Skills</h2>
        <button onclick="fetchSkills()">Refresh Skills</button>
        <table border="1" id="skillsTable">
            <thead>
                <tr>
                    <th>Skill ID</th>
                    <th>Skill Name</th>
                </tr>
            </thead>
            <tbody>
                <!-- Skills will be inserted here dynamically -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("skillForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5003/api/create_skill", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchSkills(); // Refresh skill list
        };

        async function fetchSkills() {
            let response = await fetch("http://127.0.0.1:5003/api/get_skills");
            let data = await response.json();

            let tableBody = document.getElementById("skillsTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing rows

            data.skills.forEach(skill => {
                let row = `<tr>
                    <td>${skill.id}</td>
                    <td>${skill.name}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }

        fetchSkills(); // Load skills on page load
    </script>
</body>
</html>
```

---

#### 📄 `frontend/forms/associate_skill.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Associate Skill</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Associate a Skill to a User</h2>
        <form id="associateSkillForm">
            <label>User ID</label>
            <input type="text" name="user_id" required>

            <label>Skill ID</label>
            <input type="text" name="skill_id" required>

            <button type="submit">Associate Skill</button>
        </form>

        <h2>Users and Their Skills</h2>
        <button onclick="fetchUserSkills()">Refresh User Skills</button>
        <table border="1" id="userSkillsTable">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Skill</th>
                </tr>
            </thead>
            <tbody>
                <!-- User Skills will be inserted here dynamically -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("associateSkillForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5003/api/associate_skill", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchUserSkills(); // Refresh user skills
        };

        async function fetchUserSkills() {
            let response = await fetch("http://127.0.0.1:5003/api/get_user_skills");
            let data = await response.json();

            let tableBody = document.getElementById("userSkillsTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing rows

            data.user_skills.forEach(entry => {
                let row = `<tr>
                    <td>${entry.user_id}</td>
                    <td>${entry.user_name}</td>
                    <td>${entry.skill}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }

        fetchUserSkills(); // Load user skills on page load
    </script>
</body>
</html>
```

---

## **📂 Backend API**

#### 📄 `backend/api/manage_skills.py`

```python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set up database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/users/users.db")

@app.route("/api/create_skill", methods=["POST"])
def create_skill():
    try:
        data = request.json
        skill_name = data["skill_name"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)

        cursor.execute("INSERT INTO skills (name) VALUES (?)", (skill_name,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Skill created successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get_skills", methods=["GET"])
def get_skills():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM skills")
        skills = cursor.fetchall()
        conn.close()

        skill_list = [{"id": skill[0], "name": skill[1]} for skill in skills]
        return jsonify({"skills": skill_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/associate_skill", methods=["POST"])
def associate_skill():
    try:
        data = request.json
        user_id, skill_id = data["user_id"], data["skill_id"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL
            );
        """)

        cursor.execute("INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)", (user_id, skill_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Skill associated with user."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get_user_skills", methods=["GET"])
def get_user_skills():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_skills.user_id, users.name, skills.name
            FROM user_skills
            JOIN users ON user_skills.user_id = users.id
            JOIN skills ON user_skills.skill_id = skills.id;
        """)
        user_skills = cursor.fetchall()
        conn.close()

        user_skill_list = [{"user_id": entry[0], "user_name": entry[1], "skill": entry[2]} for entry in user_skills]
        return jsonify({"user_skills": user_skill_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5003)
```

---

### **🚀 Running Everything**

1️⃣ **Start the Skill API**

```sh
python backend/api/manage_skills.py
```

2️⃣ **Visit `create_skill.html` and add skills**

```
http://127.0.0.1:5500/forms/create_skill.html
```

3️⃣ **Visit `associate_skill.html` and link skills to users**

```
http://127.0.0.1:5500/forms/associate_skill.html
```

4️⃣ **Check the database**

```sh
sqlite3 database/users/users.db
sqlite> SELECT * FROM skills;
sqlite> SELECT * FROM user_skills;
```

🚀 Let me know how it works!



----

Got it! Here’s a modified version of the `get_user_skills` API that simply **queries the `user_skills` table** without any joins.

---

### **📄 Updated `get_user_skills` API (No Joins)**

📄 **File:** `backend/api/manage_skills.py`

```python
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set up database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/users/users.db")

@app.route("/api/get_user_skills", methods=["GET"])
def get_user_skills():
    try:
        print("🔍 Fetching raw user_skills data...")  # Debugging log

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_skills;")  # No joins, raw table data
        user_skills = cursor.fetchall()
        conn.close()

        if not user_skills:
            print("⚠️ No entries found in user_skills table.")

        user_skill_list = [
            {"id": entry[0], "user_id": entry[1], "skill_id": entry[2]}
            for entry in user_skills
        ]

        print(f"✅ Retrieved {len(user_skill_list)} user skills.")  # Debugging output
        return jsonify({"user_skills": user_skill_list}), 200

    except Exception as e:
        print(f"❌ Error fetching user skills: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5003)
```

---

### **🚀 Steps to Run and Test**

1️⃣ **Restart the API**

```sh
python backend/api/manage_skills.py
```

2️⃣ **Check API manually** in a browser:

```
http://127.0.0.1:5003/api/get_user_skills
```

OR use `curl`:

```sh
curl http://127.0.0.1:5003/api/get_user_skills
```

✅ **Expected JSON Output**:

```json
{
  "user_skills": [
    { "id": 1, "user_id": 3, "skill_id": 5 },
    { "id": 2, "user_id": 4, "skill_id": 2 }
  ]
}
```

❌ **If the response is `{}` or an error**, check:

- The **`user_skills` table exists** (`sqlite3 database/users/users.db; .tables`)
- The **table has data** (`SELECT * FROM user_skills;` in SQLite)

---

### **Let me know if you need any further tweaks! 🚀**
