# Establish Internet connection
# from network import WLAN, STA_IF
# from network import mDNS
#<REQUIRED MODULES>
#for communication and actuation of hardware components connected to ESP32
from machine import Pin, PWM, I2C, UART
#for the abs() function
import math
#for converting binary to hex
from binascii import hexlify
#for keeping track of system time
import time
from mqttclient import MQTTClient
import network
import sys
import adafruit_gps
from board import LED
import gc
from network import WLAN, STA_IF
from network import mDNS

#<CONNECTED HARDWARE COMPONENTS>
loudspeaker = Pin(4, mode=Pin.OUT)
button = Pin(15, mode = Pin.IN)
led = Pin(27, mode=Pin.OUT)
uart = UART(2,tx=17,rx=16)
i2c = I2C(1,scl=Pin(22),sda=Pin(23),freq=400000)

# <NOTES SETUP WITH CORRESPONDING FREQUENCIES>
C3 = 131
DS4 = 311
B4 = 494
F5 = 698
FS6 = 1480

#<ALARM SONG SETUP>
song = [B4,F5,B4,F5]

#<WHILE LOOP VARIABLE INITIALIZATIONS>
#IMU Data Update Custom Timer Inits
imu_interval = 10
imu_start = 0
#Fall Detection Speaker Activation Custom Timer Inits
speaker_interval = 300
speaker_start = 0
#Brake Light Hold Timer Inits
light_interval = 1000
light_start = 0
#Brake Light Switch Timer Inits
switch_interval = 1000
switch_start = 0
#Memory Viewer Timer Inits
mem_interval = 500
mem_start = 0

#<MISC INITIALIZATIONS>
#Note Pointer in Song Counter Inits
note_pointer = 0
#Speaker Activation Counter Inits
fall_count = 0
current_fall = 0
prev_fall = 0
#Alarm Grace Period Inits
alarm_Interval = 10000
alarm_start = time.ticks_ms()
#Alarm Usage Tracker Inits. (so that the fall time is only recorded once)
alarm_start_check = 0
alarm_sent_check = 0
#Accelerometer Reading Calibration Inits
divide = 16393
#Fall Detection for Jerk Inits
prev_xa = 0
prev_ya = 0
prev_za = 0
#GPS Location Reading Inits
location_save = "Location unavailable"
# LED light configuration
brightness = 0
state = 0
prevCheck = 0

lightCheck = 0
lightCheck_prev = 0

lightSwitchCheck = 0
lightSwitchCheck_prev = 0
# lightHold = 0

# <HARDWARE COMPONENT INITS>
# Initialize LED light
L1 = PWM(led,freq=500,duty=brightness,timer=0)
# Initialize Loudspeaker song2=[FS6]
L2 = PWM(loudspeaker, freq=FS6, duty=0, timer=1)
# Initialize GPS
uart.init(9600, bits=8, parity=None, stop=1)

# <WIFI CONNECTION. UNCOMMENT THE CORRECT CONNECTION AND FLASH TO ESP32>
wlan = WLAN(STA_IF)
wlan.active(True)

# wlan.connect('ME100-2.4G', '122Hesse', 5000)
wlan.connect('3Yellow1Brown', 'Carolisqueen', 5000)
# wlan.connect('room4s','SphstakesonBerk1',5000)
# wlan.connect('Billisty','6g88bp2beeywj',5000)

tries = 0
while not wlan.isconnected() and tries < 15:
    # print("Waiting for wlan connection")
    time.sleep(0.5)
    tries = tries + 1

if wlan.isconnected():
    L2.duty(85)
    time.sleep(1)
    L2.duty(0)
    # print("WiFi connected at", wlan.ifconfig()[0])
else:
    L2.freq(DS4)
    L2.duty(85)
    time.sleep(1)
    L2.duty(0)
        # print("Unable to connect to WiFi")

# Advertise as 'hostname', alternative to IP address
try:
    hostname = "7750_HL"
    mdns = mDNS(wlan)
    # mdns.start(hostname, "MicroPython REPL")
    # mdns.addService('_repl', '_tcp', 23, hostname)
    mdns.start(hostname,"MicroPython with mDNS")
    _ = mdns.addService('_ftp', '_tcp', 21, "MicroPython", {"board": "ESP32", "service": "my_hostname FTP File transfer", "passive": "True"})
    _ = mdns.addService('_telnet', '_tcp', 23, "MicroPython", {"board": "ESP32", "service": "my_hostname Telnet REPL"})
    _ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "my_hostname Web server"})
    # print("Advertised locally as {}.local".format(hostname))

except OSError:
    print("Failed starting mDNS server - already started?")

# start telnet server for remote login
from network import telnet

# print("start telnet server")
telnet.start(user='ylhubert2024', password='Diandian$69')

# fetch NTP time
from machine import RTC

# print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

timeout = 2
for _ in range(timeout):
    if rtc.synced():
        break
    # print("Waiting for rtc time")
    time.sleep(1)

# if rtc.synced():
#     print(time.strftime("%c", time.localtime()))
# else:
#     print("could not get NTP time")

gc.enable()
gc.mem_alloc()

gps = adafruit_gps.GPS(uart)

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command("b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command("b'PMTK220,1000'")

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

# register with adafruit website
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'yuxinhubert'
adafruitAioKey = 'aio_sUVn46VH5hi5ZFXUuGzQYXAd5X9b'

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# Connect to Adafruit server
# print("Connecting to Adafruit")
if wlan.isconnected():
    mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
    time.sleep(0.5)
# print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
    mqtt.set_callback(sub_cb)



for i in range(len(i2c.scan())):
    print(hex(i2c.scan()[i]))

# <XYZ ACCELERATION PULLED RAW DATA>
def Xaccel(i2caddr):
    xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
    if xacc > 32767:
        xacc = xacc -65536
    return xacc
def Yaccel(i2caddr):
    yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
    if yacc > 32767:
        yacc = yacc -65536
    return yacc
def Zaccel(i2caddr):
    zacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2C,2),"little")
    if zacc > 32767:
        zacc = zacc -65536
    return zacc

# # XYZ Gyroscope pulled data
# def Xgyro(i2caddr):
#     xgyr = int.from_bytes(i2c.readfrom_mem(i2caddr,0x22,2),"little")
#     if xgyr > 32767:
#         xgyr = xgyr -65536
#     return xgyr
#     #print("%4.2f" % (xgyr/16393))
# def Ygyro(i2caddr):
#     ygyr = int.from_bytes(i2c.readfrom_mem(i2caddr,0x24,2),"little")
#     if ygyr > 32767:
#         ygyr = ygyr -65536
#     return ygyr
#     #print("%4.2f" % (ygyr/16393))
# def Zgyro(i2caddr):
#     zgyr = int.from_bytes(i2c.readfrom_mem(i2caddr,0x26,2),"little")
#     if zgyr > 32767:
#         zgyr = zgyr -65536
#     return zgyr
#     #print("%4.2f" % (zgyr/16393))

# <LIGHT MODE CHANGER>
# change light
def lightChange(localState):
    global L1
    global state
    if localState == 0:
        L1.duty(100)
        L1.freq(500)
        # if lightHold == 1:
        #     state = 1
    else:
        L1.duty(50)
        L1.freq(5)
        # if lightHold == 1:
        #     print("here_")
        #     state = 0


def lightOffDim():
    global L1
    global brightness
    L1.duty(brightness)
    L1.freq(500)

buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.1)

try:
    while(1):
        # <MEMORY MANAGEMENT UPDATE TIMER>
        gc.collect()

        # <MESSAGE UPDATE TIMER>
        if alarm_start_check == 0:
            alarm_start = time.ticks_ms()

        # <GPS UPDATE TIMER>
        gps.update()
        if gps.has_fix:
            location_save = "{} W, {} N".format(gps.longitude,gps.latitude)

        # <IMU DATA UPDATE CUSTOM TIMER>
        if time.ticks_ms() - imu_start >= imu_interval:
            check = button.value()
            if check != prevCheck and check == 1:
                state = not state
            prevCheck = check
            # print("state {},lightHold {}, check {}".format(state,lightHold,check))
            # lightHold = not state
            xa = Xaccel(i2c.scan()[i])/divide
            ya = Yaccel(i2c.scan()[i])/divide
            za = Zaccel(i2c.scan()[i])/divide
            # xg = Xgyro(i2c.scan()[i])
            # yg = Ygyro(i2c.scan()[i])
            # zg = Zgyro(i2c.scan()[i])
            # print("x acc:","%4.2f" % (xa/16393), "y acc:", "%4.2f" % (ya/16393), "z acc:","%4.2f" % (za/16393), "x gyr:", "%4.2f" % (xg/16393), "y gyr:", "%4.2f" % (yg/16393), "z gyr:", "%4.2f" % (zg/16393))
            IMU_start = time.ticks_ms()

        if abs(prev_ya-ya) > .3 and prev_ya < ya and ya < 0 and abs(xa) < .4:
            # print("lightCheck = 1")
            light_start = time.ticks_ms()
            lightCheck = 1
        # else:
        #     light_start = time.ticks_ms()
        #     lightCheck = 0
        prev_ya = ya

        # <BRAKE LIGHT HOLD TIMER>
        if lightCheck == 1:
            if time.ticks_ms() - light_start < light_interval:
                # if lightCheck == 1 and lightCheck != lightCheck_prev:
                #     lightChange(state)
                #     lightCheck_prev = lightCheck
                # if lightCheck == 1 and lightCheck == lightCheck_prev:
                #     lightChange(state)
                # if lightCheck == 0 and lightCheck != lightCheck_prev:
                #     lightChange(state)
                lightChange(state)
            else:
                # lightCheck_prev = 0
                lightCheck = 0
                lightOffDim()
                # light_start = time.ticks_ms()

        if time.ticks_ms() - switch_start >= switch_interval:
            # print("time interval")
            switch_start = time.ticks_ms()
            if lightSwitchCheck == 1 and lightSwitchCheck_prev == 0:
                brightness = 10
                state = not state
                lightOffDim()
                lightSwitchCheck_prev = lightSwitchCheck
                # lightHold = 0
                # print("night light enabled")
            elif lightSwitchCheck == 1 and lightSwitchCheck_prev == lightSwitchCheck:
                brightness = 0
                state = not state
                lightOffDim()
                lightSwitchCheck_prev = 0
                # lightHold = 0

            # print("lightSwitchCheck ", lightSwitchCheck, " lightswitchcheck_prev ",lightSwitchCheck_prev )
            lightSwitchCheck = 1
            # lightHold = 0
            # print("light hold {} state {}".format(lightHold,state))
        else:
            lightSwitchCheck = lightSwitchCheck*check
            # if lightSwitchCheck == 1:
            #     lightHold = True
            # else:
            #     lightHold = 0
            # print("light hold {} state {} lightSwitchCheck {}".format(lightHold,state,lightSwitchCheck))


        # <FALL DETECTION SPEAKER ACTIVATION CUSTOM TIMER>
        if time.ticks_ms() - speaker_start >= speaker_interval:
            xa = Xaccel(i2c.scan()[i])/divide
            button2_Status = button.value()
            # Speaker Activiation Count tracker. Will reset to zero if y accelerometer registers greater than .5 but not for 3 consecutive seconds.
            if abs(prev_xa-xa) < .3 and abs(prev_ya-ya) < .3 and abs(prev_za-za) < .3:
                current_fall = 1
            else:
                current_fall = 0
                alarm_start_check = 0
                alarm_sent_check = 0
                L2.duty(0)
            prev_xa = xa
            prev_ya = ya
            prev_za = za
            if prev_fall == current_fall:
                fall_count += current_fall
            if prev_fall != current_fall:
                fall_count  = current_fall
                prev_fall = current_fall
            # Enters into speaker activated mode after 3 consecutive seconds
            if fall_count >= 50:

                # If the OK button is not pressed, the speaker will be unmuted, and a note in the song will be played each time the counter loops.
                if button2_Status == 0:
                    alarm_start_check = 1
                    if time.ticks_ms() - alarm_start >= alarm_Interval:
                        if alarm_sent_check == 0:
                            if gps.has_fix:
                                testMessage = "Your friend might have taken a fall on {}/{}/{} at {:02}:{:02}:{:02} UTC".format(gps.timestamp_utc[1],gps.timestamp_utc[2],gps.timestamp_utc[0],gps.timestamp_utc[3],gps.timestamp_utc[4],gps.timestamp_utc[5])
                                testMessage = "{} at these location coordinates: \n\n {} \n\n**Paste the coordinates in Google or Apple Map will give you the street-specific location!** Please contact your friend to confirm safety!".format(testMessage,location_save)
                                # print("fix fall message, ",testMessage)
                            else:
                                last_print = time.gmtime()
                                print(last_print)
                                # last_print = gm_time_processor(last_print)
                                testMessage ="Your friend might have taken a fall on {}/{}/{} at {:02}:{:02}:{:02} UTC".format(last_print[1],last_print[2],last_print[0],last_print[3],last_print[4],last_print[5])
                                testMessage = "{}. The last active location coordinates were: \n\n {} \n\n**Paste the coordinates in Google or Apple Map will give you the street-specific location!** Please contact your friend to confirm safety!".format(testMessage,location_save)
                                print("no fix fall message: ",testMessage)

                            # Send test message
                            feedName = "yuxinhubert/feeds/Final_project"
                            # testMessage = "1"
                            # testMessage = "1"
                            if wlan.isconnected():
                                mqtt.publish(feedName,testMessage)
                            # print("Published {} to {}.".format(testMessage,feedName))
                                mqtt.subscribe(feedName)
                            alarm_sent_check = 1
                    L2.duty(85)
                    L2.freq(song[note_pointer])
                    if note_pointer < len(song)-1:
                        note_pointer += 1
                    else:
                        note_pointer = 0
                # If the OK button is pressed, the speaker will be muted.
                if button2_Status == 1:
                    alarm_start_check = 0
                    alarm_sent_check = 0
                    # note: assumption made that when user press the button, pick up right away, otherwise location data will be sent again
                    L2.duty(0)
                    fall_count = 0
                    note_pointer = 0
            speaker_start = time.ticks_ms()
        if time.ticks_ms() - mem_start >= mem_interval:
            # print(gc.mem_free())
            mem_start = time.ticks_ms()
except KeyboardInterrupt:
    i2c.deinit()
    L1.deinit()
    L2.deinit()
    pass
