#Libraries
import time
import RPi.GPIO as GPIO
import threading

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Define pins
trig1 = 23
echo1 = 24

GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.output(trig1,False)

#Define my stupid thread class and stuff
class USThreads(threading.Thread):
    def __init__(self, threadID, trigpin, echopin):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.trigpin = trigpin
        self.echopin = echopin
        #GPIO.setmode(GPIO.BCM)
        self.exitflag = 0

    def run(self):
        while not self.exitflag:
            dist = measure_average(self.trigpin,self.echopin)
            print('Distance: %.1f' % dist)


def measure(trigpin,echopin):
    # This function measures a distance
    GPIO.output(trigpin, True)
    time.sleep(0.00001)
    GPIO.output(echopin, False)
    start = time.time()

    while GPIO.input(echopin)==0:
        start = time.time()

    while GPIO.input(echopin)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2
    return distance

def measure_average(trigpin,echopin):
    # This function takes 3 measurements and
    # returns the average.
    distance1=measure(trigpin,echopin)
    time.sleep(0.1)
    distance2=measure(trigpin,echopin)
    time.sleep(0.1)
    distance3=measure(trigpin,echopin)
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

#Initialize thread 1
t1 = UST.USThreads(1,trig1,echo1)

#main Codes
try:
    #start thread
    t1.start()

except KeyboardInterrupt:
    t1.exitflag = 1
    t1.join()
    GPIO.cleanup()
#GPIO.cleanup()
