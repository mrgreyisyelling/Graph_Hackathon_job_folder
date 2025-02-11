Here's your **optimized and cleaned-up** version of the code, applying the same **performance improvements, readability, and maintainability enhancements** as before.

---

### **🔧 Key Fixes & Optimizations**

✅ **Extracts `columns.index()` once** for performance (avoids redundant lookups).  
✅ **Ensures all `generate_entity_id()` calls use the right unique keys**.  
✅ **Uses dictionary tracking (`location_map`, `owner_map`, etc.) effectively** to **avoid unnecessary inserts**.  
✅ **Improves readability and maintainability**.

---

### **💡 Optimized Python Code**

```python
import hashlib
import sqlite3

# Function to generate a unique entity ID
def generate_entity_id(value, entity_type):
    """Generate a unique ID for an entity based on its type and name."""
    unique_str = f"{entity_type}:{value}"
    return hashlib.md5(unique_str.encode()).hexdigest()

# Connect to SQLite
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

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
facility_name_idx = columns.index("Facility Name")
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

    # Generate unique Location ID using City, State, and Address
    location_key = f"{row[city_idx]}|{row[state_idx]}|{row[facility_addr_idx]}"
    location_id = location_map.get(location_key) or generate_entity_id(location_key, "Location")

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
        cursor.execute("""
            INSERT OR IGNORE INTO locations (location_id, city, state, zip_code, facility_address, facility_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (location_id, row[city_idx], row[state_idx], str(row[zip_idx]), row[facility_addr_idx], row[facility_name_idx]))
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

    print(f"Row {row_num}: Facility - Inserted successfully.")

# Commit changes and close the connection
conn.commit()
conn.close()
```

---

### **🛠 Why This Version is Better?**

1. **🚀 Faster Execution**
    
    - Extracts column indexes **once** instead of calling `columns.index()` multiple times.
    - Uses **dictionary maps (`location_map`, `owner_map`, etc.)** to avoid redundant `INSERT OR IGNORE` calls.
2. **🎯 More Accurate Data Handling**
    
    - Prevents inserting duplicate **Locations, Owners, Licenses, and School Districts** by checking **before inserting**.
    - Ensures the **same IDs are used consistently** across related tables.
3. **📝 Improved Readability & Maintainability**
    
    - Code is **cleaner** and easier to **modify** if needed.
    - Uses **meaningful variable names** (`facility_name_idx`, `license_number_idx`, etc.) for clarity.

---

### **🔍 Next Steps**

- ✅ Run this script and verify the database with:
    
    ```sql
    SELECT * FROM facilities LIMIT 5;
    ```
    
- ✅ If needed, add **indexes** on foreign keys (`location_id`, `owner_id`, etc.) to **speed up lookups**.

Let me know if you need any refinements! 🚀🔥