# README - Smart Mirror GUI for lighting control in Home Offices

**Date:** 27th June 2023

**Author:** Timon Faß

**Version:** 1.0

For more information on this project see the attached files in the 
'documentation' folder.

---

**Requirements**

Only tested on Windows 10.
At least Python 3.10 with following libraries needs to be installed:

*Important:* To run the program, the PC always needs an active internet
connection!

standard libraries:
- tkinter
- time
- serial

Need to be installed with pip:
- PIL (Python Imaging Library): 'pip install pillow'
- requests: 'pip install requests'
- translate: 'pip install translate'

The Arduino hardware needs to be set up according to the circuit plan, which
can be found in 'Schaltplan.pdf' in 'documentation' folder.

The HC-06 Bluetooth module needs to be paired with the used PC on port COM5.
The port can be changed in the Python code.

---

**Executing the program**

1. Connect the Arduino (with uploaded code) to power supply.
2. Turn on Bluetooth settings on the used PC
3. Start the Python program over console with 'python Smart_Mirror_GUI.py'
(Note: If you have more than one Python versions installed, it may be necessary
to use 'python3 Smart_Mirror_GUI.py')

You can shut the program down by pressing Esc.

*Important:* The Python program can be used without the Arduino hardware, too. But 
in this case the Bluetooth functionality does not work. The program will not crash, 
but you will get error messages in the console.

---

**Using the programm**

When the program is started, you see the GUI in fullscreen. In the middle of the
screen, the current date and time is shown. On the bottom left you can find the
current weather information from OpenWeather for Wilhelmshaven. If this does not
work you may create a new user account for OpenWeather at:

https://home.openweathermap.org/users/sign_up

and change the API_KEY in the Code. By changing the variable CITY, you can adjust
the program for the weather information of your current location.

The main feature with the lighting control ("Beleuchtungssteuerung") can be found 
on the top right corner of your screen. By clicking the button 'Ein-/Ausblenden' you
can open and close the control menu. The 'Ausgabe' area shows the output of the received
data by the Bluetooth module as well as a small interpretation that says if the lighting 
is ok or too dark for the user. By clicking the three buttons on the bottom right side 
of your screen you can choose different light modes and turn the light off.

---

**Arduino Code**

The Arduino Code files can be found in the 'Smart_Mirror_Light' directory.
This program was only tested with an Arduino Nano V3 ATmega328.
To start the program you need to use the Arduino IDE. For this project
Arduino IDE version 1.8.13 was used.
Before use you need to install the following library manually: 

 - Adafruit TCS34725
 
The other needed library

- SoftwareSerial

is built in with the Arduino IDE.
 
*Keep in mind:* You need to upload the program to the Arduino by 
clicking the Upload button in the IDE. First you need to choose the connected port,
the board 'Arduino Nano' and the processor 'ATmega328P (Old Bootloader)'
in the 'Tools' menu of the IDE. This settings depend on the Arduino you
use to execute the program.

Before starting the program make sure that every wired connection of the
hardware is correct according to the circuit diagram in the 
'Schaltplan.pdf' file (in 'documentation' folder) and that all components of the system
are working.

After uploading the code to the Arduino the lighting of the RGB-LEDs can be
controlled using the GUI from the Python code in the file 'Smart_Mirror_GUI.py'.

