import time
from sensor.config import config
from sensor.capture import capture
from unittest import mock, TestCase
if config.config['ENV'] == 'development':
    import FakeRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO


class Test_capture(TestCase):

    def setUp(self):
        self.device = capture.Capture(6,19)

    def test_constructor(self):
        GPIO.setup = mock.MagicMock()
        device = capture.Capture(6,19)
        self.assertEqual(device.triggerPin, 6)
        self.assertEqual(device.echoPin, 19)
        GPIO.setup.assert_has_calls([mock.call(device.triggerPin, GPIO.OUT), mock.call(device.echoPin, GPIO.IN)])

    def test_setStartState(self):
        GPIO.output = mock.MagicMock()
        time.sleep = mock.MagicMock()
        self.device.setStartState()
        assert GPIO.output.called
        assert time.sleep.called

    def test_getAverageDistance(self):
        self.device.getDistance = mock.MagicMock()
        self.device.getDistance.side_effect = [1,2,3]
        distance = self.device.getAverageDistance()
        self.assertEqual(distance, 2)

    def test_getAverageDistanceRounded(self):
        self.device.getDistance = mock.MagicMock()
        self.device.getDistance.side_effect = [1.1111,2.2222,3.3333]
        distance = self.device.getAverageDistance()
        self.assertEqual(distance, 2.22)

    def test_getAverageDistanceRounded_with_retry(self):
        self.device.getDistance = mock.MagicMock()
        self.device.getDistance.side_effect = [1.1111,-1,2.2222,3.3333]
        distance = self.device.getAverageDistance()
        self.assertEqual(distance, 2.22)

    def test_getDistance(self):
        GPIO.input = mock.MagicMock()
        time.time = mock.MagicMock()
        self.device.pulseTrigger = mock.MagicMock()
        GPIO.input.side_effect = [0,1,1,0]
        time.time.side_effect = [0.0001, 0.001, 0.002, 0.003, 0.004]
        distance = self.device.getDistance()
        self.assertEqual(distance, 17.15)
        assert self.device.pulseTrigger.called
        GPIO.input.side_effect = [0,1,1,0]
        time.time.side_effect = [0.001, 0.002, 0.003, 0.004]
    
    def test_getDistance_stuck(self):
        GPIO.input = mock.MagicMock()
        time.time = mock.MagicMock()
        self.device.pulseTrigger = mock.MagicMock()
        GPIO.input.side_effect = [0,0,0]
        time.time.side_effect = [0.001, 0.002, 0.003, 0.004, 4]
        distance = self.device.getDistance()
        self.assertEqual(distance, -1)



    def test_pulseTrigger(self):
        GPIO.output = mock.MagicMock()
        time.sleep = mock.MagicMock()
        self.device.pulseTrigger()
        GPIO.output.assert_has_calls([mock.call(self.device.triggerPin, True), mock.call(self.device.triggerPin, False)])
        time.sleep.assert_called_with(0.00001)

    def test_cleanup(self):
        GPIO.cleanup = mock.MagicMock()
        self.device.cleanup()
        assert GPIO.cleanup.called