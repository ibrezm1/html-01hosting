#!/bin/bash

# Function to kill any running Flask or ngrok processes
kill_processes() {
    echo "Killing existing Flask and ngrok processes..."
    
    # Kill Flask (assuming Flask is run with 'python' or 'flask')
    pkill -f "python app.py"  # Modify to match your Flask entry point
    pkill -f "flask run"

    # Kill ngrok
    pkill -f "ngrok"

    echo "Killed Flask and ngrok processes."
}

# Function to build Angular (dco-ui)
build_angular() {
    echo "Building dco-ui (Angular project)..."
    cd dco-ui || exit
    
    # Check if deploying to production or local
    if [ "$1" == "production" ]; then
        npx ng build -c production
    else
        npx ng build
    fi

    if [ $? -eq 0 ]; then
        echo "dco-ui built successfully."
    else
        echo "Failed to build dco-ui." >&2
        exit 1
    fi
    cd ..
}

# Function to move built Angular files to the Flask (dco-backend) static folder
move_files() {
    echo "Moving dco-ui build files to dco-backend static folder..."

    # Replace with the correct paths
    SRC_FOLDER="dco-ui/dist/dco-ui"  # Angular build output folder
    DEST_FOLDER="dco-backend/static"  # Flask static folder

    # Remove existing static files if present
    if [ -d "$DEST_FOLDER" ]; then
        rm -rf "$DEST_FOLDER"
    fi

    # Move new build files to Flask
    mv "$SRC_FOLDER" "$DEST_FOLDER"

    echo "Moved files to $DEST_FOLDER."
}

# Function to start Flask (dco-backend)
run_flask() {
    echo "Starting dco-backend (Flask server)..."
    # Navigate to dco-backend and run Flask in the background
    cd dco-backend || exit
    nohup python app.py > flask.log 2>&1 &
    echo "dco-backend is running."
    cd ..
}

# Function to start ngrok
run_ngrok() {
    echo "Starting ngrok..."
    # Running ngrok in the background
    nohup ngrok tunnel --label edge=edghts_2lwUy4mfaWAK8SElEw2w7pc1fmG http://localhost:5000 > ngrok.log 2>&1 &
    echo "ngrok is running."
}

# Main deployment function
deploy() {
    kill_processes
    build_angular "$1"
    move_files
    run_flask
    
    if [ "$1" == "production" ]; then
        run_ngrok
    fi
}

# Check for command-line argument
if [ "$#" -ne 1 ] || { [ "$1" != "local" ] && [ "$1" != "production" ]; }; then
    echo "Usage: $0 <local|production>"
    exit 1
fi

# Execute the deployment process
deploy "$1"



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