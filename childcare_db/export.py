import sqlite3
import csv
import os
import shutil

# Connect to SQLite database
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

# List of entity tables to export
entity_tables = ["facilities", "locations", "owners", "licenses", "school_districts"]

# List of relationships to export (SQL JOINs)
relationship_queries = {
    "facility_location_relationships": """
        SELECT facilities.facility_id, facilities.facility_name, locations.location_id, locations.location_name
        FROM facilities
        LEFT JOIN locations ON facilities.location_id = locations.location_id;
    """,
    "facility_owner_relationships": """
        SELECT facilities.facility_id, owners.owner_id
        FROM facilities
        LEFT JOIN owners ON facilities.owner_id = owners.owner_id;
    """,
    "facility_license_relationships": """
        SELECT facilities.facility_id, licenses.license_id
        FROM facilities
        LEFT JOIN licenses ON facilities.license_id = licenses.license_id;
    """,
    "facility_school_district_relationships": """
        SELECT facilities.facility_id, school_districts.district_id
        FROM facilities
        LEFT JOIN school_districts ON facilities.school_district_id = school_districts.district_id;
    """
}

# Directories for export and Neo4j import
export_dir = "exports/"
neo4j_import_dir = "/var/lib/neo4j/import/"

# Ensure export directory exists
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Ensure Neo4j import directory exists
if not os.path.exists(neo4j_import_dir):
    print(f"⚠️ Neo4j import directory {neo4j_import_dir} does not exist or is not accessible!")
    exit(1)

### **Step 1: Export Entity Tables**
for table in entity_tables:
    print(f"\n🔍 Exporting entity table: {table}")

    # Fetch column names dynamically
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [col[1] for col in cursor.fetchall()]

    # Fetch all rows from the table
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()

    # Define export file path
    file_path = os.path.join(export_dir, f"{table}.csv")

    # Write data to CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write header row
        writer.writerows(rows)  # Write table data

    print(f"✅ Exported {table} to {file_path}")

### **Step 2: Move Entity Files to Neo4j Import Directory**
for table in entity_tables:
    src_path = os.path.join(export_dir, f"{table}.csv")
    dest_path = os.path.join(neo4j_import_dir, f"{table}.csv")

    try:
        shutil.move(src_path, dest_path)
        print(f"🚚 Moved {table}.csv to {neo4j_import_dir}")
    except PermissionError:
        print(f"❌ Permission denied: Cannot move {src_path} to {neo4j_import_dir}")
        print("🔹 Try running the script with `sudo` or check directory permissions.")

print("\n✅ Entity files successfully moved to Neo4j import directory.")

### **Step 3: Export Relationship Tables**
for rel_name, query in relationship_queries.items():
    print(f"\n🔍 Exporting relationship: {rel_name}")

    # Execute SQL JOIN query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Fetch column names dynamically from query result
    columns = [desc[0] for desc in cursor.description]

    # Define export file path
    file_path = os.path.join(export_dir, f"{rel_name}.csv")

    # Write data to CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write header row
        writer.writerows(rows)  # Write table data

    print(f"✅ Exported {rel_name} to {file_path}")

### **Step 4: Move Relationship Files to Neo4j Import Directory**
for rel_name in relationship_queries.keys():
    src_path = os.path.join(export_dir, f"{rel_name}.csv")
    dest_path = os.path.join(neo4j_import_dir, f"{rel_name}.csv")

    try:
        shutil.move(src_path, dest_path)
        print(f"🚚 Moved {rel_name}.csv to {neo4j_import_dir}")
    except PermissionError:
        print(f"❌ Permission denied: Cannot move {src_path} to {neo4j_import_dir}")
        print("🔹 Try running the script with `sudo` or check directory permissions.")

# Close database connection
conn.close()

print("\n🚀 Export and file transfer process completed.")
