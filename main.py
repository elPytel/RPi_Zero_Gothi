import os
import asyncio
import time
import numpy as np
import argparse
from basic_colors import *
from tools import *
from Button import Button
from PIL import Image, ImageDraw, ImageFont

from SlideShow import SlideShow

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

async def init():
    global disp, ina219, font20, font10
    try:
        disp = SH1106.SH1106()
        print_success("Initialized: display driver - SH1106")
        # Initialize library.
        disp.Init()
        disp.clear()  

        print_info("Loading splash screen...")
        load_screen = asyncio.create_task(splash_screen(0))

        ina219 = INA219(addr=0x43)
        print_success("Initialized: battery driver - INA219")
        
        # join path to assets
        font_path = os.path.join(ASSETS, FONTS, FONT)
        if not os.path.exists(font_path):
            print_error(f"Font file {font_path} not found.")
        
        font20 = ImageFont.truetype(font_path, 20)
        font10 = ImageFont.truetype(font_path, 13) 
        font10 = ImageFont.truetype(os.path.join(ASSETS, FONTS, 'Doto-Black.ttf'), 10) 
        print_success("Loaded fonts.")
        await asyncio.sleep(4)
    except IOError as e:
        print_error(str(e))
    finally:
        load_screen.cancel()
        try:
            await load_screen
        except asyncio.CancelledError:
            verbose_print("Task has been successfully cancelled.")


async def battery_task(interval=1):
    """Periodicky čte data z INA219 a aktualizuje displej"""
    while True:
        bus_voltage = ina219.getBusVoltage_V()
        shunt_voltage = ina219.getShuntVoltage_mV() / 1000
        current = ina219.getCurrent_mA()
        power = ina219.getPower_W()
        percent = ina219.getRemainingPercent()
        remaining_time = ina219.getRemainingTime()

        if remaining_time < 0:
            time_string = "infinite"
        else:
            time_string = sec_to_hhmmss(remaining_time)

        if DEBUG:
            print(f"[Battery] PSU Voltage: {(bus_voltage + shunt_voltage):.3f} V")
            print(f"[Battery] Current:     {current/1000:.3f} A")
            print(f"[Battery] Power:       {power:.3f} W")
            print(f"[Battery] Percent:     {percent:.1f}%")
            print(f"[Battery] Time left:   {time_string}")
            print()

        # --- Vykreslení na displej ---
        image = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)
        texts = [
            f"Time:    {time_string}",
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
    buttons = {
            "UP": (Button(), disp.RPI.GPIO_KEY_UP_PIN),
            "DOWN": (Button(), disp.RPI.GPIO_KEY_DOWN_PIN),
            "LEFT": (Button(), disp.RPI.GPIO_KEY_LEFT_PIN),
            "RIGHT": (Button(), disp.RPI.GPIO_KEY_RIGHT_PIN),
            "ENTER": (Button(), disp.RPI.GPIO_KEY_PRESS_PIN),
            "KEY1": (Button(), disp.RPI.GPIO_KEY1_PIN),
            "KEY2": (Button(), disp.RPI.GPIO_KEY2_PIN),
            "KEY3": (Button(), disp.RPI.GPIO_KEY3_PIN),
        }
    
    while True:
        if not RPI: # Mock mode
            # Simulate button presses for testing
            disp.window.update_idletasks()

        for name, (button, pin) in buttons.items():
            # Read the button state
            raw_value = disp.RPI.digital_read(pin)  # 0 = pressed, 1 = released
            button.update(raw_value)

            if button.was_just_pressed():
                if name == "KEY1":
                    print("[Input] KEY1 pressed — Updating application...")
                    if RPI:
                        update_application()
                    else:
                        raise SystemExit(0)
                elif name == "KEY2":
                    print("[Input] KEY2 pressed — Vypínám RPi!")
                    if RPI:
                        shutdown_system()
                    return

            if button.was_just_released():
                print(f"[Input] {name} just released")

            if button.is_pressed():
                pass
        
        await asyncio.sleep(interval)

async def splash_screen(duration=0):
    """Zobrazí úvodní obrázek na začátku"""
    # Loading slide show
    path = os.path.join(ASSETS, 'icons', 'Common', 'Loading_24')
    slides = SlideShow()
    slides.init_from_path(path)

    def loading():
        """Funkce pro načítání obrázků"""
        if duration > 0:
            return time.time() < time_stemp + duration
        return True
    
    # create animation
    time_stemp = time.time()
    while loading():
        frame = slides.next_frame()
        image = Image.new('1', (disp.width, disp.height), "WHITE")
        x, y = center_image(image, frame)
        image.paste(frame, (x, y))
        disp.ShowImage(disp.getbuffer(image))
        await asyncio.sleep(1 / slides.frame_rate)

async def main():
    try:
        await init()
        await asyncio.gather(
            battery_task(),
            input_task(),
        )
    except SystemExit:
        print("[Main] SystemExit caught — Cleaning up tasks...")
        tasks = asyncio.all_tasks()
        current_task = asyncio.current_task()
        tasks.remove(current_task)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("[Main] All tasks cancelled. Exiting program.")

# ---------- MAIN LOOP ------------
if __name__=='__main__': 
    set_verbose(False)
    # parse arguments
    parser = argparse.ArgumentParser(description="Zero-Gothi main application")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode.")
    parser.add_argument("-D", "--debug", action="store_true", help="Debug mode.")
    args = parser.parse_args()
    
    if args.verbose:
        VERBOSE = True
        set_verbose(True)
    
    if args.debug:
        DEBUG = True

    # Spustíme asyncio loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_info("KeyboardInterrupt — Cleaning up")
    finally:
        disp.RPI.module_exit()
        print_success("Exiting program.")