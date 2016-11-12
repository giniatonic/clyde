#Libraries
import time
import RPi.GPIO as GPIO
import USThreads as UST

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Define pins
trig1 = 23
echo1 = 24

t1 = UST.USThreads(1,trig1,echo1)

#main Codes
try:
    t1.start()

except KeyboardInterrupt:
    t1.exitflag = 1
    t1.join()
    GPIO.cleanup()
#GPIO.cleanup()
