### **🚀 Where Does This Go?**

The `Triple` interface **should be placed in a separate file** inside your `src/` folder, ideally **`types.ts`**, to keep the code modular and reusable.

---

## **📂 Correct File Placement**

```
/GH_obsidian/.obsidian/plugins/obsidian-triple-extractor/
├── dist/
├── node_modules/
├── src/
│   ├── main.ts          <-- Main plugin logic
│   ├── parser.ts        <-- Extracts triples from YAML
│   ├── merge.ts         <-- Merges KG versions
│   ├── store.ts         <-- Stores triples in memory
│   ├── settings.ts      <-- Manages plugin settings
│   ├── view.ts          <-- (Optional) Graph visualization
│   ├── types.ts         <-- ✅ NEW FILE to store TypeScript interfaces
├── package.json
├── package-lock.json
├── manifest.json
```

---

## **✅ Step 1: Create `src/types.ts`**

Inside the `src/` folder, **create a new file** named `types.ts` and add this:

```ts
export interface Triple {
    entity: string;
    attribute: string;
    value: string;
    version?: string;  // Optional because some triples might not have it initially
}
```

---

## **✅ Step 2: Import `Triple` in Other Files**

Now, we need to **import and use `Triple` in the correct files**.

### **Modify `merge.ts`**

At the top of **`merge.ts`**, import the `Triple` interface:

```ts
import { App, TFile, normalizePath } from "obsidian";
import { Triple } from "./types";  // ✅ Import the Triple interface

export async function mergeKnowledgeGraphs(app: App, primaryPath: string, secondaryPath: string, outputPath: string) {
    const primaryFile = app.vault.getAbstractFileByPath(normalizePath(primaryPath));
    const secondaryFile = app.vault.getAbstractFileByPath(normalizePath(secondaryPath));

    if (!(primaryFile instanceof TFile) || !(secondaryFile instanceof TFile)) {
        console.error("Could not find knowledge graph files.");
        return;
    }

    const primaryData: Triple[] = JSON.parse(await app.vault.read(primaryFile));
    const secondaryData: Triple[] = JSON.parse(await app.vault.read(secondaryFile));

    let mergedData: Triple[] = [];

    primaryData.forEach((triple: Triple) => {
        const existingTriple = secondaryData.find((t: Triple) => t.entity === triple.entity && t.attribute === triple.attribute);

        if (!existingTriple) {
            mergedData.push(triple);
        } else if (existingTriple.value !== triple.value) {
            mergedData.push({ entity: triple.entity, attribute: triple.attribute, value: triple.value, version: "master_version" });
            mergedData.push({ entity: triple.entity, attribute: triple.attribute, value: existingTriple.value, version: "live_version" });
        } else {
            mergedData.push(triple);
        }
    });

    const outputFile = app.vault.getAbstractFileByPath(normalizePath(outputPath));
    if (outputFile instanceof TFile) {
        await app.vault.modify(outputFile, JSON.stringify(mergedData, null, 2));
    } else {
        await app.vault.create(normalizePath(outputPath), JSON.stringify(mergedData, null, 2));
    }

    console.log(`Merged knowledge graph saved to ${outputPath}`);
}
```

---

### **Modify `parser.ts`**

At the top of **`parser.ts`**, import `Triple`:

```ts
import { Triple } from "./types";  // ✅ Import the Triple interface

export function parseTriples(content: string): Triple[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = load(yamlMatch[1]) as any;
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());
            const cleanValue = value.replace(/^\[\[/, "").replace(/\]\]$/, ""); // Removes [[ ]]

            return [
                { entity, attribute: "has_attribute", value: attribute, version: "master_version" },
                { entity, attribute, value: cleanValue, version: "live_version" }
            ];
        }).flat();
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
```

---

### **Modify `main.ts` (If Needed)**

If `main.ts` directly manipulates triples, import the type there as well:

```ts
import { Triple } from "./types";  // ✅ Import the Triple interface
```

---

## **🚀 Why This Works Well**

✅ **Centralizes type definitions in `types.ts`, making the code cleaner.**  
✅ **Ensures every file using triples is properly typed.**  
✅ **Prevents `any` errors and keeps TypeScript strict mode happy.**

---

### **🚀 Next Steps**

1️⃣ **Rebuild the Plugin**

```sh
npm run build
cp dist/main.js ./
```

2️⃣ **Restart Obsidian**

- Run the `"Merge External Knowledge Graph"` command.
- Check if `triples.json` stores the `"master_version"` and `"live_version"` properly.

### **What’s Next?**

✅ **Do you want logging to track changes during merging?**  
✅ **Would you like a UI inside Obsidian to preview "Master" vs "Live" data before merging?**  
✅ **Should we visualize the KG structure now that merging is working?**

🚀 **Let me know what you need next!**