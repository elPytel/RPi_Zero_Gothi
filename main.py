import SH1106
import time
import config
import traceback

from basic_colors import *
from INA219 import *
from PIL import Image, ImageDraw, ImageFont



if __name__=='__main__':
    # Create an INA219 instance.
    
    ina219 = INA219(addr=0x43)
    print_info("Initializing battery driver: INA219...")
    disp = SH1106.SH1106()
    print_info("Initializing display driver: INA219...")

    try:
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()

        # Create blank image for drawing.
        image1 = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('Font.ttf', 20)
        font10 = ImageFont.truetype('Font.ttf',13)
        
        print ("***draw line")
        draw.line([(0,0),(127,0)], fill = 0)
        draw.line([(0,0),(0,63)], fill = 0)
        draw.line([(0,63),(127,63)], fill = 0)
        draw.line([(127,0),(127,63)], fill = 0)
        print ("***draw rectangle")
        
        """
        draw.text((30,0), 'Waveshare ', font = font10, fill = 0)
        draw.text((28,20), u'微雪电子 ', font = font, fill = 0)

        # image1=image1.rotate(180) 
        disp.ShowImage(disp.getbuffer(image1))
        time.sleep(2)
        
        print ("***draw image")
        Himage2 = Image.new('1', (disp.width, disp.height), 255)  # 255: clear the frame
        bmp = Image.open('pic.bmp')
        Himage2.paste(bmp, (0,5))
        # Himage2=Himage2.rotate(180) 	
        disp.ShowImage(disp.getbuffer(Himage2))
        """

    except IOError as e:
        print_error(str(e))
        
    except KeyboardInterrupt:    
        print("ctrl + c:")
        disp.RPI.module_exit()
        exit()

    while True:
        bus_voltage = ina219.getBusVoltage_V()             # voltage on V- (load side)
        shunt_voltage = ina219.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
        current = ina219.getCurrent_mA()                   # current in mA
        power = ina219.getPower_W()                        # power in W
        percent = ina219.getRemainingPercent()

        # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
        #print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
        #print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
        print("Load Voltage:  {:6.3f} V".format(bus_voltage))
        print("Current:       {:6.3f} A".format(current/1000))
        print("Power:         {:6.3f} W".format(power))
        print("Percent:       {:3.1f}%".format(percent))
        print("")

        text = "Percent: " + str(percent) + "%"
        draw.text((30,0), text, font = font10, fill = 0)

        time.sleep(2)