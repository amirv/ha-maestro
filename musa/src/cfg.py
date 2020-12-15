import json

with open("/data/options.json") as json_file:
    data = json.load(json_file)

MQTT_IP = data["mqtt_ip"]
MQTT_PORT = data["mqtt_port"]
MQTT_TOPIC_IN = data["mqtt_topic_in"]
MQTT_TOPIC_CLIMATE = data["mqtt_topic_climate"]
MQTT_TOPIC_SENSOR = data["mqtt_topic_sensor"]
MQTT_AUTH = data["mqtt_auth"]
MQTT_USER = data["mqtt_user"]
MQTT_PASS = data["mqtt_pass"]

MCZ_IP = data["mcz_ip"]
MCZ_PORT = data["mcz_port"]

INFO_INTERVAL = data["info_interval"]
