#!/usr/bin/python

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

SPI = require('spi');
spi = new SPI.Spi('../../../dev/spidev0.0', 0, 0);

# Open SPI bus
# spi = spidev.SpiDev()
# spi.open(0,0)
# spi.max_speed_hz = 100000
# spi.mode = 0

# Function to read SPI data from MCP3002 chip
# Channel must be an integer 0|1
def ReadChannel(channel):
  data           = 0
  
  for i in range(0,measurements):
    adc          = spi.xfer2([192,0])
    #adc         = spi.xfer2([1,(2+channel)<<6,0])
    
    data         += int(((adc[0]&3) << 8) + adc[1])
    #data        += ((adc[1]&31) << 6) + (adc[2] >> 2)

    time.sleep(0.2)
    print("{} | {}".format(i, adc))

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



#   var SPI = require('spi');
 
# var spi = new SPI.Spi('/dev/spidev0.0', {
#     'mode': SPI.MODE['MODE_0'],  // always set mode as the first option 
#     'chipSelect': SPI.CS['none'] // 'none', 'high' - defaults to low 
#   }, function(s){s.open();});
 
# var txbuf = new Buffer([ 0x23, 0x48, 0xAF, 0x19, 0x19, 0x19 ]);
# var rxbuf = new Buffer([ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]);
 
# spi.transfer(txbuf, rxbuf, function(device, buf) {
#     // rxbuf and buf should be the same here 
#     var s = "";
#     for (var i=0; i < buf.length; i++)
#         s = s + buf[i] + " ";
#         console.log(s + "- " + new Date().getTime());
#   });