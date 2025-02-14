Register.html to DB


### **Step 1: Set Up Local SQLite Database**

Before we wire up `register.html`, we need a database to store user data.

#### **📂 Create SQLite Database**

📄 **File:** `database/users/setup_db.py`

```python
import sqlite3

# Connect to SQLite and create the users table
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    user_type TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("Database and table created successfully.")
```

✅ **Run this script once** to initialize the `users.db` database.

---

### **Step 2: Backend API to Handle Form Submission**

Now, let’s make the API receive data from `register.html` and store it in `users.db`.

📄 **File:** `backend/api/submit_user.py`

```python
from flask import Flask, request, jsonify
import sqlite3
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for frontend requests)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/api/submit_user", methods=["POST"])
def submit_user():
    data = request.json
    name, email, user_type, password = data["name"], data["email"], data["user_type"], data["password"]
    
    hashed_password = hash_password(password)

    try:
        # Store user in SQLite
        conn = sqlite3.connect("../../database/users/users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, user_type, password) VALUES (?, ?, ?, ?)", 
                       (name, email, user_type, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully."}), 200
    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already exists."}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

✅ **Run this file**:

```sh

pip3 install flask-cors
python backend/api/submit_user.py
```

This will start a **Flask server** on **localhost:5000** to handle registration requests.

---

### **Step 3: Connect `register.html` to Backend**

Now we update the form to **send data to the API**.

📄 **File:** `frontend/forms/register.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Register</h2>
        <form id="registerForm">
            <label>Full Name</label>
            <input type="text" name="name" required>

            <label>Email</label>
            <input type="email" name="email" required>

            <label>User Type</label>
            <select name="user_type">
                <option value="parent">Parent</option>
                <option value="provider">Childcare Provider</option>
                <option value="job_seeker">Job Seeker</option>
                <option value="employer">Employer</option>
            </select>

            <label>Password</label>
            <input type="password" name="password" required>

            <label>Confirm Password</label>
            <input type="password" name="confirm_password" required>

            <button type="submit">Register</button>
        </form>
    </div>

    <script>
        document.getElementById("registerForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            if (jsonData.password !== jsonData.confirm_password) {
                alert("Passwords do not match!");
                return;
            }

            let response = await fetch("http://127.0.0.1:5000/api/submit_user", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
        };
    </script>
</body>
</html>
```

---

### **Step 4: Test Registration**

✅ **Start the backend server**

```sh
python backend/api/submit_user.py
```

✅ **Open `register.html` in your browser**

- Fill out the form
- Click "Register"
- You should get an **alert confirming success or failure**

✅ **Check the database**

```sh
sqlite3 database/users/users.db
sqlite> SELECT * FROM users;
```

You should see your newly registered user!

---

### **Immediate Next Steps**

1. **Confirm that registration works** 🚀
2. **Check the database for stored users**
3. **Let me know when that’s done, and we’ll move to querying users!**