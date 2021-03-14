import os
from unittest import mock
from sensor.mqtt import mqtt

def test_connect_mqtt():
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    broker = os.environ['BROKER']
    port = 1883
    client = mqtt.Mqtt(username,password,broker,port)
    client.connect()
