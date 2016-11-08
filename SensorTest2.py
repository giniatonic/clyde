#Ginny Schilling
#Clyde and stuff
#11/7/2016

#Libraries
import RPi.GPIO as io
import time

#setup
io.setmode(io.BCM)

#pins
senPin = 24
trigPin = 23
echoPin = 22

io.setup(senPin, io.IN)
io.setup(trigPin, io.OUT)

#set to high to begin with
io.output(trigPin, True)

#variables
#int senValue = 0
#int distValue = 0
bool measureType = 1 #1 for echo, 0 for analog sensor pin

time.sleep(0.5)

def distMeasure():
    io.output(trigPin, False) #low trigger
    time.sleep(0.00001)
    io.output(trigPin, True)
    while io.input(echoPin) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    if measureType == 1:
        distMeasure = TimeElapsed/50
    elif measureType == 0:
        senValue = io.input(senPin)
        distMeasure = senValue*0.718
    return distMeasure

try:
    while True:
        dist = distMeasure()
        print('Distance = %.1f cm' % dist)
        time.sleep(.5)

except KeyboardInterrupt:
    print('Measurement stopped by user')
    io.cleanup()
