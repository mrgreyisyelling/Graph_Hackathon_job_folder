const express = require("express");
const cors = require("cors");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");

const app = express();
const port = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Initialize SQLite Database
const db = new sqlite3.Database("./database.db", (err) => {
  if (err) console.error(err.message);
  console.log("Connected to SQLite database.");
});

// Create Tables
db.run(
  `CREATE TABLE IF NOT EXISTS forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    data TEXT NOT NULL
  )`
);

// Handle Form Submissions
app.post("/submit", (req, res) => {
  const { type, data } = req.body;

  db.run("INSERT INTO forms (type, data) VALUES (?, ?)", [type, JSON.stringify(data)], function (err) {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ id: this.lastID, message: "Data saved successfully!" });
  });
});

// Get Submitted Data (for debugging)
app.get("/submissions", (req, res) => {
  db.all("SELECT * FROM forms", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Start Server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
