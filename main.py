import time
import traceback
import numpy as np
from basic_colors import *

from PIL import Image, ImageDraw, ImageFont

def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        return 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo
    except FileNotFoundError:
        return False

DEBUG = False
RPI=is_raspberry_pi()

if RPI:
    print_success("Running on Raspberry Pi")
else:
    print_warning("Running on a different device than Raspberry Pi")

if RPI:
    import config
    import SH1106
    from INA219 import *
else:
    import SH1106_mock as SH1106
    from INA219_mock import *


if __name__=='__main__':    
    try:
        ina219 = INA219(addr=0x43)
        print_info("Initializing battery driver: INA219...")
    except IOError as e:
        print_error(str(e)) 
    
    try:
        disp = SH1106.SH1106()
        print_info("Initializing display driver: SH1106...")
        
        font20 = ImageFont.truetype('Font.ttf', 20)
        font10 = ImageFont.truetype('Font.ttf', 13) 
    except IOError as e:
        print_error(str(e))

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image = Image.new('1', (disp.width, disp.height), "WHITE")  # Bílý podklad
    draw = ImageDraw.Draw(image)

    # Načtení obrázku
    img = Image.open('loading.png')
    img = img.resize((disp.width, disp.height))  # Změna velikosti na rozměry displeje
    img = img.convert('L')  # Převod na stupně šedi
    trashold = 50
    img = img.point(lambda x: 0 if x < trashold else 255, '1')
    img = img.convert('1') # Převod na jednobitový formát (černobílý)
    
    # Vložení obrázku do bufferu
    image.paste(img, (0, 0))
    disp.ShowImage(disp.getbuffer(image))
    time.sleep(5)

    while True:
        bus_voltage = ina219.getBusVoltage_V()             # voltage on V- (load side)
        shunt_voltage = ina219.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
        current = ina219.getCurrent_mA()                   # current in mA
        power = ina219.getPower_W()                        # power in W
        percent = ina219.getRemainingPercent()

        # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
        #print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
        #print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
        if DEBUG:
            print("Load Voltage:  {:6.3f} V".format(bus_voltage))
            print("Current:       {:6.3f} A".format(current/1000))
            print("Power:         {:6.3f} W".format(power))
            print("Percent:       {:3.1f}%".format(percent))
            print("")

        texts = []
        text = f"Voltage: {bus_voltage:6.3f} V"
        texts.append(text)
        text = f"Current: {current/1000:6.3f} A"
        texts.append(text)
        text = f"Power:   {power:6.3f} W"
        texts.append(text)
        text = f"Percent: {percent:3.1f}%"
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

        time.sleep(2)
    
    """
    print ("***draw line")
    draw.line([(0,0),(127,0)], fill = 0)
    draw.line([(0,0),(0,63)], fill = 0)
    draw.line([(0,63),(127,63)], fill = 0)
    draw.line([(127,0),(127,63)], fill = 0)
    print ("***draw rectangle")
    disp.ShowImage(disp.getbuffer(image1))

    except KeyboardInterrupt:    
        print("ctrl + c:")
        disp.RPI.module_exit()
        exit()
    """