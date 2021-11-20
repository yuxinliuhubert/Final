from board import LED
from machine import Pin, PWM, Timer
from time import sleep
import math

# led = Pin(LED, mode=Pin.OUT)
led_ext = Pin(27, mode=Pin.OUT)

brightness = 100
L1 = PWM(led_ext,freq=500,duty=brightness,timer=0)

def tcb(timer):
    global brightness
    if brightness < 100:
        brightness += 1
    else:
        brightness = 0

    print(brightness)
    L1.duty(brightness)

def tcbstat(timer):
    global brightness
    if brightness == 0:
        brightness = 100
    else:
        brightness = 0

    print(brightness)
    L1.duty(brightness)



#led_ext = Pin(LED, mode=Pin.OUT)
