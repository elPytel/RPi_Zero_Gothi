# RPi_Zero_Gothi

![loading](./documentation/images/loading.png)

## Hardware

I am using a Raspberry Pi Zero WH with a Waveshare UPS HAT and a 1.3inch OLED HAT. I have used demo code from the Waveshare website for OLED HAT and UPS HAT in this project.

### RPi Zero WH


### UPS HAT

![350](https://www.waveshare.com/w/upload/thumb/0/0d/UPS-HAT-C-1.jpg/800px-UPS-HAT-C-1.jpg)

[waveshare.com/wiki](https://www.waveshare.com/wiki/UPS_HAT_(C))

### 1.3inch OLED HAT

![350](https://www.waveshare.com/w/upload/thumb/e/e3/1.3inch-OLED-HAT-1.jpg/600px-1.3inch-OLED-HAT-1.jpg)

[waveshare.com/wiki](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)

## Installation

### Prerequisites
- Raspberry Pi OS Lite
- Python 3.7 or higher
- Python 3 pip

To disable the system packages check in pip, run the this command: 
```bash
python3 -m pip config set global.break-system-packages true
```

To run shutdown command without password, you need to edit the sudoers file.

```bash
sudo visudo
```

For user `pi` add the following line to the end of the file:

```bash
pi ALL=NOPASSWD: /sbin/poweroff, /sbin/shutdown
```

### Clone the repository
```bash
git clone <repository-url>
```

### Install dependencies
```bash
cd RPi_Zero_Gothi
./install.sh
```

Installation script will set up systemd service for the application. It will also install the required Python packages and set up the virtual environment.

### Run the application (manually)
```bash
cd RPi_Zero_Gothi
python3 main.py
```

## Update

To update the application, run the following command in the project directory:

```bash
./update.sh
```

This will pull the latest changes from the repository and update the application.

## Assets

### Art

Artwork is taken from the [Flipper Zero](https://github.com/flipperdevices/flipperzero-firmware/tree/dev).

### Fonts
Fonts:
- Doto, 
- Tiny5

are downloaded from [Google Fonts](https://fonts.google.com/).

## Software

