from paho.mqtt import client as mqtt_client
import json


class Mqtt:

    def __init__(self, username, password, broker, port):
        self.username = username
        self.password = password
        self.broker = broker
        self.port = port
        self.client = mqtt_client.Client()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port)

    def publish(self, topic, message):
        result = self.client.publish(topic, message)
        status = result[0]
        if status == 0:
            print("Sent message")
        else:
            print(f"Failed to send message to topic {topic}")