### **🚨 Fix: `Cannot find module 'js-yaml'`**

This error means **Obsidian can't find the `js-yaml` package** because it's not bundled properly.

---

## **✅ Step 1: Install `js-yaml` Again**

In your plugin folder, **run this command** to ensure `js-yaml` is installed:

```sh
npm install js-yaml
```

---

## **✅ Step 2: Bundle `js-yaml` with Webpack**

By default, Obsidian **doesn't support `require()` for external modules** unless they are bundled. The best way to fix this is **using Webpack**.

### **1️⃣ Install Webpack and Required Packages**

Run:

```sh
npm install --save-dev webpack webpack-cli ts-loader
```

---

### **2️⃣ Create `webpack.config.js`**

In your plugin folder, **create a `webpack.config.js` file**:

```sh
echo 'const path = require("path");

module.exports = {
  entry: "./src/main.ts",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "main.js",
    libraryTarget: "commonjs",
  },
  mode: "production",
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [".ts", ".js"],
  },
  externals: {
    obsidian: "commonjs obsidian",
  },
};' > webpack.config.js
```

---

### **3️⃣ Update `package.json` to Use Webpack**

Open `package.json` and replace the `"scripts"` section:

```json
"scripts": {
  "build": "webpack"
}
```

---

### **4️⃣ Rebuild the Plugin with Webpack**

Now, **rebuild the plugin using Webpack**:

```sh
npm run build
```

Then copy the compiled file:

```sh
cp dist/main.js ./
```

---

## **✅ Step 3: Restart Obsidian**

1. **Disable the plugin** in **Settings → Community Plugins**.
2. **Restart Obsidian completely**.
3. **Enable the plugin again.**

---

### **🚀 Final Steps**

4. **Run:**
    
    ```sh
    npm install js-yaml
    npm install --save-dev webpack webpack-cli ts-loader
    ```
    
5. **Create `webpack.config.js`** (see above).
6. **Update `package.json` to use Webpack**.
7. **Rebuild with Webpack:**
    
    ```sh
    npm run build
    cp dist/main.js ./
    ```
    
8. **Restart Obsidian and enable the plugin.**

---

🚀 **Try this and let me know if it works!**