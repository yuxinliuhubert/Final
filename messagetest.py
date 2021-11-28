from mqttclient import MQTTClient
import network
import sys
import time
from machine import Pin, PWM, Timer,UART
import adafruit_gps
import machine
# import datetime
# Check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)


uart = UART(1,tx=17,rx=16)
uart.init(9600, bits=8, parity=None, stop=1)
gps = adafruit_gps.GPS(uart)
# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command("b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command("b'PMTK220,1000'")

# Main loop runs forever printing the location, etc. every second.
# last_print = time()

# timer set up to update every 2 seconds
# gps_start = time.ticks_ms()
# gps_interval = 2000


# t1 = Timer(1)
# t1.init(period=10, mode=t1.PERIODIC, callback=tcb)


# Set up Adafruit connection
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'yuxinhubert'
adafruitAioKey = 'aio_AEBP41Jg3PiusrNMwzIRLBxDxOhO'

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)

def gps_update():
    gps.update()

for i in range(1,100):
    gps.update()

#flashing
# t1.init(period=1,mode = t1.PERIODIC, callback=gps_update)
if gps.has_fix:
    testMessage = "Current Time is "+str(gps.timestamp_utc[0])+"/"+str(gps.timestamp_utc[1])+"/"+str(gps.timestamp_utc[2])+" "+str(round(gps.timestamp_utc[3]))+":"+str(round(gps.timestamp_utc[4]))+":"+str(round(gps.timestamp_utc[5]))
    testMessage = testMessage+", location coordinates are: "+str(gps.longitude)+" W, "+str(gps.latitude)+" N."
    print("testMessage, ",testMessage)
else:
    # current =
    # print("current time, ",testMessage)
    # if current - last_print >= 1.0:
    last_print = time.gmtime()
    testMessage ="Current Time is "+str(last_print)+", Location unavilable"
    # testMessage = "1"
    # testMessage = str(gps.timestamp_utc[0]),"/",str(gps.timestamp_utc[1]),"/",str(gps.timestamp_utc[2])," ",str(round(gps.timestamp_utc[3])),":",str(round(gps.timestamp_utc[4])),":",str(round(gps.timestamp_utc[5]))
    # print("Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(gps.timestamp_utc[0], gps.timestamp_utc[1], gps.timestamp_utc[2], gps.timestamp_utc[3], gps.timestamp_utc[4], gps.timestamp_utc[5]))
    print("no fix, returned previous time", last_print)
    print("current time, ",testMessage)


# Send test message
feedName = "yuxinhubert/feeds/Final_project"
# testMessage = "1"
# testMessage = "1"
mqtt.publish(feedName,testMessage)
print("Published {} to {}.".format(testMessage,feedName))

mqtt.subscribe(feedName)

# For one minute look for messages (e.g. from the Adafruit Toggle block) on your test feed:
# for i in range(0, 60):
#     mqtt.check_msg()
#     time.sleep(1)

# t1.deinit()
# Timer(1).deinit()
