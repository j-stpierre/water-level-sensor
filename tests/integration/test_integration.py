import src.mqtt.mqtt as mqtt
from unittest import mock
import os

def test_connect_mqtt():
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    broker = os.environ['BROKER']
    port = 1883
    client = mqtt.Mqtt(username,password,broker,port)
    client.connect()
