### **🚀 Next Step: Turning Attributes & Values into Entities**

You're absolutely right—**attributes and values should be treated as entities (notes) themselves** so we can see relationships clearly.

---

### **🔹 What Needs to Change?**

1. **Right now:**
    
    - The **Entity** (`Hell Gate`) is stored as a **main entity**.
    - The **Attribute** (`Connected to`) is stored as a **relationship type**.
    - The **Value** (`[[Basement]]`) is stored as **text**.
    - ❌ **Problem:** **Basement** isn’t treated as an entity, just as a value.
2. **New Approach:**
    
    - **Every "value" that is a `[[WikiLink]]` should also be an entity.**
    - **Attributes become edges** between entities.
    - **This turns our data into a full Knowledge Graph!**

---

### **✅ Updated Triple Format**

Instead of treating values as plain text, we convert them into **entities and edges**.

#### **Example: YAML Input**

```yaml
---
entity: "Hell Gate"
attributes:
  - "Connected to: [[Basement]]"
  - "Danger Level: High"
  - "Has Guardian: [[Cerberus]]"
---
```

#### **Becomes This Knowledge Graph:**

|Entity|Attribute|Related Entity|
|---|---|---|
|**Hell Gate**|Connected to|**Basement**|
|**Hell Gate**|Danger Level|"High" (Literal)|
|**Hell Gate**|Has Guardian|**Cerberus**|
|**Basement**|(Implicit)|Exists as an Entity|
|**Cerberus**|(Implicit)|Exists as an Entity|

---

### **🛠️ How Do We Implement This?**

1. **Modify `parseTriples` to detect `[[WikiLinks]]` and treat them as entities.**
2. **Update `triples.json` to include all detected entities.**
3. **(Optional) Create empty notes for new entities (Basement, Cerberus).**
4. **(Future) Use this structure for visualization.**

---

### **🔹 Step 1: Update `parser.ts` to Extract Entities from `[[WikiLinks]]`**

Modify `src/parser.ts` to detect `[[WikiLinks]]` and treat them as related entities.

```ts
import { load } from "js-yaml";

/**
 * Parses YAML frontmatter to extract triples (Entity, Attribute, Value).
 */
export function parseTriples(content: string): { entity: string; attribute: string; value: string, isEntity: boolean }[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = load(yamlMatch[1]) as any;
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());
            
            // ✅ Detect WikiLinks (New Entities)
            const isEntity = value.startsWith("[[") && value.endsWith("]]");
            const cleanValue = isEntity ? value.slice(2, -2) : value; // Remove [[ ]]
            
            return { entity, attribute, value: cleanValue, isEntity };
        });
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
```

---

### **🔹 Step 2: Modify `main.ts` to Store Relationships**

Update `src/main.ts` so we store **entities separately** and mark connections.

```ts
import { Plugin, TFile, normalizePath } from "obsidian";
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
            const triples = parseTriples(content);
            
            // ✅ Store entities and relationships
            this.store.updateTriples(file.path, triples);
            console.log("Extracted Triples:", triples);

            // ✅ Create placeholder notes for new entities
            await this.createEntities(triples);

            // ✅ Write triples to file
            await this.saveTriplesToFile();
        }
    }

    async createEntities(triples: any[]) {
        for (const triple of triples) {
            if (triple.isEntity) {
                const entityFilePath = normalizePath(`${triple.value}.md`);
                
                let file = this.app.vault.getAbstractFileByPath(entityFilePath);
                if (!file) {
                    console.log(`Creating entity note: ${triple.value}`);
                    await this.app.vault.create(entityFilePath, `# ${triple.value}\n\n*This entity was auto-generated.*`);
                }
            }
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

### **🚀 What This Update Does**

1. ✅ **Detects `[[WikiLinks]]` and treats them as entities.**
2. ✅ **Stores relationships between entities in `triples.json`.**
3. ✅ **Auto-generates placeholder notes for new entities (`Basement.md`, `Cerberus.md`).**

---

### **📌 Next Steps: What’s After This?**

Now that **relationships are stored as entities**, we can:

4. **Visualize the Knowledge Graph**
    
    - Use **Obsidian's Graph View** to display entity links.
    - Integrate **D3.js or Cytoscape.js** for a dynamic view.
5. **Enable Searching for Entities & Relations**
    
    - Build an **interactive sidebar** to query triples.
    - Let users **edit relationships in the UI**.
6. **Export Data for External Use**
    
    - Convert to **RDF/SPARQL for semantic web tools**.
    - Sync with **The Graph (Web3)** for decentralized storage.

---

### **🚀 Next Step: What Do You Want to Focus On?**

- **Do you want to test this update first?**
- **Should we build a simple UI next?** (For searching entities/relationships)
- **Do you want to focus on visualization?** (Graph view, nodes & edges)

🚀 **Try this update and let me know what’s next!**