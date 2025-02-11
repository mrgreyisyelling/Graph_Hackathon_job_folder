To understand your current graph structure and relationships, run the following queries in Neo4j and share the results:

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

---

## **Query to Cluster Facilities by Zip Code**

Once we confirm that **facilities connect to locations**, we can group facilities by their shared zip codes.

Try:

```cypher
MATCH (f:Facility)-[:LOCATED_IN]->(l:Location)
RETURN l.zip_code, collect(f.name) AS facilities;
```

This will show **which facilities are clustered by zip code**.

---

### **Next Steps**

1. Run the diagnostic queries above to confirm your structure.
2. Let me know the output, so I can help refine the queries.
3. Once confirmed, we can proceed to **graph clustering** based on location.

Drop the outputs here, and we’ll move to the next step! 🚀