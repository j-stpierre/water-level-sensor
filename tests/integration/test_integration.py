import src.mqtt.mqtt
from unittest import mock

def test_connect_mqtt():
    username = "user"
    password = "password"
    broker = '192.168.2.51'
    port = 1883
    client = src.mqtt.mqtt.connect_mqtt(broker, port, username, password)