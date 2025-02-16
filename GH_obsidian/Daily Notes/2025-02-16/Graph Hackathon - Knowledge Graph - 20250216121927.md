### **🚀 Next Step: Auto-Generate a Basic YAML Structure for Each New Note**

Now, every time a new note is created (for an entity, attribute, or value), we’ll add a **default YAML structure** so it follows a consistent format.

---

## **🔹 What Should the Default YAML Look Like?**

For each new note, we want to **automatically insert**:

```yaml
---
entity: "<Entity Name>"
attributes: []
---
```

- **`entity:`** The note’s name
- **`attributes:`** An empty list for relationships

---

## **✅ Step 1: Modify `createEntities` in `main.ts`**

Modify `createEntities` so every **new note includes default YAML**.

### **📝 Updated `createEntities`**

```ts
async createEntities(triples: any[]) {
    for (const triple of triples) {
        const entityName = triple.value; // Ensuring values become entities
        const attributeName = triple.attribute; // Ensuring attributes become entities

        // ✅ Create notes for entities (values)
        await this.ensureEntityNote(entityName);

        // ✅ Create notes for attributes
        await this.ensureEntityNote(attributeName);
    }
}

/**
 * Ensures a note exists for a given entity or attribute.
 * If it doesn’t exist, creates it with a default YAML frontmatter.
 */
async ensureEntityNote(entityName: string) {
    const entityFilePath = normalizePath(`${entityName}.md`);
    let file = this.app.vault.getAbstractFileByPath(entityFilePath);

    if (!file) {
        console.log(`Creating entity note: ${entityName}`);
        const defaultYaml = `---\nentity: "${entityName}"\nattributes: []\n---\n\n`;
        await this.app.vault.create(entityFilePath, defaultYaml);
    }
}
```

---

## **🔹 Expected Behavior**

### **1️⃣ Input YAML in a Note**

Before renaming:

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

---

### **2️⃣ After Renaming, the Plugin Will Create These Notes:**

|**File Name**|**Auto-Generated Content**|
|---|---|
|`Basement.md`|`yaml --- entity: "Basement" attributes: [] ---`|
|`Danger Level.md`|`yaml --- entity: "Danger Level" attributes: [] ---`|
|`High.md`|`yaml --- entity: "High" attributes: [] ---`|
|`Has Guardian.md`|`yaml --- entity: "Has Guardian" attributes: [] ---`|
|`Cerberus.md`|`yaml --- entity: "Cerberus" attributes: [] ---`|
|`Category.md`|`yaml --- entity: "Category" attributes: [] ---`|
|`Portal.md`|`yaml --- entity: "Portal" attributes: [] ---`|

---

## **✅ Step 2: Rebuild and Test**

1. **Rebuild the plugin:**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
2. **Restart Obsidian** and enable the plugin.
3. **Rename a note with YAML** and check if:
    - New notes are created.
    - Each new note has **default YAML**.

---

## **🚀 Next Steps**

4. **Test if all new entity/attribute notes have proper YAML.**
5. **If it works, do we want to auto-add relationships in these notes?**
    - Example: Should `Basement.md` get an entry saying `"Part of: [[Hell Gate]]"`?

🚀 **Try it out and let me know what’s next!**