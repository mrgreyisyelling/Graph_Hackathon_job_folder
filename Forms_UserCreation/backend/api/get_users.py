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
