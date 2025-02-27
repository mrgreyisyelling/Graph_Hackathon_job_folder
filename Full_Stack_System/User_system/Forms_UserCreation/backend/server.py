from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend")  # Serve frontend folder
CORS(app)  # Enable CORS for cross-origin requests

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/forms/<path:filename>")
def serve_forms(filename):
    return send_from_directory(f"{app.static_folder}/forms", filename)

if __name__ == "__main__":
    app.run(debug=True, port=5500)
