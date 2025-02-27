import sqlite3
import hashlib

# Connect to SQLite database
conn = sqlite3.connect("childcare_graph.db")
cursor = conn.cursor()

# Ensure the triples table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS triples (
    subject TEXT,
    predicate TEXT,
    object TEXT
);
""")

# Define Facility Schema (Only relevant attributes)
FACILITY_SCHEMA = {
    "License Number": "TEXT",
    "License Issue Date": "TEXT",
    "License Expiry Date": "TEXT",
    "License Type": "TEXT",
    "Facility Name": "TEXT",
    "Facility Address": "TEXT",
    "City": "TEXT",
    "State": "TEXT",
    "Zip Code": "INTEGER",
    "Phone Number": "TEXT",
    "Facility Type": "TEXT",
    "Capacity": "INTEGER",
    "Enrollment": "INTEGER",
    "Staff": "INTEGER",
    "Operational Schedule": "TEXT",
    "Accepts Subsidies": "TEXT",
    "Hours of Operation (Sunday)": "TEXT",
    "Hours of Operation (Monday)": "TEXT",
    "Hours of Operation (Tuesday)": "TEXT",
    "Hours of Operation (Wednesday)": "TEXT",
    "Hours of Operation (Thursday)": "TEXT",
    "Hours of Operation (Friday)": "TEXT",
    "Hours of Operation (Saturday)": "TEXT",
    "School District Affiliation": "TEXT",
    "Alternative Address": "TEXT",
    "Facility Zip (Alt)": "INTEGER",
    "Alternative Contact Number": "TEXT",
    "Date Originally Licensed": "TEXT",
    "Facility Status": "TEXT"
}

# Fetch Facility data from the existing childcare facilities table
cursor.execute("SELECT * FROM childcare_facilities;")
rows = cursor.fetchall()

# Get column names from the database
cursor.execute("PRAGMA table_info(childcare_facilities);")
columns = [col[1] for col in cursor.fetchall()]

# Function to generate a unique entity ID
def generate_entity_id(value):
    return hashlib.md5(value.encode()).hexdigest()

# Insert Facility entities into the triples table
for row in rows:
    facility_id = generate_entity_id(row[5])  # Facility Name as Unique ID
    
    # Insert Facility entity declaration
    cursor.execute("INSERT INTO triples (subject, predicate, object) VALUES (?, ?, ?)", 
                   (facility_id, "ENTITY_TYPE", "Facility"))

    # Insert attributes as triples, only including defined schema attributes
    for idx, col_value in enumerate(row):
        column_name = columns[idx]
        if col_value and column_name in FACILITY_SCHEMA:  # Only process allowed attributes
            predicate = column_name  # Column name as attribute
            object_value = str(col_value)  # Convert all values to string

            cursor.execute("INSERT INTO triples (subject, predicate, object) VALUES (?, ?, ?)", 
                           (facility_id, predicate, object_value))

# Commit and close connection
conn.commit()
conn.close()

print("Facility entities successfully created in triples format!")
