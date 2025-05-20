import sys
import time
import subprocess
from enum import Enum, auto

class Platform(Enum):
    #RPI_ZERO = auto()
    #N900 = auto()
    #OTHER = auto()
    RPI_ZERO = "Raspberry Pi Zero"
    N900 = "Nokia N900"
    OTHER = "Other"

def detect_platform():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()

        if 'BCM' in cpuinfo or 'Raspberry Pi' in cpuinfo:
            return Platform.RPI_ZERO
        elif 'n900' in cpuinfo or 'omap3430' in cpuinfo or 'Nokia RX-51' in cpuinfo:
            return Platform.N900
        else:
            return Platform.OTHER
    
    except Exception as e:
        print(f"Could not detect platform: {e}")
        return Platform.OTHER


def update_application():
    """Will run update.sh script."""
    print("🔄 Loading update script...")
    try:
        subprocess.Popen(["/bin/bash", "update.sh", "-r"])
        print("✅ Update script started successfully.")
        raise SystemExit(0)
    except Exception as e:
        print(f"❌ Failed to start update script: {e}")
    
def shutdown_system():
    """Power off the system using shutdown command."""
    print("⚠️  Powering off...")
    try:
        subprocess.Popen(["sudo", "shutdown", "-h", "now"])
        print("🛑 Power off command sent.")
        raise SystemExit(0)
    except Exception as e:
        print(f"❌ Failed to send power off command: {e}")

def center_image(canvas, img):
    x = (canvas.width - img.width) // 2
    y = (canvas.height - img.height) // 2
    return x, y

def sec_to_hhmmss(seconds: int) -> str:
    """
    Convert seconds to hh:mm:ss format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

class Timer:
    def __init__(self, sleep_time=1):
        self.start_time = time.time()
        self.sleep_time = sleep_time
        self.sleep_until = self.start_time + sleep_time

    def elapsed(self):
        return time.time() - self.start_time
    
    def reset(self):
        self.start_time = time.time()
        self.sleep_until = self.start_time + self.sleep_time

    def sleep(self, seconds):
        self.sleep_until = time.time() + seconds
        self.sleep_time = seconds
    
    def done(self):
        if time.time() >= self.sleep_until:
            self.reset()
            return True
        return False