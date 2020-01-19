import json
from typing import Dict, NoReturn, Union

import paho.mqtt.client as mqtt

import src.logger as logger
import src.cfg as cfg
import src.commands as commands


log = logger.get_logger('MQTT')


client = None
CommandQueue = commands.get_command_queue()


def on_connect(*args):
    log.info(f'MQTT connected to broker')


def on_message(client: mqtt.Client, userdata: Union[Dict, None], message: str) -> NoReturn:
    """
    Receive a mqtt message to be sent via Web Socket.
    
    Params
    ------
    `client` (`paho.mqtt.client.Client`):
        MQTT client for this callback
    `userdata` (`dict`):
        The private user data as set in Client() or userdata_set()
    `message` (`str`):
        Published message as string. It must be in the form { "command": command_name, "value": value }
    """
    message = json.loads(message.payload.decode())
    command, value = message.get('command'), message.get('value')
    log.info(f'MQTT -- Message received: {message}')
    command = commands.get_mcz_command(command) if command else None
    if not command:
        log.info('Unknown command received')
    CommandQueue.put((command, value))


def on_error(*args):
    log.info(f'MQTT error {args}')


def connect():
    """
    Connect to MQTT client awaiting for incoming messages to be sent via Web Socket to the stove.
    """
    global client
    if client: return client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_error = on_error
    client.connect(cfg.MQTT_IP, cfg.MQTT_PORT)
    client.loop_start()
    client.subscribe(cfg.MQTT_TOPIC_IN, qos=1)
    return client
