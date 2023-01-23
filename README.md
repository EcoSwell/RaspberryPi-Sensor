## <u>EcoSwell Multi-Sensor Documentation</u> 

The EcoSwell Multi-Sensor is easy to use and can measure up to eight different data types simultaneously. The sensor is versatile with adjustable parameters for data recording, including reading frequency and duration of data recording. The sensor can measure the following data types:

| Data type           | Unit  | Unit description                                             |
| ------------------- | ----- | ------------------------------------------------------------ |
| Temperature*        | *C    | Degrees celcius                                              |
| Pressure            | hPa   | Hectopascal                                                  |
| Humidity            | %     | Relative humidity as percentage                              |
| Light               | Lux   | Luminious flux per unit area                                 |
| Carbon monoxide*    | PPM   | Parts per million                                            |
| Nitrogen dioxide*   | PPM   | Parts per million                                            |
| Ammonia*            | PPM   | Parts per million                                            |
| Particulate matter* | ug/m3 | Micrograms per cubic metre of air                            |

*see section **Data Type Details** for more details

## **Disclaimers**

Whenever you want to make a change or cancel a sensor reading, it is better to log into the ssh and manually use the command "sudo reboot" instead of unplugging the USB C cable.

## **Overview** 

The sensor is contained within a plastic container and comprises of three components: Raspberry Pi (model 4), [Enviro+ Sensor Board](https://shop.pimoroni.com/products/enviro?variant=31155658457171) and [PMS5003 Air Quality Sensor](https://www.adafruit.com/product/3686), all of which are stored inside a waterproof storage box for ease of transport and monitoring. The Raspberry Pi is the 'brain' of the sensor; it executes the code which controls the sensors, processes the data recorded by the sensors and emails the data to you when it's finished. The two sensors together contain the components which measure the eight data types listed above. 

While the sensor settings must be modified online using the GitHub Repository, the sensor can operate either online or offline. Whilst reading are being recorded, all data will be saved locally to the Raspberry Pi, so no data will be lost if power to the sensor temporarily fails. Once data is finished being recorded, the Raspberry Pi will send the latest data files to an email address chosen by the user when it connects to the internet.

The sensor also contains an LCD screen which will display status updates and feedback where appropriate.



## **Raspberry Pi Diagram**

<img width="1185" alt="image" src="https://user-images.githubusercontent.com/113472300/191482319-f8906cb5-15f9-4cae-9df4-d2081a99f952.png">

The Raspberry Pi has loads of different ports and components, but luckily you don't need to worry about most of them! The two ports you need to be aware of are shown clearly in the diagram above, and are used during the initial setup process (see section **How To Use The Sensor** / **<u>Initial setup</u>**)





## **GitHub Repository**

The operational code and sensor settings are stored on an online platform called *GitHub* inside something called a repository. A repository (or 'repo') is essentially a collection of files (code, images, text files - anything goes) that is stored in an online server and can be accessed from anywhere in the world - think of it a bit like Microsoft OneDrive or Google Drive. For our EcoSwell Multi-Sensor, the repo is called [*RaspberryPi-Sensor*](https://github.com/EcoSwell/RaspberryPi-Sensor) and it belongs to the EcoSwell GitHub account. To edit any files inside this repo, you must be logged into the EcoSwell GitHub account.



The GitHub repo looks a little like this:

<img width="1321" alt="image" src="https://user-images.githubusercontent.com/113472300/191482386-95a5ce68-2faf-47cd-aa3f-60135aaf7b7a.png">


You will see three important things in the GitHub repo:

1. *code* folder - you should <u>ignore</u> all files in this folder (unless you need to modify the sensor's core operational code - this can cause issues if done incorrectly so contact Orlando Alexander if you need to modify the code) 
2. *README.md* file - this documentation you're reading right now!
3. *sensor_settings.py* file - this file is <u>important</u> as it allows you to set which sensors are active, how often readings are taken and the duration of the data readings





## **How To Use The Sensor**



<u>**Sensor settings**</u>

The sensor settings are adjusted in an online file called *sensor_settings.py* which is stored in the GitHub repo, and looks a bit like this:

<img width="1243" alt="image" src="https://user-images.githubusercontent.com/113472300/191482443-0ad89e6f-170c-4db2-8136-0776392eb864.png">


1. Plug an ethernet cable into the Raspberry Pi *ethernet port* (see **Raspberry Pi Diagram**) to connect the sensor to the internet - this *must* be done before powering up the Raspberry Pi
2. Power up sensor by plugging USB-C power cable into Raspberry Pi *USB-C port* (see **Raspberry Pi Diagram**) 
3. To modify the sensor settings you must edit the file *sensor_settings.py* by clicking the *pen icon* circled above
4. To change which email address the files storing the data reading's are sent to, follow the instructions in *sensor_settings.py* under the heading `EMAIL ADDRESS`  
5. To change which sensors are active, the reading frequency for each sensor and the duration of data recording for each sensor, follow the instructions in *sensor_settings.py* under the heading `ACTIVE SENSORS, FREQUENCY OF DATA RECORDING & DURATION OF DATA RECORDING`
6. Note: If you wish to activate the temperature sensor (sensor no. 1), then you must first adjust the value of *factor* in the file *sensor_settings.py* under the heading `ADJUST TEMPERATURE TUNING FACTOR` to calibrate the sensor - see section **Data Type Details** / **<u>Temperature</u>** for instructions
7. To save your changes to the sensor settings file *sensor_settings.py*, click the *commit changes* button circled below:

<img width="1200" alt="image" src="https://user-images.githubusercontent.com/113472300/191482517-6af56b31-556f-4876-9872-2b1277ed3eb0.png">


8. Finally, to sync these changes with the sensor, wait 2 minutes and then unplug USB-C power cable.

 

<u>**Start sensor readings**</u>

1. Power up sensor by plugging USB-C power cable into Raspberry Pi *USB-C port* (see **Raspberry Pi Diagram**) - the LCD should display this message as the sensor turns on:

<img width="1039" alt="image" src="https://user-images.githubusercontent.com/113472300/191482584-039154ca-5f2f-4e6a-bccf-6178654f1597.png">



2. Wait until the LCD screen displays a welcome message - this also states whether the sensor is connected to the internet (remember, the sensor does not need to be connected to the internet to take data readings):
<img width="1030" alt="image" src="https://user-images.githubusercontent.com/113472300/191482642-7a5d2f3c-bc9c-43ba-b220-7a00f2ff6f34.png">

3. To start the readings, place finger on proximity sensor (labelled `LIGHT` on sensor) for 5 seconds, or until the sensor's LCD screen displays the following message:
<img width="958" alt="image" src="https://user-images.githubusercontent.com/113472300/191482688-7de9cb1a-c813-4f87-8f66-4e6408e1ca22.png">

4. You now have 2 minutes to position the sensor in the desired location - after these 2 minutes, the readings will begin
 <img width="960" alt="image" src="https://user-images.githubusercontent.com/113472300/191821833-d4838901-a1af-425a-b67c-9c5c705e7513.png">


5. Leave the sensor in place until all the readings are complete, which will be indicated on the LCD screen by the following message:

<img width="1038" alt="image" src="https://user-images.githubusercontent.com/113472300/191482802-450dc9c1-9d06-436f-beda-b4395cd111f2.png">




**<u>Download sensor data</u>**

1. Data files are sent with the *csv* format and named with the following format: `sensor type - start date - start time`
   - For example, a file named `co-16.09.2022-12:58` would store carbon monoxide data readings which started to be measured at 12:58 on 16/09/2022 
2. Plug an ethernet cable into the Raspberry Pi *ethernet port* (see **Raspberry Pi Diagram**) to connect the sensor to the internet - this *must* be done before powering up the Raspberry Pi
3. Power up sensor by plugging USB-C power cable into Raspberry Pi *USB-C port* (see **Raspberry Pi Diagram**) 
4. All data recorded by the sensor will be emailed to the email address entered in the *sensor_settings.py* file - please check your spam!
5. Once you have saved the *csv* data file from the email, you can open it in Excel and perform required analysis



<u>**Restart sensor readings**</u>

1. If you want to restart the sensor readings mid data recording, you must place finger on proximity sensor (labelled `Light`) for at least 25 seconds - don't worry, the current data will be saved! 

2. The LCD display will show the following message:

<img width="1031" alt="image" src="https://user-images.githubusercontent.com/113472300/191482855-0a3bec87-2350-460b-9091-c3358c05bfc7.png">


3. To cancel the restart, simply remove your finger from the proximity sensor (labelled `Light`) - the LED display will show the following response:
<img width="1039" alt="image" src="https://user-images.githubusercontent.com/113472300/191482888-7d2fb44c-f42d-45d1-b67d-788fc3791bf0.png">



## **Data Type Details**

**<u>Temperature</u>**

The temperature reading must be adjusted slightly to compensate for the heating effect of the CPU (computer processing unit on the sensor). To tweak how much the temperature value is compensated, follow these steps:

1. Set `calculate_temp_factor` to `True` in the file *sensor_settings.py*, as shown below:
<img width="1326" alt="image" src="https://user-images.githubusercontent.com/113472300/191482999-0b5d130a-1169-4b97-a460-90493e79d70e.png">

   

2. Follow the steps in section **How To Use The Sensor** / **<u>Start sensor readings</u>** to begin the sensor readings

3. Open the Excel file [*Calculate temp factor*](https://docs.google.com/spreadsheets/d/1BLTTYUCHuqEoowzhjQEQhzlOlSYHIbCMgoVQX1paT3U/edit?usp=sharing):

 <img width="854" alt="image" src="https://user-images.githubusercontent.com/113472300/191829640-ca0add3e-b732-4bd6-9100-6787fab487e1.png">

   

4. Use an external temperature sensor to record the temperature surrounding the sensor every 60 seconds for 10 minutes, starting when the sensor begins to record data. Record each data value in the `External temperature sensor (*C)` column within the Excel file

5. Download the data (see **<u>Download sensor data</u>** for details) and import the two data columns (`Data 1` and `Data 2`) into the columns with the same headers in the Excel file 

6. The required temperature compensation factor will be displayed at the bottom of the Excel file

7. Set `Factor` in *sensor_settings.py* to this calculated temperature compensation factor 

**<u>Gas Readings</u>**

1. To calibrate the gas readings you need to set calculate_gas_factor to True. Save and leave the Raspberry Pi on for 2 minutes for changes to save.

2. Unplug the Raspberry Pi. Take the sensor to an open space and set up for taking readings. Power on the Raspberry Pi and the sensor LCD screen will display "Gas calibration starting in 10 mins" (after you hold your finger over the light sensor for 5 seconds). Allow the sensor time to calibrate after these 10 mins.

3. Unplug Raspberry Pi. The calibration factor for all three gases will be calculated automatically so that next time you take gas readings they will be in ppm.

4. When going to take actual readings make sure to set calculate_gas_factor back to False. Save and leave the Raspberry Pi on for 2 minutes for changes to save. Reboot to then take readings. The LCD screen should follow the pattern described in the section "Start sensor readings".



<u>**Carbon monoxide**</u>

The data values for the carbon monoxide readings are given in Parts Per Million.

_Important_: the carbon monoxide gas readings will *drop* with increasing concentration of carbon monoxide gas detected.

_Important_: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.

_Important_: the first reading is an anomaly so ignore this.



**<u>Nitrogen dioxide</u>**

The data values for the nitrogen dioxide readings are given in Parts Per Million.

_Important_: the nitrogen dioxide gas readings will *increase* with increasing concentration of the nitrogen dioxide gas detected. 

_Important_: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.

_Important_: the first reading is an anomaly so ignore this.


**<u>Ammonia</u>**

The data values for the ammonia readings are given in Parts Per Million.

_Important_: the ammonia gas readings will *drop* with increasing concentration of the ammonia gas detected. 

_Important_: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.

_Important_: the first reading is an anomaly so ignore this.


**<u>Particulate matter</u>**

Unlike the other data types, the particulate matter sensor records three data values: PM1.0, PM2.5 and PM10. These values refer to the size of the particles; PM10 readings include particles of 10 microns and smaller, PM2.5 readings include particles of 2.5 microns and smaller, and PM1.0 readings include particles of 1 micron and smaller. 




## **Technical Info**

Please ignore this section, unless you need to make changes to sensor's core code.

- All files on Raspberry Pi can be accessed over SSH from a laptop:

  1. Connect to *EcoHouse* wifi
  2. Enter `ssh ecoswell@ecoswell.local` on the laptop's command line
  3. When prompted to enter the password, enter `EcoSwell`

  **Important:** *DO NOT* modify any files directly on the Raspberry Pi - instead, clone the GitHub repository to a seperate device and push these changes to the GitHub repository

  

-  Raspberry Pi details:

  1. Hostname: *ecoswell.local*

  2. Username: *ecoswell*

  3. Password: *EcoSwell*

     

- SSH into Raspberry Pi remotely using [SocketXP](https://portal.socketxp.com/#/devices)



- Cloning GitHub repository onto Raspberry Pi
  1. Clone HTTPS 
  2. Run `chmod a+x RaspberryPi-Sensor` on Raspberry Pi command line








