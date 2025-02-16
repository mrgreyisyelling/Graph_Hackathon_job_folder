### **🚀 Updating the Local Master System: Store Master Status in YAML & Track Changes Separately**

Now, instead of keeping `master_locks.json`, we will:

✅ **Store "Local Master" status inside each entity's YAML**  
✅ **Allow remote changes but mark them as distinct from the "Master Version"**  
✅ **Organize versions in YAML as:**

- `"Local Version"` (User-defined Master)
- `"Live Version"` (Merged from external sources)

---

## **🔹 Step 1: Updating YAML Format for Entities**

Each entity’s note will now have a **structured YAML format**:

```yaml
---
entity: "Hell Gate"
master_version:
  Connected to: "Basement"
  Danger Level: "High"
  Has Guardian: "Cerberus"
  Category: "Portal"
live_version:
  Connected to: "Dungeon"
  Danger Level: "Medium"
  Has Guardian: "Minotaur"
  Category: "Underworld"
---
```

### **🔹 What This Does**

1. **Local Master Version (User-Defined)**
    
    - This is the **trusted source**, modified only by the user.
    - **Never overwritten by merges.**
2. **Live Version (Blockchain or External KG Merge)**
    
    - These are **new incoming updates**, merged but **kept separate**.
    - Users can **see external changes without them overriding the master version**.

---

## **✅ Step 2: Modify `mergeKnowledgeGraphs` to Track Both Versions**

Instead of **overwriting local master entities**, we **store external updates under `live_version`.**

```ts
function mergeKnowledgeGraphs(primaryPath: string, secondaryPath: string, outputPath: string) {
    const primaryData = JSON.parse(fs.readFileSync(primaryPath, "utf8"));
    const secondaryData = JSON.parse(fs.readFileSync(secondaryPath, "utf8"));

    let mergedData: any[] = [];

    primaryData.forEach(triple => {
        const existingTriple = secondaryData.find(t => t.entity === triple.entity && t.attribute === triple.attribute);

        if (!existingTriple) {
            // ✅ If no external version, keep master version as is
            mergedData.push(triple);
        } else if (existingTriple.value !== triple.value) {
            // ✅ Conflict detected! Store external data as "live_version"
            mergedData.push({ 
                entity: triple.entity, 
                attribute: triple.attribute, 
                value: triple.value, 
                version: "master_version" 
            });
            mergedData.push({ 
                entity: triple.entity, 
                attribute: triple.attribute, 
                value: existingTriple.value, 
                version: "live_version" 
            });
        } else {
            // ✅ If they are identical, store only one version
            mergedData.push(triple);
        }
    });

    fs.writeFileSync(outputPath, JSON.stringify(mergedData, null, 2));
    console.log(`Merged knowledge graph saved to ${outputPath}`);
}
```

---

## **✅ Step 3: Modify `processFile` to Check for "Local Master" Status**

When processing a note, we now **extract both "master" and "live" versions**.

```ts
async processFile(file: TFile) {
    if (file.extension === "md") {
        const content = await this.app.vault.read(file);
        const triples = parseTriples(content);

        const masterData = {};
        const liveData = {};

        triples.forEach(triple => {
            if (triple.version === "master_version") {
                masterData[triple.attribute] = triple.value;
            } else if (triple.version === "live_version") {
                liveData[triple.attribute] = triple.value;
            }
        });

        const updatedYaml = `---
entity: "${triples[0].entity}"
master_version:
${Object.entries(masterData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
live_version:
${Object.entries(liveData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
---
`;

        await this.app.vault.modify(file, updatedYaml);
    }
}
```

---

## **🔹 Expected Behavior**

### **Before Merging**

```yaml
---
entity: "Hell Gate"
Connected to: "Basement"
Danger Level: "High"
Has Guardian: "Cerberus"
Category: "Portal"
---
```

### **After Merging**

```yaml
---
entity: "Hell Gate"
master_version:
  Connected to: "Basement"
  Danger Level: "High"
  Has Guardian: "Cerberus"
  Category: "Portal"
live_version:
  Connected to: "Dungeon"
  Danger Level: "Medium"
  Has Guardian: "Minotaur"
  Category: "Underworld"
---
```

---

## **✅ Step 4: Obsidian Commands to Mark an Entity as "Master"**

Users should be able to manually **lock an entity’s version as the local master**.

### **📝 Add Commands to `onload` in `main.ts`**

```ts
this.addCommand({
    id: "set-master-version",
    name: "Set Entity as Master Version",
    callback: async () => {
        const entityName = await this.promptForEntity();
        if (entityName) {
            await this.setMasterVersion(entityName);
        }
    },
});
```

### **📝 Function to Move "Live Version" to "Master Version"**

If the user approves an external update, they can **promote it to their master version**.

```ts
async setMasterVersion(entityName: string) {
    const file = this.app.vault.getAbstractFileByPath(`${entityName}.md`);
    if (!(file instanceof TFile)) return;

    const content = await this.app.vault.read(file);
    const triples = parseTriples(content);

    const masterData = {};
    const liveData = {};

    triples.forEach(triple => {
        if (triple.version === "live_version") {
            masterData[triple.attribute] = triple.value;
        } else if (triple.version === "master_version") {
            masterData[triple.attribute] = triple.value;
        }
    });

    const updatedYaml = `---
entity: "${entityName}"
master_version:
${Object.entries(masterData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
---
`;

    await this.app.vault.modify(file, updatedYaml);
    console.log(`${entityName} has been updated as master version.`);
}
```

---

## **🚀 Final System Summary**

### **1️⃣ When a Merge Happens**

- Any changes **not in the local master** are saved as `"live_version"`.
- Local master stays **unchanged unless manually updated**.

### **2️⃣ When a User Approves a Live Update**

- They run **"Set Entity as Master Version"** from Obsidian.
- `"live_version"` is promoted to `"master_version"`, updating the entity.

### **3️⃣ When a User Edits a Local Entity**

- The **local version remains the source of truth**.
- New edits are only stored in `"master_version"`.

---

## **🚀 Next Steps**

✅ **KG now tracks both local and remote versions inside YAML**.  
✅ **Users can manually approve external changes.**  
✅ **Merging no longer overwrites local data.**

### **What’s Next?**

1️⃣ **Do you want a UI inside Obsidian to display "Live Changes" vs "Master Version"?**  
2️⃣ **Do we need a command to revert a "live update" back to the previous state?**  
3️⃣ **Do we work on visualizing how different versions relate in the knowledge graph?**

🚀 **Let me know what’s next!**