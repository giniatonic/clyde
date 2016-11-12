#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.output(GPIO_TRIGGER, False)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == GPIO.LOW
        a = 'nothing'

    #GPIO.wait_for_edge(GPIO_ECHO,GPIO.RISING)
    StopTime = time.time()


    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def distavg():
    d1 = distance()
    d2 = distance()
    d3 = distance()
    distavg = ((d1+d2+d3)/3)

    return distavg

if __name__ == '__main__':
    try:
        while True:
            dist = distavg()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(.5)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
