import json
import paho.mqtt.client as mqtt

import src.cfg as cfg


client = mqtt.Client()
client.connect(cfg.MQTT_IP, cfg.MQTT_PORT)

get_info = { 'command': 'get_info', 'value': 1 }
power_on = { 'command': 'power', 'value': 1 }
power_off = { 'command': 'power', 'value': 0 }
temperature = { 'command': 'room_temperature', 'value': 24 }

fan_state_front = { 'command': 'front_fan', 'value': 1 }
fan_state_lower_back = { 'command': 'lower_back_fan', 'value': 1 }
fan_state_lower_top = { 'command': 'lower_top_fan', 'value': 1 }

client.publish(cfg.MQTT_TOPIC_IN, json.dumps(get_info), 1)
