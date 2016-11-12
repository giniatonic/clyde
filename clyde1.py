#Libraries
import time
import RPi.GPIO as GPIO
import USThreads as UST

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Define pins
trig1 = 23
echo1 = 24

GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.output(trig1,False)

t1 = UST.USThreads(1,trig1,echo1)

#main Codes
try:
    t1.start()

except KeyboardInterrupt:
    t1.exitflag = 1
    t1.join()
    GPIO.cleanup()
#GPIO.cleanup()
