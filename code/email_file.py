'''
Sends an email to user's email address with the latest data reading file(s)
File run at startup as a cron job ('sudo crontab -e')
'''

import sys
path = '/home/ecoswell/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
import sensor_settings
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import time

NOW = datetime.now() # get current date and time
DATE = NOW.strftime("%d.%m.%Y") # get date when sensor readings begin in correct format
TIME = NOW.strftime("%H:%M:%S") # get time when sensor readings begin in correct format
SMTP_SERVER = 'smtp.gmail.com' # email server 
SMTP_PORT = 587 # server port 
GMAIL_USERNAME = 'datalogger@ecoswell.org' # change this to match your gmail account
GMAIL_PASSWORD = 'tzcbnsbevrgflhzu' # change this to match your gmail app-password (see https://bc-robotics.com/tutorials/sending-email-using-python-raspberry-pi/)
RECIPIENT = sensor_settings.email_address
SUBJECT = 'Multi-sensor data '+DATE+'-'+TIME

while True: # continually try to send email
    time.sleep(10) # delay to allow Raspberry Pi to connect to internet

    #try:
    # connect to gmail server:
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) 
    session.ehlo()
    session.starttls()
    session.ehlo()

    # login to gmail
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    msg = MIMEMultipart() # create message data
    msg['Subject'] = SUBJECT # assign message subject 

    count = 0
    directory = '/home/ecoswell/RaspberryPi-Sensor/data_final' # directory storing data files ready to be emailed
    for file in os.listdir(directory): # iterate over each file ready to be emailed
        count+=1
        filename = os.path.join(directory, file) 
        with open(filename, "rb") as f: # open file to be emailed
            part = MIMEApplication(f.read(),Name=basename(filename))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
        msg.attach(part) # add file as email attachement 

    if count != 0: # if zero files in data folder:
        # send email:
        session.sendmail(GMAIL_USERNAME, RECIPIENT, msg.as_string()) # send email to desired email address
        session.quit

        # move each emailed file to directory storing emails which have already been emailed 
        new_directory = '/home/ecoswell/RaspberryPi-Sensor/data_emailed'
        for file in os.listdir(directory):
            filename = os.path.join(directory, file)
            new_filename = os.path.join(new_directory, file)
            os.rename(filename, new_filename)
        break
#     except:
#         pass
