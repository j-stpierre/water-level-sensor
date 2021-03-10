from paho.mqtt import client as mqtt_client


def connect_mqtt(broker, port, username, password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.connect(broker, port)
    return client


def publish(client, topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print("Sent message")
    else:
        print(f"Failed to send message to topic {topic}")