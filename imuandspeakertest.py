#<REQUIRED MODULES>
#for communication and actuation of hardware components connected to ESP32
from machine import Pin, PWM, Timer, I2C
#for the abs() function
import math
#for converting binary to hex
from binascii import hexlify
#for keeping track of system time
import time

#<CONNECTED HARDWARE COMPONENTS>
loudspeaker = Pin(27, mode=Pin.OUT)
button2 = Pin(15, mode = Pin.IN)

# <INERTIAL MEASUREMENT UNIT READING TEMPERATURE, ACCELERATION, AND ANGULAR SPEED>
i2c = I2C(1,scl=Pin(22),sda=Pin(23),freq=400000)

for i in range(len(i2c.scan())):
    print(hex(i2c.scan()[i]))

def WHOAMI(i2caddr):
    whoami = i2c.readfrom_mem(i2caddr,0x0F,1)
    #print(hex(int.from_bytes(whoami,"little")))
    return whoami

# Temperature pulled data
def Temperature(i2caddr):
    temperature = i2c.readfrom_mem(i2caddr,0x20,2)
    if int.from_bytes(temperature,"little") > 32767:
        temperature = int.from_bytes(temperature,"little")-65536
    else:
        temperature = int.from_bytes(temperature,"little")
    return temperature
    #print("%4.2f" % ((temperature)/(256) + 25))

# XYZ Acceleration pulled data
def Xaccel(i2caddr):
    xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
    if xacc > 32767:
        xacc = xacc -65536
    return xacc
    #print("%4.2f" % (xacc/16393))
def Yaccel(i2caddr):
    yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
    if yacc > 32767:
        yacc = yacc -65536
    return yacc
    #print("%4.2f" % (yacc/16393))
def Zaccel(i2caddr):
    zacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2C,2),"little")
    if zacc > 32767:
        zacc = zacc -65536
    return zacc
    #print("%4.2f" % (zacc/16393))

# XYZ Gyroscope pulled data
def Xgyro(i2caddr):
    xgyr = int.from_bytes(i2c.readfrom_mem(i2caddr,0x22,2),"little")
    if xgyr > 32767:
        xgyr = xgyr -65536
    return xgyr
    #print("%4.2f" % (xgyr/16393))
def Ygyro(i2caddr):
    ygyr = int.from_bytes(i2c.readfrom_mem(i2caddr,0x24,2),"little")   
    if ygyr > 32767:
        ygyr = ygyr -65536
    return ygyr
    #print("%4.2f" % (ygyr/16393))
def Zgyro(i2caddr):
    zgyr = int.from_bytes(i2c.readfrom_mem(i2caddr,0x26,2),"little")
    if zgyr > 32767:
        zgyr = zgyr -65536
    return zgyr
    #print("%4.2f" % (zgyr/16393))


buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.1)



#<NOTES SETUP WITH CORRESPONDING FREQUENCIES>
C3 = 131 
CS3 = 139 
D3 = 147 
DS3 = 156 
E3 = 165 
F3 = 175 
FS3 = 185 
G3 = 196 
GS3 = 208 
A3 = 220 
AS3 = 233 
B3 = 247 
C4 = 262 
CS4 = 277 
D4 = 294 
DS4 = 311 
E4 = 330 
F4 = 349 
FS4 = 370 
G4 = 392 
GS4 = 415 
A4 = 440 
AS4 = 466 
B4 = 494 
C5 = 523 
CS5 = 554 
D5 = 587 
DS5 = 622 
E5 = 659 
F5 = 698 
FS5 = 740 
G5 = 784 
GS5 = 831 
A5_ = 880 
AS5 = 932 
B5 = 988 
C6 = 1047 
CS6 = 1109 
D6 = 1175 
DS6 = 1245 
E6 = 1319 
F6 = 1397 
FS6 = 1480 
G6 = 1568 
GS6 = 1661 
A6 = 1760 
AS6 = 1865 
B6 = 1976 
C7 = 2093 
CS7 = 2217 
D7 = 2349 
DS7 = 2489 
E7 = 2637 
F7 = 2794 
FS7 = 2960 
G7 = 3136 
GS7 = 3322 
A7 = 3520 
AS7 = 3729 
B7 = 3951 
C8 = 4186 
CS8 = 4435 
D8 = 4699 
DS8 = 4978 

#<SONG SETUP>
song = [C4, E4, G4, C5, E5, G4, C5, E5, C4, E4, G4, C5, E5, G4, C5, E5, 
C4, D4, G4, D5, F5, G4, D5, F5, C4, D4, G4, D5, F5, G4, D5, F5, 
B3, D4, G4, D5, F5, G4, D5, F5, B3, D4, G4, D5, F5, G4, D5, F5, 
C4, E4, G4, C5, E5, G4, C5, E5, C4, E4, G4, C5, E5, G4, C5, E5, 
C4, E4, A4, E5, A5_, A4, E5, A4, C4, E4, A4, E5, A5_, A4, E5, A4, 
C4, D4, FS4, A4, D5, FS4, A4, D5, C4, D4, FS4, A4, D5, FS4, A4, D5, 
B3, D4, G4, D5, G5, G4, D5, G5, B3, D4, G4, D5, G5, G4, D5, G5, 
B3, C4, E4, G4, C5, E4, G4, C5, B3, C4, E4, G4, C5, E4, G4, C5, 
B3, C4, E4, G4, C5, E4, G4, C5, B3, C4, E4, G4, C5, E4, G4, C5, 
A3, C4, E4, G4, C5, E4, G4, C5, A3, C4, E4, G4, C5, E4, G4, C5, 
D3, A3, D4, FS4, C5, D4, FS4, C5, D3, A3, D4, FS4, C5, D4, FS4, C5, 
G3, B3, D4, G4, B4, D4, G4, B4, G3, B3, D4, G4, B4, D4, G4, B4 ]

#<WHILE LOOP VARIABLE INITIALIZATIONS>
#IMU Data Update Custom Timer Inits
IMU_Interval = 100
IMU_Start = 0 
#Fall Detection Speaker Activation Custom Timer Inits
Speaker_Interval = 300
Speaker_Start = 0
#Note Pointer in Song Counter Inits
note_pointer = 0
#Speaker PWM Inits
L1 = PWM(loudspeaker, freq=song[note_pointer], duty=0, timer=0)
#Speaker Activation Counter Inits
fall_count = 0
current_fall = 0
prev_fall = 0

try:
    while(1):
        # IMU Data Update Custom Timer
        if time.ticks_ms() - IMU_Start >= IMU_Interval:
            xa = Xaccel(i2c.scan()[i])
            ya = Yaccel(i2c.scan()[i])
            za = Zaccel(i2c.scan()[i])
            xg = Xgyro(i2c.scan()[i])
            yg = Ygyro(i2c.scan()[i])
            zg = Zgyro(i2c.scan()[i])
            print("x acc:","%4.2f" % (xa/16393), "y acc:", "%4.2f" % (ya/16393), "z acc:","%4.2f" % (za/16393), "x gyr:", "%4.2f" % (xg/16393), "y gyr:", "%4.2f" % (yg/16393), "z gyr:", "%4.2f" % (zg/16393))
            IMU_start = time.ticks_ms()
        # Fall Detection Speaker Activation Custom Timer
        if time.ticks_ms() - Speaker_Start >= Speaker_Interval:
            ya = Yaccel(i2c.scan()[i])/16393
            button2_Status = button2.value()
            # Speaker Activiation Count tracker. Will reset to zero if y accelerometer registers greater than .5 but not for 3 consecutive seconds. 
            if abs(ya) > .5:
                current_fall = 1
            else:
                current_fall = 0
            if prev_fall == current_fall:
                fall_count += current_fall
            if prev_fall != current_fall:
                fall_count  = current_fall
                prev_fall = current_fall
            # Enters into speaker activated mode after 3 consecutive seconds
            if fall_count >= 10:
                # If the OK button is not pressed, the speaker will be unmuted, and a note in the song will be played each time the counter loops.
                if button2_Status == 0:
                    L1.duty(85)
                    L1.freq(song[note_pointer])
                    if note_pointer < len(song)-1:
                        note_pointer += 1
                    else:
                        note_pointer = 0
                # If the OK button is pressed, the speaker will be muted.
                if button2_Status == 1:
                    L1.duty(0)
                    fall_count = 0
                    note_pointer = 0
            Speaker_Start = time.ticks_ms()
except KeyboardInterrupt:
    i2c.deinit()
    L1.deinit()
    pass