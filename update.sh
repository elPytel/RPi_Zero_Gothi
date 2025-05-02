#!/bin/bash
# This script updates the local repository by pulling the latest changes from the remote repository.
# Optionally installs dependencies and runs the application or restarts the systemd service.
# Usage: ./update.sh [OPTIONS]

DEBUG=false
RUN_AFTER_UPDATE=false
RESTART_SERVICE=false
SERVICE_NAME="rpi_gotchi.service"

print_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help       Show this help message and exit"
    echo "  -d, --debug      Enable debug output"
    echo "  -r, --run        Run application after update (in foreground)"
    echo "  -R, --restart    Restart systemd service after update"
}

log_debug() {
    $DEBUG && echo "DEBUG: $*"
}

run_application() {
    echo "🚀 Starting application..."
    python3 main.py
}

# Check if systemd service exists
service_exists() {
    sudo systemctl list-unit-files | grep -q "^$SERVICE_NAME"
}

# Check if systemd service is active (running)
service_is_active() {
    sudo systemctl is-active --quiet "$SERVICE_NAME"
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
        -R|--restart)
            RESTART_SERVICE=true
            ;;
        *)
            echo "❌ Unknown parameter: $arg"
            exit 1
            ;;
    esac
    shift
done

# --- Stop systemd service if running ---
WAS_ACTIVE=false
if service_exists; then
    log_debug "Service $SERVICE_NAME exists."
    if service_is_active; then
        echo "🛑 Stopping systemd service $SERVICE_NAME before update..."
        sudo systemctl stop "$SERVICE_NAME"
        WAS_ACTIVE=true
    else
        log_debug "Service $SERVICE_NAME is not running."
    fi
else
    log_debug "Systemd service $SERVICE_NAME not found. Skipping service handling."
fi

# --- Main update logic ---
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

# --- Restart systemd service if requested or if it was running ---
if service_exists; then
    if $RESTART_SERVICE; then
        echo "🔄 Restarting systemd service $SERVICE_NAME (forced restart)..."
        sudo systemctl restart "$SERVICE_NAME"
    elif $WAS_ACTIVE; then
        echo "🔄 Restarting systemd service $SERVICE_NAME..."
        sudo systemctl start "$SERVICE_NAME"
    fi
fi

# Run application manually if requested
if $RUN_AFTER_UPDATE; then
    run_application
fi

echo "✅ Update complete."
