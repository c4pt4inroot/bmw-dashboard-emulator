
"""
modules/ignition.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides functionality to send ignition status frames
    over the CAN bus to a vehicle dashboard.

    The send_ignition function sends a CAN message indicating whether
    the ignition is ON or OFF. It also updates a rolling counter byte
    in the frame for message tracking.

Usage:
    from modules.ignition import send_ignition

    send_ignition(can, ignition_on=True)  # Turn ignition ON
    send_ignition(can, ignition_on=False) # Turn ignition OFF
"""

CAN_BUS_ID_IGNITION = 0x130

ignition_frame_on = [0x45, 0x42, 0x21, 0x8F, 0xEF]
ignition_frame_off = [0x00, 0x00, 0xC0, 0x0F, 0xE2]

def send_ignition(can, ignition_on):
    """
    Envia o frame de ignição ON ou OFF para o painel.
    
    Args:
        can (CANInterface): instância da interface CAN.
        ignition_on (bool): True para ligar, False para desligar.
    """
    global ignition_frame_on, ignition_frame_off

    if ignition_on:
        can.send_message(channel=1, can_id=f"{CAN_BUS_ID_IGNITION:03X}", data=ignition_frame_on)
        ignition_frame_on[4] = (ignition_frame_on[4] + 1) & 0xFF
    else:
        can.send_message(channel=1, can_id=f"{CAN_BUS_ID_IGNITION:03X}", data=ignition_frame_off)
        ignition_frame_off[4] = (ignition_frame_off[4] + 1) & 0xFF