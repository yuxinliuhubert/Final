# Example # 1: Simple UART for controlling
# the state of the onboard LED
# Author: George Bantique, TechToTinker
# Date: October 7, 2020

# Load the machine module in order to access the hardware
import machine

# Create the led object in GPIO 2
led = machine.Pin(2, machine.Pin.OUT)
# Create the uart object in port 2
# Rx=GPIO 16, Tx=GPIO 17
uart = machine.UART(2, tx=16,rx=17)

# Create a global variable to hold the receive data in serial
strMsg = ''

# This is the main loop
while True:
    print("nope")
    time.sleep(0.2)
	# if there is character in receive serial buffer
    if uart.any() > 0:
    	# Read all the character to strMsg variable
        strMsg = uart.read()
        # Debug print to REPL
        print(strMsg)

        # If there is 'on' string in strMsg,
        # Turn on the LED
        if 'on' in strMsg:
            led.on()
            uart.write('Turning on LED')
            print('Turning on LED')
        # If there is 'off' string in strMsg,
        # Turn off the LED
        elif 'off' in strMsg:
            led.off()
            uart.write('Turning off LED')
            print('Turning off LED')
        # Else, invalid command
        else:
            uart.write('Invalid command')
            print('Invalid command')
