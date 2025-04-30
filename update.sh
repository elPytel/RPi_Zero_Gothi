#!/bin/bash
# This script updates the local repository by pulling the latest changes from the remote repository.
# And installs any new dependencies if needed.
# Usage: ./update.sh

git pull
if [ $? -ne 0 ]; then
    echo "Error: Failed to pull the latest changes from the remote repository."
    exit 1
fi
echo "Successfully pulled the latest changes from the remote repository."

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install pip to continue."
    exit 1
fi

# run install.sh
if [ -f install.sh ]; then
    chmod +x install.sh
    ./install.sh
    if [ $? -ne 0 ]; then
        echo "Error: Failed to run install.sh."
        exit 1
    fi
else
    echo "install.sh not found. Skipping installation of dependencies."
fi
echo "Successfully installed dependencies."