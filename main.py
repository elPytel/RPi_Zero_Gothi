import os
import asyncio
import time
import numpy as np
from basic_colors import *
from tools import *
from PIL import Image, ImageDraw, ImageFont


DEBUG = False
RPI = is_raspberry_pi()
ASSETS = "assets"
FONTS = "fonts"
FONT = 'Font.ttf'
#FONT = 'Doto-Black.ttf'
#FONT = 'Tiny5-Regular.ttf'

if RPI:
    print_success("Running on Raspberry Pi")
else:
    print_warning("Running on a different device than Raspberry Pi")
    DEBUG = True

if RPI:
    import config
    import SH1106
    from INA219 import *
else:
    import SH1106_mock as SH1106
    from INA219_mock import *


# ---------- ASYNCIO TASKS ------------
async def battery_task(interval=1):
    """Periodicky čte data z INA219 a aktualizuje displej"""
    while True:
        bus_voltage = ina219.getBusVoltage_V()
        shunt_voltage = ina219.getShuntVoltage_mV() / 1000
        current = ina219.getCurrent_mA()
        power = ina219.getPower_W()
        percent = ina219.getRemainingPercent()
        remaining_time = ina219.getRemainingTime()

        if DEBUG:
            print(f"[Battery] PSU Voltage: {(bus_voltage + shunt_voltage):.3f} V")
            print(f"[Battery] Current:     {current/1000:.3f} A")
            print(f"[Battery] Power:       {power:.3f} W")
            print(f"[Battery] Percent:     {percent:.1f}%")
            print(f"[Battery] Time left:   {sec_to_hhmmss(remaining_time)}")

        # --- Vykreslení na displej ---
        image = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)
        texts = [
            f"Time:    {sec_to_hhmmss(remaining_time)}",
            f"Current: {current/1000:.3f} A",
            f"Power:   {power:.3f} W",
            f"Percent:  {percent:.1f}%",
        ]
        x_pos = 5
        y_pos = 2
        y_shift = 14
        for text in texts:
            draw.text((x_pos, y_pos), text, font=font10, fill=0)
            y_pos += y_shift

        disp.ShowImage(disp.getbuffer(image))

        await asyncio.sleep(interval)

async def input_task(interval=0.01):
    """Periodicky čte tlačítka"""
    while True:
        keys = {
            "UP": disp.RPI.digital_read(disp.RPI.GPIO_KEY_UP_PIN),
            "DOWN": disp.RPI.digital_read(disp.RPI.GPIO_KEY_DOWN_PIN),
            "LEFT": disp.RPI.digital_read(disp.RPI.GPIO_KEY_LEFT_PIN),
            "RIGHT": disp.RPI.digital_read(disp.RPI.GPIO_KEY_RIGHT_PIN),
            "ENTER": disp.RPI.digital_read(disp.RPI.GPIO_KEY_PRESS_PIN),
            "KEY1": disp.RPI.digital_read(disp.RPI.GPIO_KEY1_PIN),
            "KEY2": disp.RPI.digital_read(disp.RPI.GPIO_KEY2_PIN),
            "KEY3": disp.RPI.digital_read(disp.RPI.GPIO_KEY3_PIN),
        }
        for name, pressed in keys.items():
            if pressed:
                print(f"[Input] Key {name} pressed")
        if not RPI:
            disp.window.update_idletasks()
        await asyncio.sleep(interval)

async def splash_screen(duration=1):
    """Zobrazí úvodní obrázek na začátku"""
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    # Cesta k ikoně
    img_path = os.path.join(ASSETS, 'icons', 'Settings', 'LoadingHourglass_24x24.png')
    img = Image.open(img_path)
    x, y = center_image(image, img)
    image.paste(img, (x, y))
    disp.ShowImage(disp.getbuffer(image))
    await asyncio.sleep(duration)

async def main():
    await splash_screen()
    await asyncio.gather(
        battery_task(),
        input_task(),
    )

# ---------- MAIN LOOP ------------
if __name__=='__main__': 
    try:
        ina219 = INA219(addr=0x43)
        print_success("Initialized: battery driver - INA219")
        disp = SH1106.SH1106()
        print_success("Initialized: display driver - SH1106")
        
        # join path to assets
        font_path = os.path.join(ASSETS, FONTS, FONT)
        if not os.path.exists(font_path):
            print_error(f"Font file {font_path} not found.")
        font20 = ImageFont.truetype(font_path, 20)
        font10 = ImageFont.truetype(font_path, 13) 
        font10 = ImageFont.truetype(os.path.join(ASSETS, FONTS, 'Doto-Black.ttf'), 10) 
        print_success("Loaded fonts.")
    except IOError as e:
        print_error(str(e))

    # Initialize library.
    disp.Init()
    disp.clear()  

    # Spustíme asyncio loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_info("KeyboardInterrupt — Cleaning up")
        disp.RPI.module_exit()
