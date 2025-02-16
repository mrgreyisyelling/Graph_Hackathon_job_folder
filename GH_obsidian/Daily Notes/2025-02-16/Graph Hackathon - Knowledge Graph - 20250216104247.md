### **🚀 Next Steps: Testing the Plugin in Obsidian**

Now that the plugin **built successfully**, the next step is to **test it inside Obsidian** and verify that it extracts triples from YAML frontmatter.

---

### **1️⃣ Load the Plugin in Obsidian**

1. **Open Obsidian.**
2. Go to **Settings → Community Plugins**.
3. Scroll down and click **“Load Plugin”**.
4. Find and **enable** `KnowledgeGraphPlugin`.

---

### **2️⃣ Test Triple Extraction**

1. **Create a new Markdown note** and add this YAML frontmatter:
    
    ```yaml
    ---
    entity: "Hell Gate"
    attributes:
      - "Connected to: [[Basement]]"
      - "Danger Level: High"
    ---
    ```
    
2. **Modify or rename the note** (to trigger the event).
3. **Check the Developer Console**:
    - Press **`Ctrl + Shift + I`** (**Cmd + Option + I** on Mac).
    - Click on **Console**.
    - Look for a log message like:
        
        ```
        Extracted Triples: [{ entity: 'Hell Gate', attribute: 'Connected to', value: 'Basement' }, ...]
        ```
        

---

### **3️⃣ Open the Knowledge Graph View**

4. Click **View → More Options (⋮) → Open Triple Knowledge Graph**.
5. You should see a **list of extracted triples**.

---

### **4️⃣ Debug if Needed**

- If triples **don’t appear**, rename or modify the file.
- If nothing logs in the **console**, check if the plugin is enabled.
- If errors appear, paste them here, and I’ll debug.

---

### **5️⃣ Future Steps**

- **Sync the extracted triples to a database.**
- **Integrate a UI to edit triples inside Obsidian.**
- **Allow exporting the Knowledge Graph as JSON or RDF.**

---

🚀 **Try it out and let me know what happens!**