"""
modules/fuel.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides functionality to send fuel level information
    over the CAN bus to the vehicle dashboard.

    The send_fuel function maps the fuel percentage (0-100%) to the
    appropriate encoded value and sends it in a CAN message.

Usage:
    from modules.fuel import send_fuel

    send_fuel(can, fuel_percent=75)
"""

CAN_BUS_ID_FUEL = 0x349
_fuel_frame = [0x00, 0x00, 0x00, 0x00, 0x00]

def _map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def send_fuel(can, fuel_percent: int):
    """
    Envia o nível de combustível via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        fuel_percent (int): Percentual de combustível (0 a 100).
    """
    fuel_percent = max(0, min(fuel_percent, 100))
    fuel = _map_value(fuel_percent, 0, 100, 0, 8320)

    low = fuel & 0xFF
    high = (fuel >> 8) & 0xFF

    _fuel_frame[0] = low
    _fuel_frame[1] = high
    _fuel_frame[2] = low
    _fuel_frame[3] = high

    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_FUEL:03X}", data=_fuel_frame)
