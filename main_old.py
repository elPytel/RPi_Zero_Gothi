import os
import traceback
import numpy as np
from basic_colors import *
from tools import *

from PIL import Image, ImageDraw, ImageFont

DEBUG = False
RPI=is_raspberry_pi()
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
    import platforms.RPi.config as config
    import platforms.RPi.SH1106 as SH1106
    from platforms.RPi.INA219 import *
else:
    import platforms.PC.SH1106_mock as SH1106
    from platforms.PC.INA219_mock import *


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

    # Create blank image for drawing.
    image = Image.new('1', (disp.width, disp.height), "WHITE")  # Bílý podklad
    draw = ImageDraw.Draw(image)

    # Načtení obrázku
    img_path = os.path.join(ASSETS, 'icons', 'Settings', 'LoadingHourglass_24x24.png')
    img = Image.open(img_path)
    
    # Vložení obrázku do bufferu
    def center_image(canvas, img):
        # Vypočítání pozice pro centrování obrázku
        x = (canvas.width - img.width) // 2
        y = (canvas.height - img.height) // 2
        return x, y

    x, y = center_image(image, img)
    image.paste(img, (x, y))
    disp.ShowImage(disp.getbuffer(image))
    time.sleep(1)    
    
    sleep_1s = Timer(1)
    sleep_100ms = Timer(0.01)

    while True:
        if sleep_1s.done():
            bus_voltage = ina219.getBusVoltage_V()             # voltage on V- (load side)
            shunt_voltage = ina219.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
            current = ina219.getCurrent_mA()                   # current in mA
            power = ina219.getPower_W()                        # power in W
            percent = ina219.getRemainingPercent()
            remaining_time = ina219.getRemainingTime()

            # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
            if DEBUG:
                print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
                print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
                print("Load Voltage:  {:6.3f} V".format(bus_voltage))
                print("Current:       {:6.3f} A".format(current/1000))
                print("Power:         {:6.3f} W".format(power))
                print("Percent:       {:3.1f}%".format(percent))
                print("")
            
            if current > 0:
                # charging
                print_info("Charging")

            texts = []
            #text = f"Voltage: {bus_voltage:6.3f} V"
            text = f"Time:    {sec_to_hhmmss(remaining_time)}"
            texts.append(text)
            text = f"Current: {current/1000:6.3f} A"
            texts.append(text)
            text = f"Power:   {power:6.3f} W"
            texts.append(text)
            text = f"Percent:  {percent:3.1f}%"
            texts.append(text)

            # clear the image
            image = Image.new('1', (disp.width, disp.height), "WHITE")
            draw = ImageDraw.Draw(image)
            x_pos = 5
            y_pos = 2
            x_shift = 0
            y_shift = 14
            for text in texts:
                draw.text((x_pos, y_pos), text, font = font10, fill = 0)
                x_pos += x_shift
                y_pos += y_shift
            disp.ShowImage(disp.getbuffer(image))

        if sleep_100ms.done():
            # Kontrola stisknutí kláves
            if not RPI:
                disp.window.update_idletasks()
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY_UP_PIN):
                print("Key UP pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY_DOWN_PIN):
                print("Key DOWN pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY_LEFT_PIN):
                print("Key LEFT pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY_RIGHT_PIN):
                print("Key RIGHT pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY_PRESS_PIN):
                print("Key ENTER pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY1_PIN):
                print("Key 1 pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY2_PIN):
                print("Key 2 pressed")
            if disp.RPI.digital_read(disp.RPI.GPIO_KEY3_PIN):
                print("Key 3 pressed")

        time.sleep(0.001)