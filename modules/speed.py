"""
modules/speed.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module implements CAN message transmission for vehicle speed data.
    It maintains an internal state to accumulate speed values and manages
    a counter used in the CAN frame for timing or synchronization purposes.

    The send_speed function encodes the speed and counter into a CAN data frame
    and sends it via the provided CANInterface instance.

Usage:
    from modules.speed import send_speed
    send_speed(can, g_speed=50)
"""

CAN_BUS_ID_SPEED = 0x1A6

# Estado interno do módulo
_last_speed = 0
_speed_counter = 0x00F0

def send_speed(can, g_speed):
    """
    Envia velocidade (speed) ao painel via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        g_speed (int): Valor de velocidade para somar ao último.
    """
    global _last_speed, _speed_counter

    speed = g_speed + _last_speed
    _speed_counter = (_speed_counter + 315) & 0xFFFF

    # Quebra em bytes
    speed_low = speed & 0xFF
    speed_high = (speed >> 8) & 0xFF
    counter_low = _speed_counter & 0xFF
    counter_high = ((_speed_counter >> 8) | 0xF0) & 0xFF

    data = [
        speed_low, speed_high,
        speed_low, speed_high,
        speed_low, speed_high,
        counter_low, counter_high
    ]

    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_SPEED:03X}", data=data)

    _last_speed = speed