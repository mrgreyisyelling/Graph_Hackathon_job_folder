### **🚀 Next Enhancement: Auto-Generate Links Below YAML on Rename**

Now, we will **automatically insert links to the created entity notes** **below the YAML section** when a note is renamed.

---

## **✅ Steps to Implement**

1. **Detect all extracted entities (attributes + values).**
2. **Modify the note’s content** to **append links** to the detected entities.
3. **Save the updated content back to the note.**

---

## **🔹 Step 1: Modify `processFile` in `main.ts`**

Update the function so it **adds links to related entities** at the bottom of the note.

### **📝 Updated `processFile`**

```ts
async processFile(file: TFile) {
    if (file.extension === "md") {
        const content = await this.app.vault.read(file);
        const triples = parseTriples(content);

        // ✅ Store relationships
        this.store.updateTriples(file.path, triples);
        console.log("Extracted Triples:", triples);

        // ✅ Create placeholder notes for all detected entities
        await this.createEntities(triples);

        // ✅ Add links to extracted entities in the note
        await this.insertEntityLinks(file, content, triples);

        // ✅ Write triples to file
        await this.saveTriplesToFile();
    }
}
```

---

## **🔹 Step 2: Implement `insertEntityLinks`**

Now, we will **add links to the new entities at the bottom of the note**.

### **📝 Add This Function to `main.ts`**

```ts
async insertEntityLinks(file: TFile, content: string, triples: any[]) {
    // Extract entities from the triples
    const linkedEntities = new Set();

    triples.forEach(triple => {
        linkedEntities.add(triple.attribute); // Attributes are now entities
        linkedEntities.add(triple.value);     // Values are also entities
    });

    // Convert to [[WikiLinks]]
    const entityLinks = Array.from(linkedEntities)
        .map(entity => `[[${entity}]]`)
        .join("\n");

    // Check if links already exist to prevent duplicates
    if (content.includes(entityLinks)) {
        console.log(`Entity links already exist in ${file.path}, skipping update.`);
        return;
    }

    // Append links to the bottom of the file
    const updatedContent = `${content.trim()}\n\n## Related Entities\n${entityLinks}`;

    // Write back to the file
    await this.app.vault.modify(file, updatedContent);
    console.log(`Updated ${file.path} with entity links.`);
}
```

---

## **🔹 Expected Behavior**

### **1️⃣ Input YAML in a Markdown File**

Before renaming:

```yaml
---
entity: "Hell Gate"
attributes:
  - "Connected to: [[Basement]]"
  - "Danger Level: [[High]]"
  - "Has Guardian: [[Cerberus]]"
  - "Category: [[Portal]]"
---
```

### **2️⃣ After Renaming, the Note Will Update to:**

```yaml
---
entity: "Hell Gate"
attributes:
  - "Connected to: [[Basement]]"
  - "Danger Level: [[High]]"
  - "Has Guardian: [[Cerberus]]"
  - "Category: [[Portal]]"
---

## Related Entities
[[Connected to]]
[[Danger Level]]
[[Has Guardian]]
[[Category]]
[[Basement]]
[[High]]
[[Cerberus]]
[[Portal]]
```

---

## **🚀 Next Steps**

- **Test this update** by renaming a note with YAML frontmatter.
- **Check if new notes are linked correctly.**
- **Do you want a separate section instead of `## Related Entities`?**

🚀 **Try it out and let me know if it works as expected!**