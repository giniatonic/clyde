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
io.setup(echoPin,io.IN)

#set to low to begin with
io.output(trigPin, False)

#variables
#int senValue = 0
#int distValue = 0
measType = 1

time.sleep(0.5)

def distMeasure():
    io.output(trigPin, True) #low trigger
    time.sleep(0.00001)
    io.output(trigPin, False)

    while io.input(echoPin) == 0:
        print('my echo is low')
        StartTime = time.time()
    # save time of arrival
    while io.input(echoPin) == 1:
        print('my echo is high')
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    if measType == 1:
        distMeasure = TimeElapsed/50
    elif measType == 0:
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
