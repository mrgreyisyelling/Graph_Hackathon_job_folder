### **🚨 Fix: `createEntities` Does Not Exist**

The error:

```
TS2339: Property 'createEntities' does not exist on type 'KnowledgeGraphPlugin'.
```

means that **the function `createEntities` is missing or not properly defined in `main.ts`**.

---

## **✅ Fix: Ensure `createEntities` is Defined**

### **🔹 Step 1: Add `createEntities` to `main.ts`**

Make sure this function exists inside your `KnowledgeGraphPlugin` class:

```ts
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

        // ✅ Ensure attributes are also treated as notes
        const attributeFilePath = normalizePath(`${triple.attribute}.md`);
        let attrFile = this.app.vault.getAbstractFileByPath(attributeFilePath);
        if (!attrFile) {
            console.log(`Creating attribute note: ${triple.attribute}`);
            await this.app.vault.create(attributeFilePath, `# ${triple.attribute}\n\n*This attribute was auto-generated.*`);
        }
    }
}
```

---

### **🔹 Step 2: Rebuild and Test**

1. **Rebuild the plugin:**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
2. **Restart Obsidian** and enable the plugin.
3. **Rename a note** with YAML to test if it **correctly creates new entity notes and adds links**.

---

### **🚀 Next Steps**

- **Test if the error disappears** after adding `createEntities`.
- **Check if new notes are created correctly.**
- **Verify that `## Related Entities` is added below the YAML.**

🚀 **Try this and let me know if it works!**