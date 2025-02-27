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