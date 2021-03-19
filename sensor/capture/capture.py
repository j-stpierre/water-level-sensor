import os
import time
if os.environ['env'] == 'development':
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
        distance2 = self.getDistance()
        distance3 = self.getDistance()
        average = (distance1 + distance2 + distance3)/3
        return average

    def pulseTrigger(self):
        GPIO.output(self.triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(self.triggerPin, False)


    def getDistance(self):
        self.pulseTrigger()
        start = time.time()
        stop = time.time()
        while GPIO.input(self.echoPin)==0:
            start = time.time()

        while GPIO.input(self.echoPin)==1:
            stop = time.time()
        
        elapsed = stop-start
        distanceInTime= elapsed * 34300
        distance  = distanceInTime /2

        return round(distance,2)