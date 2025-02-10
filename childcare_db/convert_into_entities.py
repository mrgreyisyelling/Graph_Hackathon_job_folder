import sqlite3
import hashlib
from schema import ENTITY_SCHEMAS  # Import schemas from schema.py

# Connect to SQLite database
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

# Drop the existing triples table (deletes all previous data)
cursor.execute("DROP TABLE IF EXISTS triples;")

# Recreate the triples table with a uniqueness constraint
cursor.execute("""
CREATE TABLE triples (
    subject TEXT,
    predicate TEXT,
    object TEXT,
    UNIQUE(subject, predicate, object)  -- Ensures only unique triples are stored
);
""")

# Get column names from the database
cursor.execute("PRAGMA table_info(childcare_facilities);")
columns = [col[1] for col in cursor.fetchall()]

# Function to generate a unique entity ID
def generate_entity_id(value, entity_type):
    """Generate a unique ID for an entity based on its type and name."""
    unique_str = f"{entity_type}:{value}"
    return hashlib.md5(unique_str.encode()).hexdigest()

# Fetch Facility data from SQLite
cursor.execute("SELECT * FROM childcare_facilities;")
rows = cursor.fetchall()

# Process each entity type based on its schema
for entity_type, schema in ENTITY_SCHEMAS.items():
    for row in rows:
        # Generate entity ID based on a key attribute (Facility Name for most entities)
        entity_key_column = "Facility Name" if "Facility Name" in schema else list(schema.keys())[0]
        entity_value = row[columns.index(entity_key_column)]
        entity_id = generate_entity_id(entity_value, entity_type)
# Process each entity type based on its schema
for entity_type, schema in ENTITY_SCHEMAS.items():
    for row_num, row in enumerate(rows, start=1):  # Track row number
        entity_key_column = "Facility Name" if "Facility Name" in schema else list(schema.keys())[0]
        entity_value = row[columns.index(entity_key_column)]
        entity_id = generate_entity_id(entity_value, entity_type)

        # Insert ENTITY_TYPE Triple
        cursor.execute("INSERT OR IGNORE INTO triples (subject, predicate, object) VALUES (?, ?, ?)", 
                       (entity_id, "ENTITY_TYPE", entity_type))

        # Insert attributes as triples
        for column_name, data_type in schema.items():
            if column_name in columns:
                col_index = columns.index(column_name)
                col_value = row[col_index]

                if col_value is not None:
                    cursor.execute("INSERT OR IGNORE INTO triples (subject, predicate, object) VALUES (?, ?, ?)", 
                                   (entity_id, column_name, str(col_value)))

        # Print simplified output
        print(f"Row {row_num}: {entity_type} - done")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Entities successfully created in triples format!")