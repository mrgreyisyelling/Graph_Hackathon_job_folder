### **Set Up Your Local Development Environment for CSV Import & SQLite Storage**

#### **1. Create a New Project Directory**

```bash
mkdir childcare_db
cd childcare_db
```

#### **2. Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### **3. Install Required Packages**

```bash
pip install pandas sqlite-utils
sudo apt install sqlite3
```

#### **4. Place Your CSV File**

Copy your CSV file into the project directory:

```bash
mv /path/to/your_file.csv childcare_data.csv
```

#### **5. Create a Python Script to Import Data**

Create a file named `import_data.py`:

```bash
touch import_data.py
```

Then, edit it with the following code:

```python
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
```

#### **6. Run the Import Script**

```bash
python import_data.py
```

---

### **Query the Database**

#### **7. Open SQLite Shell**

```bash
sqlite3 childcare.db
```

Then, run:

```sql
SELECT * FROM childcare_facilities LIMIT 5;
```

or use Python:

```python
import sqlite3

conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM childcare_facilities LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
```

-----
----

# improved [[20250211075441 - Optimized Python Code]]

[[20250211102522 - old]] - old

	

	
	
	
	```sql
	mike@thudbucket:~/Documents/Programming/Graph_Hackathon_job_folder/childcare_db$ sqlite3 childcare.db
	SQLite version 3.37.2 2022-01-06 13:25:41
	Enter ".help" for usage hints.
	sqlite> .tables
	childcare_facilities  locations             triples             
	facilities            owners              
	licenses              school_districts    
	sqlite> PRAGMA table_info(childcare_facilities);
	0|Date Extracted|TEXT|0||0
	1|License Number|TEXT|0||0
	2|License Issue Date|TEXT|0||0
	3|License Expiry Date|TEXT|0||0
	4|License Type|TEXT|0||0
	5|Facility Name|TEXT|0||0
	6|Facility Address|TEXT|0||0
	7|Unnamed: 7|TEXT|0||0
	8|City|TEXT|0||0
	9|State|TEXT|0||0
	10|Zip Code|INTEGER|0||0
	11|Phone Number|REAL|0||0
	12|Facility Type|TEXT|0||0
	13|Capacity|INTEGER|0||0
	14|Enrollment|INTEGER|0||0
	15|Staff|REAL|0||0
	16|Unnamed: 16|REAL|0||0
	17|Operational Schedule|TEXT|0||0
	18|Accepts Subsidies|TEXT|0||0
	19|Hours of Operation (Sunday)|TEXT|0||0
	20|Hours of Operation (Monday)|TEXT|0||0
	21|Hours of Operation (Tuesday)|TEXT|0||0
	22|Hours of Operation (Wednesday)|TEXT|0||0
	23|Hours of Operation (Thursday)|TEXT|0||0
	24|Hours of Operation (Friday)|TEXT|0||0
	25|Hours of Operation (Saturday)|TEXT|0||0
	26|School District Affiliation|TEXT|0||0
	27|Alternative Address|TEXT|0||0
	28|Unnamed: 28|TEXT|0||0
	29|Unnamed: 29|TEXT|0||0
	30|Unnamed: 30|TEXT|0||0
	31|Facility Zip (Alt)|INTEGER|0||0
	32|Alternative Contact Number|REAL|0||0
	33|Date Originally Licensed|TEXT|0||0
	34|Unnamed: 34|INTEGER|0||0
	35|Unnamed: 35|TEXT|0||0
	36|Facility Status|TEXT|0||0
	sqlite> 
	
	sqlite> PRAGMA table_info(facilities);
	0|facility_id|TEXT|0||1
	1|facility_name|TEXT|1||0
	2|license_number|TEXT|1||0
	3|facility_address|TEXT|1||0
	4|phone_number|TEXT|0||0
	5|facility_type|TEXT|0||0
	6|operational_schedule|TEXT|0||0
	7|accepts_subsidies|TEXT|0||0
	8|location_id|TEXT|0||0
	9|owner_id|TEXT|0||0
	10|license_id|TEXT|0||0
	11|school_district_id|TEXT|0||0
	sqlite>
	
	
	
	```


-----


old improved [[20250211080249 - old improved]]

[[20250211102748 - old]] - old

# [[20250211083317]] - improved



------



## [[20250211082059 - improved]] - improved
[[20250211103522]]

## **8️⃣ Verify the Relationships in Neo4j**

Run these **test queries** to ensure relationships exist:

### **Check Any Relationships**

```cypher
MATCH ()-[r]->() RETURN COUNT(r);
```

### **Check Facility → Location Links**

```cypher
MATCH (f:Facility)-[:LOCATED_IN]->(l:Location)
RETURN f.name, l.city, l.state, l.zip_code LIMIT 10;
```

### **Check Facility → Owner Links**

```cypher
MATCH (f:Facility)-[:OWNED_BY]->(o:Owner)
RETURN f.name, o.license_number LIMIT 10;
```

### **Check Facility → License Links**

```cypher
MATCH (f:Facility)-[:HAS_LICENSE]->(lic:License)
RETURN f.name, lic.license_number, lic.expiry_date LIMIT 10;
```

### **Check Facility → School District Links**

```cypher
MATCH (f:Facility)-[:PART_OF_DISTRICT]->(sd:SchoolDistrict)
RETURN f.name, sd.name LIMIT 10;
```




---

### **1. Check Existing Nodes and Labels**

This will list all the node labels you have in your database:

```cypher
CALL db.labels();
```

This helps confirm that **Facility** and **Location** nodes exist.

---

### **2. Check Sample Facility and Location Nodes**

Run:

```cypher
MATCH (f:Facility) RETURN f LIMIT 5;
```

```cypher
MATCH (l:Location) RETURN l LIMIT 5;
```

This will show the **properties** stored within Facility and Location nodes.

---

### **3. Find How Facilities and Locations Are Connected**

Check the **relationship** between `Facility` and `Location`:

```cypher
MATCH (f:Facility)-[r]->(l:Location)
RETURN type(r), f, l LIMIT 5;
```

This will tell us:

- The **type of relationship** (e.g., `LOCATED_IN`).
- The **data stored** in `Facility` and `Location`.

---

### **4. Check What’s Stored in Location**

Run this to confirm if `Location` contains **zip codes**:

```cypher
MATCH (l:Location) RETURN l.zip_code, l.city, l.state LIMIT 5;
```

If `zip_code` is found inside `Location`, we need to **query it through relationships**.




## **Query to Cluster Facilities by Zip Code**

Once we confirm that **facilities connect to locations**, we can group facilities by their shared zip codes.

Try:

```cypher
MATCH (f:Facility)-[:LOCATED_IN]->(l:Location)
RETURN l.zip_code, collect(f.name) AS facilities;
```

This will show **which facilities are clustered by zip code**.

------
