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
