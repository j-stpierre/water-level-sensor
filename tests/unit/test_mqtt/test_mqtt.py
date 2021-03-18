import os
import pytest
import json
import config
from sensor.mqtt import mqtt
from unittest import mock, TestCase
from paho.mqtt import client as mqtt_client

class Test_mqtt(TestCase):
    
    def setUp(self):
        self.username = config.config['USERNAME']
        self.password = config.config['PASSWORD']
        self.broker = config.config['BROKER']
        self.port = config.config['PORT']
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
