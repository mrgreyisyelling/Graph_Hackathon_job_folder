### **Fixing `unable to open database file` Error in SQLite**

This error means that **`get_users.py` cannot access the SQLite database file (`users.db`)**. The most common causes are:

1. **Incorrect database path**
2. **Permission issues**
3. **The database file doesn't exist**
4. **The script is running from the wrong working directory**

---

### **🔹 Step 1: Check If `users.db` Exists**

Run this command in the terminal:

```sh
ls -l database/users/users.db
```

✅ **If the file exists**, you’ll see something like:

```
-rw-r--r--  1 mike  staff  8192 Feb 14 10:45 database/users/users.db
```

❌ **If it doesn’t exist**, **rerun the database setup:**

```sh
python database/users/setup_db.py
```

Then **check again**:

```sh
ls -l database/users/users.db
```

---

### **🔹 Step 2: Fix Database Path in `get_users.py`**

Modify `get_users.py` to use an **absolute path** to `users.db`.

📄 **File:** `backend/api/get_users.py`

```python
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# FIX: Ensure absolute path to database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get script directory
DB_PATH = os.path.join(BASE_DIR, "../../database/users/users.db")
print(f"📌 Using database path: {DB_PATH}")

@app.route("/api/get_users", methods=["GET"])
def get_users():
    try:
        print("🔍 Fetching users from database...")

        if not os.path.exists(DB_PATH):
            print("❌ ERROR: Database file not found!")
            return jsonify({"error": "Database file not found"}), 500

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, user_type, created_at FROM users")
        users = cursor.fetchall()
        conn.close()

        if not users:
            print("⚠️ No users found in database.")

        user_list = [
            {"id": user[0], "name": user[1], "email": user[2], "user_type": user[3], "created_at": user[4]}
            for user in users
        ]

        print(f"✅ Retrieved {len(user_list)} users.")
        return jsonify({"users": user_list}), 200

    except Exception as e:
        print(f"❌ Error fetching users: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

✅ **What This Fix Does:**

- Prints the exact database path being used.
- Checks if `users.db` exists before trying to open it.
- Uses an **absolute path** instead of a relative one.

---

### **🔹 Step 3: Fix File Permissions (If Necessary)**

If `users.db` **exists** but still cannot be opened, check its permissions:

```sh
ls -l database/users/users.db
```

If it **doesn’t have read/write permissions**, fix it:

```sh
chmod 666 database/users/users.db
```

---

### **🔹 Step 4: Restart Everything and Test**

1️⃣ **Restart the API**

```sh
python backend/api/get_users.py
```

2️⃣ **Check the API manually**  
Visit:

```
http://127.0.0.1:5001/api/get_users
```

If it works, the output should be:

```json
{
  "users": [
    {"id": 1, "name": "Alice Smith", "email": "alice@example.com", "user_type": "parent", "created_at": "2025-02-14 10:30:00"}
  ]
}
```

3️⃣ **Check the browser console (`F12 → Console tab`)**

- If `fetchUsers()` logs `"✅ API Response:"` but the table is empty, the frontend isn't inserting rows correctly.
- If `"❌ Error fetching users:"` appears, the API isn't reachable.

---

### **Final Fix**

✅ **Database path is absolute**  
✅ **Permissions are correct**  
✅ **Database exists**  
✅ **Restarted API and tested manually**

🚀 **Try these steps and let me know the output!**