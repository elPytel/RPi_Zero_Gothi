from enum import Enum, auto
import tkinter as tk
from PIL import Image, ImageTk

LCD_WIDTH   = 128 #LCD width
LCD_HEIGHT  = 64  #LCD height
SIZE_MULTIPLIER = 3  # Size multiplier for the mock display
BACKGROUND_COLOR = "black"
FOREGROUND_COLOR = "blue"

class RaspberryPi():
    GPIO_KEY_UP_PIN = 1
    GPIO_KEY_DOWN_PIN = 2
    GPIO_KEY_LEFT_PIN = 3
    GPIO_KEY_RIGHT_PIN = 4
    GPIO_KEY_PRESS_PIN = 5
    GPIO_KEY1_PIN = 6
    GPIO_KEY2_PIN = 7
    GPIO_KEY3_PIN = 8

    def __init__(self,spi=None,spi_freq=None,rst = 27,dc = 25,bl = 18,bl_freq=1000,i2c=None):
        self.pins = {
            "Up": (RaspberryPi.GPIO_KEY_UP_PIN, False),
            "Down": (RaspberryPi.GPIO_KEY_DOWN_PIN, False),
            "Left": (RaspberryPi.GPIO_KEY_LEFT_PIN, False),
            "Right": (RaspberryPi.GPIO_KEY_RIGHT_PIN, False),
            "Return": (RaspberryPi.GPIO_KEY_PRESS_PIN, False),
            "1": (RaspberryPi.GPIO_KEY1_PIN, False),
            "2": (RaspberryPi.GPIO_KEY2_PIN, False),
            "3": (RaspberryPi.GPIO_KEY3_PIN, False),
        }

    def key_press(self, event):
        """Handle key press events."""
        for key, (pin, state) in self.pins.items():
            if event.keysym == key:
                self.pins[key] = (pin, True)
                break

    def key_release(self, event):
        """Handle key release events."""
        for key, (pin, state) in self.pins.items():
            if event.keysym == key:
                self.pins[key] = (pin, False)
                break
    
    def digital_read(self, pin):
        """Mock digital read function."""
        for key, (p, state) in self.pins.items():
            if p == pin:
                return state

class SH1106(object):
    def __init__(self):
        self.width = LCD_WIDTH
        self.height = LCD_HEIGHT
        self.RPI = RaspberryPi()
        self.window = tk.Tk()
        self.window.title("SH1106 Mock Display")
        self.canvas = tk.Canvas(self.window, width=self.width*SIZE_MULTIPLIER, height=self.height*SIZE_MULTIPLIER, bg="black")
        self.canvas.pack()
        self.tk_image = None
        self.clear()

        # Bind key events to the window
        self.window.bind("<KeyPress>", self.RPI.key_press)
        self.window.bind("<KeyRelease>", self.RPI.key_release)

    def command(self, cmd):
        pass

    def Init(self):
        """Initialize the mock display."""
        print("SH1106 Mock: Initialized")
        
    def reset(self):
        """Reset the display"""
        self.buffer = Image.new("1", (self.width*SIZE_MULTIPLIER, self.height*SIZE_MULTIPLIER), "WHITE")
        self.__update_display()
        print("SH1106 Mock: Reset")
    
    def getbuffer(self, image):
        """Convert the image to a buffer (mock implementation)."""
        # if not 1-bit image, raise an error
        if image.mode != "1":
            raise ValueError("Image must be in 1-bit mode")
        return image
    
    def ShowImage(self, buffer):
        """Display the image on the mock display."""
        self.buffer = buffer
        self.__update_display()

    def clear(self):
        """Clear the display."""
        self.buffer = Image.new("1", (self.width*SIZE_MULTIPLIER, self.height*SIZE_MULTIPLIER), "WHITE")
        self.__update_display()

    def __update_display(self):
        """Update the tkinter window with the current image."""
        # convert from 1-bit to 8-bit Color
        # black background with light blue foreground
        resized_image = self.buffer.resize((self.width * SIZE_MULTIPLIER, self.height * SIZE_MULTIPLIER), Image.NEAREST)
        # invert BW
        resized_image = resized_image.point(lambda x: 255 if x == 0 else 0, '1')
        # convert to RGB and apply color
        #self.tk_image = ImageTk.PhotoImage(self.resized_image.convert("RGB").resize((self.width * SIZE_MULTIPLIER, self.height * SIZE_MULTIPLIER), Image.NEAREST))
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.window.update_idletasks()
        self.window.update()

