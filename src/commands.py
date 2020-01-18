from typing import Union


class MaestroCommand:

    def __init__(self, name: str, maestro_id: int, command_type: str):
        """
        Params
        ------
        - `name` (`str`):
            user friendly commnd name
        - `maestro_id` (`int`):
            Maestro Web Socket ID
        - `command_type` (`str`):
            Command type
        """
        self.name = name
        self.maestro_id = maestro_id
        self.command_type = command_type


MAESTRO_COMMANDS = {
    'Refresh': MaestroCommand('Refresh', 0, 'Refresh'),
    'Power': MaestroCommand('Power', 34, 'onoff40'),
    'GetInfo': MaestroCommand('GetInfo', 0, 'GetInfo'),
    'Temperature_Setpoint': MaestroCommand('Temperature_Setpoint', 42, 'temperature'),
    'Boiler_Setpoint': MaestroCommand('Boiler_Setpoint', 51, 'temperature'),
    'Chronostat': MaestroCommand('Chronostat', 1111, 'onoff'),
    'Chronostat_T1': MaestroCommand('Chronostat_T1', 1108, 'temperature'),
    'Chronostat_T2': MaestroCommand('Chronostat_T2', 1109, 'temperature'),
    'Chronostat_T3': MaestroCommand('Chronostat_T3', 1110, 'temperature'),
    'Power_Level': MaestroCommand('Power_Level', 36, 'int'),
    'Silent_Mode': MaestroCommand('Silent_Mode', 45, 'onoff'),
    'Active_Mode': MaestroCommand('Active_Mode', 35, 'onoff'),
    'Eco_Mode': MaestroCommand('Eco_Mode', 41, 'onoff'),
    'Sound_Effects': MaestroCommand('Sound_Effects', 50, 'onoff'),
    # 0, 1, 2, 3, 4, 5, 6
    'Fan_State': MaestroCommand('Fan_State', 37, 'int'),
    # 0 -> Auto, 1 -> Manual
    'Control_Mode': MaestroCommand('Control_Mode', 40, 'onoff'),
}


def get_maestro_command(name: str) -> MaestroCommand:
    """
    Params
    -------
    `alias`: `str`
        `MaestroCommand` alias

    Returns
    -------
        `mc` (`MaestroCommand`):
            Maestro Command instance relative to the alias
    """
    mc = MAESTRO_COMMANDS.get(name) or MaestroCommand('Unknown', -1, 'Unknown')
    return mc


def format_websocket_message(
        maestro_command: MaestroCommand,
        value: Union[str, int, float]
    ) -> str:
    """
    Format a Maestro Command and a value to Web Socket message.
    It converts automatically Power (0, 1 -> 40, 1) and Temperature (25°C -> 25 * 2) values .

    Examples:

        - GetInfo (get stove information): 'C|RecuperoInfo'
        - Power (off): 'C|WriteParametri|34|40' Note: power off value = 40
        - Power (on): 'C|WriteParametri|34|1'
        - Temperature (25°C): 'C|WriteParametri|42|50' Note: temperature = value * 2

    Params
    ------
    `maestro_command` (`MaestroCommand`):
        MestroCommand object
    `value` (`str | float | int`):
        Value to be sent via Web Socket

    Returns
    ------
    `ws_message` (`str`):
        Web Socket formatted message

    """
    ws_message = 'C|RecuperoInfo'
    if not maestro_command.name == 'GetInfo':
        ws_message = 'C|WriteParametri'
        value = int(value)
        if maestrocommand.command_type == 'temperature':
            value = value * 2
        elif maestrocommand.command_type == 'onoff40':
            value = 40 if not int(value) else 1
        elif maestrocommand.command_type == 'onoff':
            value = value if value == 1 else 0
        ws_message = f'{ws_message}|{maestro_command.maestroid)|{writevalue}'
    return ws_message
