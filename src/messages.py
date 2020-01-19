import datetime
from enum import Enum 
from typing import Dict, Union


class MCZInformation:

    def __init__(self, frame_id: int, name: str, message_type: str):
        """
        Params
        ------
        - `frame_id` (`int`):
            Position in RecuperoInfo frame
        - `name` (`str`)
            MCZ command name to be sent via Web Socket
        - `message_type` (`str`):
            Message type
        """
        self.frame_id = frame_id
        self.name = name
        self.message_type = message_type


MAESTRO_INFORMATION = [
    MCZInformation(0, 'message_type', 'message_type'),
    MCZInformation(1, 'stove_state', 'int'),
    MCZInformation(2, 'front_fan', 'int'),
    MCZInformation(3, 'lower_back_fan', 'int'),
    MCZInformation(4, 'lower_top_fan', 'int'),
    MCZInformation(5, 'fume_temperature', 'temperature'),
    MCZInformation(6, 'ambient_temperature', 'temperature'),
    MCZInformation(7, 'puffer_temperature', 'temperature'),
    MCZInformation(8, 'boiler_temperature', 'temperature'),
    MCZInformation(9, 'NTC3_temperature', 'temperature'),
    MCZInformation(10, 'candle_condition', 'int'),
    MCZInformation(11, 'active_set', 'int'),
    MCZInformation(12, 'rpm_fan_fume', 'int'),
    MCZInformation(13, 'rpm_wormwheel_set', 'int'),
    MCZInformation(14, 'rpm_wormwheel_life', 'int'),
    MCZInformation(15, '3wayvalve', '3way'),
    MCZInformation(16, 'pump_pwr', 'int'),
    MCZInformation(17, 'brazier', 'brazier'),
    MCZInformation(18, 'profile', 'int'),
    MCZInformation(19, 'modbus_address', 'int'),
    MCZInformation(20, 'active_mode', 'int'),
    MCZInformation(21, 'active_live', 'int'),
    # 0: auto mode, 1: manual mode
    MCZInformation(22, 'manual_control_mode', 'int'),
    MCZInformation(23, 'eco', 'int'),
    MCZInformation(24, 'silent', 'int'),
    MCZInformation(25, 'chrono', 'int'),
    MCZInformation(26, 'room_temperature', 'temperature'),
    MCZInformation(27, 'boiler_temperature', 'temperature'),
    MCZInformation(28, 'motherboard_temperature', 'temperature'),
    MCZInformation(29, 'power_level', 'int'),
    MCZInformation(30, 'firmware_version', 'int'),
    MCZInformation(31, 'database_id', 'int'),
    MCZInformation(32, 'hour', 'date-H'),
    MCZInformation(33, 'minute', 'date-M'),
    MCZInformation(34, 'day', 'date-d'),
    MCZInformation(35, 'month', 'date-m'),
    MCZInformation(36, 'year', 'date-Y'),
    MCZInformation(37, 'total_operating_hours', 'timespan'),
    MCZInformation(38, 'hours_of_operation_in_power1', 'timespan'),
    MCZInformation(39, 'hours_of_operation_in_power2', 'timespan'),
    MCZInformation(40, 'hours_of_operation_in_power3', 'timespan'),
    MCZInformation(41, 'hours_of_operation_in_power4', 'timespan'),
    MCZInformation(42, 'hours_of_operation_in_power5', 'timespan'),
    MCZInformation(43, 'hours_of_service', 'int'),
    MCZInformation(44, 'minutes_to_switch_off', 'int'),
    MCZInformation(45, 'number_of_ignitions', 'int'),
    MCZInformation(46, 'active_temperature', 'int'),
    MCZInformation(47, 'ferenheit', 'onoff'),
    MCZInformation(48, 'sound_effects', 'onoff'),
    MCZInformation(49, 'sound_effects_state', 'onoff'),
    MCZInformation(50, 'sleep', 'onoff'),
    MCZInformation(51, 'mode', 'onoff'),
    MCZInformation(52, 'wifi_sonde_temperature1', 'int'),
    MCZInformation(53, 'wifi_sonde_temperature2', 'int'),
    MCZInformation(54, 'wifi_sonde_temperature3', 'int'),
    MCZInformation(55, 'unknown', 'int'),
    MCZInformation(56, 'puffer', 'int'),
    MCZInformation(57, 'boiler', 'int'),
    MCZInformation(58, 'health', 'int'),
    MCZInformation(59, 'returntemperature', 'temperature'),
    MCZInformation(60, 'antifreeze', 'onoff'),
]


def get_mcz_info(frame_id: int) -> MCZInformation:
    """
    Return the MCZInformation relative to a RecuperoInfo position.

    Params
    ------
    `frame_id` (`int`):
        Frame ID position corresponding to a RecuperoInfo position

    Returns
    ------
    `mcz_information` (`MCZInformation`):
        MCZInformation relative to a RecuperoInfo position.
    """
    mcz_information = None
    if frame_id >= 0 and frame_id <= 60:
        mcz_information = MAESTRO_INFORMATION[frame_id]
    else:
        mcz_information = MCZInformation(frame_id, f'Unknown {frame_id}', 'int')
    return mcz_information


def format_seconds(seconds: int) -> str:
    """
    Formats seconds into HH:MM:SS

    Params
    ------
    - `seconds` (`int`):
        seconds integer

    Returns
    ------
    - `HH:MM:SS` (`str`)
    """
    return str(datetime.timedelta(seconds=seconds))


def websocket_message_to_dict(message: str) -> Dict[str, Union[float, int, str]]:
    """
    Format a Web Socket message into a human-readable dictionary.

    Params
    ------
    - `message` (`str`):
        Web Socket Message

    Returns
    ------
    - `result` (`dict`):
        Formatted result dictionary
    """
    result = {}
    message = message.split('|')
    date = 'Y-m-d H:M'
    for idx, content in enumerate(message):
        info = get_mcz_info(idx)
        content = int(content, 16)
        if info.message_type == 'temperature':
            result[info.name] = float(content) / 2
        elif info.message_type == 'timespan':
            result[info.name] = format_seconds(content)
        elif info.message_type == '3way':
            result[info.name] = 'Sani' if content == 1 else 'Risc'
        elif info.message_type == 'brazier':
            result[info.name] = 'OK' if content == 0 else 'CLEAR'
        elif info.message_type.startswith('date-'):
            date_part = info.message_type[-1]
            content = str(content)
            content = '0' + content if date_part == 'm' and len(content) == 1 else content
            date = date.replace(date_part, str(content))
        else:
            result[info.name] = content
    result['date'] = date
    return result
