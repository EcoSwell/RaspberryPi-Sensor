## <u>EcoSwell Multi-Sensor Documentation</u> 

The EcoSwell Multi-Sensor is easy to use and can measure eight different data types with adjustable parameters for data recording, including reading frequency and duration of data recording. The sensor can measure the following data types:

| Data type           | Unit  | Unit description                                             |
| ------------------- | ----- | ------------------------------------------------------------ |
| Temperature*        | *C    | Degrees celcius                                              |
| Pressure            | hPa   | Hectopascal                                                  |
| Humidity            | %     | Relative humidity as percentage                              |
| Light               | Lux   | Luminious flux per unit area                                 |
| Carbon monoxide*    | -     | Arbitrary - measure changes relative to baseline value (TODO) |
| Nitrogen dioxide*   | -     | Arbitrary - measure changes relative to baseline value (TODO) |
| Ammonia*            | -     | Arbitrary - measure changes relative to baseline value (TODO) |
| Particulate matter* | ug/m3 | Micrograms per cubic metre of air                            |

*see section **Data Type Details** for more details



## **Overview** 

The sensor is contained within a plastic container and comprises of three components: Raspberry Pi (model 4), [Enviro+ Sensor Board](https://shop.pimoroni.com/products/enviro?variant=31155658457171) and [PMS5003 Air Quality Sensor](https://www.adafruit.com/product/3686), all of which are stored inside a waterproof storage box for ease of transport and monitoring. The Raspberry Pi is the 'brain' of the sensor; it executes the code which controls the sensors, processes the data recorded by the sensors and uploads this data to the GitHub Repository (see section **GitHub Repository** for more details). The two sensors together contain the components which measure the eight data types listed above. 

While the sensor settings must be modified online using the GitHub Repository, the sensor can operate either online or offline. Whilst reading are being recorded, all data will be saved locally to the Raspberry Pi, so no data will be lost if power to the sensor temporarily fails. Once data is finished being recorded, the Raspberry Pi will send the latest data files to an email address chosen by the user when it connects to the internet.

The sensor also contains an LCD screen which will display status updates and feedback where appropriate.



## **Raspberry Pi Diagram**

<img width="1185" alt="image" src="https://user-images.githubusercontent.com/113472300/191482319-f8906cb5-15f9-4cae-9df4-d2081a99f952.png">

The Raspberry Pi has loads of different ports and components, but luckily you don't need to worry about most of them! The two ports you need to be aware of are shown clearly in the diagram above, and are used during the initial setup process (see section **How To Use The Sensor** / **<u>Initial setup</u>**)





## **GitHub Repository**

The operational code and sensor settings are stored on an online platform called *GitHub* inside something called a repository. A repository (or 'repo') is essentially a collection of files (code, images, text files - anything goes) that is stored in an online server and can be accessed from anywhere in the world - think of it a bit like Microsoft OneDrive or Google Drive. For our EcoSwell Multi-Sensor, the repo is called [*RaspberryPi-Sensor*](https://github.com/EcoSwell/RaspberryPi-Sensor) and it belongs to the EcoSwell GitHub account. To edit any files inside this repo, you must be logged into the EcoSwell GitHub account - here are the login details:

​	*username:* EcoSwell	

​	*email:* info@ecoswell.org

​	*password*: *5u5t@1n@b1l1ty*

The GitHub repo looks a little like this:

<img width="1321" alt="image" src="https://user-images.githubusercontent.com/113472300/191482386-95a5ce68-2faf-47cd-aa3f-60135aaf7b7a.png">


You will see three important things in the GitHub repo:

1. *code* folder - you can <u>ignore</u> all files in this folder, unless you want/need to modify the sensor's core operational code
2. *README.md* file - this documentation you're readin right now!
3. *sensor_settings.py* file - this file is <u>important</u> as it allows you to set which sensors are active, how often readings are taken and the duration of the data readings



## **How To Use The Sensor**



<u>**Sensor settings**</u>

The sensor settings are adjusted in an online file called *sensor_settings.py* which is stored in the GitHub repo, and looks a bit like this:

<img width="1243" alt="image" src="https://user-images.githubusercontent.com/113472300/191482443-0ad89e6f-170c-4db2-8136-0776392eb864.png">


1. To modify the sensor settings you must edit the file *sensor_settings.py* by clicking the *pen icon* circled above

2. To change which email address the files storing the data reading's are sent to, follow the instructions in *sensor_settings.py* under the heading `EMAIL ADDRESS`  

3. To change which sensors are active, the reading frequency for each sensor and the duration of data recording for each sensor, follow the instructions in *sensor_settings.py* under the heading `ACTIVE SENSORS, FREQUENCY OF DATA RECORDING & DURATION OF DATA RECORDING`

4. Note: If you wish to activate the temperature sensor (sensor no. 1), then you must first adjust the value of *factor* in the file *sensor_settings.py* under the heading `ADJUST TEMPERATURE TUNING FACTOR` to calibrate the sensor - see section **Data Type Details** / **<u>Temperature</u>** for instructions

5. To save your changes to the sensor settings file *sensor_settings.py*, click the *commit changes* button circled below:

<img width="1200" alt="image" src="https://user-images.githubusercontent.com/113472300/191482517-6af56b31-556f-4876-9872-2b1277ed3eb0.png">


4. Finally, to sync these changes with the sensor, plug an ethernet cable into the Raspberry Pi *ethernet port*  (see **Raspberry Pi Diagram**) to connect the sensor to the internet and wait around 1 minute

 

<u>**Start sensor readings**</u>

1. Power up sensor by plugging micro USB power cable into Raspberry Pi *micro USB port* (see **Raspberry Pi Diagram**) - the LCD should display this message as the sensor turns on:

<img width="1039" alt="image" src="https://user-images.githubusercontent.com/113472300/191482584-039154ca-5f2f-4e6a-bccf-6178654f1597.png">



2. Wait until the LCD screen displays a welcome message, which also states whether the sensor is connected to the internet at boot:
<img width="1030" alt="image" src="https://user-images.githubusercontent.com/113472300/191482642-7a5d2f3c-bc9c-43ba-b220-7a00f2ff6f34.png">

3. To start the readings, place finger on proximity sensor (labelled `LIGHT` on sensor) for 5 seconds, or until the sensor's LCD screen displays the following message:
<img width="958" alt="image" src="https://user-images.githubusercontent.com/113472300/191482688-7de9cb1a-c813-4f87-8f66-4e6408e1ca22.png">

4. You now have 2 minutes to position the sensor in the desired location - after these 2 minutes, the readings will begin

5. Leave the sensor in place until all the readings are complete, which will be indicated on the LCD screen by the following message:

<img width="1038" alt="image" src="https://user-images.githubusercontent.com/113472300/191482802-450dc9c1-9d06-436f-beda-b4395cd111f2.png">





**<u>Download sensor data</u>**

1. Data files are sent with the *csv* format and named with the following format: `sensor type - start date - start time`
   - For example, a file named `co-16.09.2022-12:58` would store carbon monoxide data readings which started to be measured at 12:58 on 16/09/2022 
2. Plug ethernet cable into Raspberry Pi *ethernet port* (see **Raspberry Pi Diagram**) 
3. All data recorded by the sensor will be emailed to the email address entered in the *sensor_settings.py* file 
4. Once you have saved the *csv* data file from the email, you can open it in Excel and perform required analysis



<u>**Restart sensor readings**</u>

1. If you want to restart the sensor readings mid data recording, you must place finger on proximity sensor (labelled `Start`) for at least 25 seconds - don't worry, the current data will be saved! 

2. The LCD display will show the following message:

<img width="1031" alt="image" src="https://user-images.githubusercontent.com/113472300/191482855-0a3bec87-2350-460b-9091-c3358c05bfc7.png">


3. To cancel the restart, simply remove your finger from the proximity sensor (labelled `Start`) - the LED display will show the following response:
<img width="1039" alt="image" src="https://user-images.githubusercontent.com/113472300/191482888-7d2fb44c-f42d-45d1-b67d-788fc3791bf0.png">



## **Data Type Details**

**<u>Temperature</u>**

The temperature reading must be adjusted slightly to compensate for the heating effect of the CPU (computer processing unit on the sensor). To tweak how much the temperature value is compensated, follow these steps:

1. Set `calculate_factor` to `True` in the file *sensor_settings.py*, as shown below:
<img width="1326" alt="image" src="https://user-images.githubusercontent.com/113472300/191482999-0b5d130a-1169-4b97-a460-90493e79d70e.png">

   

2. Follow the steps in section **How To Use The Sensor** / **<u>Start sensor readings</u>** to begin the sensor readings

3. Open the Excel file [*Calculate temp factor*](https://docs.google.com/spreadsheets/d/1BLTTYUCHuqEoowzhjQEQhzlOlSYHIbCMgoVQX1paT3U/edit?usp=sharing):

   ![image-20220916222157041](/Users/orlandoalexander/Library/Application Support/typora-user-images/image-20220916222157041.png)

   

4. Use an external temperature sensor to record the temperature surrounding the sensor every 60 seconds for 10 minutes, starting when the sensor begins to record data. Record each data value in the `External temperature sensor (*C)` column within the Excel file

5. Download the data (see **<u>Download sensor data</u>** for details) and import the two data columns (`Data 1` and `Data 2`) into the columns with the same headers in the Excel file 

6. The required temperature compensation factor will be displayed at the bottom of the Excel file

7. Set `Factor` in *sensor_settings.py* to this calculated temperature compensation factor 



**<u>Carbon monoxide</u>**

The data values for the carbon monoxide readings are given in arbitrary units (technically, they are given as resistance values - but don't worry about this!). Therefore, it is not possible to measure exact concentrations of carbon monoxide in parts per million. Instead, you should use the results to measure the change in the concentration of carbon monoxide particles in the air relative to the baseline value of (TODO) - this value was calculated in an open space away from any buildings or sources of pollution.

**Important**: the carbon monoxide gas readings will *drop* with increasing concentration of carbon monoxide gas detected.

**Important**: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.



**<u>Nitrogen dioxide</u>**

The data values for the nitrogen dioxide readings are given in arbitrary units (technically, they are given as resistance values - but don't worry about this!). Therefore, it is not possible to measure exact concentrations of nitrogen dioxide in parts per million. Instead, you should use the results to measure the change in the concentration of nitrogen dioxide particles in the air relative to the baseline value of (TODO) - this value was calculated in an open space away from any buildings or sources of pollution.

**Important**: the nitrogen dioxide gas readings will *increase* with increasing concentration of the nitrogen dioxide gas detected. 

**Important**: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.



**<u>Ammonia</u>**

The data values for the ammonia readings are given in arbitrary units (technically, they are given as resistance values - but don't worry about this!). Therefore, it is not possible to measure exact concentrations of ammonia in parts per million. Instead, you should use the results to measure the change in the concentration of ammonia particles in the air relative to the baseline value of (TODO) - this value was calculated in an open space away from any buildings or sources of pollution.

**Important**: the ammonia gas readings will *drop* with increasing concentration of the ammonia gas detected. 

**Important**: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.



**<u>Particulate matter</u>**

Unlike the other data types, the particulate matter sensor records three data values: PM1.0, PM2.5 and PM10. These values refer to the size of the particles; PM10 readings include particles of 10 microns and smaller, PM2.5 readings include particles of 2.5 microns and smaller, and PM1.0 readings include particles of 1 micron and smaller. 











