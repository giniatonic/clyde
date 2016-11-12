#Libraries
import time
import USThreads as UST

#GPIO Mode (BOARD / BCM)


#Define pins
trig1 = 23
echo1 = 24

t1 = UST(1,trig1,echo1)

#main Codes
try:
    t1.start()

except KeyboardInterrupt:
    UST.exitflag = 1
    t1.join()
    GPIO.cleanup()
GPIO.cleanup()
