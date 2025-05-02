import os
from PIL import Image

class SlideShow:
    def __init__(self, frames=None, frame_rate=30):
        self.frames = frames
        self.current_frame = 0
        self.frame_rate = frame_rate

    def next_frame(self):
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        frame = self.frames[self.current_frame]
        self.current_frame += 1
        return frame
    
    def load_frames_from_directory(self, directory):
        """
        Load frames from a directory.
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")
        # list all files in the directory
        files = os.listdir(directory)
        # sort files by name
        files.sort()
        # filter files by extension
        files = [f for f in files if f.endswith('.png')]
        # load all files
        self.frames = []
        for file in files:
            img_path = os.path.join(directory, file)
            img = Image.open(img_path)
            self.frames.append(img)

    def load_frame_rate(self, frame_rate_file):
        """
        Load frame rate from a file.
        """
        if os.path.exists(frame_rate_file):
            with open(frame_rate_file, 'r') as f:
                self.frame_rate = float(f.read().strip())
        else:
            self.frame_rate = 30

    def init_from_path(self, path):
        """
        Initialize the slideshow from a path.
        """
        self.load_frames_from_directory(path)
        self.load_frame_rate(os.path.join(path, 'frame_rate'))