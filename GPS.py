 # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries # SPDX-License-Identifier: MIT
# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location # and other details.
from machine import Pin, PWM, Timer,UART
import adafruit_gps
import time
import machine


uart = UART(2,tx=17,rx=16)
uart.init(9600, bits=8, parity=None, stop=1)
time.sleep(1)


gps = adafruit_gps.GPS(uart)

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command("b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command("b'PMTK220,1000'")

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

# timer set up to update every 2 seconds
gps_start = time.ticks_ms()
gps_interval = 2000

try:

    while True:

         # Make sure to call gps.update() every loop iteration and at least twice
         # as fast as data comes from the GPS unit (usually every second).
         # This returns a bool that's true if it parsed new data (you can ignore it # though if you don't care and instead look at the has_fix property).
        gps.update()

        # Every second print out current location details if there's a fix.
        if time.ticks_ms() - gps_start >= gps_interval:
            if gps.has_fix:
                current = time.monotonic()
                if current - last_print >= 1.0:
                    last_print = current
                print("=" * 40) # Print a separator line.
                print("Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(gps.timestamp_utc[0], gps.timestamp_utc[1], gps.timestamp_utc[2], gps.timestamp_utc[3], gps.timestamp_utc[4], gps.timestamp_utc[5]))
                print("Latitude: {0:.6f} degrees".format(gps.latitude))
                print("Longitude: {0:.6f} degrees".format(gps.longitude))
                print("Fix quality: {}".format(gps.fix_quality))

                # Some attributes beyond latitude, longitude and timestamp are optional # and might not be present. Check if they're None before trying to use!
                if gps.satellites is not None:
                    print("# satellites: {}".format(gps.satellites))
                if gps.altitude_m is not None:
                    print("Altitude: {} meters".format(gps.altitude_m))
                if gps.speed_knots is not None:
                    print("Speed: {} knots".format(gps.speed_knots))
                if gps.track_angle_deg is not None:
                    print("Track angle: {} degrees".format(gps.track_angle_deg))
                if gps.horizontal_dilution is not None:
                    print("Horizontal dilution: {}".format(gps.horizontal_dilution))
                if gps.height_geoid is not None:
                    print("Height geoid: {} meters".format(gps.height_geoid))
            else:
                print("Waiting for fix...")
            gps_start = time.ticks_ms()

except KeyboardInterrupt:
    uart.deinit()
    pass
