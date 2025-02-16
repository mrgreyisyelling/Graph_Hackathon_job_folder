### **🚀 Start Fresh: Full Reset & Rebuild the Plugin**

Since the plugin **isn’t loading properly**, let's **wipe everything and set it up correctly from scratch**.

---

## **Step 1: Remove the Old Plugin Files**

Since something is misconfigured, **delete the entire plugin folder**:

```sh
rm -rf /home/mike/Documents/Programming/Graph_Hackathon_job_folder/GH_obsidian/.obsidian/plugins/obsidian-triple-extractor
```

Then **recreate the plugin folder**:

```sh
mkdir /home/mike/Documents/Programming/Graph_Hackathon_job_folder/GH_obsidian/.obsidian/plugins/obsidian-triple-extractor
cd /home/mike/Documents/Programming/Graph_Hackathon_job_folder/GH_obsidian/.obsidian/plugins/obsidian-triple-extractor
```

---

## **Step 2: Reinitialize the Plugin (`package.json`)**

Inside the plugin folder, **reinitialize NPM**:

```sh
npm init -y
```

Then **edit `package.json`** and replace it with:

```json
{
  "name": "obsidian-triple-extractor",
  "version": "1.0.0",
  "description": "Extracts triples from YAML frontmatter in Obsidian.",
  "main": "main.js",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "obsidian": "latest"
  },
  "devDependencies": {
    "typescript": "^5.7.3"
  }
}
```

---

## **Step 3: Create `manifest.json`**

Create a **new `manifest.json`**:

```sh
echo '{
  "id": "obsidian-triple-extractor",
  "name": "Obsidian Triple Extractor",
  "version": "1.0.0",
  "minAppVersion": "0.12.0",
  "description": "Extracts triples from YAML frontmatter.",
  "author": "Your Name",
  "authorUrl": "https://your-website.com",
  "isDesktopOnly": false
}' > manifest.json
```

---

## **Step 4: Create `tsconfig.json`**

Run:

```sh
echo '{
  "compilerOptions": {
    "target": "ES6",
    "module": "CommonJS",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*.ts"]
}' > tsconfig.json
```

---

## **Step 5: Create the Plugin Code**

### **🔹 Create the `src/` Folder**

```sh
mkdir src
```

### **🔹 Create `src/main.ts`**

```sh
echo 'import { Plugin, TFile } from "obsidian";
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
}' > src/main.ts
```

---

### **🔹 Create `src/parser.ts`**

```sh
echo 'import { parseYaml } from "obsidian";

export function parseTriples(content: string): { entity: string; attribute: string; value: string }[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = parseYaml(yamlMatch[1]);
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());
            return { entity, attribute, value };
        });
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}' > src/parser.ts
```

---

### **🔹 Create `src/store.ts`**

```sh
echo 'export class KnowledgeGraphStore {
    private triples: Map<string, { entity: string; attribute: string; value: string }[]> = new Map();

    updateTriples(filePath: string, newTriples: { entity: string; attribute: string; value: string }[]): void {
        this.triples.set(filePath, newTriples);
    }

    getTriples(): { entity: string; attribute: string; value: string }[] {
        return Array.from(this.triples.values()).flat();
    }

    clear(): void {
        this.triples.clear();
    }
}' > src/store.ts
```

---

## **Step 6: Install Dependencies**

Run:

```sh
npm install
npm install -D typescript obsidian
```

---

## **Step 7: Build the Plugin**

```sh
npm run build
```

---

## **Step 8: Move Compiled `main.js` to Root**

```sh
cp dist/main.js ./
```

---

## **Step 9: Load the Plugin in Obsidian**

1. Open **Obsidian**.
2. Go to **Settings → Community Plugins**.
3. Click **Load Plugin** and enable `Obsidian Triple Extractor`.
4. **Create a note with this YAML frontmatter**:
    
    ```yaml
    ---
    entity: "Hell Gate"
    attributes:
      - "Connected to: [[Basement]]"
      - "Danger Level: High"
    ---
    ```
    
5. **Rename the note** to trigger the event.
6. **Check the Developer Console (`Ctrl + Shift + I`)**:
    - Look for logs:
        
        ```
        Extracted Triples: [{ entity: 'Hell Gate', attribute: 'Connected to', value: 'Basement' }, ...]
        ```
        

---

## **🎯 What This Does**

✅ **Completely wipes & resets the plugin folder**  
✅ **Ensures correct `package.json`, `manifest.json`, and `tsconfig.json`**  
✅ **Uses a clean TypeScript structure**  
✅ **Ensures `main.js` is in the right place**

🚀 **Try these steps and let me know if it works!**