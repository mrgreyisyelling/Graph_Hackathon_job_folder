from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/api/submit_user", methods=["POST"])
def submit_user():
    data = request.json
    name, email, user_type, password = data["name"], data["email"], data["user_type"], data["password"]
    
    hashed_password = hash_password(password)

    # Store in SQLite
    conn = sqlite3.connect("../database/users/users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, user_type, password) VALUES (?, ?, ?, ?)", 
                   (name, email, user_type, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully."})

if __name__ == "__main__":
    app.run(debug=True)
