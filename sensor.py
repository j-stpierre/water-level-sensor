import json
import time
import sys
from sensor.config import config
from sensor.mqtt import mqtt
from sensor.capture import capture

def main():
    broker = mqtt.Mqtt(
                    config.config['USERNAME'],
                    config.config['PASSWORD'],
                    config.config['BROKER'],
                    config.config['PORT'])
    sensor = capture.Capture(6,19)
    try:
        broker.connect()
        
        sensor.setStartState()
        while True:
            distance = sensor.getAverageDistance()
            distance = json.dumps({'distance': distance})
            broker.publish(config.config['TOPIC'], distance)
            time.sleep(5)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Measurement stopped")
    finally:
        sensor.cleanup()
        sys.exit(1)

if __name__ == '__main__':
    main()