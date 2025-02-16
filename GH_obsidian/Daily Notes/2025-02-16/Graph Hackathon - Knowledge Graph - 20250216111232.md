### **🚨 Fix: Cannot Find Module `'./parser'`**

The error:

```
Plugin failure: knowledge-graph-plugin Error: Cannot find module './parser'
```

means that **Obsidian can't find `parser.js`** in the compiled plugin.

---

## **✅ Fix 1: Ensure `parser.js` is in the Plugin Folder**

Run:

```sh
ls -l /home/mike/Documents/Programming/Graph_Hackathon_job_folder/GH_obsidian/.obsidian/plugins/knowledge-graph-plugin/
```

You should see:

```
main.js
manifest.json
parser.js
store.js
view.js
```

🔹 **If `parser.js` is missing**, move it from `dist/`:

```sh
cp dist/parser.js ./
```

---

## **✅ Fix 2: Change Import Paths in `main.ts`**

Your `main.ts` **might be importing `parser.ts` incorrectly**.

### **🔹 Edit `src/main.ts`**

Change:

```ts
import { parseTriples } from "./parser";
```

To:

```ts
import { parseTriples } from "parser";
```

Then rebuild:

```sh
npm run build
cp dist/*.js ./
```

---

## **✅ Fix 3: Fully Restart Obsidian**

1. **Disable the plugin** in **Settings → Community Plugins**.
2. **Restart Obsidian completely**.
3. **Enable the plugin again**.

---

### **🚀 Final Steps**

4. **Check if `parser.js` exists.**
5. **Update the import path in `main.ts`.**
6. **Run:**
    
    ```sh
    npm run build
    cp dist/*.js ./
    ```
    
7. **Restart Obsidian** and try again.

🚀 **Try this and let me know what happens!**