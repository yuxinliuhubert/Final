from machine import Pin, PWM, Timer, I2C
#for the abs() function
import math
#for converting binary to hex
from binascii import hexlify
#for keeping track of system time
import time

loudspeaker = Pin(4, mode=Pin.OUT)

#<NOTES SETUP WITH CORRESPONDING FREQUENCIES>
C3 = 131
B4 = 494
F5 = 698
FS6 = 1480
DS4 = 311

# song2=[FS6]
L2 = PWM(loudspeaker, freq=DS4, duty=0, timer=1)
# while (1):
L2.duty(50)
time.sleep(5)
L2.duty(0)
