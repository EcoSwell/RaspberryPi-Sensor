'''
Take measurements of desired environmental factors and save data to CSV file
'''

import sys
path = '/home/ecoswell/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
import sensor_settings
import time
import threading
import os.path
import csv
import math
from datetime import datetime
from lcd_display import display_text, backlight_off, backlight_on


try:
    # transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559() # initialise LTR559 light/proximity sensor
except ImportError:
    import ltr559
from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas

bme280 = BME280() # initialise BME280 temperature/pressure/humidity sensor
pms5003 = PMS5003() # intitialise PMS5003 particulate sensor



class SensorReadings(): # class containing methods to take sensor readings
    def __init__(self):
        now = datetime.now() # get current date and time
        self.date = now.strftime("%d.%m.%Y") # get date when sensor readings begin in correct format
        self.time = now.strftime("%H:%M:%S") # get time when sensor readings begin in correct format
        self.sensors = sensor_settings.sensors # access sensor settings defined by user in file 'sensor_settings.py' 
        self.factor = sensor_settings.factor # access factor by which temperature reading is compensated as defined by user in file 'sensor_settings.py' 
        self.calculate_temp_factor = sensor_settings.calculate_temp_factor # boolean which stores whether user wishes to calculate the temperature compensation factor
        self.calculate_gas_factor = sensor_settings.calculate_gas_factor # boolean which stores whether user wishes to calibrate the gas sensors      
        self.sensors_dict = {1:self.temp_queue, 2:self.pressure_queue, 3:self.humidity_queue, 4:self.light_queue, 5:self.co_queue, 6:self.no2_queue, 7:self.nh3_queue, 8:self.pm_queue} # dictionary to translate between sensor number and sensor queue method (which triggers sensor execution)
        self.queue = [] # queue stores sensors which are due to take readings - this avoids multiple sensors taking readings simultaneously and therefore prevents collisions
        self.sensor_status = [False for i in range(8)] # queue stores status of each sensor (True = active, False = inactive)
        cpu_temp = self.get_cpu_temperature() # take initial reading to stabalise sensor
        self.cpu_temps = [self.get_cpu_temperature()] * 5 # get five readings of CPU temperature
        self.co_factor, self.no2_factor, self.nh3_factor = None, None, None # assign each gas calibration factor to 'None' as default
        if os.stat('/home/ecoswell/RaspberryPi-Sensor/code/gas_factors.txt').st_size != 0: # if user has calculated calibration factor for gas readings
            with open('/home/ecoswell/RaspberryPi-Sensor/code/gas_factors.txt','r') as f: 
                gas_factors = f.readlines()
                self.co_R0, self.no2_R0, self.nh3_R0 = float(gas_factors[0].strip()), float(gas_factors[1].strip()), float(gas_factors[2].strip()) # get R0 value for each gas 
                f.close()

    def get_cpu_temperature(self): # get the temperature of the CPU for compensation
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = f.read()
                temp = int(temp) / 1000.0
            return temp

    def temp_factor(self): # record required data to allow user to calculate temperature compensation factor
        raw_temp = bme280.get_temperature() # take initial reading to stabalise sensor
        time.sleep(2)
        for i in range(15): 
            sensor = 'calculate_temp_factor'
            freq = 60
            dur = 15
            raw_temp = bme280.get_temperature() # get raw reading of temp
            cpu_temp = self.get_cpu_temperature() # get current CPU temperature
            self.cpu_temps = self.cpu_temps[1:] + [cpu_temp] # remove oldest reading of CPU temp and append latest reading of CPU temp to 'cpu_temps'
            avg_cpu_temp = sum(self.cpu_temps) / float(len(self.cpu_temps)) # get average of CPU temp to decrease jitter
            data_heading = ['Data 1','Data 2']
            data = [(avg_cpu_temp-raw_temp), raw_temp] # the two data values required to calculate the temperature compensation factor
            self.save_data(sensor, freq, dur, data, data_heading)
            time.sleep(60)
        self.save_data_final() # move data file to folder storing complete data files
        backlight_on() # turn on LCD backlight
        display_text('Temperature factor\n readings\n complete',17)
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return

    def gas_factor(self): # calculate value of R0 in open space to use as calibration factor to convert readings of gas from Rs to ppm (using Roscoe's conversion)
        gas_readings = [0 for i in range(3)] # empty list to store gas readings of co, no2 and nh3 
        gas_data = gas.read_all() # take initial reading to stabalise sensor
        for i in range (10): # take readings of R0 for each gas every minute for 10 mins
            gas_data = gas.read_all() # get readings of concentration of all gasses
            co = gas_data.reducing / 1000 # convert carbon monoxide gas concentration resistance into kOhm
            no2 = gas_data.oxidising / 1000 # convert nitrogen dioxide gas concentration into kOhm
            nh3 = gas_data.nh3 / 1000 # convert ammonia gas concentration resistance into kOhm
            gas_readings[0] += co # add together all co readings
            gas_readings[1] += no2 # add together all no2 readings
            gas_readings[2] += nh3 # add together all nh3 readings
            time.sleep(60)
        co_R0 = str(round(gas_readings[0]/10,2)) # store average R0 value for co 
        no2_R0 = str(round(gas_readings[1]/10,2)) # store average R0 value for no2 
        nh3_R0 = str(round(gas_readings[2]/10,2)) # store average R0 value for nh3 
        with open('/home/ecoswell/RaspberryPi-Sensor/code/gas_factors.txt','w') as f:
            f.write(f'{co_R0}\n{no2_R0}\n{nh3_R0}') # write R0 value of each gas to text file
            f.close()
        backlight_on() # turn on LCD backlight
        display_text('Gas calibration\n readings\n complete',17)
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return
        

    def temp_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'temp' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.temp) # add 'temp' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[0] = False # change temp sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Temperature\n readings\n complete',20) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return

    def temp(self): # measure temperature
        raw_temp = bme280.get_temperature() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'temp'
        freq = list(filter(lambda x: x[0] == 1, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for temp sensor (sensor number 1)
        dur = list(filter(lambda x: x[0] == 1, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for temp sensor (sensor number 1)
        data_heading = ['Temperature (*C)']
        cpu_temp = self.get_cpu_temperature() # get current CPU temperature
        self.cpu_temps = self.cpu_temps[1:] + [cpu_temp] # remove oldest reading of CPU temp and append latest reading of CPU temp to 'cpu_temps'
        avg_cpu_temp = sum(self.cpu_temps) / float(len(self.cpu_temps)) # get average of CPU temp to decrease jitter
        raw_temp = bme280.get_temperature() # get raw reading of temp
        compensated_temp = raw_temp - ((avg_cpu_temp - raw_temp) / self.factor) # temp value ajdusted to compensate for CPU heating
        data = [compensated_temp]
        self.save_data(sensor, freq, dur, data, data_heading)
        return

    def pressure_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'pressure' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.pressure) # add 'pressure' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[1] = False # change pressure sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Pressure\nreadings\ncomplete',20) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return

    def pressure(self): # measure pressue
        pressure = bme280.get_pressure() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'pressure'
        freq = list(filter(lambda x: x[0] == 2, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for pressure sensor (sensor number 2)
        dur = list(filter(lambda x: x[0] == 2, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for pressure sensor (sensor number 2)
        data_heading = ['Pressure (hPa)']
        pressure = bme280.get_pressure() # get reading of pressure
        data = [pressure]
        self.save_data(sensor, freq, dur, data, data_heading)
        return

    def humidity_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'humidity' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.humidity) # add 'humidity' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[2] = False # change humidity sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Humidity\nreadings\ncomplete',20) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return

    def humidity(self): # measure humidiity
        humidity = bme280.get_humidity() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'humidity'
        freq = list(filter(lambda x: x[0] == 3, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for humidity sensor (sensor number 3)
        dur = list(filter(lambda x: x[0] == 3, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for humidity sensor (sensor number 3)
        data_heading = ['Humidity (%)']
        humidity = bme280.get_humidity() # get reading of humidity
        data = [humidity]
        self.save_data(sensor, freq, dur, data, data_heading)
        return

    def light_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'light' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.light) # add 'light' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[3] = False # change light sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Light \nreadings \ncomplete',20) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return 

    def light(self): # measure light intensity
        light = ltr559.get_lux() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'light'
        freq = list(filter(lambda x: x[0] == 4, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for light sensor (sensor number 4)
        dur = list(filter(lambda x: x[0] == 4, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for light sensor (sensor number 4)
        data_heading = ['Light (lux)']
        proximity = ltr559.get_proximity() # get reading of proximity
        if proximity < 10: # no object near the sensor (small values of proximity indicate greater proximity)
            light = ltr559.get_lux() # get reading of light intensity
        else: # larger value of proximity --> closer proximity --> object near the sensor --> cannot take reading of light intensity
            light = 1 # dark
        data = [light]
        self.save_data(sensor, freq, dur, data, data_heading)
        return

    def co_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'co' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.co) # add 'co' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[4] = False # change co sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Carbon monoxide\nreadings \ncomplete',18) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return 

    def co(self): # measures concentration of carbon monoxide (reducing) gas
        gas_data = gas.read_all() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'co'
        freq = list(filter(lambda x: x[0] == 5, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for co sensor (sensor number 5)
        dur = list(filter(lambda x: x[0] == 5, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for co sensor (sensor number 5)
        data_heading = ['Carbon monoxide (ppm)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        co_Rs = gas_data.reducing / 1000 # convert carbon monoxide gas concentration resistance into kOhm
        if self.co_R0 != None: # if user has calculated calibration factor for gas readings
            co = math.pow(10, -1.25 * math.log10(co_Rs/self.co_R0) + 0.64) # convert co reading from kOhm to ppm (Roscoe method)
        else: 
            co = co_Rs
        data = [co]
        self.save_data(sensor, freq, dur, data, data_heading)
        return
    
    def no2_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'no2' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.no2) # add 'no2' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[5] = False # change light sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Nitrogen dioxide \nreadings \ncomplete',18) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return 

    def no2(self): # measures concentration of nitrogen dioxide (oxidising) gas
        gas_data = gas.read_all() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'no2'
        freq = list(filter(lambda x: x[0] == 6, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for no2 sensor (sensor number 6)
        dur = list(filter(lambda x: x[0] == 6, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for no2 sensor (sensor number 6)
        data_heading = ['Nitrogen dioxide (ppm)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        no2_Rs = gas_data.oxidising / 1000 # convert nitrogen dioxide gas concentration into kOhm
        if self.no2_R0 != None: # if user has calculated calibration factor for gas readings
            no2 = math.pow(10, math.log10(no2_Rs/self.no2_R0) - 0.8129) # convert no2 reading from kOhm to ppm (Roscoe method)
        else: 
            no2 = no2_Rs
        data = [no2]
        self.save_data(sensor, freq, dur, data, data_heading)
        return
    
    def nh3_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'nh3' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.nh3) # add 'nh3' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[6] = False # change nh3 sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Ammonia \nreadings \ncomplete',20) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return 
        
    def nh3(self): # measures concentration of ammonia gas
        gas_data = gas.read_all() # take initial reading to stabalise sensor
        time.sleep(2) 
        sensor = 'nh3'
        freq = list(filter(lambda x: x[0] == 7, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for nh3 sensor (sensor number 7)
        dur = list(filter(lambda x: x[0] == 7, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for nh3 sensor (sensor number 7)
        data_heading = ['Ammonia (ppm)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        nh3_Rs = gas_data.nh3 / 1000 # convert ammonia gas concentration resistance into kOhm
        if self.nh3_R0 != None: # if user has calculated calibration factor for gas readings
            nh3 = math.pow(10, -1.8 * math.log10(nh3_Rs/self.nh3_R0) - 0.163) # convert nh2 reading from kOhm to ppm (Roscoe method)
        else: 
            nh3 = nh3_Rs
        data = [nh3]
        self.save_data(sensor, freq, dur, data, data_heading)
        return

    def pm_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'pm' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.pm) # add 'pm' method to 'queue' at set intervals to take sensor readings at desired frequency
        time.sleep(dur)
        self.sensor_status[7] = False # change pm sensor status to False (i.e. inactive) as all readings are now complete
        backlight_on() # turn on LCD backlight
        display_text('Particulate matter \nreadings \ncomplete',17) # display sensor reading status on LCD once all readings are complete
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        return 

    def pm(self): # measures concentration of PM1.0, PM2.5 and PM10 particulate matter
        try:
            data = pms5003.read() # take initial reading to stabalise sensor
        except pmsReadTimeoutError:
            pass
        time.sleep(2) 
        sensor = 'pm'
        freq = list(filter(lambda x: x[0] == 8, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for pm sensor (sensor number 8)
        dur = list(filter(lambda x: x[0] == 8, self.sensors))[0][2] # lambda function filters list 'self.sensors' (which stores active sensors, delay between sensor readings and sensor reading duration in tuple format: (active sensor number, delay between sensor readings, sensor reading duration)) to access reading frequency for pm sensor (sensor number 8)
        data_heading = ['PM1.0 (ug/m3)','PM2.5 (ug/m3)', 'PM10 (ug/m3)']
        try:
            data = pms5003.read() # get readings of concentration of PM1.0, PM2.5 and PM10 particulate matter
        except pmsReadTimeoutError:
            display_text('Failed to read \nPMS5003',22) # display error message on LCD screen
            pass
        else:
            pm1 = float(data.pm_ug_per_m3(1.0)) # get readings of concentration of PM1.0
            pm25 = float(data.pm_ug_per_m3(2.5)) # get readings of concentration of PM2.5
            pm10 = float(data.pm_ug_per_m3(10)) # get readings of concentration of PM10
            data = [pm1,pm25,pm10]
            self.save_data(sensor, freq, dur, data, data_heading)
        return

    def save_data(self, sensor, freq, dur, data, data_heading): # save sensor data to CSV file
        data = [round(i, 3) for i in data] # round data values to 3 dp - must iterate over each element in list as data values stored in list
        filename = sensor+'-'+self.date+'-'+self.time+'.csv' # filename stores sensor type and current date
        if os.path.isfile(f'/home/ecoswell/RaspberryPi-Sensor/data/{filename}'): # if CSV file storing data for 'sensor' already exists
            f = open(f'/home/ecoswell/RaspberryPi-Sensor/data/{filename}', 'a') # create/open CSV file to store data for 'sensor'
            writer = csv.writer(f)
        else: # if CSV file storing data for 'sensor' has just been created
            f = open(f'/home/ecoswell/RaspberryPi-Sensor/data/{filename}', 'w') # create/open CSV file to store data for 'sensor'
            writer = csv.writer(f)
            heading = ['Date', 'Time'] + data_heading # enables unlimited number of data headings as 'data_heading' stores an array of each data heading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
            writer.writerow(['Time between readings(sec): ',freq]) # record delay between sensor readings
            writer.writerow(['Duration of readings (mins): ', dur]) # record duration of sensor readings
            writer.writerow(heading) # write headings to file
        now = datetime.now() # get current date and time
        date = now.strftime("%d.%m.%Y") # get current date in correct format
        time = now.strftime("%H:%M:%S") # get current time in correct format
        row = [date, time] + data # enables unlimited number of data readings to be stored as 'data' stores an array of each data reading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
        writer.writerow(row) # write current date, current time, data reading to file
        f.close() # close file
        return

    def save_data_final(self): # move data file to folder storing complete data files
        directory = '/home/ecoswell/RaspberryPi-Sensor/data'
        new_directory = '/home/ecoswell/RaspberryPi-Sensor/data_final'
        for file in os.listdir(directory):
            filename = os.path.join(directory, file)
            new_filename = os.path.join(new_directory, file)
            os.rename(filename, new_filename)
        
    def queue_op(self, freq, dur, stime, sensor_method): # general operation for sensor queue - adds sensor execution method to 'self.queue' every 'freq' seconds to take sensor readings at desired intervals to take sensor readings for 'dur' secs, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        if time.time() - stime >= dur: # if duration for which sensor readings should be taken (as defined by the user in 'sensor_settings.py') has been reached, terminate execution of sensor readings
            return
        else:
            threading.Timer(freq, self.queue_op, [freq, dur, stime, sensor_method]).start() # recursively call 'queue_op' method at frequency specified by 'freq' to add sensor method to 'queue' (which executes sensor readings such that collisions are avoided) at desired frequency and pass required arguments in list
            self.queue.append(sensor_method) # add sensor method to 'self.queue' to schedule execution of sensor reading
            
    def dequeue(self): # remove each queued sensor reading from the queue and execute the sensor reading, avoiding multiple sensors taking readings simultaneously  
        while True:
            if len(self.queue) >= 1: # if there are sensors readings to be taken
                self.queue.pop(0)() # execute reading for front sensor in queue and remove sensor from queue
                time.sleep(2) # 2 second delay between each sensor reading
            elif True not in self.sensor_status: # if all sensors are inactive
                time.sleep(5)
                display_text('All readings \nnow complete.\nYou can safely unplug \n the sensor now.',15) # display sensor reading status on LCD screen
                self.save_data_final() # move data file to folder storing complete data files
                break # all readings are complete, so terminate
            time.sleep(1)

    def main(self): # control operation of active sensors
        if self.calculate_temp_factor == True and self.calculate_gas_factor == False: # if user wishes to calculate the temperature compensation factor
            self.temp_factor()
        elif self.calculate_gas_factor == True and self.calculate_temp_factor == False: # if user wishes to calibrate the gas sensors
            self.gas_factor()
        elif self.calculate_gas_factor == True and self.calculate_temp_factor == True: # if user has accidently set both 'calculate_gas_factor' and 'calculate_temp_factor' to True 
            display_text('Error!\nCannot calculate temp\nand gas factor.',15)
        else:
            for sensor in self.sensors: # iterate through active sensors as defined by user in 'sensor_settings.py'
                sensor_num, sensor_freq, sensor_dur = sensor[0], sensor[1], sensor[2]*60 # first element in tuple stores sensor number, second element stores reading frequency for sensor, third element stores duration of sensor recordings (in minutes)
                self.sensor_status[sensor_num-1] = True # change sensor status to True (i.e. active) for each sensor which user has defined to be active in 'sensor_settings.py'
                sensor_method = self.sensors_dict[sensor_num] # lookup sensor method that is associated with the sensor number ('sensor_num') using 'sensors_dict'
                sensor_thread = threading.Thread(target=sensor_method, args = (sensor_freq, sensor_dur, time.time())) # run sensor queue methods (e.g. 'temp_queue') in background thread
                sensor_thread.start()
            queue_thread = threading.Thread(target=self.dequeue) # run queue in background thread
            queue_thread.start()



