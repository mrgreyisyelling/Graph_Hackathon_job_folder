### **🚀 Goal: Newly Created Notes Should Also Generate Triples**

Right now, we **create notes** for new entities, attributes, and values but **don’t generate triples for them**.

Now, we need to make sure **every entity (including auto-created ones)** exists in the **triple representation** of the knowledge graph.

---

## **🔹 What Should an "Empty" Triple Look Like?**

A triple has the form:  
**(Entity, Attribute, Value)**  
Since newly created notes have **no relationships yet**, we still need **a placeholder triple** to show they exist.

### **✅ Empty Triple Format**

If we create a new note for `"Basement"`, it should **at least have a self-reference**:

|**Entity**|**Attribute**|**Value**|
|---|---|---|
|`Basement`|`is_entity`|`Basement`|

This ensures that **Basement exists in the KG**, even before we add relationships.

---

## **🔹 Step 1: Modify `createEntities` to Generate Triples**

We need to **automatically add "self-identity triples"** for every created note.

### **📝 Updated `createEntities`**

Modify `createEntities` in `main.ts`:

```ts
async createEntities(triples: any[]) {
    for (const triple of triples) {
        const entityName = triple.value; // Ensuring values become entities
        const attributeName = triple.attribute; // Ensuring attributes become entities

        // ✅ Create notes for entities (values) & ensure they exist as triples
        await this.ensureEntityNote(entityName);
        await this.addEntityTriple(entityName);

        // ✅ Create notes for attributes & ensure they exist as triples
        await this.ensureEntityNote(attributeName);
        await this.addEntityTriple(attributeName);
    }
}
```

---

## **🔹 Step 2: Implement `addEntityTriple`**

This function **adds a "self-triple" for every entity**.

### **📝 Add This Function in `main.ts`**

```ts
async addEntityTriple(entityName: string) {
    const selfTriple = { entity: entityName, attribute: "is_entity", value: entityName };
    
    // ✅ Check if it already exists to avoid duplicates
    const existingTriples = this.store.getTriples();
    const alreadyExists = existingTriples.some(
        (t) => t.entity === entityName && t.attribute === "is_entity"
    );

    if (!alreadyExists) {
        console.log(`Adding self-triple for ${entityName}`);
        this.store.updateTriples(entityName, [selfTriple]);
        await this.saveTriplesToFile();
    }
}
```

---

## **🔹 Step 3: Expected Behavior**

### **Before Renaming a Note**

```yaml
---
entity: "Hell Gate"
attributes:
  - "Connected to: Basement"
  - "Danger Level: High"
  - "Has Guardian: Cerberus"
  - "Category: Portal"
---
```

### **After Renaming, These Notes Get Created:**

|**Note Name**|**Auto-Generated Content**|
|---|---|
|`Basement.md`|`yaml --- entity: "Basement" attributes: [] ---`|
|`Danger Level.md`|`yaml --- entity: "Danger Level" attributes: [] ---`|
|`High.md`|`yaml --- entity: "High" attributes: [] ---`|
|`Has Guardian.md`|`yaml --- entity: "Has Guardian" attributes: [] ---`|
|`Cerberus.md`|`yaml --- entity: "Cerberus" attributes: [] ---`|
|`Category.md`|`yaml --- entity: "Category" attributes: [] ---`|
|`Portal.md`|`yaml --- entity: "Portal" attributes: [] ---`|

### **Newly Created Triples in `triples.json`**

```json
[
  { "entity": "Hell Gate", "attribute": "Connected to", "value": "Basement" },
  { "entity": "Hell Gate", "attribute": "Danger Level", "value": "High" },
  { "entity": "Hell Gate", "attribute": "Has Guardian", "value": "Cerberus" },
  { "entity": "Hell Gate", "attribute": "Category", "value": "Portal" },
  { "entity": "Basement", "attribute": "is_entity", "value": "Basement" },
  { "entity": "Danger Level", "attribute": "is_entity", "value": "Danger Level" },
  { "entity": "High", "attribute": "is_entity", "value": "High" },
  { "entity": "Has Guardian", "attribute": "is_entity", "value": "Has Guardian" },
  { "entity": "Cerberus", "attribute": "is_entity", "value": "Cerberus" },
  { "entity": "Category", "attribute": "is_entity", "value": "Category" },
  { "entity": "Portal", "attribute": "is_entity", "value": "Portal" }
]
```

---

## **🔹 Step 4: Rebuild and Test**

1. **Rebuild the plugin:**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
2. **Restart Obsidian** and enable the plugin.
3. **Rename a note with YAML** and check if:
    - New notes are created with **YAML frontmatter**.
    - `triples.json` now **contains `is_entity` triples**.

---

### **🚀 What’s Next?**

- **Does this update work as expected?**
- **Should we auto-link "parent" relationships?**
    - Example: `Basement.md` should say `"Part of: [[Hell Gate]]"`
- **Do we start working on a visualization?**

🚀 **Try this out and let me know what’s next!**