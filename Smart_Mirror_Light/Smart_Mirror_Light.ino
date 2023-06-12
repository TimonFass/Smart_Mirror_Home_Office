/*
 * Main file of the program. Initializes everything and contains the
 * 'setup' and 'loop' function.
 *  
 * Author: Timon Fass
 * Email: timon.fass@student.jade-hs.de
 * Date: 27.06.2023
 * Version: 1.0
 * 
 * Licence: 
 *  Copyright: (c) 2023 Timon Fass
 *  This code is published under the terms of the 3-Clause BSD License.
 *  The full text can be seen at:
 *  https://opensource.org/licenses/BSD-3-Clause
 */

// Include library for RGB-sensor
#include "Adafruit_TCS34725.h"

// Include library for Bluetooth module
#include <SoftwareSerial.h>

// Define TX and RX pins of the Bluetooth module
SoftwareSerial BT(2, 3); 

// Initialise RGB-sensor with specific integration time and gain values 
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_614MS,
 TCS34725_GAIN_1X);

// Define the pins of the RGB-LEDs
const int bluePin = 9;
const int greenPin = 10;
const int redPin = 11;

// Define variable, which is used to send messages to the Bluetooth module
char message;

// Define the variable, which is changed according to the light mode
int mode;  

// Declare the values of the sensor
uint16_t r, g, b, c, colorTemp, lux;

// Declare RGB-values again as float to use internal 'getRGB' function 
float r_value, g_value, b_value;

// Declare a buffer variable which will be filled with the received sensor
// values later during the Bluetooth communication.
char buf[100];

void setup() {
  /*
   * Setup function. After powering up the Arduino everything in this
   * function is done once.
   */

  // Start serial monitor by setting its data rate
  Serial.begin(9600);

  // Set the data rate for the SoftwareSerial port and therefore the
  // Bluetooth module
  BT.begin(9600);

  // Checking for a connected TCS34725 sensor
  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }

  // Set every RGB-value to 0, to start with the LEDs turned OFF
  setColorRGB(0, 0, 0);
}

void loop() {
  /*
   * Loop function. After the 'setup' function is done, everything in this
   * function is done over and over again until the Arduino is powered off. 
   */
                                                                                          
  // Check the value of 'mode' to switch to the affiliated operation mode
  switch(mode){

    // If 'mode' is 0 the RGB-LEDs are turned off
    case 0:
      setColorRGB(0, 0, 0);
      readRGBSensor();
      break;
    
    // If 'mode' is 1 bright white light is turned on
    case 1:
      setColorRGB(255, 255, 255);
      readRGBSensor();
      break;
    
    // If 'mode' is 2 daylight white light us turned on 
    case 2:
      setColorRGB(145, 80, 15);
      readRGBSensor();
      break;

    // If 'mode' is 3 cold white light is turned on
    case 3:
      setColorRGB(120,78,92);
      readRGBSensor();
      break;
    
  }

  // Checking for messages sent via the Bluetooth module
  if (BT.available()){

    // Read the message sent via Bluetooth
    message = (BT.read());

    // Call the Bluetooth function
    chooseBluetoothMode(message);
  }
}
