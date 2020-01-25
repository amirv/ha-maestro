import queue
from typing import Union


COMMAND_QUEUE = None


def get_command_queue():
    global COMMAND_QUEUE
    if COMMAND_QUEUE is None:
        COMMAND_QUEUE = queue.Queue()
    return COMMAND_QUEUE


class MCZCommand:
    def __init__(self, name: str, mcz_id: int, command_type: str):
        """
        Params
        ------
        `name` (`str`):
            user friendly commnd name
        `mcz_id` (`int`):
            MCZ Web Socket ID
        `command_type` (`str`):
            Command type
        """
        self.name = name
        self.mcz_id = mcz_id
        self.command_type = command_type


MAESTRO_COMMANDS = {
    "get_info": MCZCommand("get_info", 0, "get_info"),
    "power": MCZCommand("power", 34, "onoff40"),
    "chrono": MCZCommand("chrono", 1111, "onoff"),
    "silent": MCZCommand("silent", 45, "onoff"),
    "active_mode": MCZCommand("active_mode", 35, "onoff"),
    "eco_mode": MCZCommand("eco_mode", 41, "onoff"),
    "room_temperature": MCZCommand("room_temperature", 42, "temperature"),
    "boiler_temperature": MCZCommand("boiler_temperature", 51, "temperature"),
    "chrono_t1": MCZCommand("chrono_t1", 1108, "temperature"),
    "chrono_t2": MCZCommand("chrono_t2", 1109, "temperature"),
    "chrono_t3": MCZCommand("chrono_t3", 1110, "temperature"),
    # 0: auto mode, 1: manual mode
    "manual_control_mode": MCZCommand("manual_control_mode", 40, "onoff"),
    "sound_effects": MCZCommand("sound_effects", 50, "onoff"),
    # 0, 1, 2, 3, 4, 5, 6
    # stove front fan (Air Fan)
    "front_fan": MCZCommand("front_fan", 37, "int"),
    # lower-back fan level (Ducted 1)
    "lower_back_fan": MCZCommand("lower_back_fan", 38, "int"),
    # lower-top fan level (Ducted 2)
    "lower_top_fan": MCZCommand("top_back_fan", 39, "int"),
    # manual power level
    "power_level": MCZCommand("power_level", 36, "int"),
}


def get_mcz_command(name: str) -> MCZCommand:
    """
    Params
    -------
    `alias`: `str`
        `MCZCommand` alias

    Returns
    -------
    `mc` (`MCZCommand`):
        MCZ Command instance relative to the alias
    """
    mc = MAESTRO_COMMANDS.get(name)
    return mc


def format_websocket_message(
    mcz_command: MCZCommand, value: Union[str, int, float]
) -> str:
    """
    Format a MCZ Command and a value to Web Socket message.
    It converts automatically Power (0, 1 -> 40, 1) and Temperature (25°C -> 25 * 2) values .

    Examples:

        - get_info (get stove information): 'C|RecuperoInfo'
        - Power (off): 'C|WriteParametri|34|40' Note: power off value = 40
        - Power (on): 'C|WriteParametri|34|1'
        - Temperature (25°C): 'C|WriteParametri|42|50' Note: temperature = value * 2

    Params
    ------
    `mcz_command` (`MCZCommand`):
        MestroCommand object
    `value` (`str | float | int`):
        Value to be sent via Web Socket

    Returns
    ------
    `ws_message` (`str`):
        Web Socket formatted message

    """
    ws_message = "C|RecuperoInfo"
    if not mcz_command.name == "get_info":
        ws_message = "C|WriteParametri"
        value = int(value)
        if mcz_command.command_type == "temperature":
            value = value * 2
        elif mcz_command.command_type == "onoff40":
            value = 40 if not value else 1
        elif mcz_command.command_type == "onoff":
            value = 1 if value else 0
        ws_message = f"{ws_message}|{mcz_command.mcz_id}|{value}"
    return ws_message
