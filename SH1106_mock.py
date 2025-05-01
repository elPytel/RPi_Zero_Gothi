import tkinter as tk
from PIL import Image, ImageTk

LCD_WIDTH   = 128 #LCD width
LCD_HEIGHT  = 64  #LCD height
SIZE_MULTIPLIER = 3  # Size multiplier for the mock display
BACKGROUND_COLOR = "black"
FOREGROUND_COLOR = "blue"

class RaspberryPi:
    def __init__(self,spi=None,spi_freq=None,rst = 27,dc = 25,bl = 18,bl_freq=1000,i2c=None):

        self.GPIO_KEY_UP_PIN     = False
        self.GPIO_KEY_DOWN_PIN   = False
        self.GPIO_KEY_LEFT_PIN   = False
        self.GPIO_KEY_RIGHT_PIN  = False
        self.GPIO_KEY_PRESS_PIN  = False

        self.GPIO_KEY1_PIN       = False
        self.GPIO_KEY2_PIN       = False
        self.GPIO_KEY3_PIN       = False

    def key_press(self, event):
        """Handle key press events."""
        if event.keysym == "Up":
            self.GPIO_KEY_UP_PIN = True
        elif event.keysym == "Down":
            self.GPIO_KEY_DOWN_PIN = True
        elif event.keysym == "Left":
            self.GPIO_KEY_LEFT_PIN = True
        elif event.keysym == "Right":
            self.GPIO_KEY_RIGHT_PIN = True
        elif event.keysym == "Return":  # Enter key
            self.GPIO_KEY_PRESS_PIN = True
        elif event.keysym == "1":
            self.GPIO_KEY1_PIN = True
        elif event.keysym == "2":
            self.GPIO_KEY2_PIN = True
        elif event.keysym == "3":
            self.GPIO_KEY3_PIN = True

    def key_release(self, event):
        """Handle key release events."""
        if event.keysym == "Up":
            self.GPIO_KEY_UP_PIN = False
        elif event.keysym == "Down":
            self.GPIO_KEY_DOWN_PIN = False
        elif event.keysym == "Left":
            self.GPIO_KEY_LEFT_PIN = False
        elif event.keysym == "Right":
            self.GPIO_KEY_RIGHT_PIN = False
        elif event.keysym == "Return":  # Enter key
            self.GPIO_KEY_PRESS_PIN = False
        elif event.keysym == "1":
            self.GPIO_KEY1_PIN = False
        elif event.keysym == "2":
            self.GPIO_KEY2_PIN = False
        elif event.keysym == "3":
            self.GPIO_KEY3_PIN = False
    
    def digital_read(self, pin):
        return pin

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

