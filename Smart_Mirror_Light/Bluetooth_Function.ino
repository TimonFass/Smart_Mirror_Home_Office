/*
 * This file contains the function 'chooseBluetoothMode', which switches
 * the user modes based on Bluetooth messages by the Python GUI.
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

int chooseBluetoothMode(char message){
  /*
   * Function to choose the LED mode by getting Bluetooth messages.
   * 
   * Parameters
   * ----------
   * message: char
   *  Messages sent by the App via Bluetooth connection.
   */

  // Set the 'mode' variable according to the
  // received Bluetooth message
  switch(message){
      
    // Turn the LEDs off
    case '0':
      
      BT.println("LEDs OFF");
      mode = 0;
      break;

    // Switch to bright white light mode  
    case '1':
      
      // Send color temperature and illuminance values via Bluetooth
      sprintf(buf, "%d, %d", colorTemp, lux);
      BT.println(buf);
      mode = 1;                  
      break;

    // Switch to daylight white mode
    case '2':
      
      // Send color temperature and illuminance values via Bluetooth
      sprintf(buf, "%d, %d", colorTemp, lux);
      BT.println(buf);               
      mode = 2;
      break;

    // Switch to cold white light mode
    case '3':
      
      // Send color temperature and illuminance values via Bluetooth
      sprintf(buf, "%d, %d", colorTemp, lux);
      BT.println(buf);               
      mode = 3;
      break;
      
    // If the received Bluetooth message does not fit to any of the
    // cases above, the program switches the LEDs off.
    default:
      BT.println("LEDs OFF");
      mode = 0;                  
      break;   
  }
}
