from sensor.mqtt import mqtt
import os
import unittest
import pytest
import json
from unittest import mock
from paho.mqtt import client as mqtt_client

class Test_mqtt(unittest.TestCase):
    
    def setUp(self):
        self.username = os.environ['USERNAME']
        self.password = os.environ['PASSWORD']
        self.broker = os.environ['BROKER']
        self.port = 1883
        self.client = mqtt.Mqtt(self.username, self.password, self.broker, self.port)
        
    def test_mqtt_constructor(self):
        self.assertEqual(self.client.username, self.username)
        self.assertEqual(self.client.password, self.password)
        self.assertEqual(self.client.broker, self.broker)
        self.assertEqual(self.client.port, self.port)
        self.assertIsInstance(self.client.client, mqtt_client.Client)

    def test_connect(self):
        self.client.client.username_pw_set = mock.MagicMock()
        self.client.client.connect = mock.MagicMock()
        self.client.connect()
        self.client.client.username_pw_set.assert_called_with(self.username, self.password)
        self.client.client.connect.assert_called_with(self.broker, self.port)

    def test_publish(self):
        topic = 'python/mqtt'
        message = {"test": "test"}
        self.client.client.publish = mock.MagicMock()
        self.client.publish(topic, message)
        self.client.client.publish.assert_called_with(topic, message)
