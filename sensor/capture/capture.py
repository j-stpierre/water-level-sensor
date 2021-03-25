import os
import time
from sensor.config import config
if config.config['ENV'] == 'development':
    import FakeRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO


class Capture:

    def __init__(self, triggerPin, echoPin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.triggerPin = triggerPin
        self.echoPin = echoPin

        GPIO.setup(self.triggerPin,GPIO.OUT)
        GPIO.setup(self.echoPin,GPIO.IN)

    def setStartState(self):
        GPIO.output(self.triggerPin, False)
        # Allow module to settle
        time.sleep(2)

    def getAverageDistance(self):
        distance1 = self.getDistance()
        while distance1 == -1 :
            distance1 = self.getDistance()

        distance2 = self.getDistance()
        while distance2 == -1 :
            distance2 = self.getDistance()

        distance3 = self.getDistance()
        while distance3 == -1 :
            distance3 = self.getDistance()

        average = (distance1 + distance2 + distance3)/3
        average = round(average, 2)
        return average

    def pulseTrigger(self):
        GPIO.output(self.triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(self.triggerPin, False)


    def getDistance(self):
        self.pulseTrigger()
        breakFunction = False
        breakTime = 3

        functionTime = time.time()
        start = time.time()
        stop = time.time()

        while GPIO.input(self.echoPin)==0:
            start = time.time()
            print (start-functionTime)
            if ((start - functionTime) > breakTime):
                breakFunction = True
                break

        while GPIO.input(self.echoPin)==1:
            stop = time.time()
            if ((start - functionTime) > breakTime):
                breakFunction = True
                break
        
        if (breakFunction):
            return -1

        elapsed = stop-start
        distanceInTime= elapsed * 34300
        distance  = distanceInTime /2
        time.sleep(1)

        return round(distance,2)

    def cleanup(self):
        GPIO.cleanup()