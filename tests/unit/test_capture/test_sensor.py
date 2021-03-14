import src.sensor.sensor as sensor
import unittest
import time
from unittest import mock
import os
if os.environ['env'] == 'development':
    import FakeRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO


class Test_sensor(unittest.TestCase):

    def setUp(self):
        self.device = sensor.Sensor(6,19)

    def test_constructor(self):
        GPIO.setup = mock.MagicMock()
        device = sensor.Sensor(6,19)
        
        self.assertEqual(device.triggerPin, 6)
        self.assertEqual(device.echoPin, 19)
        GPIO.setup.assert_has_calls([mock.call(device.triggerPin, GPIO.OUT), mock.call(device.echoPin, GPIO.IN)])

    def test_setStartState(self):
        GPIO.output = mock.MagicMock()
        time.sleep = mock.MagicMock()
        self.device.setStartState()
        GPIO.output.called
        time.sleep.called

    def test_getAverageDistance(self):
        self.device.getDistance = mock.MagicMock()
        self.device.getDistance.side_effect = [1,2,3]
        distance = self.device.getAverageDistance()
        self.assertEqual(distance, 2)

    def test_getDistance(self):
        GPIO.input = mock.MagicMock()
        time.time = mock.MagicMock()
        GPIO.input.side_effect = [0,1,1,0]
        time.time.side_effect = [0.001, 0.002, 0.003, 0.004]
        
        distance = self.device.getDistance()
        self.assertEqual(distance, 17.15)

    def test_pulseTrigger(self):
        GPIO.output = mock.MagicMock()
        time.sleep = mock.MagicMock()
        self.device.pulseTrigger()
        GPIO.output.assert_has_calls([mock.call(self.device.triggerPin, True), mock.call(self.device.triggerPin, False)])
        time.sleep.assert_called_with(0.00001)