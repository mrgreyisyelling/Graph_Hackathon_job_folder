### **How to Test Your Obsidian Plugin**

Now that you have the **code copied** and an **Obsidian note with YAML** ready, follow these steps to **load and test the plugin in Obsidian**.

---

### **Step 1: Set Up Obsidian for Plugin Development**

#### **A. Enable Developer Mode in Obsidian**

1. Open **Obsidian**.
2. Go to **Settings → Community Plugins**.
3. Scroll down and enable **Developer Mode**.
4. Restart Obsidian.

#### **B. Locate the Obsidian Plugins Folder**

1. Navigate to the `.obsidian/plugins/` folder inside your vault.
    - On **Windows**: `C:\Users\YourUsername\ObsidianVault\.obsidian\plugins\`
    - On **Mac/Linux**: `~/ObsidianVault/.obsidian/plugins/`
2. Create a new folder: `obsidian-triple-extractor`
3. Inside `obsidian-triple-extractor`, add these files:
    - `main.ts` (paste the plugin code here)
    - `manifest.json` (metadata file)
    - `styles.css` (if you need UI styling)

---

### **Step 2: Create `manifest.json`**

Obsidian requires a **manifest.json** file. Create this file in your plugin folder (`obsidian-triple-extractor`) with the following content:

```json
{
  "id": "obsidian-triple-extractor",
  "name": "Obsidian Triple Extractor",
  "version": "0.1.0",
  "minAppVersion": "0.12.0",
  "description": "Extracts triples from YAML frontmatter in notes.",
  "author": "Your Name",
  "authorUrl": "https://your-website.com",
  "isDesktopOnly": false
}
```

---

### **Step 3: Install Node.js & Obsidian API**

You'll need **Node.js** to compile the plugin.

#### **A. Install Node.js**

4. [Download Node.js](https://nodejs.org/)
5. Install the **LTS version**.

#### **B. Install Obsidian Plugin Tools**

Open a **terminal/command prompt**, navigate to your plugin folder, and run:

```sh
npm install
npm install -D obsidian
```

This installs Obsidian’s API dependencies.

---

### **Step 4: Build and Load the Plugin**

Run the following command in your plugin directory:

```sh
npm run build
```

Now:

6. Open **Obsidian**.
7. Go to **Settings → Community Plugins**.
8. Click **Load Plugin**.
9. Select `Obsidian Triple Extractor`.
10. Toggle it ON.

---

### **Step 5: Test the Plugin**

#### **A. Add a Note with YAML**

In Obsidian, create a new note and add this YAML:

```yaml
---
entity: "Hell Gate"
type: "Location"
attributes:
  - "Danger Level: High"
  - "Connected to: [[Basement]]"
  - "Story Element: Entrance to the underworld"
---
```

#### **B. Check the Console for Extracted Triples**

11. Press **Ctrl + Shift + I** (**Cmd + Option + I** on Mac) to open Developer Tools.
12. Click on **Console**.
13. If the plugin is working, it should log:

```
Extracted Triple: Hell Gate | Connected to | Basement
Extracted Triple: Hell Gate | Story Element | Entrance to the underworld
```

---

### **Next Steps**

- If this works, I can add a **sidebar UI** in Obsidian to display the triples visually.
- We can then add **syncing to a local KG** before moving to a global one.

**Let me know if this runs successfully!** 🚀