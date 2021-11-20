from machine import Pin, PWM, Timer
import math



led_ext = Pin(27, mode=Pin.OUT)
button = Pin(15, mode = Pin.IN)

# pinMode(15,INPUT)



state = 0
brightness = 100
L1 = PWM(led_ext,freq=500,duty=brightness,timer=0)
try:
    while(1):
        check = button.value()
        # print("button value", check)
        if check == 1:
            state = state + 1
            # L1.duty(100)
            # L1.duty(0)
        if state >= 3:
            state = 0
        print("button", check)

        if state == 0:
            L1.duty(0)
        elif state == 1:
            L1.duty(50)
            L1.freq(5)
        elif state == 2:
            L1.duty(100)
            L1.freq(5)
        print("state value", state)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
