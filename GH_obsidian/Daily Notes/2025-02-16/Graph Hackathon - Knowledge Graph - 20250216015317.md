### **🚀 Files We Are Modifying**

To implement **Local Master Control + Merging KG Versions**, we will update the following files:

---

## **1️⃣ `main.ts` (Main Plugin Logic)**

### **✅ What We Are Adding**

- **Tracking `master_version` and `live_version` in YAML.**
- **Preventing direct overwrites of `master_version`.**
- **Adding Obsidian commands for managing versions.**

### **🔹 Modifications**

- **Modify `processFile`** to handle separate `"live_version"` and `"master_version"`.
- **Modify `mergeKnowledgeGraphs`** to ensure merging **does not overwrite master**.
- **Add new commands**:
    - `"set-master-version"` (Allows users to promote `"live_version"` to `"master_version"`).

---

## **2️⃣ `parser.ts` (Extracting Triples)**

### **✅ What We Are Adding**

- Ensuring that all incoming KG data **tracks its version**:
    - `"master_version"` → User-defined
    - `"live_version"` → Merged data

### **🔹 Modifications**

- Update `parseTriples` to **read & extract both master and live versions**.
- Ensure **attributes from external sources are stored in `live_version`**.

---

## **3️⃣ `merge.ts` (Merging KGs Without Overwriting Local Master)**

### **✅ What We Are Adding**

- A **custom merging strategy**:
    - Entities **marked as local master** are **not overwritten**.
    - Instead, **incoming changes are stored under `live_version`**.

### **🔹 Modifications**

- Update `mergeKnowledgeGraphs` to:
    - Detect `"master_version"` fields in an entity.
    - Store conflicting updates as `"live_version"` instead of overwriting.

---

## **4️⃣ YAML in Each Entity’s Markdown (`*.md`)**

### **✅ What We Are Modifying**

- When an entity is processed, we **rewrite its YAML** to track both versions.
    
- **Example: Before Updating**
    
    ```yaml
    ---
    entity: "Hell Gate"
    Connected to: "Basement"
    Danger Level: "High"
    Has Guardian: "Cerberus"
    Category: "Portal"
    ---
    ```
    
- **After Updating**
    
    ```yaml
    ---
    entity: "Hell Gate"
    master_version:
      Connected to: "Basement"
      Danger Level: "High"
      Has Guardian: "Cerberus"
      Category: "Portal"
    live_version:
      Connected to: "Dungeon"
      Danger Level: "Medium"
      Has Guardian: "Minotaur"
      Category: "Underworld"
    ---
    ```
    

---

### **🔹 Full List of Modified Files**

|**File**|**Changes**|
|---|---|
|`main.ts`|Plugin logic, version management, and UI commands|
|`parser.ts`|Extracting & structuring master/live versions|
|`merge.ts`|Preventing local overwrites, merging updates cleanly|
|`*.md` (Obsidian Notes)|YAML changes to track `"master_version"` and `"live_version"`|

---

## **🚀 Next Steps**

- **Do you need a function breakdown for each file?**
- **Would you like a test plan to ensure it’s working properly?**
- **Should we move toward a visualization or review UI inside Obsidian next?**

🚀 **Let me know what you need next!**