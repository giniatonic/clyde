#Clyde robot
#Author: Ginny Schilling, 11/13/2016
#Last Edited: Ginny Schilling, 12/13/2016
#-------------------------------------------------------

#Libraries
import time
import RPi.GPIO as GPIO
import threading
import Robot

GPIO.setwarnings(False)
#-------------------------------------------------------
#DEFINE FUNCTIONS

#Thread Target function
def us_run(threadID,name,trigger, echo, stop_event):
    global distances #create global variable for distances
    while not stop_event.is_set():
        distances[threadID] = measure_average(trigger, echo)
        time.sleep(0.1)
        print('Distance' + name + ': %.1f' % distances[threadID])


def measure(trigpin,echopin):
    # This function measures a distance
    GPIO.output(trigpin, True)
    time.sleep(0.00001)
    GPIO.output(trigpin, False)
    start = time.time()

    while GPIO.input(echopin)==0:
        start = time.time()

    stop = time.time()

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

#----------------------------------------------------------
#SETUP

#Constants
TRIG0 = 23
ECHO0 = 24
TRIG1 = 12
ECHO1 = 13
TRIG2 = 27
ECHO2 = 22

#create distances list for keeping track of ultrasonic sensor data
distances = []

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# SETUP GPIO pins
GPIO.setup(TRIG0,GPIO.OUT)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO0,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ECHO1,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ECHO2,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.output(TRIG0,False)
GPIO.output(TRIG1,False)
GPIO.output(TRIG2,False)

#SETUP threads
#The way to stop a thread, taken from thread library
thread_stop = threading.Event()
#create list for the threads to make them all stop from same event
threads = []

#add element to distances list
distances.append(0)
#create 0th thread
threads.append(threading.Thread(target=us_run, args=(0,'thread 0',TRIG0, ECHO0, thread_stop)))

distances.append(0)
#create 1st thread
threads.append(threading.Thread(target=us_run, args=(1,'thread 1',TRIG1, ECHO1, thread_stop)))

distances.append(0)
#create 2nd thread
threads.append(threading.Thread(target=us_run, args=(2,'thread 2',TRIG2, ECHO2, thread_stop)))

#SETUP motors
LEFT_TRIM = 0
RIGHT_TRIM = 0

clyde = Robot.Robot(left_id = 1, right_id = 2, left_trim = LEFT_TRIM, right_trim = RIGHT_TRIM)

#-------------------------------------------------------
#MAIN CODE

if __name__ == '__main__':
    try:
        threads[0].start()
        threads[1].start()
        threads[2].start()
        #lock = threading.Lock()
        time.sleep(1)
        stopped = 1
        while True:
            #lock.acquire()
            dF = distances[0]
            dR = distances[1]
            dL = distances[2]

            print('%f, %f, %f' % (dF, dR, dL))

            if(dF<15 and dR<15 and dL<15):
            #Cornered
                print('case1')
                clyde.stop()
                clyde.backward(30,2)
                clyde.left(150,7) #turn around
            elif(dF<15 and dR<15 and dL>15):
            #Blocked in front and to the right
                print('case2')
                clyde.stop()
                clyde.left(150,1)
            elif(dF<15 and dR>15 and dL<15):
            #Blocked in front and to the left
                print('case3')
                clyde.stop()
                clyde.right(150,1)
            elif(dF<15 and dR>15 and dL>15):
            #At an intersection where he could go right or left
                print('case4')
                if(dR>dL):
                #Decides to go right
                    print('case5')
                    clyde.right(150,2)
                else:
                #Decides to go left
                    print('case6')
                    clyde.left(150,2)
            elif(dF>15 and dR<15 and dL<15):
            #In a corridor
                print('case7')
                clyde.forward(50)
            elif(dF>15 and dR<15 and dL>15):
            #Askew in a corridor
                print('case8')
                clyde.stop()
                clyde.left(150,1)
            elif(dF>15 and dR>15 and dL<15):
            #Askew in a corridor
                print('case9')
                clyde.stop()
                clyde.right(150,1)
            elif(dF>15 and dR>15 and dL>15):
            #In open space
                print('case10')
                clyde.forward(50)
            else:
            #Any case not thought of
                print('case11')
                clyde.stop()
                if(dR>dL):
                #Decides to go right
                    print('case12')
                    clyde.right(150,1)
                else:
                #Decides to go left
                    print('case13')
                    clyde.left(150,1)

            time.sleep(.1)
            #print('distances: %.1f , %.1f' % (distances[0], distances[1]))
            #lock.release()

    except KeyboardInterrupt:
        thread_stop.set()
        for thread in threads:
            thread.join()
        GPIO.cleanup()

    except Exception as e:
        print('Dude whats my error?')
        print(e.message)
        thread_stop.set()
        for thread in threads:
            thread.join()
        GPIO.cleanup()
