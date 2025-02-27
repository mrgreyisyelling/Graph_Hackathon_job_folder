import pandas as pd
import sqlite3

# Load CSV file
csv_file = "childcare_data.csv"  # Change if needed
df = pd.read_csv(csv_file)

# Connect to SQLite (or create it)
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

# Define table schema (adjust as needed)
table_name = "childcare_facilities"
df.to_sql(table_name, conn, if_exists="replace", index=False)

# Verify import
print("Imported rows:", len(df))

# Close connection
conn.close()

# -----



import sqlite3
import hashlib
from schema import ENTITY_SCHEMAS  # Import schemas from schema.py

# Connect to SQLite database
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

# Drop existing tables and recreate them
cursor.executescript("""
DROP TABLE IF EXISTS facilities;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS owners;
DROP TABLE IF EXISTS licenses;
DROP TABLE IF EXISTS school_districts;

CREATE TABLE facilities (
    facility_id TEXT PRIMARY KEY,
    facility_name TEXT NOT NULL,
    facility_address TEXT NOT NULL,
    phone_number TEXT,
    license_number TEXT NOT NULL,
    facility_type TEXT,
    operational_schedule TEXT,
    accepts_subsidies TEXT,
    location_id TEXT,
    owner_id TEXT,
    license_id TEXT,
    school_district_id TEXT,
    UNIQUE(facility_name, license_number, facility_address)  -- Prevents duplicates
);

CREATE TABLE locations (
    location_id TEXT PRIMARY KEY,
    location_name TEXT NOT NULL,
    location_address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    UNIQUE(city, state, location_address, location_name)  -- Ensures unique locations
);

CREATE TABLE owners (
    owner_id TEXT PRIMARY KEY,
    license_number TEXT NOT NULL,
    phone_number TEXT,
    alternative_contact_number TEXT,
    UNIQUE(license_number)  -- Ensures unique owners by license number
);

CREATE TABLE licenses (
    license_id TEXT PRIMARY KEY,
    license_number TEXT NOT NULL,
    license_type TEXT,
    license_issue_date TEXT,
    license_expiry_date TEXT,
    UNIQUE(license_number)  -- Prevents duplicate licenses
);

CREATE TABLE school_districts (
    district_id TEXT PRIMARY KEY,
    district_name TEXT NOT NULL,
    UNIQUE(district_name)  -- Prevents duplicate school districts
);
""")


# Function to generate a unique entity ID
def generate_entity_id(value, entity_type):
    """Generate a unique ID for an entity based on its type and name."""
    unique_str = f"{entity_type}:{value}"
    return hashlib.md5(unique_str.encode()).hexdigest()


# Fetch column names from the database
cursor.execute("PRAGMA table_info(childcare_facilities);")
columns = [col[1] for col in cursor.fetchall()]

# Fetch all rows from the childcare facilities table
cursor.execute("SELECT * FROM childcare_facilities;")
rows = cursor.fetchall()

# Get column indexes once for performance
city_idx = columns.index("City")
state_idx = columns.index("State")
zip_idx = columns.index("Zip Code")
facility_addr_idx = columns.index("Facility Address")
location_address = facility_addr_idx
facility_name_idx = columns.index("Facility Name")
location_name = facility_name_idx
phone_idx = columns.index("Phone Number")
facility_type_idx = columns.index("Facility Type")
op_schedule_idx = columns.index("Operational Schedule")
accepts_subsidies_idx = columns.index("Accepts Subsidies")
alt_contact_idx = columns.index("Alternative Contact Number")
license_type_idx = columns.index("License Type")
license_issue_date_idx = columns.index("License Issue Date")
license_expiry_date_idx = columns.index("License Expiry Date")
license_number_idx = columns.index("License Number")
school_district_idx = columns.index("School District Affiliation")

# Dictionaries to track existing entities to prevent duplicate inserts
location_map = {}
owner_map = {}
license_map = {}
school_district_map = {}

# Process each facility row
for row_num, row in enumerate(rows, start=1):
    # Generate unique Facility ID using Name + License Number + Address
    facility_key = f"{row[facility_name_idx]}|{row[license_number_idx]}|{row[facility_addr_idx]}"
    facility_id = generate_entity_id(facility_key, "Facility")

    # Generate unique Location ID using City, State, and Zip Code
    location_key = f"{row[city_idx]}|{row[state_idx]}|{row[facility_addr_idx]}|{row[facility_name_idx]}"
    location_id = location_map.get(location_key) or generate_entity_id(location_key, "Location")
    # if location_key =="Detroit|MI|19346 Albany|Linda J. Taylor":
    #     print(facility_key)
    #     print(location_key)
    #     print(location_id)
    #     print(row[city_idx])
    #     print(row[state_idx]) 
    #     print(str(row[zip_idx]))
    #     print(row[location_address])
    #     print(row[location_name])
                


    # Generate unique Owner ID using License Number
    owner_key = row[license_number_idx]
    owner_id = owner_map.get(owner_key) or generate_entity_id(owner_key, "Owner")

    # Generate unique License ID using License Number
    license_id = license_map.get(owner_key) or generate_entity_id(owner_key, "License")

    # Generate unique School District ID using District Name
    school_district_key = row[school_district_idx]
    school_district_id = school_district_map.get(school_district_key) or generate_entity_id(school_district_key, "School District")

    # Insert Location (Skip duplicates)
    if location_key not in location_map:
        # cursor.execute("""
        # INSERT OR IGNORE INTO locations (location_id, city, state, zip_code, location_address, location_name)
        # VALUES (?, ?, ?, ?, ?, ?)
        # """, (location_id, row[city_idx], row[state_idx], str(row[zip_idx]), row[location_address], row[location_name]))

        # Define the SQL query
        sql_query = """
            INSERT OR IGNORE INTO locations (location_id, city, state, zip_code, location_address, location_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        # Define the values to insert
        values = (location_id, row[city_idx], row[state_idx], str(row[zip_idx]), row[location_address], row[location_name])

        # Print the SQL query with the actual values for debugging
        # print(f"Executing SQL Query: {sql_query}")
        # print(f"With Values: {values}")

        # Execute the SQL query
        cursor.execute(sql_query, values)



    # Check if the insert was successful by retrieving the latest inserted row
    cursor.execute("SELECT * FROM locations WHERE location_id = ?", (location_id,))
    inserted_row = cursor.fetchone()

    # if location_id =="e0a80a19331259dc3bf756fa66402c31":
    #     # Print the SQL query with the actual values for debugging
    #     print(f"Executing SQL Query: {sql_query}")
    #     print(f"With Values: {values}")
    #     print(f"✅ Inserted Location: {inserted_row}")  # Print the inserted location

    # Store the location ID in the map to prevent re-insertion
    location_map[location_key] = location_id


    # Insert Owner (Skip duplicates)
    if owner_key not in owner_map:
        cursor.execute("""
            INSERT OR IGNORE INTO owners (owner_id, license_number, alternative_contact_number)
            VALUES (?, ?, ?)
        """, (owner_id, owner_key, row[alt_contact_idx]))
        owner_map[owner_key] = owner_id

    # Insert License (Skip duplicates)
    if owner_key not in license_map:
        cursor.execute("""
            INSERT OR IGNORE INTO licenses (license_id, license_number, license_type, license_issue_date, license_expiry_date)
            VALUES (?, ?, ?, ?, ?)
        """, (license_id, owner_key, row[license_type_idx], row[license_issue_date_idx], row[license_expiry_date_idx]))
        license_map[owner_key] = license_id

    # Insert School District (Skip duplicates)
    if school_district_key not in school_district_map:
        cursor.execute("""
            INSERT OR IGNORE INTO school_districts (district_id, district_name)
            VALUES (?, ?)
        """, (school_district_id, school_district_key))
        school_district_map[school_district_key] = school_district_id

    # Insert Facility with references to Location, Owner, License, and School District
    cursor.execute("""
        INSERT OR IGNORE INTO facilities (
            facility_id, facility_name, license_number, facility_address, phone_number, facility_type,
            operational_schedule, accepts_subsidies, location_id, owner_id, license_id, school_district_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (facility_id, row[facility_name_idx], row[license_number_idx],
          row[facility_addr_idx], row[phone_idx],
          row[facility_type_idx], row[op_schedule_idx],
          row[accepts_subsidies_idx], location_id, owner_id, license_id, school_district_id))

    #print(f"Row {row_num}: Facility - Inserted successfully.")

# Commit changes and close the connection
conn.commit()
conn.close()

print("All unique entities successfully inserted!")
