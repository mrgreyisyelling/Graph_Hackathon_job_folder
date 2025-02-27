import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set up database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/users/users.db")

@app.route("/api/create_relationship", methods=["POST"])
def create_relationship():
    try:
        data = request.json
        user_a, user_b, relationship_type = data["user_a_id"], data["user_b_id"], data["relationship_type"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_a TEXT NOT NULL,
                user_b TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("INSERT INTO relationships (user_a, user_b, relationship_type) VALUES (?, ?, ?)", 
                       (user_a, user_b, relationship_type))
        conn.commit()
        conn.close()

        return jsonify({"message": "Relationship created successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/get_relationships", methods=["GET"])
def get_relationships():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT user_a, relationship_type, user_b FROM relationships")
        relationships = cursor.fetchall()
        conn.close()

        relationship_list = [
            {"user_a": rel[0], "type": rel[1], "user_b": rel[2]}
            for rel in relationships
        ]

        return jsonify({"relationships": relationship_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
