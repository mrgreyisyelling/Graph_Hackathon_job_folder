Here’s a **Python script** to automate copying the plugin files from your **development folder** to your **Obsidian plugin testing folder**, and then run the necessary build commands.

### **What This Script Does:**

1. **Copies all files** from your development folder to your Obsidian plugin folder.
2. **Installs dependencies** if needed (`npm install`).
3. **Builds the plugin** (`npm run build`).
4. **Notifies you when it’s done**.

---

### **Python Script (`deploy_obsidian_plugin.py`)**

Save this in **`/home/mike/Documents/Programming/Graph_Hackathon_job_folder/`**, and run it when you want to update your Obsidian plugin.

```python
import os
import shutil
import subprocess

# Define paths
DEV_FOLDER = "/home/mike/Documents/Programming/Graph_Hackathon_job_folder/obsidian_plugin"
OBS_TEST_FOLDER = "/home/mike/Documents/Programming/Graph_Hackathon_job_folder/GH_obsidian/.obsidian/plugins/obsidian-triple-extractor"

# Ensure the destination folder exists
os.makedirs(OBS_TEST_FOLDER, exist_ok=True)

# Copy files from development to testing folder
def copy_plugin_files():
    print(f"Copying files from {DEV_FOLDER} to {OBS_TEST_FOLDER}...")
    
    # Remove existing files in the test plugin folder
    for filename in os.listdir(OBS_TEST_FOLDER):
        file_path = os.path.join(OBS_TEST_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

    # Copy files
    for item in os.listdir(DEV_FOLDER):
        source = os.path.join(DEV_FOLDER, item)
        destination = os.path.join(OBS_TEST_FOLDER, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)

    print("Copy complete.")

# Run npm install and build in the testing folder
def build_plugin():
    print("Installing dependencies and building the plugin...")
    try:
        subprocess.run(["npm", "install"], cwd=OBS_TEST_FOLDER, check=True)
        subprocess.run(["npm", "run", "build"], cwd=OBS_TEST_FOLDER, check=True)
        print("Build successful.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    copy_plugin_files()
    build_plugin()
    print("Deployment complete. Restart Obsidian to load the updated plugin.")
```

---

### **How to Use**

1. **Save the script** as `deploy_obsidian_plugin.py` inside `/home/mike/Documents/Programming/Graph_Hackathon_job_folder/`.
    
2. Open a **terminal** and run:
    
    ```sh
    python3 /home/mike/Documents/Programming/Graph_Hackathon_job_folder/deploy_obsidian_plugin.py
    ```
    
3. The script will:
    
    - Copy files from your **development** folder to your **Obsidian plugin** folder.
    - Run `npm install` (only needed if dependencies change).
    - Build the plugin using `npm run build`.
    - Tell you when it's done.
4. **Restart Obsidian** to load the updated plugin.
    

---

### **Bonus: Make It Even Faster**

If you're frequently updating the plugin, you can add an **alias** in your `~/.bashrc` or `~/.zshrc`:

```sh
alias deploy_obsidian="python3 /home/mike/Documents/Programming/Graph_Hackathon_job_folder/deploy_obsidian_plugin.py"
```

Then, you can just run:

```sh
deploy_obsidian
```

---

This will **eliminate manual copying and building**, making development much faster. 🚀 Let me know if you want any tweaks!