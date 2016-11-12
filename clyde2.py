#Libraries
import time
import RPi.GPIO as GPIO
import threading

#Globals
#Define pins
TRIG1 = 23
ECHO1 = 24

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Setup GPIO
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.output(TRIG1,False)

def us_run(trigger, echo, stop_event):
    while not stop_event.is_set():
        dist = measure_average(trigger, echo)
        print('Distance: %.1f' % dist)

def measure(trigpin,echopin):
    # This function measures a distance
    GPIO.output(trigpin, True)
    time.sleep(0.00001)
    GPIO.output(trigpin, False)
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

thread_stop = threading.Event()
threads = []

threads[0] = threading.Thread(target=us_run, args=(TRIG1, ECHO1, thread_stop))

try:
    threads[0].start()

    while True:
        print('Stilling running!')
        sleep(1)

except KeyboardInterrupt:
    thread_stop.set()
    for thread in threads:
        thread.join()
