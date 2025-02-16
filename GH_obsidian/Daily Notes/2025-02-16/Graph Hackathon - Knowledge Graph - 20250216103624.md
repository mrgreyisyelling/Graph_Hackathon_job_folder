Your existing `main.ts` is well-structured, but it needs **two key fixes** to prevent build errors:

### **Key Fixes:**

1. **Change the `"modify"` event** → `"modify"` is no longer valid in the Obsidian API.
    
    - Replace:
        
        ```ts
        this.registerEvent(this.app.vault.on("modify", this.processFile.bind(this)));
        ```
        
    - With:
        
        ```ts
        this.registerEvent(this.app.vault.on("rename", this.processFile.bind(this)));
        ```
        
2. **Ensure `store.ts` has an `updateTriples` function** → The current code calls `this.store.updateTriples(file.path, triples)`, but `store.ts` may not have `updateTriples`.
    

---

### **✅ Updated `main.ts` with Fixes**

```ts
import { App, Plugin, PluginSettingTab, Setting, TFile } from "obsidian";
import { parseTriples } from "./parser";
import { KnowledgeGraphStore } from "./store";
import { TripleView, VIEW_TYPE_TRIPLE } from "./view";

export default class KnowledgeGraphPlugin extends Plugin {
    store: KnowledgeGraphStore;

    async onload() {
        console.log("Loading Knowledge Graph Plugin");
        this.store = new KnowledgeGraphStore();
        this.addSettingTab(new KnowledgeGraphSettingsTab(this.app, this));
        
        // ✅ FIX: Replace "modify" with "rename" to match latest Obsidian API
        this.registerEvent(this.app.vault.on("rename", this.processFile.bind(this)));

        this.registerView(VIEW_TYPE_TRIPLE, (leaf) => new TripleView(leaf, this.store));

        await this.loadKnowledgeGraph();
    }

    async processFile(file: TFile) {
        if (file.extension === "md") {
            const content = await this.app.vault.read(file);
            const triples = parseTriples(content);
            
            // ✅ FIX: Ensure `store.ts` has `updateTriples`
            this.store.updateTriples(file.path, triples);
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

class KnowledgeGraphSettingsTab extends PluginSettingTab {
    plugin: KnowledgeGraphPlugin;

    constructor(app: App, plugin: KnowledgeGraphPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display() {
        const { containerEl } = this;
        containerEl.empty();

        new Setting(containerEl)
            .setName("Knowledge Graph Settings")
            .setDesc("Configure how the plugin processes knowledge graphs.")
            .addToggle(toggle => toggle
                .setValue(true)
                .onChange(async (value) => {
                    console.log("Settings updated: ", value);
                }));
    }
}
```

---

### **✅ Update `store.ts` to Add `updateTriples`**

If `store.ts` does **not** have `updateTriples`, add this:

```ts
export class KnowledgeGraphStore {
    private triples: Map<string, { entity: string; attribute: string; value: string }[]> = new Map();

    /**
     * Updates triples for a specific file path.
     */
    updateTriples(filePath: string, newTriples: { entity: string; attribute: string; value: string }[]): void {
        this.triples.set(filePath, newTriples);
    }

    /**
     * Retrieves all stored triples.
     */
    getTriples(): { entity: string; attribute: string; value: string }[] {
        return Array.from(this.triples.values()).flat();
    }

    /**
     * Clears the knowledge graph store.
     */
    clear(): void {
        this.triples.clear();
    }
}
```

---

### **🚀 Next Steps**

1. Replace `main.ts` and `store.ts` with the **fixed versions** above.
2. Run:
    
    ```sh
    npm run build
    ```
    
3. If you get **new errors**, paste them here!

These fixes should **eliminate the API error and module issues**. 🚀 Let me know how it goes!