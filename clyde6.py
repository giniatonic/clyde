#Clyde robot
#Author: Ginny Schilling, 11/13/2016
#Last Edited: Ginny Schilling, 12/12/2016
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
            if stopped == 0:
                print('case1')
                if(dF > 25 and dR < 25 and dL < 25):
                #In a corridor
                    print('case2')
                    if(abs(dL-dR) > 5):
                        print('case3')
                        if(dL > dR):
                            print('case4')
                            clyde.left(100,1)
                        else:
                            print('case5')
                            clyde.right(100,1)
                    clyde.forward(50) #go forward
                    stopped = 0
                elif(dF < 25):
                #Obstacle in front
                    print('case6')
                    clyde.stop()
                    stopped = 1

            if stopped == 1:
                print('case7')
                if(dF<25 and dR<25 and dL>25):
                    print('case8')
                #In a Left handed L-bracket
                    clyde.left(100,5.5)
                elif(dF<25 and dR>25 and dL<25):
                    print('case9')
                #In a Right handed L-bracket
                    clyde.right(100,5.5)
                elif(dF<25 and dR>25 and dL>25):
                    print('case10')
                #In a T-Junction
                    if(dR>dL):
                        print('case11')
                        clyde.right(100,5.5)
                    elif(dR<dL):
                        print('case12')
                        clyde.left(100,5.5)
                elif(dF<25 and dR<25 and dL<25):
                    print('case13')
                #Cornered!
                    clyde.backward(30,2)
                    clyde.left(100,10)
                elif(dF>25 and dR<20 and dL<20):
                    print('case14')
                #back in a corridor
                    clyde.forward(50)
                    stopped = 0
                elif(dF>25 and dR>20 and dL>20):
                    print('case15')
                #In open space
                    clyde.forward(50)
                    stopped = 0

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
