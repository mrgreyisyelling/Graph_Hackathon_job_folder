### **🚀 Where Does `mergeKnowledgeGraphs` Go?**

The `mergeKnowledgeGraphs` function is responsible for merging two knowledge graphs while ensuring that local **master entities** are not overwritten.

This function should be placed in a **new file** called **`merge.ts`** inside your plugin's `src` directory.

---

## **📂 File Structure After Adding `merge.ts`**

```
/GH_obsidian/.obsidian/plugins/obsidian-triple-extractor/
├── dist/
├── node_modules/
├── src/
│   ├── main.ts          <-- Main plugin logic
│   ├── parser.ts        <-- Extracts triples from YAML
│   ├── merge.ts         <-- ✅ New file for merging KGs
│   ├── store.ts         <-- Stores triples in memory
│   ├── settings.ts      <-- Manages plugin settings
│   ├── view.ts          <-- (Optional) Graph visualization
│   ├── types.ts         <-- (Optional) Defines types
├── package.json
├── package-lock.json
├── manifest.json
```

---

## **📌 How to Add `merge.ts`**

### **1️⃣ Create `src/merge.ts` and Add This Code**

```ts
import fs from "fs";

/**
 * Merges two knowledge graphs while preserving local master entities.
 * - Local master entities remain unchanged.
 * - Conflicting updates are stored under `live_version`.
 */
export function mergeKnowledgeGraphs(primaryPath: string, secondaryPath: string, outputPath: string) {
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

### **2️⃣ Import `mergeKnowledgeGraphs` in `main.ts`**

Now that the function is in `merge.ts`, we need to **call it from `main.ts`** when merging new knowledge graphs.

Modify **`main.ts`**:

```ts
import { mergeKnowledgeGraphs } from "./merge";  // ✅ Import merge logic

// Example usage in Obsidian command
this.addCommand({
    id: "merge-knowledge-graph",
    name: "Merge External Knowledge Graph",
    callback: async () => {
        const primaryPath = "triples.json"; // Local KG
        const secondaryPath = "merged_triples.json"; // External KG
        const outputPath = "triples.json"; // Save merged KG back to primary

        mergeKnowledgeGraphs(primaryPath, secondaryPath, outputPath);
        new Notice("Knowledge Graph merged successfully.");
    },
});
```

---

## **🚀 Next Steps**

✅ **Placed `mergeKnowledgeGraphs` inside `src/merge.ts`.**  
✅ **Imported it into `main.ts` and added an Obsidian command to trigger merging.**

### **Where Do We Go Next?**

1️⃣ **Do we build a UI inside Obsidian to preview "Master" vs "Live" data?**  
2️⃣ **Do we work on visualizing the merged KG?**  
3️⃣ **Do you need logging to see exactly what changed during merging?**

🚀 **Let me know what’s next!**