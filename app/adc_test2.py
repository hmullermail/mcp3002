#!/usr/bin/python

import spidev
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
spi.mode = 0

def bitstring(n):
    s = bin(n)[2:]
    return '0'*(8-len(s)) + s
    
# Function to read SPI data from MCP3002 chip
# Channel must be an integer 0|1
def ReadChannel(channel):
  data           = 0
  cmd = 192
  if channel:
    cmd += 32
  adc = spi.xfer2([cmd, 0])
  reply_bitstring = ''.join(bitstring(n) for n in adc)
  reply = reply_bitstring[5:15]
  spi.close()
  return int(reply, 2) / 2**10

while True:
  # Read the light sensor data
  level_0 = ReadChannel(channel_0)
  volts_0 = round((level_0 * 3.33) / float(1024), 2)

  # Print out results
  timenow = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
  print("{} | {} | {}".format(timenow, level_0, volts_0))

  # Wait before repeating loop
  time.sleep(delay)