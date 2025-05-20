import subprocess
import re
import time
from platforms.template.battery import *

LOW_VOLTAGE = 3.0
HIGH_VOLTAGE = 4.2

def get_battery_info():
    output = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_bq27200_0"], text=True)
    info = {}
    for line in output.splitlines():
        if ":" in line:
            key, val = line.strip().split(":", 1)
            info[key.strip()] = val.strip()
    return info

class Nokia_battery(Battery):
    def __init__(self):
        self.last_update_time = time.time()
        self.voltage = 0.0
        self.current = 0.0
        self.power = 0.0
        self.percent = 0.0
        self.state = "unknown"
        self.temp = "N/A"
        self.time_to_empty = 0

    def _update_battery_status(self):
        if time.time() - self.last_update_time < 1:
            return
        
        def to_seconds(time_str) -> int:
            """
            XX.X hours 
            XX.X minutes 
            XX.X seconds
            --> int seconds
            """
            if "hours" in time_str:
                return int(float(time_str.split()[0]) * 3600)
            elif "minutes" in time_str:
                return int(float(time_str.split()[0]) * 60)
            elif "seconds" in time_str:
                return int(float(time_str.split()[0]))
            else:
                return 0

        self.last_update_time = time.time()
        info = get_battery_info()
        try:
            self.voltage = float(info.get("voltage", "0").split()[0])
            self.power = float(info.get("energy-rate", "0").split()[0])
            self.percent = float(info.get("percentage", "0").replace("%", ""))
            self.state = info.get("state", "unknown")
            self.temp = info.get("temperature", "N/A")
            self.time_to_empty = to_seconds(info.get("time to empty", "0:00"))
        except Exception as e:
            print(f"Error parsing battery info: {e}")

    def getVoltage_V(self):
        """
        Returns the bus voltage in volts.
        """
        self._update_battery_status()
        return round(self.voltage, 3)

    def getCurrent_mA(self):
        current = self.power / self.voltage * 1000.0
        return current

    def getPower_W(self):
        """
        Returns the power in watts.
        """
        self._update_battery_status()
        return round(self.power, 3)
    
    def getRemainingPercent(self):
        """
        Returns the remaining battery percentage.
        """
        self._update_battery_status()
        return self.percent
    
    def getRemainingTime(self) -> int:
        """
        Returns the remaining time in seconds.
        """
        self._update_battery_status()
        return self.time_to_empty
