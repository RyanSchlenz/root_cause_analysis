import subprocess
import os
import time
from project_config import config

def run_script(script_name):
    """Run a Python script using subprocess."""
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

def delete_files_after_timeout(file_paths, timeout=180):
    """Delete files after a timeout (in seconds)."""
    print(f"Waiting {timeout // 60} minutes before deleting files...")
    time.sleep(timeout)  # Wait for the specified timeout (3 minutes = 180 seconds)

    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"File not found: {file_path}")

def main():
    # Retrieve the list of scripts and files to delete from the config file
    scripts = config['scripts']
    files_to_delete = config['files_to_delete']  # List of files to delete after 3 minutes

    for script in scripts:
        print(f"Running {script}...")
        run_script(script)

    # Delete files after 3 minutes (180 seconds)
    delete_files_after_timeout(files_to_delete, timeout=180)

if __name__ == "__main__":
    main()
