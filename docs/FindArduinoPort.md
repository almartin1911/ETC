# Find and setup Arduino port

Arduino's (and other USB-serial devices) end up as recognized ```/dev/ttyACM*``` or ```/dev/ttyUSB*``` in your **Linux-based** host OS. Next are steps for a **first-time only setup**. However, some of these commands might be useful if you're experiencing issues with the Arduino board connection.

## On Linux
1. Open a terminal and type:
```bash
$ ls -l /dev/ttyACM*
```
With your board plugged in will tell you if it'd been recognized and what group(s) can access it. you should see and output similar to this:
```bash
crw-rw---- 1 root dialout 166, 0 oct 22 11:23 /dev/ttyACM0
```
Note the presence of ```root``` and ```dialout``` groups. So now it's time to add yourself to the ```dialout``` group.

2. Add ```$YOUR_USERNAME``` to the ```dialout``` group by typing:
```bash
$ sudo usermod -a -G dialout $YOUR_USERNAME
```

3. Logout and then log back.

4. Finally, open a terminal and run ```$ groups $YOUR_USERNAME``` and look for ```dialout``` in the output.  

**Note**: In case group change isn't recognized after the logout/log-back step, try rebooting the system.

## On Windows

No special setup is required. Finding the port should be really straightforward.

1. Open **Device Manager**, and expand the ```Ports (COM & LPT)``` list.
![Serial port identification on Windows](https://www.mathworks.com/help/supportpkg/arduinoio/ug/win_dev_mngr_port.png)
2. Finally, note the port number ( ```COM*```) of the Arduino board.
