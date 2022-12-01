import RPi.GPIO as GPIO                                                                                                         
import sys
import time                                                             

import random
import sysv_ipc
GPIO.setmode (GPIO.BCM)                                                 

TRIG_FRONT = 17
ECHO_FRONT = 27
TRIG_LEFT = 5
ECHO_LEFT = 6
TRIG_RIGHT = 20                                                               # Trigger output for the ultrasonic sensor
ECHO_RIGHT = 21                                                               # Echo return from the ultrasonic sensor


# can use (17, 27), (5, 6), (20, 21)

# source code: https://forums.raspberrypi.com/viewtopic.php?t=77534 #godbless
def get_distance (trig_t, echo_t):

    trig = trig_t
    echo = echo_t
    if GPIO.input (echo):                                               # If the 'Echo' pin is already high
        return (100)                                                    # then exit with 100 (sensor fault)

    distance = 0                                                        # Set initial distance to zero

    GPIO.output (trig,False)                                            # Ensure the 'Trig' pin is low for at
    time.sleep (0.05)                                                   # least 50mS (recommended re-sample time)

    GPIO.output (trig,True)                                             # Turn on the 'Trig' pin for 10uS (ish!)
    dummy_variable = 0                                                  # No need to use the 'time' module here,
    dummy_variable = 0                                                  # a couple of 'dummy' statements will do fine
    
    GPIO.output (trig,False)                                            # Turn off the 'Trig' pin
    time1, time2 = time.time(), time.time()                             # Set inital time values to current time
    
    while not GPIO.input (echo):                                        # Wait for the start of the 'Echo' pulse
        time1 = time.time()                                             # Get the time the 'Echo' pin goes high
        if time1 - time2 > 0.02:                                        # If the 'Echo' pin doesn't go high after 20mS
            distance = 100                                              # then set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
    
    while GPIO.input (echo):                                            # Otherwise, wait for the 'Echo' pin to go low
        time2 = time.time()                                             # Get the time the 'Echo' pin goes low
        if time2 - time1 > 0.02:                                        # If the 'Echo' pin doesn't go low after 20mS
            distance = 100                                              # then ignore it and set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
        
                                                                        # Sound travels at approximately 2.95uS per mm
                                                                        # and the reflected sound has travelled twice
                                                                        # the distance we need to measure (sound out,
                                                                        # bounced off object, sound returned)
                                                                        
    distance = (time2 - time1) / 0.00000295 / 2 / 10                    # Convert the timer values into centimetres
    return (distance)                                                   # Exit with the distance in centimetres


GPIO.setwarnings(False)
sides = sys.argv[1: ]
active_sensors = []
if "LEFT" not in sides and "RIGHT" not in sides and "FRONT" not in sides:
    print("Please enter a valid sensor direction.")
    sys.exit()
if "LEFT" in sides: 
    GPIO.setup(TRIG_LEFT, GPIO.OUT)
    GPIO.setup(ECHO_LEFT, GPIO.IN)
    active_sensors.append("left")
if "RIGHT" in sides:
    GPIO.setup(TRIG_RIGHT, GPIO.OUT)
    GPIO.setup(ECHO_RIGHT, GPIO.IN)
    active_sensors.append("right")
if "FRONT" in sides:
    GPIO.setup(TRIG_FRONT, GPIO.OUT)
    GPIO.setup(ECHO_FRONT, GPIO.IN)
    active_sensors.append("front")

memory = sysv_ipc.SharedMemory(0x1234)
memory.write("I am testing a  write")

# only need to write if you are below the value? 
# i = memory_value.find('\0')
# if i != -1:
#     memory_value = memory_value[:i]
while(1):
    pass
# while (1):
#     print(get_distance(TRIG_RIGHT, ECHO_RIGHT))