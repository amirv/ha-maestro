"""
Example of messages publishing on MQTT broker.
"""
import json
import paho.mqtt.client as mqtt


MQTT_IP = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC_IN = 'in_mcz'


get_info = { 'command': 'get_info', 'value': 1 }
# power_on = { 'command': 'power', 'value': 1 }
# power_off = { 'command': 'power', 'value': 0 }
# temperature = { 'command': 'room_temperature', 'value': 24 }
# fan_state_front = { 'command': 'front_fan', 'value': 1 }
# fan_state_lower_back = { 'command': 'lower_back_fan', 'value': 1 }
# fan_state_lower_top = { 'command': 'top_back_fan', 'value': 1 }

client = mqtt.Client()
client.connect(MQTT_IP, MQTT_PORT)
client.publish(MQTT_TOPIC_IN, json.dumps(get_info), 1)
