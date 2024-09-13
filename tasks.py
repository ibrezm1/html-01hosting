from invoke import task, run
import os
import signal
import subprocess
import shutil
import zipfile

# Function to kill Flask and ngrok processes
@task
def kill_processes(c):
    print("Killing existing Flask and ngrok processes...")
    
    # Kill Flask (modify if needed)
    c.run("pkill -f 'python app.py'", warn=True)
    c.run("pkill -f 'flask run'", warn=True)
    
    # Kill ngrok
    c.run("pkill -f 'ngrok'", warn=True)

    print("Killed Flask and ngrok processes.")

# Function to build the Angular (dco-ui) project
@task
def build_angular(c, environment="local"):
    print("Building dco-ui (Angular project)...")
    with c.cd("dco-ui"):
        if environment == "production":
            result = c.run("npx ng build -c production", warn=True)
        else:
            result = c.run("npx ng build", warn=True)

        if result.ok:
            print("dco-ui built successfully.")
        else:
            print("Failed to build dco-ui.")
            raise SystemExit(1)

# Function to move the built Angular files to Flask's static folder
@task
def move_files(c):
    print("Moving dco-ui build files to dco-backend static folder...")

    src_folder = "dco-ui/dist/dco-ui"  # Angular build output folder
    dest_folder = "dco-backend/static"  # Flask static folder

    # Remove existing JS, map, and CSS files
    for file in os.listdir(dest_folder):
        if file.endswith((".js", ".map", ".css", ".txt", ".woff2", ".woff", ".txt")):
            os.remove(os.path.join(dest_folder, file))


    # Remove existing static files if present
    # Move the build files to the destination folder, preserving existing files
    for file in os.listdir(src_folder):
        src_path = os.path.join(src_folder, file)
        dest_path = os.path.join(dest_folder, file)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)

    print(f"Moved files to {dest_folder}.")

# Function to run Flask in the background
@task
def run_flask(c):
    print("Starting dco-backend (Flask server)...")
    # Optional: Print working directory
    subprocess.Popen(["nohup", "python", "app.py"], stdout=open("flask.log", "a"), stderr=subprocess.STDOUT,cwd="./dco-backend")
    print("dco-backend is running.")

# Function to run ngrok in the background
@task
def run_ngrok(c):
    print("Starting ngrok...")
    subprocess.Popen(["nohup", "ngrok", "tunnel", "--label", "edge=edghts_2lwUy4mfaWAK8SElEw2w7pc1fmG", "http://localhost:5000"], stdout=open("ngrok.log", "a"), stderr=subprocess.STDOUT)
    print("ngrok is running.")

def create_zip(zip_name="dco-backend.zip"):
    print(f"Creating ZIP file: {zip_name}")

    with zipfile.ZipFile(zip_name, "w") as zip_ref:
        for root, dirs, files in os.walk("dco-backend"):
            if "__pycache__" in dirs or "venv" in dirs:
                dirs[:] = [d for d in dirs if d not in ["__pycache__", "tvenv"]]
            for file in files:
                zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.getcwd()))

    print(f"ZIP file created in: {zip_name}")

# Main deployment function
@task
def deploy(c, environment="local"):
    kill_processes(c)
    build_angular(c, environment)
    move_files(c)
    create_zip()
    run_flask(c)
    
    if environment == "production":
        run_ngrok(c)

# Usage check and main function call
@task
def main(c, mode="local"):
    if mode not in ["local", "production", "kill"]:
        print("Usage: invoke main --mode=<local|production|kill>")
        raise SystemExit(1)

    if mode == "kill":
        kill_processes(c)
    else:
        deploy(c, environment=mode)

@task
def run_from_zip(c, zip_file="dco-backend.zip"):
    print(f"Unzipping {zip_file}...")

    # Temporary directory to extract the ZIP
    temp_dir = "dco-backend-temp"
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    print("Unzipped files to temporary directory:")
    print(temp_dir)

    # Run Flask from the extracted directory
    with c.cd(temp_dir):
        c.run("nohup python app.py &")

    print("dco-backend is running from the extracted ZIP.")

# edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa
# https://equipped-crab-readily.ngrok-free.app/
# ngrok tunnel --label edge=edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa http://localhost:5000
# 
# $ cat /home/ibrez/.config/ngrok/ngrok.yml
# version: 3
# agent:
#   authtoken: xxxxxxXXXXXXXXXXXX_XXXXXXXXXXXXXXXXXXXX
# ngrok config check
# ngrok tunnel --label edge=edghts_2lnTTHwUtP6DU9BIGjYw9fjKKTa http://localhost:5000

# invoke main --mode=local
# invoke main --mode=production
# invoke main --mode=kill
# invoke main --mode=run-from-zip