### **🚀 Why is `"isEntity": true` Used in Some Triples?**

The `"isEntity": true` field in the triples is **marking whether the value is an entity**, but **this may not be necessary**.

Let's analyze why it's there and whether we should **keep, modify, or remove it**.

---

### **🔹 What is `"isEntity": true` Doing?**

1. **Marks when a value is an entity rather than plain text.**
    
    - Example:
        
        ```json
        {
          "entity": "Hell Gate",
          "attribute": "has_attribute",
          "value": "Danger Level",
          "isEntity": true
        }
        ```
        
    - This means that **"Danger Level" is treated as an entity** (it gets its own note and relationships).
2. **Helps distinguish between values that are entities vs. literals.**
    
    - Example of a **literal** (which might not need a new note):
        
        ```json
        {
          "entity": "Hell Gate",
          "attribute": "Danger Level",
          "value": "High"
        }
        ```
        
    - Here, `"High"` is just a value, not necessarily an entity.
3. **Ensures we create the right notes in Obsidian.**
    
    - If `"isEntity": true`, we make sure that **Danger Level** gets its own note.

---

### **🔹 Is `"isEntity": true` Actually Needed?**

🔹 **We already create all values as entities**

- **Everything is a note** in Obsidian, whether it's an entity, attribute, or value.
- **If we're treating everything as an entity, then `"isEntity": true"` is redundant.**

🔹 **Better Alternative: Just Store Everything as a Triple**

- Instead of tracking `"isEntity": true`, just **store the relationships normally**.
- **Attributes should always be entities.**

---

### **✅ Fix: Remove `"isEntity": true"`**

Instead of:

```json
{
  "entity": "Hell Gate",
  "attribute": "has_attribute",
  "value": "Danger Level",
  "isEntity": true
}
```

Use:

```json
{
  "entity": "Hell Gate",
  "attribute": "has_attribute",
  "value": "Danger Level"
}
```

---

### **🔹 Step 1: Modify `parseTriples` to Remove `"isEntity": true`**

Edit `parser.ts` so that `"isEntity": true` is no longer included in the output.

```ts
export function parseTriples(content: string): { entity: string; attribute: string; value: string }[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = load(yamlMatch[1]) as any;
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());

            // ✅ Ensure values are standardized (remove [[ ]])
            const cleanValue = value.replace(/^\[\[/, "").replace(/\]\]$/, ""); // Removes [[ ]]

            return [
                { entity, attribute: "has_attribute", value: attribute },
                { entity, attribute, value: cleanValue }
            ];
        }).flat();
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
```

---

### **🔹 Step 2: Rebuild & Test**

4. **Rebuild the plugin**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
5. **Restart Obsidian** and rename a note.
6. **Check `triples.json`** to confirm `"isEntity": true` is **gone**.

---

### **🚀 Next Steps**

- **Does this fix make sense?**
- **Do we need a better way to distinguish attributes vs. values?**
- **What’s next: Graph visualization or querying?**

🚀 **Try this and let me know if it works as expected!**