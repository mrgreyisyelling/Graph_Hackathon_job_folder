import { readFileSync } from 'fs';
import { Triple, type Op } from "@graphprotocol/grc-20";
import { publish, type PublishResult } from "./publish.js";
import { wallet } from "./wallet.js";
import 'dotenv/config';


type LocalTriple = {
    attributeId: string;
    entityId: string;
    value: {
      type: string;
      value: string;
    };
  };
  
  type Entity = {
    entityId: string;
    triples: LocalTriple[];
  };

  // Use the deployed space ID from testnet
const SPACE_ID = "0x------" as `0x${string}`;

// ok so we have several things here
// First - we have the raw data
// second - we need to move that data into entity/relationship format
// third - we need to publish that data to the graph geo system

// # First - we have the raw data
// we dealt with this previously let me fetch that code ( this is python code)

import pandas as pd
import sqlite3

// # Load CSV file
csv_file = "childcare_data.csv"  # Change if needed
df = pd.read_csv(csv_file)

// # Connect to SQLite (or create it)
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

// # Define table schema (adjust as needed)
table_name = "childcare_facilities"
df.to_sql(table_name, conn, if_exists="replace", index=False)

// # Verify import
print("Imported rows:", len(df))

// # Close connection
conn.close()

// Ok so that logic, basically digested the CSV file and put it into a sqlite database
// From here we want to break apart the database into entities, types, properties, and relationships
// Each thing will need its own ID, so we will need to generate those as well, and then store them

// so reading 'README_philosophyOfSchema.md' we see this logic:

// The incoming data is row data, and it can be divided into multiple parts:

// 1 - description of the facility
// 2 - Description of the location
// 3 - description of the Owner
// 4 - description of the license
// 5 - description of the School district


// Facility:
//     - has a relationship to     
//         - a license
//             - this has specific information about starting and stopping
//         - a location relationship
//         - an owner relationship
//         - a schedule
//         - a school district affiliation
//         - properties
//             - accepts subidies
//             - has a type

// Location has a
//     - relationship to a:
//         - city
//         - state
//         - zip code
//         - street
//         - street address
//         - closest corner // For future logic

// Owner has 
//     - a relationship to
//         - facilities
//         - licenses
//         - phone numbers

// License has
//     - a relationship to
//         - facility
//             - data originally licensed
//     - the properties
//         - number
//         - type
//         - issue date
//         - expiry date
    
// School District has
//     - properties
//         - school district affiliation

// This following code is the preliminary code - it breaks apart the original data into tables of certain types.
// what we need to do is update this system so that the schema, entity, properties and relationships are separated and individually defined

// This is python code, so we will need to convert it to javascript/typescript



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

// ok so instead of this logic, we need something that is more systematic about each type

// so looking at 


// Facility:
//     - has a relationship to     
//         - a license
//             - this has specific information about starting and stopping
//         - a location relationship
//         - an owner relationship
//         - a schedule
//         - a school district affiliation
//         - properties
//             - accepts subidies
//             - has a type

// so in this logic, we need to create an entity for each of these elements, and then create a relationship between them and the facility
// So we need to create the logic for License, Location, Owner, Schedule, and School District to have a relationship to the facility
// The facility has limited properties, so we can just add those to the facility entity

// so when we create these elements - do we need to fully sketch them out?
// I think we do - we need to create a schema for each type, so it can be extracted from the base data and then inserted into the graph

// So for example - we create a database strcuture to take a row from the childcare facility db, 
// then break it apart into the elements that are needed for the graph
// We create a facility element with certain properties
// we create a license element with certain properties
// we create a location element with certain properties
// we create an owner element with certain properties
// we create a schedule element with certain properties
// we create a school district element with certain properties

// Once each of those things have been individually created or matched in the system, each given a unique ID
// we can then create relationships between them

// But PRIOR to creating relationships or even entities - we have to create the attributeIDs of each entity so that 
// they can be defined by them as they are created.

// So PRIOR to creating the entities, we need to create a list of the individual attributes 
// and generate the IDs for them

// So we need to look at the list of elements in the db and determine which are attributes and which are entities
// So a license is an entity  - it has a attribute of a license number. Thats specific to the license and doesn't provide any clustering value
// a license has a relationship to a type.
// a license has a issue date that has a relatoinship to a date
// a license has a expiry date that has a relationship to a date

// So a majority of its features are in its relationship to other facts, not in its own properties

// These are the headers from the childcare_facility database:
// license Number,License Issue Date,License Expiry Date,License Type,Facility Name,Facility Address,,
// City,State,Zip Code,Phone Number,Facility Type,Capacity,Enrollment,Staff,,Operational Schedule,
// Accepts Subsidies,Hours of Operation (Sunday),Hours of Operation (Monday),Hours of Operation (Tuesday),
// Hours of Operation (Wednesday),Hours of Operation (Thursday),Hours of Operation (Friday),Hours of Operation (Saturday),
// School District Affiliation,Alternative Address,,,,Facility Zip (Alt),Alternative Contact Number,
// Date Originally Licensed,,,Facility Status

// So this is the previous schema logic we used 

// # Schema definitions for different entity types

// # Facility Schema (Based on Provided Columns)
// FACILITY_SCHEMA = {
//     "Date Extracted": "TEXT",
//     "License Number": "TEXT",
//     "License Issue Date": "TEXT",
//     "License Expiry Date": "TEXT",
//     "License Type": "TEXT",
//     "Facility Name": "TEXT",
//     "Facility Address": "TEXT",
//     "City": "TEXT",
//     "State": "TEXT",
//     "Zip Code": "INTEGER",
//     "Phone Number": "TEXT",
//     "Facility Type": "TEXT",
//     "Operational Schedule": "TEXT",
//     "Accepts Subsidies": "TEXT",
//     "Hours of Operation (Sunday)": "TEXT",
//     "Hours of Operation (Monday)": "TEXT",
//     "Hours of Operation (Tuesday)": "TEXT",
//     "Hours of Operation (Wednesday)": "TEXT",
//     "Hours of Operation (Thursday)": "TEXT",
//     "Hours of Operation (Friday)": "TEXT",
//     "Hours of Operation (Saturday)": "TEXT",
//     "School District Affiliation": "TEXT",
//     "Alternative Address": "TEXT",
//     "Facility Zip (Alt)": "INTEGER",
//     "Alternative Contact Number": "TEXT",
//     "Date Originally Licensed": "TEXT",
//     "Facility Status": "TEXT"
// }


// # Location Schema (Based on Provided Columns)
// LOCATION_SCHEMA = {
//     "Facility Address": "TEXT",
//     "City": "TEXT",
//     "State": "TEXT",
//     "Zip Code": "INTEGER",
//     "Facility Zip (Alt)": "INTEGER",
//     "Alternative Address": "TEXT"
// }


// # Owner Schema (Based on Provided Columns)
// OWNER_SCHEMA = {
//     "Facility Name": "TEXT",
//     "License Number": "TEXT",
//     "License Type": "TEXT",
//     "Alternative Contact Number": "TEXT"
// }

// LICENSE_SCHEMA = {
//     "License Number": "TEXT",
//     "License Type": "TEXT",
//     "License Issue Date": "TEXT",
//     "License Expiry Date": "TEXT",
//     "Facility Name": "TEXT",
//     "Date Originally Licensed": "TEXT"
// }

// SCHOOL_DISTRICT_SCHEMA = {
//     "Facility Name": "TEXT",
//     "School District Affiliation": "TEXT"
// }

// So we need to reduce this list so that it only describes the attributes of the entity and relationships are described 
// in the relationship entities.

// Can you take this list and reduce it to essential attributes and what are represented as relationships?

// Here’s a structured breakdown of **essential attributes** and **relationships** based on the schema logic:

// ---

// ### **1. Facility Entity**
// #### **Attributes**:
// - `facility_id` (Generated ID)
// - `facility_name`
// - `facility_status`
// - `facility_type`
// - `accepts_subsidies`
// - `operational_schedule`

// #### **Relationships**:
// - **License** (1-to-1) → `license_id`
// - **Location** (1-to-1) → `location_id`
// - **Owner** (1-to-1) → `owner_id`
// - **School District** (1-to-1) → `school_district_id`

// ---

// ### **2. Location Entity**
// #### **Attributes**:
// - `location_id` (Generated ID)
// - `city`
// - `state`
// - `zip_code`
// - `alternative_zip`
// - `address`
// - `alternative_address`

// #### **Relationships**:
// - **Facility** (1-to-1)
// - **Closest Corner** (Future extension)

// ---

// ### **3. Owner Entity**
// #### **Attributes**:
// - `owner_id` (Generated ID)
// - `alternative_contact_number`

// #### **Relationships**:
// - **Facility** (1-to-Many)
// - **License** (1-to-Many)
// - **Phone Numbers** (Many-to-Many)

// ---

// ### **4. License Entity**
// #### **Attributes**:
// - `license_id` (Generated ID)
// - `license_number`
// - `license_type`
// - `date_originally_licensed`

// #### **Relationships**:
// - **Facility** (1-to-1)
// - **License Issue Date** (1-to-1) → `date_id`
// - **License Expiry Date** (1-to-1) → `date_id`

// ---

// ### **5. School District Entity**
// #### **Attributes**:
// - `district_id` (Generated ID)
// - `district_name`

// #### **Relationships**:
// - **Facility** (1-to-Many)

// ---

// ### **6. Schedule Entity (NEW)**
// **(Represents operational hours for each facility)**
// #### **Attributes**:
// - `schedule_id` (Generated ID)

// #### **Relationships**:
// - **Facility** (1-to-1)
// - **Hours of Operation** (7 separate relationships, each day as a separate entity reference)

// ---

// ### **7. Date Entity (NEW)**
// **(Represents license dates as unique entities to standardize date tracking)**  
// #### **Attributes**:
// - `date_id` (Generated ID)
// - `date_value`

// #### **Relationships**:
// - **License Issue Date**
// - **License Expiry Date**

// ---

// ### **Summary of Key Changes**
// 1. **Entities now contain only their core attributes** (e.g., `Facility` doesn’t store location details but instead references a `Location` entity).
// 2. **Relationships define connections**, reducing data duplication.
// 3. **New entities**:
//    - **`Schedule`**: Instead of embedding operational hours in the facility, each day is a separate relation.
//    - **`Date`**: Standardizes license issue/expiry dates as reusable references.
// 4. **Better normalization** for knowledge graph and structured storage.

// ---

// This structure keeps **entities atomic** while ensuring **relationships define connectivity**. Let me know if you want modifications before implementing this in TypeScript. 🚀

// ok So what we want to do at this point is to create the schema for each of these entities
// In python - can you create a 'schema processing' function that will take a row from this database
// and create the entities and then the relationships based on the structure above

// import sqlite3
// import hashlib
// import json
// from datetime import datetime

// # Function to generate a unique entity ID
// def generate_entity_id(value, entity_type):
//     """Generate a unique ID for an entity based on its type and name."""
//     unique_str = f"{entity_type}:{value}"
//     return hashlib.md5(unique_str.encode()).hexdigest()

// # Function to process a row and create entities & relationships
// def process_facility_row(row, column_indexes):
//     """Processes a row and returns structured entity and relationship data."""

//     # Extract necessary fields from the row using predefined indexes
//     facility_name = row[column_indexes["Facility Name"]]
//     facility_status = row[column_indexes["Facility Status"]]
//     facility_type = row[column_indexes["Facility Type"]]
//     accepts_subsidies = row[column_indexes["Accepts Subsidies"]]
//     operational_schedule = row[column_indexes["Operational Schedule"]]
    
//     city = row[column_indexes["City"]]
//     state = row[column_indexes["State"]]
//     zip_code = row[column_indexes["Zip Code"]]
//     alternative_zip = row[column_indexes["Facility Zip (Alt)"]]
//     address = row[column_indexes["Facility Address"]]
//     alternative_address = row[column_indexes["Alternative Address"]]

//     license_number = row[column_indexes["License Number"]]
//     license_type = row[column_indexes["License Type"]]
//     date_originally_licensed = row[column_indexes["Date Originally Licensed"]]
//     license_issue_date = row[column_indexes["License Issue Date"]]
//     license_expiry_date = row[column_indexes["License Expiry Date"]]

//     school_district = row[column_indexes["School District Affiliation"]]
//     alternative_contact_number = row[column_indexes["Alternative Contact Number"]]

//     # Generate unique IDs for entities
//     facility_id = generate_entity_id(f"{facility_name}|{license_number}|{address}", "Facility")
//     location_id = generate_entity_id(f"{city}|{state}|{address}", "Location")
//     owner_id = generate_entity_id(license_number, "Owner")
//     license_id = generate_entity_id(license_number, "License")
//     school_district_id = generate_entity_id(school_district, "School District")
//     schedule_id = generate_entity_id(facility_id, "Schedule")

//     # Generate unique IDs for license dates
//     issue_date_id = generate_entity_id(license_issue_date, "Date") if license_issue_date else None
//     expiry_date_id = generate_entity_id(license_expiry_date, "Date") if license_expiry_date else None

//     # Define entity dictionaries
//     facility_entity = {
//         "entity_id": facility_id,
//         "type": "Facility",
//         "attributes": {
//             "facility_name": facility_name,
//             "facility_status": facility_status,
//             "facility_type": facility_type,
//             "accepts_subsidies": accepts_subsidies,
//             "operational_schedule": operational_schedule
//         }
//     }

//     location_entity = {
//         "entity_id": location_id,
//         "type": "Location",
//         "attributes": {
//             "city": city,
//             "state": state,
//             "zip_code": zip_code,
//             "alternative_zip": alternative_zip,
//             "address": address,
//             "alternative_address": alternative_address
//         }
//     }

//     owner_entity = {
//         "entity_id": owner_id,
//         "type": "Owner",
//         "attributes": {
//             "alternative_contact_number": alternative_contact_number
//         }
//     }

//     license_entity = {
//         "entity_id": license_id,
//         "type": "License",
//         "attributes": {
//             "license_number": license_number,
//             "license_type": license_type,
//             "date_originally_licensed": date_originally_licensed
//         }
//     }

//     school_district_entity = {
//         "entity_id": school_district_id,
//         "type": "School District",
//         "attributes": {
//             "district_name": school_district
//         }
//     }

//     schedule_entity = {
//         "entity_id": schedule_id,
//         "type": "Schedule",
//         "attributes": {}  # This can be filled with hours of operation if needed
//     }

//     # Date entities
//     date_entities = []
//     if issue_date_id:
//         date_entities.append({
//             "entity_id": issue_date_id,
//             "type": "Date",
//             "attributes": {"date_value": license_issue_date}
//         })
//     if expiry_date_id:
//         date_entities.append({
//             "entity_id": expiry_date_id,
//             "type": "Date",
//             "attributes": {"date_value": license_expiry_date}
//         })

//     # Define relationships
//     relationships = [
//         {"from": facility_id, "to": location_id, "type": "LOCATED_AT"},
//         {"from": facility_id, "to": owner_id, "type": "OWNED_BY"},
//         {"from": facility_id, "to": license_id, "type": "LICENSED_UNDER"},
//         {"from": facility_id, "to": school_district_id, "type": "AFFILIATED_WITH"},
//         {"from": facility_id, "to": schedule_id, "type": "FOLLOWS_SCHEDULE"}
//     ]
    
//     if issue_date_id:
//         relationships.append({"from": license_id, "to": issue_date_id, "type": "ISSUED_ON"})
//     if expiry_date_id:
//         relationships.append({"from": license_id, "to": expiry_date_id, "type": "EXPIRES_ON"})

//     return {
//         "entities": [facility_entity, location_entity, owner_entity, license_entity, school_district_entity, schedule_entity] + date_entities,
//         "relationships": relationships
//     }

// # Connect to the SQLite database
// conn = sqlite3.connect("childcare.db")
// cursor = conn.cursor()

// # Fetch column names from the database
// cursor.execute("PRAGMA table_info(childcare_facilities);")
// columns = [col[1] for col in cursor.fetchall()]
// column_indexes = {col: index for index, col in enumerate(columns)}

// # Fetch all rows from the childcare facilities table
// cursor.execute("SELECT * FROM childcare_facilities;")
// rows = cursor.fetchall()

// # Process each row
// processed_data = []
// for row in rows:
//     processed_data.append(process_facility_row(row, column_indexes))

// # Close connection
// conn.close()

// # Output structured data (as JSON for easy reading)
// print(json.dumps(processed_data, indent=4))


// lets go over the logic here
// # Define entity dictionaries
//     facility_entity = {
//         "entity_id": facility_id,
//         "type": "Facility",
//         "attributes": {
//             "facility_name": facility_name,
//             "facility_status": facility_status,
//             "facility_type": facility_type,
//             "accepts_subsidies": accepts_subsidies,
//             "operational_schedule": operational_schedule
//         }
//     }



// OK this looks mostly right  - I want to clarify some things. 
// Lets first look at Schedule entity
// You have hours of operation
// So we need to define a date entity that can describe that
// then associated the hours with that entity
// Do for example we need to define a schedule as having a certain set of saturday hours
// how would we do this?

// the data looks like this:
// ,Operational Schedule,Accepts Subsidies,Hours of Operation (Sunday),Hours of Operation (Monday),Hours of Operation (Tuesday),Hours of Operation (Wednesday),Hours of Operation (Thursday),Hours of Operation (Friday),Hours of Operation (Saturday),
// School Year,YES,NOT OPEN,DAY ONLY,DAY ONLY,DAY ONLY,DAY ONLY,DAY ONLY,NOT OPEN,


// focus only on this code
// 
// 
// 
// -------------------
// def process_schedule(facility_id, row, column_indexes):
//     """Processes schedule information and creates structured entries for each day."""
//     schedule_id = generate_entity_id(facility_id, "Schedule")
//     schedule_entity = {
//         "entity_id": schedule_id,
//         "type": "Schedule",
//         "attributes": {}  # No direct attributes; links to schedule entries
//     }

//     schedule_entries = []
//     relationships = []

//     # Define days of the week and their column indexes
//     days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
//     for day in days:
//         column_key = f"Hours of Operation ({day})"
//         if column_key in column_indexes:
//             hours = row[column_indexes[column_key]].strip()  # Extract time info

//             if hours:  # Skip if no data
//                 schedule_entry_id = generate_entity_id(f"{facility_id}_{day}", "ScheduleEntry")

//                 schedule_entry = {
//                     "entity_id": schedule_entry_id,
//                     "type": "ScheduleEntry",
//                     "attributes": {
//                         "day_of_week": day,
//                         "hours": hours  # Raw value for now (can be standardized)
//                     }
//                 }

//                 # Relationship: Schedule → ScheduleEntry
//                 relationships.append({"from": schedule_id, "to": schedule_entry_id, "type": "HAS_OPERATION_HOURS"})
//                 schedule_entries.append(schedule_entry)

//     return schedule_entity, schedule_entries, relationships

//------
// Example Output
// For a facility operating:

// Monday-Friday: "DAY ONLY"
// Closed on Sundays & Saturdays: "NOT OPEN"
// Entities

// [
//     {
//         "entity_id": "12345", 
//         "type": "Schedule",
//         "attributes": {}
//     },
//     {
//         "entity_id": "12345_Monday",
//         "type": "ScheduleEntry",
//         "attributes": {
//             "day_of_week": "Monday",
//             "hours": "DAY ONLY"
//         }
//     },
//     {
//         "entity_id": "12345_Tuesday",
//         "type": "ScheduleEntry",
//         "attributes": {
//             "day_of_week": "Tuesday",
//             "hours": "DAY ONLY"
//         }
//     },
//     ...
// ]

// // Relationships
// [
//     {
//         "from": "12345",
//         "to": "12345_Monday",
//         "type": "HAS_OPERATION_HOURS"
//     },
//     {
//         "from": "12345",
//         "to": "12345_Tuesday",
//         "type": "HAS_OPERATION_HOURS"
//     }
// ]


// ok so we want the scheduleentry to have a relationship to the day of the week, and we want the hours defined as a relationship
// so a relationship to the day of the week
// opening time relationship to time
// closing time relationship to time

//--------------------------------

// def process_schedule(facility_id, row, column_indexes):
//     """Processes schedule information and creates structured ScheduleEntry entities with relationships."""
//     schedule_id = generate_entity_id(facility_id, "Schedule")
//     schedule_entity = {
//         "entity_id": schedule_id,
//         "type": "Schedule",
//         "attributes": {}
//     }

//     schedule_entries = []
//     time_entities = []
//     relationships = []
    
//     days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
//     for day in days:
//         column_key = f"Hours of Operation ({day})"
//         if column_key in column_indexes:
//             hours = row[column_indexes[column_key]].strip()  # Extract time info
            
//             # Generate IDs
//             schedule_entry_id = generate_entity_id(f"{facility_id}_{day}", "ScheduleEntry")
//             day_of_week_id = generate_entity_id(day, "DayOfWeek")

//             schedule_entry = {
//                 "entity_id": schedule_entry_id,
//                 "type": "ScheduleEntry",
//                 "attributes": {}
//             }

//             # Relationship: Schedule → ScheduleEntry
//             relationships.append({"from": schedule_id, "to": schedule_entry_id, "type": "HAS_OPERATION_HOURS"})
            
//             # Relationship: ScheduleEntry → DayOfWeek
//             relationships.append({"from": schedule_entry_id, "to": day_of_week_id, "type": "HAS_DAY"})

//             if hours == "NOT OPEN":
//                 closed_id = generate_entity_id("CLOSED", "Status")
//                 relationships.append({"from": schedule_entry_id, "to": closed_id, "type": "STATUS"})
//             else:
//                 # Extract opening and closing times if available
//                 open_time, close_time = parse_hours(hours)

//                 if open_time and close_time:
//                     open_time_id = generate_entity_id(open_time, "Time")
//                     close_time_id = generate_entity_id(close_time, "Time")

//                     time_entities.append({"entity_id": open_time_id, "type": "Time", "attributes": {"time_value": open_time}})
//                     time_entities.append({"entity_id": close_time_id, "type": "Time", "attributes": {"time_value": close_time}})

//                     relationships.append({"from": schedule_entry_id, "to": open_time_id, "type": "OPENS_AT"})
//                     relationships.append({"from": schedule_entry_id, "to": close_time_id, "type": "CLOSES_AT"})

//             schedule_entries.append(schedule_entry)

//     return schedule_entity, schedule_entries, time_entities, relationships


// def parse_hours(hours):
//     """Parses raw hour strings into opening and closing times."""
//     if hours == "DAY ONLY":
//         return "08:00", "17:00"
//     elif hours == "NIGHT ONLY":
//         return "17:00", "23:00"
//     elif hours == "24 HOURS":
//         return "00:00", "23:59"
//     else:
//         return None, None  # Could improve by adding regex parsing for specific time formats

// We should associated time zone with the location

// We actually should make time zone an entity.

// We should actually make city an entity
// state
// zipcode
// address
// all should be entities associated with  this location

// //     location_entity = {
// //         "entity_id": location_id,
// //         "type": "Location",
// //         "attributes": {
// //             "city": city,
// //             "state": state,
// //             "zip_code": zip_code,
// //             "alternative_zip": alternative_zip,
// //             "address": address,
// //             "alternative_address": alternative_address
// //         }
// //     }

// --------------------------------

// def process_location(row, column_indexes):
//     """Processes location details, creating separate entities for City, State, Zip Code, Address, and Time Zone."""
    
//     city = row[column_indexes["City"]]
//     state = row[column_indexes["State"]]
//     zip_code = row[column_indexes["Zip Code"]]
//     alternative_zip = row[column_indexes["Facility Zip (Alt)"]]
//     address = row[column_indexes["Facility Address"]]
//     alternative_address = row[column_indexes["Alternative Address"]]
//     time_zone = determine_time_zone(state)  # Function to infer timezone from state

//     # Generate unique IDs for each entity
//     location_id = generate_entity_id(f"{city}|{state}|{zip_code}|{address}", "Location")
//     city_id = generate_entity_id(city, "City")
//     state_id = generate_entity_id(state, "State")
//     zip_id = generate_entity_id(zip_code, "ZipCode")
//     address_id = generate_entity_id(address, "Address")
//     alternative_address_id = generate_entity_id(alternative_address, "Address") if alternative_address else None
//     timezone_id = generate_entity_id(time_zone, "TimeZone")

//     # Define entities
//     location_entity = {
//         "entity_id": location_id,
//         "type": "Location",
//         "attributes": {}
//     }

//     city_entity = {
//         "entity_id": city_id,
//         "type": "City",
//         "attributes": {"name": city}
//     }

//     state_entity = {
//         "entity_id": state_id,
//         "type": "State",
//         "attributes": {"name": state}
//     }

//     zip_entity = {
//         "entity_id": zip_id,
//         "type": "ZipCode",
//         "attributes": {"zip_code": zip_code}
//     }

//     address_entity = {
//         "entity_id": address_id,
//         "type": "Address",
//         "attributes": {"full_address": address}
//     }

//     if alternative_address:
//         alternative_address_entity = {
//             "entity_id": alternative_address_id,
//             "type": "Address",
//             "attributes": {"full_address": alternative_address}
//         }
//     else:
//         alternative_address_entity = None

//     timezone_entity = {
//         "entity_id": timezone_id,
//         "type": "TimeZone",
//         "attributes": {"name": time_zone}
//     }

//     # Define relationships
//     relationships = [
//         {"from": location_id, "to": city_id, "type": "LOCATED_IN"},
//         {"from": location_id, "to": state_id, "type": "IN_STATE"},
//         {"from": location_id, "to": zip_id, "type": "HAS_ZIP"},
//         {"from": location_id, "to": address_id, "type": "HAS_ADDRESS"},
//         {"from": location_id, "to": timezone_id, "type": "USES_TIMEZONE"}
//     ]

//     if alternative_address:
//         relationships.append({"from": location_id, "to": alternative_address_id, "type": "HAS_ALT_ADDRESS"})

//     # Return entities & relationships
//     entities = [location_entity, city_entity, state_entity, zip_entity, address_entity, timezone_entity]
//     if alternative_address_entity:
//         entities.append(alternative_address_entity)

//     return entities, relationships


// def determine_time_zone(state):
//     """Returns the time zone based on the state."""
//     time_zone_map = {
//         "California": "America/Los_Angeles",
//         "Texas": "America/Chicago",
//         "New York": "America/New_York",
//         "Michigan": "America/Detroit",
//         # Add other state mappings...
//     }
//     return time_zone_map.get(state, "America/New_York")  # Default to Eastern Time



// ------

// ### **📌 Complete List of Entities, Relationships, and Attributes**  

// ---

// ## **📍 Entities**
// Each entity represents a **distinct concept** in the system.

// ### **1️⃣ Facility**
// - Represents a **childcare facility** (or any service location).
// - **Relationships** connect it to **Location, Owner, License, Schedule, and School District**.

// ### **2️⃣ Location**
// - Represents **where a facility exists**.
// - **Relationships** connect it to **City, State, ZipCode, Address, and TimeZone**.

// ### **3️⃣ City**
// - Represents a **city**.
// - **Relationships** connect it to **State**.

// ### **4️⃣ State**
// - Represents a **state (or province)**.
// - **Relationships** connect it to **Cities**.

// ### **5️⃣ ZipCode**
// - Represents a **postal code**.
// - **Relationships** connect it to **City, State**.

// ### **6️⃣ Address**
// - Represents a **specific street address**.
// - **Relationships** connect it to **Location**.

// ### **7️⃣ TimeZone**
// - Represents a **time zone** (e.g., `America/New_York`).
// - **Relationships** connect it to **Location**.

// ### **8️⃣ Owner**
// - Represents the **owner of a facility**.
// - **Relationships** connect it to **Phone Numbers, Facility, License**.

// ### **9️⃣ PhoneNumber**
// - Represents a **phone number**.
// - **Relationships** connect it to **Owner, Facility, Business**.

// ### **🔟 License**
// - Represents a **legal license** assigned to a facility.
// - **Relationships** connect it to **Facility, License Type, Issue Date, Expiry Date**.

// ### **1️⃣1️⃣ LicenseType**
// - Represents the **type of license** (e.g., `"Family Childcare License"`).
// - **Relationships** connect it to **License**.

// ### **1️⃣2️⃣ Date**
// - Represents a **specific date**.
// - **Used for:** License issue date, expiry date, and potentially historical events.
// - **Relationships** connect it to **License, BirthYear**.

// ### **1️⃣3️⃣ Schedule**
// - Represents **a facility’s schedule**.
// - **Relationships** connect it to **ScheduleEntry**.

// ### **1️⃣4️⃣ ScheduleEntry**
// - Represents **a specific day’s schedule**.
// - **Relationships** connect it to **DayOfWeek, Opening Time, Closing Time**.

// ### **1️⃣5️⃣ DayOfWeek**
// - Represents **a day of the week** (Sunday - Saturday).
// - **Relationships** connect it to **ScheduleEntry**.

// ### **1️⃣6️⃣ Time**
// - Represents a **specific time** (`08:00`, `17:00`).
// - **Relationships** connect it to **ScheduleEntry (Opening/Closing Time)**.

// ### **1️⃣7️⃣ SchoolDistrict**
// - Represents a **school district**.
// - **Relationships** connect it to **Facility**.

// ### **1️⃣8️⃣ BirthYear**
// - Represents the **year of birth** for a person.
// - **Relationships** connect it to **Person**.

// ### **1️⃣9️⃣ AgeGroup**
// - Represents an **age category** (e.g., `"30-39"`, `"Children"`).
// - **Relationships** connect it to **Person**.

// ### **2️⃣0️⃣ Status**
// - Represents **a status like "Closed"**.
// - **Relationships** connect it to **ScheduleEntry**.

// ---

// ## **📍 Relationships**
// Each relationship **links entities** based on how they interact.

// | **From Entity** | **To Entity** | **Relationship Type** |
// |---------------|--------------|----------------|
// | **Facility** → **Location** | `LOCATED_AT` |
// | **Facility** → **Owner** | `OWNED_BY` |
// | **Facility** → **License** | `LICENSED_UNDER` |
// | **Facility** → **Schedule** | `FOLLOWS_SCHEDULE` |
// | **Facility** → **SchoolDistrict** | `AFFILIATED_WITH` |
// | **Location** → **City** | `LOCATED_IN` |
// | **Location** → **State** | `IN_STATE` |
// | **Location** → **ZipCode** | `HAS_ZIP` |
// | **Location** → **Address** | `HAS_ADDRESS` |
// | **Location** → **TimeZone** | `USES_TIMEZONE` |
// | **City** → **State** | `IN_STATE` |
// | **State** → **Country** (Optional Future) | `IN_COUNTRY` |
// | **Owner** → **PhoneNumber** | `HAS_PHONE` |
// | **Owner** → **Facility** | `OWNS_FACILITY` |
// | **Owner** → **License** | `HOLDS_LICENSE` |
// | **License** → **Facility** | `GRANTED_TO` |
// | **License** → **LicenseType** | `HAS_TYPE` |
// | **License** → **Date (Issue Date)** | `ISSUED_ON` |
// | **License** → **Date (Expiry Date)** | `EXPIRES_ON` |
// | **Schedule** → **ScheduleEntry** | `HAS_OPERATION_HOURS` |
// | **ScheduleEntry** → **DayOfWeek** | `HAS_DAY` |
// | **ScheduleEntry** → **Time (Opening Time)** | `OPENS_AT` |
// | **ScheduleEntry** → **Time (Closing Time)** | `CLOSES_AT` |
// | **ScheduleEntry** → **Status (Closed)** | `STATUS` |
// | **Person** → **BirthYear** | `BORN_IN` |
// | **Person** → **AgeGroup** | `BELONGS_TO` |

// ---

// ## **📍 Attributes**
// Attributes **describe** an entity but **do not define relationships**.

// | **Entity** | **Attributes** |
// |------------|--------------|
// | **Facility** | `facility_name`, `facility_status`, `facility_type`, `accepts_subsidies` |
// | **City** | `name` |
// | **State** | `name` |
// | **ZipCode** | `zip_code` |
// | **Address** | `full_address` |
// | **TimeZone** | `name` |
// | **Owner** | `alternative_contact_number` |
// | **PhoneNumber** | `number` |
// | **License** | `license_number`, `date_originally_licensed` |
// | **LicenseType** | `name` |
// | **Date** | `date_value` |
// | **Time** | `time_value` |
// | **SchoolDistrict** | `district_name` |
// | **BirthYear** | `year` |
// | **AgeGroup** | `label` |
// | **Status** | `status` (e.g., `"Closed"`) |

// ---

// ## **📌 Summary**
// | **Category** | **Count** | **Examples** |
// |-------------|----------|-------------|
// | **Entities** | 20 | `Facility, City, Owner, License, TimeZone` |
// | **Relationships** | 26 | `LOCATED_AT, OWNED_BY, HAS_PHONE, FOLLOWS_SCHEDULE` |
// | **Attributes** | 17+ | `facility_name, zip_code, time_value` |

// ---



// ok I want to rewrite this in parts to make each part modular and correct the logic :

// import sqlite3
// import hashlib
// import json
// from datetime import datetime

// # Function to generate a unique entity ID
// def generate_entity_id(value, entity_type):
//     """Generate a unique ID for an entity based on its type and name."""
//     unique_str = f"{entity_type}:{value}"
//     return hashlib.md5(unique_str.encode()).hexdigest()

// # Function to process a row and create entities & relationships
// def process_facility_row(row, column_indexes):
//     """Processes a row and returns structured entity and relationship data."""

//     # Extract necessary fields from the row using predefined indexes
//     facility_name = row[column_indexes["Facility Name"]]
//     facility_status = row[column_indexes["Facility Status"]]
//     facility_type = row[column_indexes["Facility Type"]]
//     accepts_subsidies = row[column_indexes["Accepts Subsidies"]]
//     operational_schedule = row[column_indexes["Operational Schedule"]]
    
//     city = row[column_indexes["City"]]
//     state = row[column_indexes["State"]]
//     zip_code = row[column_indexes["Zip Code"]]
//     alternative_zip = row[column_indexes["Facility Zip (Alt)"]]
//     address = row[column_indexes["Facility Address"]]
//     alternative_address = row[column_indexes["Alternative Address"]]

//     license_number = row[column_indexes["License Number"]]
//     license_type = row[column_indexes["License Type"]]
//     date_originally_licensed = row[column_indexes["Date Originally Licensed"]]
//     license_issue_date = row[column_indexes["License Issue Date"]]
//     license_expiry_date = row[column_indexes["License Expiry Date"]]

//     school_district = row[column_indexes["School District Affiliation"]]
//     alternative_contact_number = row[column_indexes["Alternative Contact Number"]]

//     # Generate unique IDs for entities
//     facility_id = generate_entity_id(f"{facility_name}|{license_number}|{address}", "Facility")
//     location_id = generate_entity_id(f"{city}|{state}|{address}", "Location")
//     owner_id = generate_entity_id(license_number, "Owner")
//     license_id = generate_entity_id(license_number, "License")
//     school_district_id = generate_entity_id(school_district, "School District")
//     schedule_id = generate_entity_id(facility_id, "Schedule")

//     # Generate unique IDs for license dates
//     issue_date_id = generate_entity_id(license_issue_date, "Date") if license_issue_date else None
//     expiry_date_id = generate_entity_id(license_expiry_date, "Date") if license_expiry_date else None

//     # Define entity dictionaries
//     facility_entity = {
//         "entity_id": facility_id,
//         "type": "Facility",
//         "attributes": {
//             "facility_name": facility_name,
//             "facility_status": facility_status,
//             "facility_type": facility_type,
//             "accepts_subsidies": accepts_subsidies,
//             "operational_schedule": operational_schedule
//         }
//     }

//     location_entity = {
//         "entity_id": location_id,
//         "type": "Location",
//         "attributes": {
//             "city": city,
//             "state": state,
//             "zip_code": zip_code,
//             "alternative_zip": alternative_zip,
//             "address": address,
//             "alternative_address": alternative_address
//         }
//     }

//     owner_entity = {
//         "entity_id": owner_id,
//         "type": "Owner",
//         "attributes": {
//             "alternative_contact_number": alternative_contact_number
//         }
//     }

//     license_entity = {
//         "entity_id": license_id,
//         "type": "License",
//         "attributes": {
//             "license_number": license_number,
//             "license_type": license_type,
//             "date_originally_licensed": date_originally_licensed
//         }
//     }

//     school_district_entity = {
//         "entity_id": school_district_id,
//         "type": "School District",
//         "attributes": {
//             "district_name": school_district
//         }
//     }

//     schedule_entity = {
//         "entity_id": schedule_id,
//         "type": "Schedule",
//         "attributes": {}  # This can be filled with hours of operation if needed
//     }

//     # Date entities
//     date_entities = []
//     if issue_date_id:
//         date_entities.append({
//             "entity_id": issue_date_id,
//             "type": "Date",
//             "attributes": {"date_value": license_issue_date}
//         })
//     if expiry_date_id:
//         date_entities.append({
//             "entity_id": expiry_date_id,
//             "type": "Date",
//             "attributes": {"date_value": license_expiry_date}
//         })

//     # Define relationships
//     relationships = [
//         {"from": facility_id, "to": location_id, "type": "LOCATED_AT"},
//         {"from": facility_id, "to": owner_id, "type": "OWNED_BY"},
//         {"from": facility_id, "to": license_id, "type": "LICENSED_UNDER"},
//         {"from": facility_id, "to": school_district_id, "type": "AFFILIATED_WITH"},
//         {"from": facility_id, "to": schedule_id, "type": "FOLLOWS_SCHEDULE"}
//     ]
    
//     if issue_date_id:
//         relationships.append({"from": license_id, "to": issue_date_id, "type": "ISSUED_ON"})
//     if expiry_date_id:
//         relationships.append({"from": license_id, "to": expiry_date_id, "type": "EXPIRES_ON"})

//     return {
//         "entities": [facility_entity, location_entity, owner_entity, license_entity, school_district_entity, schedule_entity] + date_entities,
//         "relationships": relationships
//     }

// def process_schedule(facility_id, row, column_indexes):
//     """Processes schedule information and creates structured ScheduleEntry entities with relationships."""
//     schedule_id = generate_entity_id(facility_id, "Schedule")
//     schedule_entity = {
//         "entity_id": schedule_id,
//         "type": "Schedule",
//         "attributes": {}
//     }

//     schedule_entries = []
//     time_entities = []
//     relationships = []
    
//     days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
//     for day in days:
//         column_key = f"Hours of Operation ({day})"
//         if column_key in column_indexes:
//             hours = row[column_indexes[column_key]].strip()  # Extract time info
            
//             # Generate IDs
//             schedule_entry_id = generate_entity_id(f"{facility_id}_{day}", "ScheduleEntry")
//             day_of_week_id = generate_entity_id(day, "DayOfWeek")

//             schedule_entry = {
//                 "entity_id": schedule_entry_id,
//                 "type": "ScheduleEntry",
//                 "attributes": {}
//             }

//             # Relationship: Schedule → ScheduleEntry
//             relationships.append({"from": schedule_id, "to": schedule_entry_id, "type": "HAS_OPERATION_HOURS"})
            
//             # Relationship: ScheduleEntry → DayOfWeek
//             relationships.append({"from": schedule_entry_id, "to": day_of_week_id, "type": "HAS_DAY"})

//             if hours == "NOT OPEN":
//                 closed_id = generate_entity_id("CLOSED", "Status")
//                 relationships.append({"from": schedule_entry_id, "to": closed_id, "type": "STATUS"})
//             else:
//                 # Extract opening and closing times if available
//                 open_time, close_time = parse_hours(hours)

//                 if open_time and close_time:
//                     open_time_id = generate_entity_id(open_time, "Time")
//                     close_time_id = generate_entity_id(close_time, "Time")

//                     time_entities.append({"entity_id": open_time_id, "type": "Time", "attributes": {"time_value": open_time}})
//                     time_entities.append({"entity_id": close_time_id, "type": "Time", "attributes": {"time_value": close_time}})

//                     relationships.append({"from": schedule_entry_id, "to": open_time_id, "type": "OPENS_AT"})
//                     relationships.append({"from": schedule_entry_id, "to": close_time_id, "type": "CLOSES_AT"})

//             schedule_entries.append(schedule_entry)

//     return schedule_entity, schedule_entries, time_entities, relationships

// ---------------------

// 1 - separate the logic that involves breaking apart the row of data - make the row of data an object that is passed from function to function to create the entities

// 2 - make the definition of each entity from the row data a unique function

// 3-  review and redefine the schemas so they are defined individually and provide the instructions for the function how to handle the row of data

// 4 - every attribute needs to be given an ID
// 5 - then every schema type needs to be given an ID
// 6 - then every entity of a type needs to be defined and given an ID
// 7 - then every relationship type needs an ID
// 8 - then every relationship between entities needs to be defined and given an ID

// 

// -----

import sqlite3
import hashlib
import json
from datetime import datetime

### ✅ Step 1: Utility Functions

def generate_id(value, prefix):
    """Generate a unique ID for a given value."""
    return hashlib.md5(f"{prefix}:{value}".encode()).hexdigest()


### ✅ Step 2: Schema Definitions
SCHEMA_DEFINITIONS = {
    "Facility": {
        "schema_id": generate_id("Facility", "Schema"),
        "attributes": ["facility_name", "facility_status", "facility_type", "accepts_subsidies"],
        "relationships": {
            "LOCATED_AT": "Location",
            "OWNED_BY": "Owner",
            "LICENSED_UNDER": "License",
            "FOLLOWS_SCHEDULE": "Schedule",
            "AFFILIATED_WITH": "SchoolDistrict"
        }
    },
    "Location": {
        "schema_id": generate_id("Location", "Schema"),
        "attributes": [],
        "relationships": {
            "LOCATED_IN": "City",
            "IN_STATE": "State",
            "HAS_ZIP": "ZipCode",
            "HAS_ADDRESS": "Address",
            "USES_TIMEZONE": "TimeZone"
        }
    },
    "City": {
        "schema_id": generate_id("City", "Schema"),
        "attributes": ["name"],
        "relationships": {
            "IN_STATE": "State"
        }
    },
    "State": {
        "schema_id": generate_id("State", "Schema"),
        "attributes": ["name"],
        "relationships": {}
    },
    "ZipCode": {
        "schema_id": generate_id("ZipCode", "Schema"),
        "attributes": ["zip_code"],
        "relationships": {
            "IN_CITY": "City",
            "IN_STATE": "State"
        }
    },
    "Address": {
        "schema_id": generate_id("Address", "Schema"),
        "attributes": ["full_address"],
        "relationships": {
            "BELONGS_TO": "Location"
        }
    },
    "TimeZone": {
        "schema_id": generate_id("TimeZone", "Schema"),
        "attributes": ["name"],
        "relationships": {
            "USED_BY": "Location"
        }
    },
    "Owner": {
        "schema_id": generate_id("Owner", "Schema"),
        "attributes": ["alternative_contact_number"],
        "relationships": {
            "HAS_PHONE": "PhoneNumber",
            "OWNS_FACILITY": "Facility",
            "HOLDS_LICENSE": "License"
        }
    },
    "PhoneNumber": {
        "schema_id": generate_id("PhoneNumber", "Schema"),
        "attributes": ["number"],
        "relationships": {
            "USED_BY": ["Owner", "Facility", "Business"]
        }
    },
    "License": {
        "schema_id": generate_id("License", "Schema"),
        "attributes": ["license_number", "date_originally_licensed"],
        "relationships": {
            "GRANTED_TO": "Facility",
            "HAS_TYPE": "LicenseType",
            "ISSUED_ON": "Date",
            "EXPIRES_ON": "Date"
        }
    },
    "LicenseType": {
        "schema_id": generate_id("LicenseType", "Schema"),
        "attributes": ["name"],
        "relationships": {
            "USED_IN": "License"
        }
    },
    "Date": {
        "schema_id": generate_id("Date", "Schema"),
        "attributes": ["date_value"],
        "relationships": {
            "RELATED_TO": ["License", "BirthYear"]
        }
    },
    "Schedule": {
        "schema_id": generate_id("Schedule", "Schema"),
        "attributes": [],
        "relationships": {
            "HAS_OPERATION_HOURS": "ScheduleEntry"
        }
    },
    "ScheduleEntry": {
        "schema_id": generate_id("ScheduleEntry", "Schema"),
        "attributes": [],
        "relationships": {
            "HAS_DAY": "DayOfWeek",
            "OPENS_AT": "Time",
            "CLOSES_AT": "Time",
            "STATUS": "Status"
        }
    },
    "DayOfWeek": {
        "schema_id": generate_id("DayOfWeek", "Schema"),
        "attributes": ["day"],
        "relationships": {
            "PART_OF": "ScheduleEntry"
        }
    },
    "Time": {
        "schema_id": generate_id("Time", "Schema"),
        "attributes": ["time_value"],
        "relationships": {
            "USED_IN": "ScheduleEntry"
        }
    },
    "SchoolDistrict": {
        "schema_id": generate_id("SchoolDistrict", "Schema"),
        "attributes": ["district_name"],
        "relationships": {
            "OVERSEES": "Facility"
        }
    },
    "BirthYear": {
        "schema_id": generate_id("BirthYear", "Schema"),
        "attributes": ["year"],
        "relationships": {
            "BORN_IN": "Person"
        }
    },
    "AgeGroup": {
        "schema_id": generate_id("AgeGroup", "Schema"),
        "attributes": ["label"],
        "relationships": {
            "BELONGS_TO": "Person"
        }
    },
    "Status": {
        "schema_id": generate_id("Status", "Schema"),
        "attributes": ["status"],
        "relationships": {
            "USED_IN": "ScheduleEntry"
        }
    }
}


def parse_row_data(row, column_indexes):
    """Extracts row data into a structured object."""
    return {
        "facility_name": row[column_indexes["Facility Name"]],
        "facility_status": row[column_indexes["Facility Status"]],
        "facility_type": row[column_indexes["Facility Type"]],
        "accepts_subsidies": row[column_indexes["Accepts Subsidies"]],
        "city": row[column_indexes["City"]],
        "state": row[column_indexes["State"]],
        "zip_code": row[column_indexes["Zip Code"]],
        "alternative_zip": row[column_indexes["Facility Zip (Alt)"]],
        "address": row[column_indexes["Facility Address"]],
        "alternative_address": row[column_indexes["Alternative Address"]],
        "license_number": row[column_indexes["License Number"]],
        "license_type": row[column_indexes["License Type"]],
        "date_originally_licensed": row[column_indexes["Date Originally Licensed"]],
        "license_issue_date": row[column_indexes["License Issue Date"]],
        "license_expiry_date": row[column_indexes["License Expiry Date"]],
        "school_district": row[column_indexes["School District Affiliation"]],
        "alternative_contact_number": row[column_indexes["Alternative Contact Number"]]
    }


data = parse_row_data(row, column_indexes)

def process_facility(data):
    """Processes a single row of data to create a Facility entity."""
    
    # Generate a unique Facility ID
    facility_id = generate_id(f"{data['facility_name']}", "Facility")
    
    # Extract schema details for Facility
    schema = SCHEMA_DEFINITIONS["Facility"]
    
    # Create the Facility entity
    facility_entity = {
        "entity_id": facility_id,
        "type": "Facility",
        "schema_id": schema["schema_id"],
        "attributes": {
            attr: data[attr] for attr in schema["attributes"] if attr in data  # Ensure valid attributes
        }
    }
    
    return facility_entity



    import hashlib

# Global ID dictionary
ID_INDEX = {
    "Entity": {},        # Stores entity type -> ID
    "Attribute": {},     # Stores attribute name -> ID
    "Relationship": {}   # Stores relationship type -> ID
}

def get_or_create_id(value, category):
    """
    Retrieves an existing ID if the value exists in ID_INDEX,
    otherwise generates a new one and stores it.
    
    Args:
        value (str): The name of the entity, attribute, or relationship.
        category (str): One of ["Entity", "Attribute", "Relationship"].
    
    Returns:
        str: The unique ID for the given value.
    """

    # Ensure the category exists in the dictionary
    if category not in ID_INDEX:
        raise ValueError(f"Invalid category: {category}")

    # Check if ID already exists
    if value in ID_INDEX[category]:
        return ID_INDEX[category][value]

    # Generate a new unique ID
    unique_id = hashlib.md5(f"{category}:{value}".encode()).hexdigest()

    # Store the new ID
    ID_INDEX[category][value] = unique_id

    return unique_id



def process_facility(data):
    """Processes a single row of data to create a Facility entity, its relationships, and related entities."""

    # Retrieve or create Facility entity
    facility_id = get_or_create_entity("Facility", f"{data['facility_name']}|{data['license_number']}|{data['address']}")

    # Retrieve or create attributes
    attributes = get_or_create_attributes("Facility", data)

    # Retrieve or create related entities (Location, Owner, License, School District, Schedule)
    location_id = get_or_create_entity("Location", f"{data['city']}|{data['state']}|{data['address']}")
    owner_id = get_or_create_entity("Owner", data["license_number"])
    license_id = get_or_create_entity("License", data["license_number"])
    school_district_id = get_or_create_entity("SchoolDistrict", data["school_district"])
    schedule_id = get_or_create_entity("Schedule", facility_id)

    # Retrieve or create relationships
    relationships = [
        get_or_create_relationship(facility_id, location_id, "LOCATED_AT"),
        get_or_create_relationship(facility_id, owner_id, "OWNED_BY"),
        get_or_create_relationship(facility_id, license_id, "LICENSED_UNDER"),
        get_or_create_relationship(facility_id, school_district_id, "AFFILIATED_WITH"),
        get_or_create_relationship(facility_id, schedule_id, "FOLLOWS_SCHEDULE")
    ]

    # Construct Facility entity
    facility_entity = {
        "entity_id": facility_id,
        "type": "Facility",
        "schema_id": get_or_create_id("Facility", "Entity"),
        "attributes": attributes,
        "relationships": relationships
    }

    return facility_entity

def get_or_create_entity(entity_type, unique_key):
    """Retrieve or create an entity and return its ID."""
    entity_id = get_or_create_id(unique_key, "Entity")
    return entity_id


def get_or_create_attributes(entity_type, data):
    """Retrieve or create attribute IDs and return them as a dictionary."""
    schema = SCHEMA_DEFINITIONS[entity_type]
    attributes_with_ids = {}

    for attr in schema["attributes"]:
        if attr in data:
            attr_id = get_or_create_id(attr, "Attribute")
            attributes_with_ids[attr_id] = {
                "name": attr,
                "value": data[attr]
            }

    return attributes_with_ids

    
def get_or_create_relationship(from_id, to_id, relationship_type):
    """Retrieve or create a relationship and return its ID."""
    if not from_id or not to_id:  # Ensure valid IDs before creating relationships
        return None

    relationship_id = get_or_create_id(f"{from_id}->{to_id}", "Relationship")
    return {
        "relationship_id": relationship_id,
        "from": from_id,
        "to": to_id,
        "type": relationship_type
    }

    
ENTITY_DEFINITIONS = {
        "Facility": lambda data: f"{data['facility_name']}|{data['license_number']}|{data['address']}",
        "Location": lambda data: f"{data['address']}|{data['city']}|{data['state']}|{data['zip_code']}",
        "Owner": lambda data: f"{data['facility_name']}_person",
        "License": lambda data: data["license_number"],
        "SchoolDistrict": lambda data: data["school_district"],
        "Schedule": lambda data: f"{data['operational_schedule']}|{data['Hours of Operation (Sunday)']}|{data['Hours of Operation (Monday)']}|{data['Hours of Operation (Tuesday)']}|{data['Hours of Operation (Wednesday)']}|{data['Hours of Operation (Thursday)']}|{data['Hours of Operation (Friday)']}|{data['Hours of Operation (Saturday)']}"
    }
    
def get_or_create_entity(entity_type, data):
        """
        Retrieve or create an entity ID using standardized definitions.

        Args:
            entity_type (str): The entity type (e.g., "Facility", "Location").
            data (dict): The row data used for unique identification.

        Returns:
            str: The unique ID of the entity.
        """
        if entity_type not in ENTITY_DEFINITIONS:
            raise ValueError(f"Entity type '{entity_type}' is not defined.")

        # Generate the unique key based on the entity definition
        unique_key = ENTITY_DEFINITIONS[entity_type](data)

        # Get or create the entity ID
        entity_id = get_or_create_id(unique_key, "Entity")

        return entity_id

def process_facility(data):
        """Processes a single row of data to create a Facility entity, its relationships, and related entities."""
    
        # Retrieve or create Facility entity
        facility_id = get_or_create_entity("Facility", data)
    
        # Retrieve or create attributes
        attributes = get_or_create_attributes("Facility", data)
    
        # Retrieve or create related entities using standardized definitions
        location_id = get_or_create_entity("Location", data)
        owner_id = get_or_create_entity("Owner", data)
        license_id = get_or_create_entity("License", data)
        school_district_id = get_or_create_entity("SchoolDistrict", data)
        schedule_id = get_or_create_entity("Schedule", data)
    
        # Retrieve or create relationships
        relationships = [
            get_or_create_relationship(facility_id, location_id, "LOCATED_AT"),
            get_or_create_relationship(facility_id, owner_id, "OWNED_BY"),
            get_or_create_relationship(facility_id, license_id, "LICENSED_UNDER"),
            get_or_create_relationship(facility_id, school_district_id, "AFFILIATED_WITH"),
            get_or_create_relationship(facility_id, schedule_id, "FOLLOWS_SCHEDULE")
        ]
    
        # Construct Facility entity
        facility_entity = {
            "entity_id": facility_id,
            "type": "Facility",
            "schema_id": get_or_create_id("Facility", "Entity"),
            "attributes": attributes,
            "relationships": relationships
        }
    
        return facility_entity
    


        // ### **📌 Complete List of Entity Processing Functions**
        // We will need to create **a processing function for each entity type**. Each function will:
        // 1. **Create the entity** using `get_or_create_entity()`.
        // 2. **Define its attributes** using `get_or_create_attributes()`.
        // 3. **Define its relationships** using `get_or_create_relationship()`.
        
        // ---
        
        // ## **📍 Entity Processing Functions & Their Relationships**
        // Each entity is listed with the **other entities it connects to and the relationship type**.
        
        // ---
        
        // ### **1️⃣ Facility**
        // - **Attributes:** `facility_name, facility_status, facility_type, accepts_subsidies`
        // - **Relationships:**
        //   - `LOCATED_AT` → **Location**
        //   - `OWNED_BY` → **Owner**
        //   - `LICENSED_UNDER` → **License**
        //   - `AFFILIATED_WITH` → **SchoolDistrict**
        //   - `FOLLOWS_SCHEDULE` → **Schedule**
        
        // ---
        
        // ### **2️⃣ Location**
        // - **Attributes:** (None—location is defined by its relationships)
        // - **Relationships:**
        //   - `LOCATED_IN` → **City**
        //   - `IN_STATE` → **State**
        //   - `HAS_ZIP` → **ZipCode**
        //   - `HAS_ADDRESS` → **Address**
        //   - `USES_TIMEZONE` → **TimeZone**
        
        // ---
        
        // ### **3️⃣ City**
        // - **Attributes:** `name`
        // - **Relationships:**
        //   - `IN_STATE` → **State**
        
        // ---
        
        // ### **4️⃣ State**
        // - **Attributes:** `name`
        // - **Relationships:** (None—this is a standalone entity)
        
        // ---
        
        // ### **5️⃣ ZipCode**
        // - **Attributes:** `zip_code`
        // - **Relationships:**
        //   - `IN_CITY` → **City**
        //   - `IN_STATE` → **State**
        
        // ---
        
        // ### **6️⃣ Address**
        // - **Attributes:** `full_address`
        // - **Relationships:**
        //   - `BELONGS_TO` → **Location**
        
        // ---
        
        // ### **7️⃣ TimeZone**
        // - **Attributes:** `name`
        // - **Relationships:**
        //   - `USED_BY` → **Location**
        
        // ---
        
        // ### **8️⃣ Owner**
        // - **Attributes:** `alternative_contact_number`
        // - **Relationships:**
        //   - `HAS_PHONE` → **PhoneNumber**
        //   - `OWNS_FACILITY` → **Facility**
        //   - `HOLDS_LICENSE` → **License**
        
        // ---
        
        // ### **9️⃣ PhoneNumber**
        // - **Attributes:** `number`
        // - **Relationships:**
        //   - `USED_BY` → **Owner, Facility, Business**
        
        // ---
        
        // ### **🔟 License**
        // - **Attributes:** `license_number, date_originally_licensed`
        // - **Relationships:**
        //   - `GRANTED_TO` → **Facility**
        //   - `HAS_TYPE` → **LicenseType**
        //   - `ISSUED_ON` → **Date**
        //   - `EXPIRES_ON` → **Date**
        
        // ---
        
        // ### **1️⃣1️⃣ LicenseType**
        // - **Attributes:** `name`
        // - **Relationships:**
        //   - `USED_IN` → **License**
        
        // ---
        
        // ### **1️⃣2️⃣ Date**
        // - **Attributes:** `date_value`
        // - **Relationships:**
        //   - `RELATED_TO` → **License, BirthYear**
        
        // ---
        
        // ### **1️⃣3️⃣ Schedule**
        // - **Attributes:** (None—schedule is defined by `ScheduleEntries`)
        // - **Relationships:**
        //   - `HAS_OPERATION_HOURS` → **ScheduleEntry**
        
        // ---
        
        // ### **1️⃣4️⃣ ScheduleEntry**
        // - **Attributes:** (None—defined by relationships)
        // - **Relationships:**
        //   - `HAS_DAY` → **DayOfWeek**
        //   - `OPENS_AT` → **Time**
        //   - `CLOSES_AT` → **Time**
        //   - `STATUS` → **Status**
        
        // ---
        
        // ### **1️⃣5️⃣ DayOfWeek**
        // - **Attributes:** `day`
        // - **Relationships:**
        //   - `PART_OF` → **ScheduleEntry**
        
        // ---
        
        // ### **1️⃣6️⃣ Time**
        // - **Attributes:** `time_value`
        // - **Relationships:**
        //   - `USED_IN` → **ScheduleEntry**
        
        // ---
        
        // ### **1️⃣7️⃣ SchoolDistrict**
        // - **Attributes:** `district_name`
        // - **Relationships:**
        //   - `OVERSEES` → **Facility**
        
        // ---
        
        // ### **1️⃣8️⃣ BirthYear**
        // - **Attributes:** `year`
        // - **Relationships:**
        //   - `BORN_IN` → **Person**
        
        // ---
        
        // ### **1️⃣9️⃣ AgeGroup**
        // - **Attributes:** `label`
        // - **Relationships:**
        //   - `BELONGS_TO` → **Person**
        
        // ---
        
        // ### **2️⃣0️⃣ Status**
        // - **Attributes:** `status`
        // - **Relationships:**
        //   - `USED_IN` → **ScheduleEntry**
        
        // ---
        
        // ### **📌 Next Steps**
        // ✅ **Does this list cover everything you had in mind?**  
        // ✅ **If yes, we can now write the standard processing function template for all entities.** 🚀


        def process_location(data):
        """Processes a Location entity, defining its attributes and relationships."""
        location_id = get_or_create_entity("Location", data)
        attributes = get_or_create_attributes("Location", data)
        
        # Related Entities
        city_id = get_or_create_entity("City", data)
        state_id = get_or_create_entity("State", data)
        zipcode_id = get_or_create_entity("ZipCode", data)
        address_id = get_or_create_entity("Address", data)
        timezone_id = get_or_create_entity("TimeZone", data)
    
        # Relationships
        relationships = [
            get_or_create_relationship(location_id, city_id, "LOCATED_IN"),
            get_or_create_relationship(location_id, state_id, "IN_STATE"),
            get_or_create_relationship(location_id, zipcode_id, "HAS_ZIP"),
            get_or_create_relationship(location_id, address_id, "HAS_ADDRESS"),
            get_or_create_relationship(location_id, timezone_id, "USES_TIMEZONE")
        ]
    
        return {"entity_id": location_id, "type": "Location", "attributes": attributes, "relationships": relationships}
    
    
    def process_owner(data):
        """Processes an Owner entity."""
        owner_id = get_or_create_entity("Owner", data)
        attributes = get_or_create_attributes("Owner", data)
    
        phone_id = get_or_create_entity("PhoneNumber", data)
        facility_id = get_or_create_entity("Facility", data)
        license_id = get_or_create_entity("License", data)
    
        relationships = [
            get_or_create_relationship(owner_id, phone_id, "HAS_PHONE"),
            get_or_create_relationship(owner_id, facility_id, "OWNS_FACILITY"),
            get_or_create_relationship(owner_id, license_id, "HOLDS_LICENSE")
        ]
    
        return {"entity_id": owner_id, "type": "Owner", "attributes": attributes, "relationships": relationships}
    
    
    def process_license(data):
        """Processes a License entity."""
        license_id = get_or_create_entity("License", data)
        attributes = get_or_create_attributes("License", data)
    
        facility_id = get_or_create_entity("Facility", data)
        license_type_id = get_or_create_entity("LicenseType", data)
        issue_date_id = get_or_create_entity("Date", {"date_value": data["license_issue_date"]})
        expiry_date_id = get_or_create_entity("Date", {"date_value": data["license_expiry_date"]})
    
        relationships = [
            get_or_create_relationship(license_id, facility_id, "GRANTED_TO"),
            get_or_create_relationship(license_id, license_type_id, "HAS_TYPE"),
            get_or_create_relationship(license_id, issue_date_id, "ISSUED_ON"),
            get_or_create_relationship(license_id, expiry_date_id, "EXPIRES_ON")
        ]
    
        return {"entity_id": license_id, "type": "License", "attributes": attributes, "relationships": relationships}
    
    
    def process_school_district(data):
        """Processes a School District entity."""
        district_id = get_or_create_entity("SchoolDistrict", data)
        attributes = get_or_create_attributes("SchoolDistrict", data)
    
        facility_id = get_or_create_entity("Facility", data)
    
        relationships = [
            get_or_create_relationship(district_id, facility_id, "OVERSEES")
        ]
    
        return {"entity_id": district_id, "type": "SchoolDistrict", "attributes": attributes, "relationships": relationships}
    
    
    def process_schedule(data):
        """Processes a Schedule entity."""
        schedule_id = get_or_create_entity("Schedule", data)
        attributes = get_or_create_attributes("Schedule", data)
    
        facility_id = get_or_create_entity("Facility", data)
        schedule_entries = [get_or_create_entity("ScheduleEntry", {"day": day, "time": data[f"Hours of Operation ({day})"]})
                            for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]]
    
        relationships = [get_or_create_relationship(schedule_id, entry, "HAS_OPERATION_HOURS") for entry in schedule_entries]
    
        return {"entity_id": schedule_id, "type": "Schedule", "attributes": attributes, "relationships": relationships}
    
    
    def process_schedule_entry(data, day):
        """Processes a single ScheduleEntry entity for a given day."""
        schedule_entry_id = get_or_create_entity("ScheduleEntry", {"day": day, "time": data[f"Hours of Operation ({day})"]})
        attributes = get_or_create_attributes("ScheduleEntry", {"day": day, "time": data[f"Hours of Operation ({day})"]})
    
        day_of_week_id = get_or_create_entity("DayOfWeek", {"day": day})
        open_time_id = get_or_create_entity("Time", {"time_value": data[f"Hours of Operation ({day})"].split('-')[0]})
        close_time_id = get_or_create_entity("Time", {"time_value": data[f"Hours of Operation ({day})"].split('-')[-1]})
    
        relationships = [
            get_or_create_relationship(schedule_entry_id, day_of_week_id, "HAS_DAY"),
            get_or_create_relationship(schedule_entry_id, open_time_id, "OPENS_AT"),
            get_or_create_relationship(schedule_entry_id, close_time_id, "CLOSES_AT")
        ]
    
        return {"entity_id": schedule_entry_id, "type": "ScheduleEntry", "attributes": attributes, "relationships": relationships}
    
    
    def process_day_of_week(data):
        """Processes a DayOfWeek entity."""
        day_id = get_or_create_entity("DayOfWeek", data)
        attributes = get_or_create_attributes("DayOfWeek", data)
    
        return {"entity_id": day_id, "type": "DayOfWeek", "attributes": attributes, "relationships": []}
    
    
    def process_time(data):
        """Processes a Time entity."""
        time_id = get_or_create_entity("Time", data)
        attributes = get_or_create_attributes("Time", data)
    
        return {"entity_id": time_id, "type": "Time", "attributes": attributes, "relationships": []}
    
    
    def process_status(data):
        """Processes a Status entity."""
        status_id = get_or_create_entity("Status", data)
        attributes = get_or_create_attributes("Status", data)
    
        return {"entity_id": status_id, "type": "Status", "attributes": attributes, "relationships": []}
    