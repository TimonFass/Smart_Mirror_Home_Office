/*
 * This file includes the functions 'readRGBSensor' to read all data of a
 * RGB-sensor and 'setColorRGB' to set the color of a RGB-LED with values 
 * from 0 to 255.
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

 void readRGBSensor(){
  /*
   * Function to read all the data of the RGB-sensor
   */

  // Getting the raw data from the sensor
  tcs.getRawData(&r, &g, &b, &c);
  
  // Getting RGB-values from the sensor
  tcs.getRGB(&r_value, &g_value, &b_value);
  
  // Calculate color temperature and illuminance by using the sensors'
  // library
  colorTemp = tcs.calculateColorTemperature_dn40(r, g, b, c);
  lux = tcs.calculateLux(r, g, b);   
}

void setColorRGB(unsigned int red, unsigned int green, unsigned int blue){
  /*
   * Function to set the color of the RGB-LED to every single pin of the
   * LED.
   * 
   * Parameters
   * ----------
   * red: unsigned int
   *  Contains the value of the red light from 0 to 255
   *  
   * green: unsigned int
   *  Contains the value of the green light from 0 to 255
   *  
   * blue: unsigned int
   *  Contains the value of the blue light from 0 to 255
   */
   
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}
