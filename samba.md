# Samba
[RPi:samba](https://www.raspberrypi.com/documentation/computers/remote-access.html#sharing-a-folder-from-your-raspberry-pi)

## Linux
Create a Samba share on PostmarketOS:
```sh
cd ~
mkdir shared
chmod 0755 shared
```

Add user to Samba:
```sh
sudo smbpasswd -a <username>
```

Comands to control Samba:
```sh
sudo rc-service samba start
sudo rc-service samba stop
sudo rc-service samba restart
sudo rc-service samba status
```

### Samba configuration
Edit the `/etc/samba/smb.conf` file:
```sh
sudo vim /etc/samba/smb.conf
```
```txt
[global]
   workgroup = WORKGROUP
   netbios name = N900
   server string = Nokia N900
   security = user
   map to guest = Bad User

[share]
    path = /home/user/shared
    valid users = user
    read only = no
    browsable = yes
    writable = yes
    guest ok = no

[public]
    path = /home/user/public
    read only = yes
    guest ok = yes
    browsable = yes
```

> [!note]
> Restart Samba after changing the configuration.

### Start Samba on boot
To start Samba on boot, you can use the following command:
```sh
sudo rc-update add samba default
```

#### Alternative: Custom script in local.d
If rc-update does not work (e.g. you do not have the correct init scripts), you can use local.d, which is also supported by PostmarketOS:

Create the directory if it does not exist:
```sh
sudo mkdir -p /etc/local.d
```

Create the script samba.start:
```sh
sudo nano /etc/local.d/samba.start
```

And insert:
```sh
#!/bin/sh
smbd
nmbd
```

Make sure it is executable:
```sh
sudo chmod +x /etc/local.d/samba.start
```

Make sure local.d is enabled:
```sh
sudo rc-update add local default
```

## Win

Enable SMB1 on Windows:
Run `optionalfeatures.exe`

Find "SMB 1.0/CIFS File Sharing Support"

Check all options

Restart the computer

### Access the share

Open File Explorer
In the address bar, type `\\<ip-address>\<shared folder>` to access the share.

