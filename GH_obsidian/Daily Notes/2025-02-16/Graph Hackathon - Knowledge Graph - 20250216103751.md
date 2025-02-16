### **Fixing the Two Errors in `main.ts`**

---

#### **1. Fix "Property 'store' has no initializer"**

**Error:**

```
Property 'store' has no initializer and is not definitely assigned in the constructor.
```

This happens because TypeScript **requires explicit initialization**. Fix it by using **`!` (definite assignment assertion)** or initializing in the constructor.

#### **✅ Fix: Modify `store` Declaration**

Change:

```ts
store: KnowledgeGraphStore;
```

To:

```ts
private store!: KnowledgeGraphStore;
```

or initialize it in the constructor:

```ts
private store: KnowledgeGraphStore = new KnowledgeGraphStore();
```

---

#### **2. Fix `this.app.vault.on("rename", this.processFile.bind(this))`**

**Error:**

```
Argument of type '(file: TFile) => Promise<void>' is not assignable to parameter of type '(file: TAbstractFile, oldPath: string) => any'.
```

This means that `"rename"` events in Obsidian require **two arguments (`file: TAbstractFile, oldPath: string`)**, but `processFile(file: TFile)` only expects one.

#### **✅ Fix: Adjust Event Registration**

Modify this:

```ts
this.registerEvent(this.app.vault.on("rename", this.processFile.bind(this)));
```

To this:

```ts
this.registerEvent(this.app.vault.on("rename", async (file: TAbstractFile, oldPath: string) => {
    if (file instanceof TFile) {
        await this.processFile(file);
    }
}));
```

This ensures **only markdown files (`TFile`) are processed**, fixing the type mismatch.

---

### **🚀 Final Fixed `main.ts`**

```ts
import { App, Plugin, PluginSettingTab, Setting, TFile, TAbstractFile } from "obsidian";
import { parseTriples } from "./parser";
import { KnowledgeGraphStore } from "./store";
import { TripleView, VIEW_TYPE_TRIPLE } from "./view";

export default class KnowledgeGraphPlugin extends Plugin {
    private store!: KnowledgeGraphStore;  // ✅ Fix 1: Ensure store is initialized

    async onload() {
        console.log("Loading Knowledge Graph Plugin");
        this.store = new KnowledgeGraphStore();
        this.addSettingTab(new KnowledgeGraphSettingsTab(this.app, this));

        // ✅ Fix 2: Handle "rename" event with correct types
        this.registerEvent(this.app.vault.on("rename", async (file: TAbstractFile, oldPath: string) => {
            if (file instanceof TFile) {
                await this.processFile(file);
            }
        }));

        this.registerView(VIEW_TYPE_TRIPLE, (leaf) => new TripleView(leaf, this.store));

        await this.loadKnowledgeGraph();
    }

    async processFile(file: TFile) {
        if (file.extension === "md") {
            const content = await this.app.vault.read(file);
            const triples = parseTriples(content);
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

### **🚀 Next Steps**

1. **Replace `main.ts` with the fixed version.**
2. **Run the build again:**
    
    ```sh
    npm run build
    ```
    
3. If errors persist, **paste them here!** 🚀

This should **fully resolve** the issues!