import json
import config
from sensor.mqtt import mqtt
from sensor.capture import capture

def main():
    broker = mqtt.Mqtt(
                    config.config['USERNAME'],
                    config.config['PASSWORD'],
                    config.config['BROKER'],
                    config.config['PORT'])

    try:
        broker.connect()
        sensor = capture.Capture(6,19)
        sensor.setStartState()
        distance = sensor.getAverageDistance()
        broker.publish(config.config['TOPIC'], distance)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Measurement stopped")
    finally:
        sensor.cleanup()

if __name__ == '__main__':
    main()