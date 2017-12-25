#!/usr/bin/python

# python imports
import spidev
import string
import time
import os
import math
from time import gmtime, strftime
import psutil

# import sqlchemy
from init import db, Reading

# read environment variables + set defaults
#interval         = os.getenv('INTERVAL', '20');
delay            = float(os.getenv('DELAY', '0.003'));       # Delay between readings
measurements     = int(os.getenv('MEASUREMENT', '1000'));  # Number of readings for average value

# Definitions
channel_0        = 0               # ADC Channel 0
channel_1        = 1               # ADC Channel 1
#delay            = 0.003               # Delay between readings
#measurements     = 1000               # Number of readings for average value
volts_0 = 0

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1200000
spi.mode = 0

# Function to read SPI data from MCP3002 chip
# Channel must be an integer 0|1
def ReadChannel(channel):
  data           = 0
  
  for i in range(0,measurements):
    adc          = spi.xfer2([104,0])
    #adc         = spi.xfer2([1,(2+channel)<<6,0])
    
    data         += int(((adc[0]&3) << 8) + adc[1])
    #data        += ((adc[1]&31) << 6) + (adc[2] >> 2)

    time.sleep(delay)

  data           = float(data) / measurements
  return data

def log():
  #cpu = psutil.cpu_percent()
  newLog = Reading(value = volts_0)
  db.session.add(newLog)
  db.session.commit()
  print "LDR value: " + str(volts_0) + " - " + str(count_logs()) + " readings have been recorded"

def count_logs():
  return db.session.query(Reading).count()

def reading_logs(points):
  #print str(Reading.query.all())
  print str(Reading.query.filter_by(id=1).first())
  #print str(Reading.query.filter_by(id=str(points)))
  print str(Reading.query.filter_by(id=4000).all())

#  return db.session.query(Reading).all()

while True:
  # Read the light sensor data
  level_0 = ReadChannel(channel_0)
  volts_0 = round((level_0 * 3.3) / float(1023), 2)
  log()
  reading_logs(4000)
  # Print out results
  #timenow = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
  #print("{} | {} | {}".format(timenow, level_0, volts_0))

  # Wait before repeating loop
  time.sleep(delay)
