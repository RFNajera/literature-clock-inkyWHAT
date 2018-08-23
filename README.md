# literature-clock
Clock using time quotes from the literature, based on work and idea by
        [Jaap Meijers](http://www.eerlijkemedia.nl/) ([E-reader clock](https://www.instructables.com/id/Literary-Clock-Made-From-E-reader/)) and the web version by [JohannesNE](https://github.com/JohannesNE/literature-clock).

This fork runs on python using PyQt4 and is designed for the for using the Raspberry Pi 7" touch screen. 

## Install

On the Raspberry pi

`sudo apt-get install python-qt4`

or

`sudo apt-get install python3-pyqt4` if you are running python 3.


download or clone the this repo and run `python pi_clock.py` for the downloads directory

## Usage

The app runs full screen and is designed for an 800x480 display. To quit, press/click anywhere to bring up the quit button.

There's also a `.desktop` file. You can edit the paths in the file for your system, copy it into `~./Desktop` if you want to start the app from the desktop.

### Starting the app via SSH.

If you SSH into your pi like I do, by default the clock runs on my mac rather than the pi. Change the display settings:
```
export DISPLAY=:0
nohup python pi_clock.py &
```
The `nohup` detaches the process from the terminal so you can log out and leave the app running.

