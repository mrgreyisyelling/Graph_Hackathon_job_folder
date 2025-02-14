To serve `register.html` properly, we need a **basic Flask server** that serves static files. Here’s how you can do it:

---

### **Step 1: Set Up a Flask Server for Frontend**

📄 **File:** `backend/server.py`

```python
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
```

---

### **Step 2: Start the Frontend Server**

Run this command in your terminal:

```sh
python backend/server.py
```

✅ This will serve the frontend at:  
**[http://127.0.0.1:5500/forms/register.html](http://127.0.0.1:5500/forms/register.html)**

---

### **Step 3: Test the Full Registration Flow**

1. Open **[http://127.0.0.1:5500/forms/register.html](http://127.0.0.1:5500/forms/register.html)** in your browser.
2. Fill out the form and submit.
3. It should **send data to the backend at `http://127.0.0.1:5000/api/submit_user`**.
4. Check `users.db` to confirm the user is stored.

---

### **Next Steps**

1. **Confirm that `register.html` loads and submits data properly.**
2. **Once that works, we move on to querying the database for registered users.** 🚀

Let me know when you’re ready!