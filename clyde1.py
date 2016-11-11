#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Define pins
trig1 = 14
trig2 = 15
echo1 = 23
echo2 = 24

#Setup pins
GPIO.setup(trig1, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(trig2, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(echo1, GPIO.IN)
GPIO.setup(echo2, GPIO.IN)

def echo_callback1(channel):
    start = time.time()
    GPIO.wait_for_edge(echo1,GPIO.RISING)
    stop = time.time()
    elapsed = stop - start
    return elapsed

#Create callback events
GPIO.add_event_detect(echo1 ,GPIO.FALLING, callback = echo_callback1)
GPIO.add_event_detect(echo2 ,GPIO.FALLING, callback = echo_callback2)

#main Codes
try:
    while True:
        print('stuff')
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
