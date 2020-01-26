"""
Example of reading get_info messages from MQTT broker.
"""
import json
import time
import paho.mqtt.client as mqtt


MQTT_IP = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC_OUT = "/mcz/out"


def on_message(client, userdata, message):
    print(f"Message received {message.payload.decode()}")


client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_IP, MQTT_PORT)
client.subscribe(MQTT_TOPIC_OUT, qos=1)
client.loop_start()


while True:
    print("MQTT connection is active")
    time.sleep(60)
