import os
import sqlite3
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.abspath("../../database/users/users.db")  # Make sure this is correct
print(f"Using database at: {DB_PATH}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/api/submit_user", methods=["POST"])
def submit_user():
    data = request.json
    name, email, user_type, password = data["name"], data["email"], data["user_type"], data["password"]
    
    hashed_password = hash_password(password)

    try:
        conn = sqlite3.connect(DB_PATH)  # Make sure we're using the correct database
        cursor = conn.cursor()

        # Check if table exists before inserting
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if cursor.fetchone() is None:
            return jsonify({"error": "Database does not contain a 'users' table. Run setup_db.py!"}), 500

        cursor.execute("INSERT INTO users (name, email, user_type, password) VALUES (?, ?, ?, ?)", 
                       (name, email, user_type, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully."}), 200
    except sqlite3.OperationalError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
