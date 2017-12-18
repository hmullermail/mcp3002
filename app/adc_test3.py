#!/usr/bin/python

import spidev
import bcm2835
import string
import time
import os
import math
from time import gmtime, strftime

# Definitions
channel_0        = 0               # ADC Channel 0
channel_1        = 1               # ADC Channel 1
delay            = 1               # Delay between readings
measurements     = 5               # Number of readings for average value


# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000


# Function to read SPI data from MCP3002 chip
# Channel must be an integer 0|1
def ReadChannel(channel):
  data           = 0
  
  for i in range(0,measurements):
    #adc          = spi.xfer2([104,0])
    adc         = spi.xfer2([1,(2+channel)<<6,0])
    
    #data         += int(((adc[0]&3) << 8) + adc[1])
    data        += ((adc[1]&31) << 6) + (adc[2] >> 2)

    time.sleep(0.2)
    print("{}".format(i))

  data           = float(data) / measurements
  return data

while True:
  # Read the light sensor data
  level_0 = ReadChannel(channel_0)
  volts_0 = round((level_0 * 3.33) / float(1024), 2)

  # Print out results
  timenow = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
  print("{} | {} | {}".format(timenow, level_0, volts_0))

  # Wait before repeating loop
  time.sleep(delay)