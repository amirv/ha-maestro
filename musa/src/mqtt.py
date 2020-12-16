import json
from typing import Dict, NoReturn, Union

import paho.mqtt.client as mqtt

import src.logger as logger
import src.cfg as cfg
import src.commands as commands
from src.cfg import MQTT_TOPIC_CLIMATE, MQTT_TOPIC_IN

log = logger.get_logger("MQTT")


client = None
COMMAND_QUEUE = commands.get_command_queue()

def on_connect(*args):
    log.info(f"MQTT connected to broker")

def on_message(
    client: mqtt.Client, userdata: Union[Dict, None], message: str
) -> NoReturn:
    log.info(f"unexpected topic: {message}")

def on_command(
    client: mqtt.Client, userdata: Union[Dict, None], message: str
) -> NoReturn:
    try:
        message = json.loads(message.payload.decode())
    except Exception as e:
        log.info(f"Error parsing payload {e}")
        return

    command, value = message.get("command"), message.get("value")
    log.info(f"MQTT -- Message received: {message}")
    command = commands.get_mcz_command(command) if command else None
    if not command:
        log.info("Unknown command received")
    COMMAND_QUEUE.put((command, value))

def send_state():
    command, value = commands.get_mcz_command("get_info"), 0
    COMMAND_QUEUE.put((command, value))

def on_mode (
    client: mqtt.Client, userdata: Union[Dict, None], message: str
) -> NoReturn:
    mode = message.payload.decode()
    command = commands.get_mcz_command("power")
    value = {
        "off": 0,
        "heat": 1
    }.get(mode, None)

    if value == None:
        log.info("Bad mode: {mode}")
        return

    COMMAND_QUEUE.put((command, value))
    send_state()

def on_target_temp (
    client: mqtt.Client, userdata: Union[Dict, None], message: str
) -> NoReturn:
    temp = message.payload.decode()
    command = commands.get_mcz_command("room_temperature")
    value = round(float(temp))

    COMMAND_QUEUE.put((command, value))
    send_state()

def on_error(*args):
    log.info(f"MQTT error {args}")

def on_log(*args):
    log.info(f"MQTT log {args}")

def connect():
    """
    Connect to MQTT client awaiting for incoming messages to be sent via Web Socket to the stove.
    """
    global client
    if client:
        return client
    client = mqtt.Client()
    if cfg.MQTT_AUTH:
        client.username_pw_set(username=cfg.MQTT_USER, password=cfg.MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_error = on_error
    client.connect(cfg.MQTT_IP, cfg.MQTT_PORT)
    client.loop_start()
    client.subscribe(f"{cfg.MQTT_TOPIC_IN}/#", qos=1)
    client.message_callback_add(f"{cfg.MQTT_TOPIC_IN}/command", on_command)
    client.message_callback_add(f"{cfg.MQTT_TOPIC_IN}/target_temp", on_target_temp)
    client.message_callback_add(f"{cfg.MQTT_TOPIC_IN}/mode", on_mode)

    config = {
                "name":"Livingroom",
                "mode_cmd_t": f"{MQTT_TOPIC_IN}/mode",
                "mode_stat_t": f"{MQTT_TOPIC_CLIMATE}/state",
                "mode_stat_tpl": "{%- if value_json.power == 0 %}off{% else %}heat{% endif -%}",
                "temp_cmd_t": f"{MQTT_TOPIC_IN}/target_temp",
                "temp_stat_t": f"{MQTT_TOPIC_CLIMATE}/state",
                "temp_stat_tpl":"{{ value_json.room_temperature }}",
                "curr_temp_t": f"{MQTT_TOPIC_CLIMATE}/state",
                "curr_temp_tpl": "{{ value_json.ambient_temperature }}",
                "min_temp":"15",
                "max_temp":"25",
                "temp_step":"1",
                "json_attributes_topic": f"{MQTT_TOPIC_CLIMATE}/state",
                "modes":["off", "heat"]
    }
    client.publish(f"{MQTT_TOPIC_CLIMATE}/config", json.dumps(config), retain = True, qos = 1)

    config = {
                "name":"Stove state",
                "state_topic": f"{MQTT_TOPIC_CLIMATE}/state",
                "value_template": "{{ value_json.power_mode_description }}",
                "json_attributes_topic": f"{MQTT_TOPIC_CLIMATE}/state",
    }
    client.publish(f"{cfg.MQTT_TOPIC_SENSOR}/config", json.dumps(config), retain = True, qos = 1)



    return client
