#Ginny Schilling
#Clyde and stuff
#11/7/2016

#Libraries
import RPi.GPIO as io
import time

#setup
io.setmode(io.BCM)

#pins
#senPin = 24
trigPin = 18
echoPin = 24

#io.setup(senPin, io.IN)
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
    time.sleep(0.0001)
    io.output(trigPin, False)

    StartTime = time.time()
    print(StartTime)
    while io.input(echoPin) == 0:
        continue

    StopTime = time.time()
    print(StopTime)
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    TimeElapsed = TimeElapsed*(1*10^6)
    print('Time: %.1f us' % TimeElapsed)

    if measType == 1:
        distMeasure = TimeElapsed/50
    elif measType == 0:
        senValue = io.input(senPin)
        distMeasure = senValue*0.718
    return distMeasure

try:
    while True:
        dist = distMeasure()
        #print('Distance = %.1f cm' % dist)
        time.sleep(.5)

except KeyboardInterrupt:
    print('Measurement stopped by user')
    io.cleanup()
