"""
Creates a GUI for a Smart Mirror with Bluetooth connection to Arduino to use it
for lighting control in a Home Office.

Code is based on a student project 'Social Mirror' in 2021 by:
    Angela Erpenbeck
    Wiebke Janssen
    Simona Peschke
    Scharon Kraudelt
    Tobias Boeer
    Timon Fass

Date: 27. June 2023

Author:
    Timon Fass

Email:
    timon.fass@student.jade-hs.de

Version: 1.0

Licence: 
    
    Copyright: (c) 2023, Fass
    This code is published under the terms of the 3-Clause BSD License.
    The full text can be seen in the 'LICENCE' file.
"""

from tkinter import *
import tkinter as tk

import time
from datetime import date

from PIL import ImageTk, Image

import requests
import serial

from translate import Translator


class Gui(tk.Tk):
    """
    This class provides functions to create a GUI. The GUI illustrates the 
    important information of a Smart Mirror as well as the control panel for
    lighting control.

    Functions:

    get_weather_data() -- Includes weather data from OpenWeather
    exit() -- Embedding of the escape button
    digital_clock() -- Embedding of time
    button1_clicked() -- Click event of button 1
    button2_clicked() -- Click event of button 2
    button3_clicked() -- Click event of button 3
    button4_clicked() -- Click event of button 4
    toggle_button_clicked() -- Click event of toggle button
    send_receive_serial_message() -- Sends and receives data to Arduino Bluetooth device
    translate_text() -- Translates English text to German
    """

    def __init__(self):
        super().__init__()
        """Create the GUI of the Smart Mirror

        The creation of GUI is based on Tkinter package.      
        """  

        # Variable to connect to OpenWeather user account
        API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                
        # City of which the weather data is displayed
        CITY = "Wilhelmshaven, DE"

        # Variable to check the visibility of the buttons later
        # At the beginning, the buttons are hidden, therefore it
        # gets the value 'False'.
        self.button_visibility = False  

        # Creation of textstyles
        text_style_tiny=("Boulder",15)
        text_style_small=("Boulder",25)              
        text_style_big=("Boulder",35)

        
        # Creation of black background, fullscreen mode
        self.configure(background='black')
        self.attributes("-fullscreen", True)

        # Label for header of lighting control
        label_date = Label(self, text="Beleuchtungssteuerung", font=text_style_small, bg='black', fg='white', bd=25)
        label_date.place(relx=0.6, rely=0.0, relwidth=0.4)

        # Label for Output window
        self.output_label = Label(self, text="Ausgabe", font=text_style_tiny, bg='black', fg='white')

        # Creating a frame
        self.output_frame = Frame(width=200, height=200, relief="solid", borderwidth=2, bg='black')

        # Add label widget to frame to display the output
        self.output_frame_label = Label(self.output_frame, text="Keine Ausgabe", font=text_style_small, bg='black', fg='white', width=200, height=200)
        self.output_frame_label.pack()

        # Add label widget to display interpretation of sensor values
        self.interpretation_label = Label(self, text="Keine Interpretation", font=text_style_tiny, bg='black', fg='white', width=200, height=50)
        
        # Create four buttons
        self.button1 = Button(self, text="OFF", font=text_style_small, bg='black', fg='white', bd=5, command=self.button1_clicked)
        self.button2 = Button(self, text="Helles Weiß", font=text_style_small, bg='black', fg='white', bd=5, command=self.button2_clicked)
        self.button3 = Button(self, text="Tageslichtweiß", font=text_style_small, bg='black', fg='white', bd=5, command=self.button3_clicked)
        self.button4 = Button(self, text="Kaltweiß", font=text_style_small, bg='black', fg='white', bd=5, command=self.button4_clicked)

        # Add button to toggle visibility of the other four buttons
        self.toggle_button = Button(self, text="Ein-/Ausblenden", font=("Helvetica", 24), bg='black', fg='white', bd=5, command=self.toggle_button_clicked)
        self.toggle_button.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)

        # Date settings
        today = date.today()
        actual_date = today.strftime("%d. %B %Y")
        actual_date = actual_date.split()
        
        # Automatic translation of the month in German language
        actual_date[1] = self.translate_text(actual_date[1])
        
        # Add label to display the date
        label_date = Label(self, text=actual_date, font=text_style_big, bg='black', fg='white', bd=25)
        label_date.place(relx=0.5, rely=0.25, relwidth=0.4, anchor='n')

        # Clock settings
        self.time_live = tk.StringVar() 
        self.label = Label(self, textvariable=self.time_live,font=text_style_big, bg='black', fg='white', bd=25)
        self.label.place(relx=0.5, rely=0.35, relwidth=0.2,  anchor='n')
    
        # Embedding of escape to close the GUI
        self.bind('<Escape>', (lambda event: exit()))

        # Request of function digital_clock()
        self.digital_clock()

        # Get the weather data by calling the function 'get_weather_data' with API_KEY and CITY  
        weather_data = self.get_weather_data(API_KEY, CITY)
        
        # Display error message if program fails to get weather data from OpenWeather
        if weather_data is None:

            error_label = tk.Label(self, text="Error retrieving weather data.")
            error_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.4)
            return

        # Unpack weather data
        temperature, weather_desc, humidity, wind_speed, icon_id = weather_data

        # Automatic translation of weather descriptions from:
        # https://openweathermap.org/weather-conditions
        german_weather = self.translate_text(weather_desc)

        # Create label for weather data
        weather_label = tk.Label(self, text=f"Stadt: {CITY}\nWetter (eng): {weather_desc}\nWetter (de): {german_weather}\nTemperatur: {temperature}°C\nLuftfeuchtigkeit: {humidity}%\nWindgeschwindigkeit: {wind_speed} m/s", font=text_style_tiny, bg='black', fg='white')
        weather_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.4)

        # If query to select the right weather image.
        # Weather conditions according to:
        # https://openweathermap.org/weather-conditions
        if icon_id == "01d" or icon_id == "01n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/sonne.png').resize((150,150)))
        elif icon_id == "02d" or icon_id == "02n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/sonne_wolken.png').resize((150,100)))
        elif icon_id == "03d" or icon_id == "03n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/wolkig2.png').resize((150,100)))
        elif icon_id == "04d" or icon_id == "04n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/wolkig.png').resize((150,100)))
        elif icon_id == "09d" or icon_id == "09n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/sonne_regen.png').resize((150,150)))
        elif icon_id == "10d" or icon_id == "10n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/regen.png').resize((150,100)))
        elif icon_id == "11d" or icon_id == "11n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/gewitter.png').resize((150,100)))
        elif icon_id == "13d" or icon_id == "13n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/schnee.png').resize((150,100)))
        elif icon_id == "50d" or icon_id == "50n":
            picture_weather = ImageTk.PhotoImage(Image.open('img/nebel.png').resize((150,100)))
        else:
            picture_weather = ImageTk.PhotoImage(Image.open('img/unknown.png').resize((150, 150)))

        # Weather image settings
        label_w_pic = Label(self, bg='black', height=200, width=200)
        label_w_pic.configure(image=picture_weather)
        label_w_pic.image = picture_weather
        label_w_pic.place(relx=0.2, rely=0.4,anchor='n')


    def get_weather_data(self, api_key, city):
        """Get the weather data from OpenWeather API

        Parameters
        ----------
        api_key : String containing the API key of the OpenWeather user account
        city : String containing the name of the city

        Returns
        -------
        temperature : Float containing the temperature in °C
        weather_desc : String containing the English weather description
        humidity : Integer containing the humidity in %
        wind_speed : Float containing the wind speed in m/s
        icon_id : String containing the icon ID for the image
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temperature = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            icon_id = data["weather"][0]["icon"]
            return temperature, weather_desc, humidity, wind_speed, icon_id
        else:
            print(f"Error: {data['message']}")
            return None

    
    def exit(self, event):
        """Embedding the escape button to close the GUI
        
        Parameters
        ----------
        event : event
                appeals function exit()      
        """
        self.destroy()


        
    def digital_clock(self): 
        """Embedding the clock
        """
        self.time_live.set( time.strftime("%H:%M:%S"))
        self.after(1000, self.digital_clock)


    def button1_clicked(self):
        """Calls function 'send_receive_serial_message if button 1 is clicked.
        """

        # Choose the port of the Bluetooth module
        port = 'COM5'  

        # Choose the baud rate
        baudrate = 9600 
        
        # Choose the message to send
        message = "0"

        # Call function 'send_receive_serial_message'
        self.send_receive_serial_message(port, baudrate, message)

    def button2_clicked(self):
        """Calls function 'send_receive_serial_message if button 2 is clicked.
        """

        # Choose the port of the Bluetooth module
        port = 'COM5'  

        # Choose the baud rate
        baudrate = 9600  
        
        # Choose the message to send
        message = "1"

        # Call function 'send_receive_serial_message'
        self.send_receive_serial_message(port, baudrate, message)

    def button3_clicked(self):
        """Calls function 'send_receive_serial_message if button 3 is clicked.
        """

        # Choose the port of the Bluetooth module
        port = 'COM5'  

        # Choose the baud rate
        baudrate = 9600  

        # Choose the message to send
        message = "2"

        # Call function 'send_receive_serial_message'
        self.send_receive_serial_message(port, baudrate, message)

    def button4_clicked(self):
        """Calls function 'send_receive_serial_message if button 4 is clicked.
        """

        # Choose the port of the Bluetooth module
        port = 'COM5'  

        # Choose the baud rate
        baudrate = 9600  

        # Choose the message to send
        message = "3"

        # Call function 'send_receive_serial_message'
        self.send_receive_serial_message(port, baudrate, message)

    def toggle_button_clicked(self):              
        """Toggle the visibility of the other four buttons, when toggle_button is clicked.
        """

        # If the buttons are visible, hide them and set visibility to 'False'
        if self.button_visibility:
            self.button1.place_forget()
            self.button2.place_forget()
            self.button3.place_forget()
            self.button4.place_forget()
            self.output_label.place_forget()
            self.output_frame.place_forget()
            self.interpretation_label.place_forget()
            self.button_visibility = False
        else:

            # Place the buttons at the same position as before and set visibility to 'True'
            self.button1.place(relx=0.7, rely=0.85, relwidth=0.2, relheight=0.1)
            self.button2.place(relx=0.7, rely=0.65, relwidth=0.2, relheight=0.1)
            self.button3.place(relx=0.7, rely=0.75, relwidth=0.2, relheight=0.1)
            self.button4.place(relx=0.7, rely=0.55, relwidth=0.2, relheight=0.1)
            self.output_label.place(relx=0.7, rely=0.2)
            self.output_frame.place(relx=0.7, rely=0.25, relwidth=0.2, relheight=0.2)
            self.interpretation_label.place(relx=0.7, rely=0.43, relwidth=0.2, relheight=0.2)
            self.button_visibility = True

    def send_receive_serial_message(self, port, baudrate, message):
        """Sends and receives serial messages to the Arduino Bluetooth module.

        Parameters
        ----------
        port : String containing the serial port
        baudrate : Integer containing the baud rate
        message : String containing the message to send
        """

        # Initialise serial connection
        ser = serial.Serial(port, baudrate)

        # Check connection
        if ser.is_open:
            print(f"Verbindung zur seriellen Schnittstelle {port} hergestellt.")

        # Send data to the Bluetooth module
        ser.write(message.encode())

        # Receive data from the Bluetooth module
        data = ser.readline().decode().strip()
    
        # Close serial connection
        ser.close()
        if not ser.is_open:
            print("Serielle Verbindung geschlossen.")

        # Update the Output Frame label with the contents of 'data'             
        if data == "LEDs OFF": 
            self.output_frame_label.config(text=data)
            self.interpretation_label.config(text="Keine Interpretation")
        else:
            # Split data into separate values for color temperature and illuminance
            separate_values = data.split(',')
            colorTemp = separate_values[0].strip()
            lux = separate_values[1].strip()
            
            # Set the values to the Output Frame Label
            self.output_frame_label.config(text=f"Farbtemperatur:\n{colorTemp} K\nBeleuchtungsstärke:\n{lux} lx")
            
            # Set the interpretation label according to the minimal lux value of DIN EN 12464-1
            if int(lux) >= 500:
                self.interpretation_label.config(text="Die Beleuchtung ist ausreichend.")
            else:
                self.interpretation_label.config(text="Die Beleuchtung ist zu dunkel.")

    def translate_text(self, text):
        """Use the 'translate' package to translate English text
            to German automatically. May not always be accurate.
        
        Parameters
        ----------
        text : String containing the text to translate.

        Returns
        -------
        translated_text : String containing the translated text.
        """
        translator = Translator(to_lang="de")
        translated_text = translator.translate(text)
        return translated_text

if __name__ == "__main__":

    # create object of the GUI class
    root = Gui()
    root.mainloop()