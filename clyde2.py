#Libraries
import time
import RPi.GPIO as GPIO
import threading

#Globals
#Define pins
TRIG0 = 23
ECHO0 = 24
TRIG1 = 14
ECHO1 = 15

distances = []

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Setup GPIO
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.output(TRIG1,False)

def us_run(threadID,trigger, echo, stop_event):
    global distances
    while not stop_event.is_set():
        distances[threadID] = measure_average(trigger, echo)
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

distances.append(0)
threads.append(threading.Thread(target=us_run, args=(0,TRIG0, ECHO0, thread_stop)))

distances.append(0)
threads.append(threading.Thread(target=us_run, args=(1,TRIG1, ECHO1, thread_stop)))

try:
    threads[0].start()
    threads[1].start()

    while True:
        print('Stilling running!')
        time.sleep(1)

except KeyboardInterrupt:
    thread_stop.set()
    for thread in threads:
        thread.join()
