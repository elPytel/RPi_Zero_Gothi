import subprocess
import re
import time

class Battery:
    pass

def get_battery_info():
    output = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_bq27200_0"], text=True)
    info = {}
    for line in output.splitlines():
        if ":" in line:
            key, val = line.strip().split(":", 1)
            info[key.strip()] = val.strip()
    return info

def print_battery_status():
    info = get_battery_info()
    try:
        voltage = float(info.get("voltage", "0").split()[0])
        power = float(info.get("energy-rate", "0").split()[0])
        percent = float(info.get("percentage", "0").replace("%", ""))
        state = info.get("state", "unknown")
        temp = info.get("temperature", "N/A")
    except Exception as e:
        print(f"Chyba při parsování: {e}")
        return

    print(f"Napájecí stav:  {state}")
    print(f"Napětí:         {voltage:.3f} V")
    print(f"Příkon:         {power:.3f} W")
    print(f"Kapacita:       {percent:.1f} %")
    print(f"Teplota:        {temp}")
    print()

if __name__ == "__main__":
    while True:
        print_battery_status()
        time.sleep(5)
