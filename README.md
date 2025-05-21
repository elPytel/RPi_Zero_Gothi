# RPi_Zero_Gothi

![loading](./documentation/images/loading.png)

> [!warning]
> This project is in early development stage. It is not ready for production use. Use at your own risk.

## Hardware

HW which can natively run this application:
- [N900](https://en.wikipedia.org/wiki/Nokia_N900)
- [Raspberry Pi Zero WH](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)

### N900

> [!note]
> The N900 is a Linux-based pre-smartphone that can run a variety of applications. The N900 has a 0.6 GHz ARM Cortex-A8 processor and 256MB of RAM. It has a 5MP camera and a 32GB internal storage. It has a 3.5 inch screen with a resolution of 800x480 pixels.

You can use Nokia N900 with Postmarket OS and Python 3.
As it is phone with a keyboard, battery, touchscreen and a stylus, it is a perfect device for this project. 
SD card is used for storage (up to 400GB). 

- [Postmarket OS](https://wiki.postmarketos.org/wiki/Nokia_N900_(nokia-n900))

It is based on Alpine Linux and uses the mainline Linux kernel. It is designed to be lightweight and fast, with a focus on security and privacy. Postmarket OS is designed to run on a variety of devices, including the Nokia N900.

### RPi Zero WH

I am using a Raspberry Pi Zero WH with a Waveshare UPS HAT and a 1.3inch OLED HAT. I have used demo code from the Waveshare website for OLED HAT and UPS HAT in this project.

#### UPS HAT

![350](https://www.waveshare.com/w/upload/thumb/0/0d/UPS-HAT-C-1.jpg/800px-UPS-HAT-C-1.jpg)

[waveshare.com/wiki](https://www.waveshare.com/wiki/UPS_HAT_(C))

#### 1.3inch OLED HAT

![350](https://www.waveshare.com/w/upload/thumb/e/e3/1.3inch-OLED-HAT-1.jpg/600px-1.3inch-OLED-HAT-1.jpg)

[waveshare.com/wiki](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)

## Installation

### Prerequisites
- Raspberry Pi OS Lite / N900 - Postmarket OS
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

### Samba

[www.raspberrypi.com:samba](https://www.raspberrypi.com/documentation/computers/remote-access.html#sharing-a-folder-from-your-raspberry-pi)