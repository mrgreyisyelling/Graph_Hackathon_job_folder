---
entity: Hell Gate
attributes:
  - "Connected to: [[Basement]]"
  - "Danger Level: High"
---
### **🚀 Goal: Store Extracted Triples in a Local File**

We'll **save extracted triples to a JSON file** every time a note is renamed. This lets you **review outputs over multiple tests**.

---

### **✅ Step 1: Modify `main.ts` to Save Triples to a File**

We'll **write the extracted triples to `triples.json`** inside your Obsidian vault.

**🔹 Edit `src/main.ts` and replace `processFile` with this:**

```ts
import { Plugin, TFile, normalizePath } from "obsidian";
import { load } from "js-yaml"; // ✅ Use js-yaml instead
import { parseTriples } from "./parser";
import { KnowledgeGraphStore } from "./store";

export default class KnowledgeGraphPlugin extends Plugin {
    private store: KnowledgeGraphStore = new KnowledgeGraphStore();
    private outputFile = "triples.json"; // ✅ Path for output file

    async onload() {
        console.log("Loading Knowledge Graph Plugin");

        this.registerEvent(this.app.vault.on("rename", async (file) => {
            if (file instanceof TFile) {
                await this.processFile(file);
            }
        }));

        await this.loadKnowledgeGraph();
    }

    async processFile(file: TFile) {
        if (file.extension === "md") {
            const content = await this.app.vault.read(file);
            
            // ✅ Use js-yaml to parse YAML
            const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
            if (!yamlMatch) return;

            const yamlData = load(yamlMatch[1]) as any;

            const triples = parseTriples(content);
            this.store.updateTriples(file.path, triples);
            console.log("Extracted Triples:", triples);

            // ✅ Write triples to a file
            await this.saveTriplesToFile();
        }
    }

    async saveTriplesToFile() {
        const path = normalizePath(this.outputFile);
        const storedTriples = this.store.getTriples();

        // ✅ Convert to JSON
        const jsonData = JSON.stringify(storedTriples, null, 2);

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

    async loadKnowledgeGraph() {
        const files = this.app.vault.getMarkdownFiles();
        for (const file of files) {
            await this.processFile(file);
        }
    }

    onunload() {
        console.log("Unloading Knowledge Graph Plugin");
    }
}
```

---

### **✅ Step 2: Rebuild and Test**

1. **Rebuild the plugin:**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
2. **Restart Obsidian** and enable the plugin.
3. **Create a note with this YAML:**
    
    ```yaml
    ---
    entity: "Hell Gate"
    attributes:
      - "Connected to: [[Basement]]"
      - "Danger Level: High"
    ---
    ```
    
4. **Rename the note** to trigger the event.
5. **Check `triples.json` inside your vault.**
    - Open `triples.json` in Obsidian or a text editor.
    - It should contain:
        
        ```json
        [
          { "entity": "Hell Gate", "attribute": "Connected to", "value": "[[Basement]]" },
          { "entity": "Hell Gate", "attribute": "Danger Level", "value": "High" }
        ]
        ```
        

---

### **✅ Step 3: Debugging (If Needed)**

- If `triples.json` **doesn't appear**, check **Obsidian's Developer Console** (`Ctrl + Shift + I` → Console).
- If an error appears, **paste it here, and I'll debug**.

---

### **🚀 Next Steps**

- **Does this work as expected?**
- **Do you want to append data instead of overwriting the file?**
- **What’s next after logging the triples?** (Visualization? Exporting to RDF?)

🚀 **Try it out and let me know what happens!**

## Related Entities
[[Connected to]]
[[[[Basement]]]]
[[Danger Level]]
[[High]]