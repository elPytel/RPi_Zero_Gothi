import time

def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        return 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo
    except FileNotFoundError:
        return False

def center_image(canvas, img):
    x = (canvas.width - img.width) // 2
    y = (canvas.height - img.height) // 2
    return x, y

def sec_to_hhmmss(seconds: int) -> str:
    """
    Convert seconds to hh:mm:ss format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

class Timer:
    def __init__(self, sleep_time=1):
        self.start_time = time.time()
        self.sleep_time = sleep_time
        self.sleep_until = self.start_time + sleep_time

    def elapsed(self):
        return time.time() - self.start_time
    
    def reset(self):
        self.start_time = time.time()
        self.sleep_until = self.start_time + self.sleep_time

    def sleep(self, seconds):
        self.sleep_until = time.time() + seconds
        self.sleep_time = seconds
    
    def done(self):
        if time.time() >= self.sleep_until:
            self.reset()
            return True
        return False