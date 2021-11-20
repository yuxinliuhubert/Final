# from IMU.py import Hello
# from Light import *
import time
from time import sleep
from machine import Pin, PWM, Timer
from machine import I2C
from binascii import hexlify
from board import LED
import math

# initialize pins
led_ext = Pin(27, mode=Pin.OUT)
button = Pin(15, mode = Pin.IN)

brightness = 0
state = 0
prevCheck = 0

lightCheck = 0
lightCheck_prev = 0

lightSwitchCheck = 0
lightSwitchCheck_prev = 0
# initialize LED light
L1 = PWM(led_ext,freq=500,duty=brightness,timer=0)

# initialize i2C protocol
i2c = I2C(1,scl=Pin(5),sda=Pin(23),freq=400000)

# multi-threading timer comparing variables
IMU_start = time.ticks_ms()
IMU_interval = 10

light_start = 0
light_interval = 1500

switch_start = 0
switch_interval = 1000

# def tcbstat(timer):
#     global brightness
#     if brightness == 0:
#         brightness = 100
#     else:
#         brightness = 0
#
#     print(brightness)
#     L1.duty(brightness)


# reading the IMU
for i in range(len(i2c.scan())):
	print(hex(i2c.scan()[i]))
def WHOAMI(i2caddr):
	whoami = i2c.readfrom_mem(i2caddr,0x0F,1)
	print(hex(int.from_bytes(whoami,"little")))
def Temperature(i2caddr):
	temperature = i2c.readfrom_mem(i2caddr,0x20,2)
	if int.from_bytes(temperature,"little") > 32767:
		temperature = int.from_bytes(temperature,"little")-65536
	else:
		temperature = int.from_bytes(temperature,"little")
	# print("%4.2f" % ((temperature)/(256) + 25))
def Zaccel(i2caddr):
	zacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2C,2),"little")
	if zacc > 32767:
		zacc = zacc -65536

	return zacc
	# print("%4.2f" % (zacc/16393))
def Xaccel(i2caddr):
	xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
	if xacc > 32767:
		xacc = xacc -65536
	return xacc
	# print("%4.2f" % (xacc/16393))
def Yaccel(i2caddr):
	yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
	if yacc > 32767:
		yacc = yacc -65536
	return yacc
	# print("%4.2f" % (yacc/16393))

# change light
def lightChange(localState):
    global L1
    global state
    if localState == 0:
        # print("state 0")
        L1.duty(brightness)
        L1.freq(500)
    elif localState == 1:
        L1.duty(50)
        L1.freq(5)

    elif localState == 2:
        L1.duty(100)
    else:
        state = 0
        L1.duty(brightness)

buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.01)


try:
    # button.callback(Pin.IRQ_RISING, lightChange)
    while(1):
        if time.ticks_ms() - IMU_start >= IMU_interval:
            check = button.value()
            if check != prevCheck and check == 1:
                state = state + 1
            prevCheck = check
            # print("prevCheck ", prevCheck, "  check ", check, "state", state)

            xacc = Xaccel(i2c.scan()[i])/16393
            yacc = Yaccel(i2c.scan()[i])/16393
            zacc = Zaccel(i2c.scan()[i])/16393
            # print("x,y,z ","%4.2f" % (xacc),"%4.2f" % (yacc-1),"%4.2f" % (zacc))
            # print("%4.2f" % (yacc-1))
            IMU_start = time.ticks_ms()

        if time.ticks_ms() - light_start < light_interval:
            if yacc-1.00<0.00 and abs(yacc-1)>0.075:
                lightCheck = 1
            else:
                lightCheck = 0

            if lightCheck == 1 and lightCheck != lightCheck_prev:
                lightChange(state)
                lightCheck_prev = lightCheck
            if lightCheck == 1 and lightCheck == lightCheck_prev:
                lightChange(state)
            if lightCheck == 0 and lightCheck != lightCheck_prev:
                lightChange(state)
        else:
            lightCheck_prev = 0
            lightChange(0)
            light_start = time.ticks_ms()

        if time.ticks_ms() - switch_start >= switch_interval:
            # print("time interval")
            switch_start = time.ticks_ms()
            if lightSwitchCheck == 1 and lightSwitchCheck_prev == 0:
                brightness = 30
                L1.duty(brightness)
                L1.freq(500)
                lightSwitchCheck_prev = lightSwitchCheck
                # print("night light enabled")
            elif lightSwitchCheck == 1 and lightSwitchCheck_prev == lightSwitchCheck:
                brightness = 0
                L1.duty(brightness)
                L1.freq(500)
                lightSwitchCheck_prev = 0

            # print("lightSwitchCheck ", lightSwitchCheck, " lightswitchcheck_prev ",lightSwitchCheck_prev )
            lightSwitchCheck = 1

        else:
            lightSwitchCheck = lightSwitchCheck*check
            # print("lightSwitchCheck ", lightSwitchCheck, " check ",check )

except KeyboardInterrupt:
	i2c.deinit()
	pass
