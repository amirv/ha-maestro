import _thread as thread
import json
import threading
import time
from typing import NoReturn
import websocket

import src.cfg as cfg
import src.logger as logger
import src.commands as commands
import src.messages as messages
import src.mqtt as mqtt


log = logger.get_logger("WebSocket")
COMMAND_QUEUE = commands.get_command_queue()


def get_stove_info():
    """
    Get Stove information every `INFO_INTERVAL` seconds.
    """
    threading.Timer(cfg.INFO_INTERVAL, get_stove_info).start()
    command, value = commands.get_mcz_command("get_info"), 0
    COMMAND_QUEUE.put((command, value))


def on_open(ws: websocket.WebSocketApp) -> NoReturn:
    """
    Queue messages consumer. It sends the encoded messages to MCZ Musa Web Socket.
    """
    log.info("Successfully connected. Consuming message on MQTT queue")

    def run():
        while ws.keep_running:
            time.sleep(0.25)
            while not COMMAND_QUEUE.empty():
                command, value = COMMAND_QUEUE.get()
                log.debug(f"command: {command} value: {value}")

                ws_message = commands.format_websocket_message(command, value)
                log.debug(f"Sending message: {ws_message}")
                try:
                    ws.send(ws_message)
                except Exception as e:
                    log.error(f"Web Socket connection error {e}")
                    ws.close()

            log.warn("COMMAND_QUEUE thread exited")

    thread.start_new_thread(run, ())


def on_message(ws: websocket.WebSocketApp, message: str) -> NoReturn:
    """
    Parse info message (eg. 01|some|other|values) and publish it to MQTT.
    """
    if message.split("|")[0] == "01":
        # Info message code: 01
        log.debug("Info message received")
        parsed_message = messages.websocket_message_to_dict(message)
        client = mqtt.connect()
        #log.info(f"Publishing message to MQTT: {parsed_message}")
        client.publish(f"{cfg.MQTT_TOPIC_CLIMATE}/state", json.dumps(parsed_message), 1)
    else:
        log.warn(f"Unsupported message received {message}")


def on_error(ws: websocket.WebSocketApp, error: str) -> NoReturn:
    log.warn(f"WebSocket error: {error}")
    if isinstance(error, KeyboardInterrupt):
        raise KeyboardInterrupt


def _connect() -> NoReturn:
    """
    Connect to MCZ Musa Web Socket.
    """
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        f"ws://{cfg.MCZ_IP}:{cfg.MCZ_PORT}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
    )
    while True:
        try:
            ws.run_forever(ping_interval=5, ping_timeout=2)
        except KeyboardInterrupt:
            log.info("Connection interrupted by user")
            break
        except:
            ws.close()
            time.sleep(5)


def connect() -> NoReturn:
    """
    Connect to MCZ Musa Web Socket and keep the connection alive.
    """
    log.info("Connecting to MCZ MUSA")
    _connect()
