 # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries # SPDX-License-Identifier: MIT
# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location # and other details.
from micropyGPS import MicropyGPS
from machine import Pin, PWM, Timer,UART
import adafruit_gps
import time
import machine

# ttx = Pin(17, mode=Pin.OUT)
rrx = Pin(16, mode=Pin.IN)
uart = UART(2,tx=17,rx=16)
# uart = UART(1,9600)
uart.init(9600, bits=8, parity=None, stop=1)
time.sleep(1)


# If using I2C, we'll create an I2C interface to talk to using default pins #
# i2c = board.I2C()
# gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
# gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# gps.send_command(b"PMTK220,1000")
# last_print = time.monotonic()
# gps = adafruit_gps.GPS(uart, debug=False)
# last_print = time.monotonic()

while True:

    # gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    # gps.send_command(b"PMTK220,1000")


    rrxRead = rrx.value()
    mygps = uart.read()
    print("gps, ", mygps)
    print("rrx ",rrxRead)


    yes = str(mygps)

    time.sleep(0.3)

    print(yes)
#     gps.update()
# # Every second print out current location details if there's a fix.
#     current = time.monotonic()
#     if current - last_print >= 1.0:
#         last_print = current
#     if not gps.has_fix:
#         print("Waiting for fix...")
#         continue
#     print("=" * 40) # Print a separator line.
#     print("Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format( gps.timestamp_utc.tm_mon, gps.timestamp_utc.tm_mday, gps.timestamp_utc.tm_year, gps.timestamp_utc.tm_hour, gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec))
#     print("Latitude: {0:.6f} degrees".format(gps.latitude))
#     print("Longitude: {0:.6f} degrees".format(gps.longitude))
#     print("Fix quality: {}".format(gps.fix_quality))
#
#     # Some attributes beyond latitude, longitude and timestamp are optional # and might not be present. Check if they're None before trying to use!
#     if gps.satellites is not None:
#         print("# satellites: {}".format(gps.satellites))
#     if gps.altitude_m is not None:
#         print("Altitude: {} meters".format(gps.altitude_m))
#     if gps.speed_knots is not None:
#         print("Speed: {} knots".format(gps.speed_knots))
#     if gps.track_angle_deg is not None:
#         print("Track angle: {} degrees".format(gps.track_angle_deg))
#     if gps.horizontal_dilution is not None:
#         print("Horizontal dilution: {}".format(gps.horizontal_dilution))
#     if gps.height_geoid is not None:
#         print("Height geoid: {} meters".format(gps.height_geoid))
