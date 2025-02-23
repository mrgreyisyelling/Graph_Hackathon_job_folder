```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Knowledge Chunk Form</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    form > div { margin-bottom: 1rem; }
    label { display: block; margin-bottom: 0.5rem; }
    input, textarea { width: 100%; padding: 0.5rem; }
    button { padding: 0.5rem 1rem; }
  </style>
</head>
<body>
  <h1>Submit a Knowledge Chunk</h1>
  <form action="submit.php" method="POST">
    <div>
      <label for="entityName">Name of Entity:</label>
      <input type="text" id="entityName" name="entityName" required>
    </div>
    <div>
      <label for="entityDescription">Description of Entity:</label>
      <textarea id="entityDescription" name="entityDescription" rows="4" required></textarea>
    </div>
    <div>
      <label for="entityData">Data Describing Entity:</label>
      <textarea id="entityData" name="entityData" rows="4" required></textarea>
    </div>
    <div>
      <button type="submit">Submit Knowledge Chunk</button>
    </div>
  </form>
</body>
</html>

```


```php
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve and sanitize form data
    $entityName = htmlspecialchars(trim($_POST['entityName']));
    $entityDescription = htmlspecialchars(trim($_POST['entityDescription']));
    $entityData = htmlspecialchars(trim($_POST['entityData']));

    // Create a knowledge chunk array
    $knowledgeChunk = [
        'name' => $entityName,
        'description' => $entityDescription,
        'data' => $entityData,
    ];

    // Here, you might save the knowledge chunk to a database or further process it.
    // For demonstration, we'll simply output the data.
    echo "<h1>Knowledge Chunk Received</h1>";
    echo "<p><strong>Name:</strong> " . $knowledgeChunk['name'] . "</p>";
    echo "<p><strong>Description:</strong> " . $knowledgeChunk['description'] . "</p>";
    echo "<p><strong>Data:</strong> " . $knowledgeChunk['data'] . "</p>";
} else {
    // If the form is not submitted via POST
    echo "Invalid request method.";
}
?>


```

We are going to alter things so that we move the data to some thing stable quickly

Create mysql table

```sql
CREATE TABLE knowledge_chunks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  data TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

# Inserting into the table


```php
<?php
// Database configuration
$servername = "localhost";
$username = "your_db_username";
$password = "your_db_password";
$dbname = "your_db_name";

// Create connection using MySQLi
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Only process POST requests
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve and sanitize form data
    $entityName = trim($_POST['entityName']);
    $entityDescription = trim($_POST['entityDescription']);
    $entityData = trim($_POST['entityData']);

    // Prepare an SQL statement to insert the data
    $stmt = $conn->prepare("INSERT INTO knowledge_chunks (name, description, data) VALUES (?, ?, ?)");
    if ($stmt === false) {
        die("Prepare failed: " . $conn->error);
    }

    $stmt->bind_param("sss", $entityName, $entityDescription, $entityData);

    if ($stmt->execute()) {
        echo "Knowledge chunk saved successfully.";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
} else {
    echo "Invalid request method.";
}
?>


```

Ok from this insert - we transform into KG format.

- entity ode
- attibutes -  description and data
-
load into graph database.

Python that reads from mysql and writes to the neo4j KG - 

```python
import mysql.connector
from py2neo import Graph, Node, Relationship

# Connect to MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="your_db_username",
    password="your_db_password",
    database="your_db_name"
)
cursor = mysql_conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM knowledge_chunks")

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j_password"))

for row in cursor:
    entity_name = row['name']
    entity_description = row['description']
    entity_data = row['data']
    
    # Create the primary entity node
    entity_node = Node("Entity", name=entity_name,
                       description=entity_description,
                       data=entity_data)
    graph.create(entity_node)
    
    # Optional: Create additional nodes/relationships if needed.
    # For example, if the description contains a type like "Type: X", you might:
    # if "Type:" in entity_description:
    #     type_val = entity_description.split("Type:")[1].split()[0]
    #     type_node = Node("Type", name=type_val)
    #     graph.merge(type_node, "Type", "name")
    #     rel = Relationship(entity_node, "IS_A", type_node)
    #     graph.create(rel)

# Clean up
cursor.close()
mysql_conn.close()

print("Data has been transferred to the knowledge graph.")

```

