#!/bin/bash
# This script updates the local repository by pulling the latest changes from the remote repository.
# Optionally installs dependencies and runs the application.
# Usage: ./update.sh [OPTIONS]

DEBUG=false
RUN_AFTER_UPDATE=false

print_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help      Show this help message and exit"
    echo "  -d, --debug     Enable debug output"
    echo "  -r, --run       Run application after update"
}

log_debug() {
    $DEBUG && echo "DEBUG: $*"
}

run_application() {
    echo "🚀 Starting application..."
    python3 main.py
}

# --- Argument parsing ---
if [ $# -eq 0 ]; then
    print_help
    exit 2
fi

while [[ $# -gt 0 ]]; do
    arg=$1

    case $arg in
        -h|--help)
            print_help
            exit 0
            ;;
        -d|--debug)
            DEBUG=true
            ;;
        -r|--run)
            RUN_AFTER_UPDATE=true
            ;;
        *)
            echo "❌ Unknown parameter: $arg"
            exit 1
            ;;
    esac
    shift
done

# --- Main logic ---

log_debug "Running git pull..."
git pull
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to pull the latest changes from the remote repository."
    exit 1
fi
echo "✅ Successfully pulled the latest changes."

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip could not be found. Please install pip to continue."
    exit 1
fi

# Run install.sh if present
if [ -f install.sh ]; then
    log_debug "Running install.sh..."
    ./install.sh
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to run install.sh."
        exit 1
    fi
    echo "✅ Successfully installed dependencies."
else
    echo "ℹ️  install.sh not found. Skipping installation of dependencies."
fi

# Run application if requested
if $RUN_AFTER_UPDATE; then
    run_application
fi
