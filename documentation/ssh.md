# SSH Access to Raspberry Pi Zero

```ssh
rpizero.local
```

- [SSH Access to Raspberry Pi Zero](#ssh-access-to-raspberry-pi-zero)
  - [Generate SSH keys on Windows](#generate-ssh-keys-on-windows)
    - [Using PuTTYgen](#using-puttygen)
    - [Using keygen from Git Bash](#using-keygen-from-git-bash)
  - [Copy the public key to Raspberry Pi Zero](#copy-the-public-key-to-raspberry-pi-zero)
  - [How to login using SSH](#how-to-login-using-ssh)
  - [How to regenerate SSH keys and copy them to SD card directly](#how-to-regenerate-ssh-keys-and-copy-them-to-sd-card-directly)
    - [More about authorized\_keys file](#more-about-authorized_keys-file)


## Generate SSH keys on Windows

### Using PuTTYgen
You can use PuTTYgen to generate SSH keys on Windows. Download it from the official PuTTY website: [PuTTy](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

Open PuTTYgen and click on "Generate" to create a new key pair. Move your mouse around the blank area to generate randomness.

Once the keys are generated, save the private key to your computer by clicking on "Save private key". You can also copy the public key from the text box at the top of the window.

### Using keygen from Git Bash
If you have Git Bash installed, you can use the `ssh-keygen` command to generate SSH keys. Open Git Bash and run the following command:
```bash
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa
```
This will create a new RSA key pair with a length of 2048 bits and save it to the specified file.

## Copy the public key to Raspberry Pi Zero
You can copy the public key to your Raspberry Pi Zero using the `ssh-copy-id` command. Open a terminal and run the following command:
```bash
ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub pi@rpizero.local
```
Replace `~/.ssh/id_rsa.pub` with the path to your public key file if it's different.

## How to login using SSH

Is RPi Zero's IP address known? If yes, use it instead of `rpizero.local`.
Open a terminal and run the following command to check connectivity:
```bash
ping rpizero.local
```

For connecting to the Raspberry Pi Zero via SSH, use the following command:
```bash
ssh pi@rpizero.local
```
If you changed the default port, use the `-p` option to specify the port number:
```bash
ssh -p 22 pi@rpizero.local
```

## How to regenerate SSH keys and copy them to SD card directly

If you lost access to your Raspberry Pi Zero over the network and need to regenerate SSH keys, you can do so by mounting the SD card on another computer. 
1. Open a terminal and run the following command to generate a new SSH key pair:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/rpizero_new -C "rpizero"
```

2. Insert the SD card into your computer and navigate to the boot partition. 
```bash
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL
```
You are looking for the partition with the label "boot". Mount point may vary depending on your system:
- `mnt/user/root`
- `media/username/root`

Chceck fs size `100xMB` and type `fat32` to identify the boot partition. 

Base user on Raspberry Pi OS is `pi`.

3. Next, create a directory named `.ssh` in the root partition of the SD card if it doesn't already exist:
```bash
mkdir -p /path/to/rootfs/home/pi/.ssh/
```

4. Add the newly generated public key to the `.ssh` directory on the SD card and rename it to `authorized_keys`:
```bash
cp ~/.ssh/rpizero_new.pub /path/to/rootfs/home/pi/.ssh/authorized_keys
```

> [!note]
> Make sure to set the correct permissions for the `.ssh` directory and the `authorized_keys` file:
```bash
chmod 700 /path/to/rootfs/home/pi/.ssh
chmod 600 /path/to/rootfs/home/pi/.ssh/authorized_keys
sudo chown -R 1000:1000 /mnt/rpi_root/home/pi/.ssh   # UID:GID for /etc/passwd in image
```

5. Finally, unmount the SD card and insert it back into your Raspberry Pi Zero. You should now be able to log in using the new SSH key.

Now you can log in to your Raspberry Pi Zero using the new SSH key:
```bash
ssh -i ~/.ssh/rpizero_new pi@rpizero.local
```

### More about authorized_keys file
> [!tip]
> Adding more public keys to `authorized_keys` file is possible. Just append them to the file.

Format of `authorized_keys` file:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE... user1@pc
ssh-rsa   AAAAB3NzaC1yc2EAAAADAQABAAABAQC... other@laptop
ecdsa-sha2-nistp256 AAAAE2VjZHNhLX... someone@example.com
```
Each key should be on its own line.
Line endings should be LF (`\n`), not CRLF (`\r\n`).

Root user example:
```bash
cat ~/.ssh/id_rsa.pub >> /path/to/authorized_keys
```

With sudo:
```bash
sudo tee -a /mnt/rpi_root/home/pi/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
```