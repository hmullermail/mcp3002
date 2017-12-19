from __future__ import division
import spidev

def bitstring(n):
    s = bin(n)[2:]
    return '0'*(8-len(s)) + s

def read(adc_channel=0, spi_channel=0):
    conn = spidev.SpiDev(0, spi_channel)
    conn.open(0,0)
    conn.max_speed_hz = 1200000 # 1.2 MHz
    conn.mode = 0
    print "mode = ", conn.mode
    cmd = 192
    if adc_channel:
        cmd += 32
    reply_bytes = conn.xfer2([cmd, 0])
    reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
    reply = reply_bitstring[5:15]
    conn.close()
    return int(reply, 2) / 2**10

if __name__ == '__main__':

    while True:
      # Read the light sensor data
      level_0 = read(channel_0)
      volts_0 = round((level_0 * 3.3) / float(1023), 2)

      # Print out results
      timenow = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
      print("{} | {} | {}".format(timenow, level_0, volts_0))

      # Wait before repeating loop
      time.sleep(delay)


    
