'''Edit this file to modify the settings of the sensor'''

'''
EMAIL ADDRESS

Enter the email address to which the files storing the data readings should be sent:
'''
email_address = 'hugo.fernandez@ecoswell.org'


'''
ACTIVE SENSORS, FREQUENCY OF DATA RECORDING & DURATION OF DATA RECORDING 

The sensor has the following sensors: 

1. Temperature
2. Pressure
3. Humidity
4. Light
5. Carbon monoxide
6. Nitrogen dioxide
7. Ammonia 
8. Particulate matter

Modify the values inside the brackets below for each active sensor with the following format 
(sensor number, delay between readings (secs), duration of data recording (mins)) 
i.e. to measure temperature and ammonia with a time delay between readings of 60 and 120 secs 
and a data recording duration of 4 hours and 7 hours respectively, you should write [(1,60,240), (7,120,420)]
'''
sensors = [(1,60,3), (2,60,3), (3,60,3), (4,60,3), (5,60,3), (6,60,3), (7,60,3), (8,60,3)]



'''
ADJUST TEMPERATURE TUNING FACTOR

The temperature reading must be adjusted slightly to compensate for the heating effect of the CPU (computer processing unit on the sensor). 
To determine the factor required to correctly compensate the tenmperature reading, 
set 'calculate_temp_factor' to True and follow the instructions in the documentation (README.md).
Note: if you want to calculate the temperature tuning factor, 'calculate_gas_factor' must be set to False.
'''
calculate_temp_factor = False

factor = 1.31


'''
GAS CALIBRATION

To obtain gas readings in ppm, you must first calibrate the sensors by taking readings of gas concentration in an open space away from buildings (e.g. a field).
To calibrate the gas sensors, set 'calculate_gas_factor' to True and follow the instructions in the documentation (README.md).
Note: if you want to calculate the gas calibration factor, 'calculate_temp_factor' must be set to False.
'''
calculate_gas_factor = False

"""
TECHNICAL INFORMATION

All files on Raspberry Pi can be accessed over SSH from a laptop by entering 'ssh ecoswell@ecoswell.local' on the laptop's command line. 
When prompted to enter the password, enter 'EcoSwell'

Raspberry Pi details:
hostname: ecoswell.local
username: ecoswell
password: EcoSwell

The sensor settings file 'sensor_settings.py' is downloaded from the Github repository onto the Raspberry Pi every minute 
(where Raspberry Pi is connected to internet) using cron job on Raspberry Pi (access with 'sudo crontab -e')
"""
