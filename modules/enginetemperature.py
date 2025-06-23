"""
modules/engine_temperature.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides functionality to send engine temperature data
    over CAN to the vehicle dashboard.

    The send_engine_temperature function encodes the engine temperature
    with a fixed offset and sends it as part of a CAN frame. A control byte
    is incremented on each message to simulate dynamic data.

Usage:
    from modules.engine_temperature import send_engine_temperature

    send_engine_temperature(can, temp_celsius=90)
"""

CAN_BUS_ID_ENGINE_TEMP = 0x1D0

_engine_temp_frame = [0x00, 0xFF, 0x63, 0xCD, 0x5D, 0x37, 0xCD, 0xA8]

def send_engine_temperature(can, temp_celsius: int):
    """
    Envia temperatura do motor via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        temp_celsius (int): Temperatura do motor em graus Celsius.
    """
    # Converte temperatura (offset de +48)
    temp_encoded = (temp_celsius + 48) & 0xFF
    _engine_temp_frame[0] = temp_encoded

    # Incrementa byte de controle
    _engine_temp_frame[2] = (_engine_temp_frame[2] + 1) & 0xFF

    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_ENGINE_TEMP:03X}", data=_engine_temp_frame)
