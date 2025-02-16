Thanks for uploading `main.ts`. I'll review it now and fix any remaining issues to ensure your plugin builds correctly.

I've reviewed your `main.ts` file. The **main issue** is that `parseYaml` is being used incorrectly. You need to either **use `js-yaml` instead** or import `parseYaml` correctly.

---

### **✅ Fix 1: Remove `parseYaml` and Use `js-yaml`**

Since `parseYaml` is **not built into TypeScript**, it's better to use `js-yaml`.

### **🔹 Updated `main.ts`**

Replace the existing **YAML parsing section** in `main.ts` with this:

```ts
import { Plugin, TFile } from "obsidian";
import { load } from "js-yaml"; // ✅ Use js-yaml instead
import { parseTriples } from "./parser";
import { KnowledgeGraphStore } from "./store";

export default class KnowledgeGraphPlugin extends Plugin {
    private store: KnowledgeGraphStore = new KnowledgeGraphStore();

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

### **✅ Fix 2: Ensure `js-yaml` Types Are Installed**

Run this command in your plugin folder:

```sh
npm install js-yaml
npm install --save-dev @types/js-yaml
```

---

### **🚀 Next Steps**

1. **Replace `main.ts` with the updated version**.
2. **Run:**
    
    ```sh
    npm install js-yaml
    npm install --save-dev @types/js-yaml
    ```
    
3. **Rebuild the plugin:**
    
    ```sh
    npm run build
    ```
    
4. **Restart Obsidian** and try enabling the plugin.

🚀 **Try this and let me know what happens!**