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