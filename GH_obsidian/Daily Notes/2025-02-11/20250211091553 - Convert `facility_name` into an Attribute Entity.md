### **Step 1: Convert `facility_name` into an Attribute Entity**

We will **extract `facility_name` from `Facility` and `Location`**, create an **`Attribute` entity** for the name, and **link both Facility and Location to this shared attribute**.

---

### **💡 Cypher Query for Conversion**

```cypher
// Step 1: Create Attribute Entity for Facility Names
MATCH (f:Facility)
MERGE (attr:Attribute {name: "facility_name"})
MERGE (val:Value {value: f.name})
MERGE (attr)-[:OF_VALUE]->(val)
MERGE (f)-[:HAS]->(attr)
MERGE (f)-[:OF_VALUE]->(val);
```

✅ **This does the following:**

- Creates a **single `Attribute` node** with `{name: "facility_name"}`.
- Creates **a `Value` node** for each **unique facility name**.
- Links **Facilities to the Attribute and Value**.

---

### **💡 Link `Location` to the Same Attribute and Value**

```cypher
// Step 2: Link Locations to the Same Facility Name Attribute and Value
MATCH (l:Location)
MERGE (attr:Attribute {name: "facility_name"})
MERGE (val:Value {value: l.facility_name})
MERGE (attr)-[:OF_VALUE]->(val)
MERGE (l)-[:HAS]->(attr)
MERGE (l)-[:OF_VALUE]->(val);
```

✅ **This ensures:**

- `Facility` and `Location` **share the same Attribute (`facility_name`)**.
- If they have the same name, they **connect to the same `Value` node**.
- **Future entities** (e.g., `Owners`, `Schools`) can reference the same structure.

---

### **🔍 Verify the Structure**

```cypher
MATCH (e)-[:HAS]->(a:Attribute)-[:OF_VALUE]->(v:Value)
RETURN e, a, v LIMIT 10;
```

This will show **entities (`Facility`, `Location`)**, the **Attribute (`facility_name`)**, and their **shared values**.

---

### **🚀 Next Steps**

1. **Run the queries** in Neo4j.
2. **Check for shared facility names** using:
    
    ```cypher
    MATCH (f:Facility)-[:OF_VALUE]->(v:Value)<-[:OF_VALUE]-(l:Location)
    RETURN f, l, v;
    ```
    
    This will return **facilities and locations with the same name**.
3. **Do you want to apply this structure to other attributes (e.g., address, zip code)?**

Let me know how you want to proceed! 🚀