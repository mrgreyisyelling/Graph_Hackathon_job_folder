![[Pasted image 20250214110125.png]]


### **Building the Relationship Creation Form**

Based on the diagram, the form should:

1. **Collect relationship data** (e.g., User A is connected to User B as "Works With").
2. **Submit the relationship to the local database**.
3. **Sync the relationship with the Global Knowledge Graph (KG)**.

---

### **📂 Frontend: Relationship Form**

#### 📄 `frontend/forms/create_relationship.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Relationship</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h2>Create a Relationship</h2>
        <form id="relationshipForm">
            <label>User A ID</label>
            <input type="text" name="user_a_id" required>

            <label>User B ID</label>
            <input type="text" name="user_b_id" required>

            <label>Relationship Type</label>
            <select name="relationship_type">
                <option value="KNOWS">Knows</option>
                <option value="WORKS_WITH">Works With</option>
                <option value="BELONGS_TO">Belongs To</option>
                <option value="HIRED_BY">Hired By</option>
            </select>

            <button type="submit">Create Relationship</button>
        </form>

        <h2>Existing Relationships</h2>
        <button onclick="fetchRelationships()">Refresh Relationships</button>
        <table border="1" id="relationshipsTable">
            <thead>
                <tr>
                    <th>User A</th>
                    <th>Relationship</th>
                    <th>User B</th>
                </tr>
            </thead>
            <tbody>
                <!-- Relationships will be inserted here dynamically -->
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById("relationshipForm").onsubmit = async function(e) {
            e.preventDefault();
            let formData = new FormData(e.target);
            let jsonData = Object.fromEntries(formData);

            let response = await fetch("http://127.0.0.1:5002/api/create_relationship", {
                method: "POST",
                body: JSON.stringify(jsonData),
                headers: { "Content-Type": "application/json" }
            });

            let result = await response.json();
            alert(result.message);
            fetchRelationships();  // Refresh the relationships list
        };

        async function fetchRelationships() {
            let response = await fetch("http://127.0.0.1:5002/api/get_relationships");
            let data = await response.json();

            let tableBody = document.getElementById("relationshipsTable").querySelector("tbody");
            tableBody.innerHTML = ""; // Clear existing rows

            data.relationships.forEach(rel => {
                let row = `<tr>
                    <td>${rel.user_a}</td>
                    <td>${rel.type}</td>
                    <td>${rel.user_b}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }

        fetchRelationships(); // Load relationships on page load
    </script>
</body>
</html>
```

---

### **📂 Backend API: Handling Relationships**

#### 📄 `backend/api/manage_relationships.py`

```python
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
```

---

### **📂 Syncing Relationships to the Global Knowledge Graph**

Once relationships are stored in SQLite, we need to sync them into **Neo4j**.

#### 📄 `backend/cron_jobs/cron_transfer_relationships.py`

```python
from neo4j import GraphDatabase
import sqlite3
import os

# Connect to Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/users/users.db")

def transfer_relationships_to_neo4j():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_a, user_b, relationship_type FROM relationships")
    relationships = cursor.fetchall()
    conn.close()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as session:
        for rel in relationships:
            session.run(
                "MATCH (a:User {id: $user_a}), (b:User {id: $user_b}) "
                "MERGE (a)-[r:"+rel[2]+"]->(b)",
                user_a=rel[0], user_b=rel[1]
            )

    driver.close()

if __name__ == "__main__":
    transfer_relationships_to_neo4j()
```

✅ **Transfers relationships from SQLite to Neo4j.**  
✅ **Ensures relationships are represented in the Knowledge Graph.**

---

### **📂 Neo4j Schema Update**

#### 📄 `database/neo4j/schema.cypher`

```cypher
// Create relationships between users
MATCH (a:User {id: $user_a}), (b:User {id: $user_b})
MERGE (a)-[r:$relationship_type]->(b);
```

✅ **Ensures relationship types are preserved in Neo4j.**

---

### **🚀 Final Steps to Run Everything**

1️⃣ **Start the Relationship API**

```sh
python backend/api/manage_relationships.py
```

2️⃣ **Test Creating a Relationship**  
Visit:

```
http://127.0.0.1:5500/forms/create_relationship.html
```

- Add two user IDs and select a relationship type.
- Click **"Create Relationship"**.

3️⃣ **Verify SQLite Database**

```sh
sqlite3 database/users/users.db
sqlite> SELECT * FROM relationships;
```

4️⃣ **Sync Relationships to Neo4j**

```sh
python backend/cron_jobs/cron_transfer_relationships.py
```

5️⃣ **Query Neo4j**

```cypher
MATCH (a)-[r]->(b) RETURN a, r, b;
```

---

### **✅ Expected Outcome**

- **Frontend allows relationship creation.**
- **Relationships appear in SQLite.**
- **Sync process moves relationships into Neo4j.**
- **Neo4j maintains the structured graph.**

Let me know how it works for you! 🚀