### **🚨 Issues in the `triples.json` Output**

Looking at the extracted triples, we have a few **issues to fix**:

---

### **🛑 Issue 1: Duplicate Triples**

Example:

```json
{
  "entity": "Hell Gate",
  "attribute": "Connected to",
  "value": "Basement"
},
{
  "entity": "Hell Gate",
  "attribute": "Connected to",
  "value": "Basement"
},
{
  "entity": "Hell Gate",
  "attribute": "Connected to",
  "value": "[[Basement]]"
}
```

- **Problem:** The same relationship appears **multiple times**.
- **Fix:** Ensure that triples are **not duplicated** before adding them.

---

### **🛑 Issue 2: `[[]]` Wrapped Values**

Example:

```json
{
  "entity": "Hell Gate",
  "attribute": "Connected to",
  "value": "[[Basement]]"
}
```

- **Problem:** Some values have `[[WikiLinks]]` while others don’t.
- **Fix:** Ensure **only one format** is used.

---

### **🛑 Issue 3: `is_entity` Triples for `[[WikiLinks]]`**

Example:

```json
{
  "entity": "[[Basement]]",
  "attribute": "is_entity",
  "value": "[[Basement]]"
}
```

- **Problem:** Entities are stored **with** and **without** `[[WikiLinks]]`, leading to duplicates.
- **Fix:** **Standardize entity names** (no `[[WikiLinks]]` in `triples.json`).

---

## **✅ Fixing These Issues in `main.ts`**

### **🔹 Step 1: Prevent Duplicates**

Modify **`addEntityTriple`** to avoid adding the same entity multiple times.

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

### **🔹 Step 2: Standardize Entity Names (Remove `[[WikiLinks]]`)**

Modify **`parseTriples`** in `parser.ts`:

```ts
export function parseTriples(content: string): { entity: string; attribute: string; value: string, isEntity: boolean }[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = load(yamlMatch[1]) as any;
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());

            // ✅ Ensure attributes are also treated as entities
            const isAttributeEntity = true;

            // ✅ Ensure values are standardized (remove [[ ]])
            const isValueEntity = true;
            const cleanValue = value.replace(/^\[\[/, "").replace(/\]\]$/, ""); // Removes [[ ]]

            return [
                { entity, attribute: "has_attribute", value: attribute, isEntity: isAttributeEntity },
                { entity, attribute, value: cleanValue, isEntity: isValueEntity }
            ];
        }).flat();
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
```

---

### **🔹 Step 3: Remove Duplicates Before Saving**

Modify **`saveTriplesToFile`** to filter out duplicate triples:

```ts
async saveTriplesToFile() {
    const path = normalizePath(this.outputFile);
    let storedTriples = this.store.getTriples();

    // ✅ Remove duplicate triples
    const uniqueTriples = Array.from(new Set(storedTriples.map(JSON.stringify))).map(JSON.parse);

    // ✅ Convert to JSON
    const jsonData = JSON.stringify(uniqueTriples, null, 2);

    // ✅ Write to a local file in Obsidian
    try {
        let file = this.app.vault.getAbstractFileByPath(path);
        if (file instanceof TFile) {
            await this.app.vault.modify(file, jsonData);
        } else {
            await this.app.vault.create(path, jsonData);
        }
        console.log(`Triples saved to ${path}`);
    } catch (err) {
        console.error("Failed to save triples:", err);
    }
}
```

---

## **🔹 Step 4: Expected Fixed Output**

### **✅ `triples.json` After Fix**

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

### **🔹 What’s Fixed?**

✅ **No more duplicate triples**  
✅ **No more `[[WikiLinks]]` inside `triples.json`**  
✅ **No extra `"Connected to"` and `"is_entity"` duplicates**

---

### **🚀 Next Steps**

1. **Rebuild & Test**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
2. **Verify `triples.json` is now correct.**
3. **Decide the next step:**
    - Do we **start working on a visualization**?
    - Do we **build a way to query this knowledge graph?**

🚀 **Try this and let me know if `triples.json` looks clean now!**