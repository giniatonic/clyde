import threading
import time
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)

class USThreads(threading.Thread):
    def __init__(self, threadID, trigpin, echopin):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.trigpin = trigpin
        self.echopin = echopin
        #GPIO.setmode(GPIO.BCM)
        self.exitflag = 0
        GPIO.setup(trigpin,GPIO.OUT)
        GPIO.setup(echopin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        GPIO.output(trigpin,False)

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
