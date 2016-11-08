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

io.setup(senPin, io.IN)
io.setup(trigPin, io.OUT)

#variables
#int senValue = 0
#int distValue = 0

time.sleep(0.5)

def distMeasure():
    io.output(trigPin, True)
    time.sleep(0.00001)
    io.output(trigPin, False)
    senValue = io.input(senPin)
    distMeasure = senValue*0.718
    return distMeasure

try:
    while True:
        dist = distMeasure()
        print('Distance = %.1f cm' % dist)
        time.sleep(.25)

except KeyboardInterrupt:
    print('Measurement stopped by user')
    io.cleanup()
