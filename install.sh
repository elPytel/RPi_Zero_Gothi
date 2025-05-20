#!/bin/bash
# By Pytel - Install script with systemd service setup

SERVICE_NAME="rpi_gotchi.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
python_dependencies="requirements.txt"
apt_dependencies="apt_dependencies.txt"
apk_dependencies="apk_dependencies.txt"

echo "🔧 Starting installation..."

install_apt_deps() {
    if [ -f "$apt_dependencies" ]; then
        echo "📦 Installing APT dependencies from $apt_dependencies..."
        xargs sudo apt-get -y install < "$apt_dependencies"
    else
        echo "ℹ️ No $apt_dependencies found. Skipping APT install."
    fi
}

install_apk_deps() {
    if [ -f "$apk_dependencies" ]; then
        echo "📦 Installing APK dependencies from $apk_dependencies..."
        xargs sudo apk add < "$apk_dependencies"
    else
        echo "ℹ️ No $apk_dependencies found. Skipping APK install."
    fi
}

# --- Detect package manager and install dependencies ---
if command -v apt-get >/dev/null 2>&1; then
    echo "🟢 Detected apt-get package manager."
    install_apt_deps
elif command -v apk >/dev/null 2>&1; then
    echo "🟢 Detected apk package manager."
    install_apk_deps
else
    echo "❌ No supported package manager found (apt-get or apk)."
    exit 1
fi

# --- Install python dependencies ---
if [ -f "$python_dependencies" ]; then
    echo "🐍 Installing Python dependencies from $python_dependencies..."
    pip install -r "$python_dependencies"
else
    echo "ℹ️ No $python_dependencies found. Skipping Python install."
fi

# --- Create or update systemd service ---
echo "🛠️ Setting up systemd service: $SERVICE_NAME"

SERVICE_CONTENT="[Unit]
Description=Raspberry Pi Gotchi Application
After=network.target

[Service]
ExecStart=/usr/bin/python3 $(pwd)/main.py
WorkingDirectory=$(pwd)
Restart=on-failure
StandardOutput=journal+console
StandardError=journal+console
User=$USER

[Install]
WantedBy=multi-user.target
"

echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_PATH" > /dev/null

# --- Reload systemd daemon and enable service ---
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "✅ Service file created/updated at $SERVICE_PATH"

# Optional: enable service to auto-start on boot
echo "⚙️ Enabling service to start on boot..."
sudo systemctl enable "$SERVICE_NAME"

echo "🎉 Done! You can control your service with:"
echo "   sudo systemctl start $SERVICE_NAME"
echo "   sudo systemctl stop $SERVICE_NAME"
echo "   sudo systemctl restart $SERVICE_NAME"
echo "   sudo systemctl status $SERVICE_NAME"
