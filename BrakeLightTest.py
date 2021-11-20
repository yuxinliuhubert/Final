# from IMU.py import Hello
# from Light import *
import time
from time import sleep
from machine import Pin, PWM, Timer
from machine import I2C
from binascii import hexlify
from board import LED
import math

led_ext = Pin(27, mode=Pin.OUT)
button = Pin(15, mode = Pin.IN)
brightness = 0
state = 0
prevCheck = 0
L1 = PWM(led_ext,freq=500,duty=brightness,timer=0)


def tcbstat(timer):
    global brightness
    if brightness == 0:
        brightness = 100
    else:
        brightness = 0

    print(brightness)
    L1.duty(brightness)


i2c = I2C(1,scl=Pin(5),sda=Pin(23),freq=400000)

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
	print("%4.2f" % ((temperature)/(256) + 25))

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
        print("state 0")
        L1.duty(0)
    elif localState == 1:
        t1.init(period= 100, mode=t1.ONE_SHOT, callback=state1Light)

    elif localState == 2:
        t1.init(period= 100, mode=t1.ONE_SHOT, callback=state2Light)
    else:
        state = 0

def state1Light(timer):
    print("state 1 enabled")
    L1.duty(50)
    L1.freq(5)

def state2Light(timer):
    print("state 2 enabled")
    L1.duty(100)
    L1.freq(5)

buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.01)


t1 = Timer(1)


try:
    # button.callback(Pin.IRQ_RISING, lightChange)
    while(1):
        time.sleep(0.01)

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

        # plt.scatter(time,y)
        if yacc-1.00<0.00 and abs(yacc-1)>0.075:
            # print("rrerewrwerwrwer")
            lightChange(state)
            # time.sleep(1.5)
        # elif 1.00-yacc<0.00 and abs(yacc-1)>0.05:
        #     L1.duty(100)
        else:
            lightChange(0)
            t1.deinit()


except KeyboardInterrupt:
	i2c.deinit()
	pass
