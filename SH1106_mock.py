import tkinter as tk
from PIL import Image, ImageTk

LCD_WIDTH   = 128 #LCD width
LCD_HEIGHT  = 64  #LCD height
SIZE_MULTIPLIER = 3  # Size multiplier for the mock display
BACKGROUND_COLOR = "black"
FOREGROUND_COLOR = "blue"

class SH1106(object):
    def __init__(self):
        self.width = LCD_WIDTH
        self.height = LCD_HEIGHT
        self.window = tk.Tk()
        self.window.title("SH1106 Mock Display")
        self.canvas = tk.Canvas(self.window, width=self.width*SIZE_MULTIPLIER, height=self.height*SIZE_MULTIPLIER, bg="black")
        self.canvas.pack()
        self.tk_image = None
        self.clear()

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
        self.window.update()

