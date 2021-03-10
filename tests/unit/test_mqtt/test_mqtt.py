import src.mqtt.mqtt
from unittest import mock
from paho.mqtt import client as mqtt_client


def test_connect_mqtt():
    username = "user"
    password = "password"
    broker = '192.168.2.51'
    port = 1883
    mqtt_client.Client = mock.MagicMock()

    client = src.mqtt.mqtt.connect_mqtt(broker, port, username, password)
    assert mqtt_client.Client.called
    client.username_pw_set.assert_called_with(username, password)
    assert client.connect.called

def test_publishes():
    topic = 'python/test'
    message = {'test': 'test'}
    client = mock.MagicMock()
    src.mqtt.mqtt.publish(client, topic, message)
    assert client.publish.called
