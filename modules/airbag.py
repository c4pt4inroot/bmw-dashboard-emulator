"""
modules/airbag.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module handles sending CAN messages related to the airbag system status
    to the vehicle's dashboard cluster.

    The `send_airbag` function sends a predefined CAN frame when the airbag system
    is disabled (airbag_enabled=False). It increments a byte in the frame to simulate
    frame variation over time.

Usage:
    from modules.airbag import send_airbag

    send_airbag(can, airbag_enabled=False)
"""

CAN_BUS_ID_AIRBAG = 0x0D7

_airbag_frame = [0xC3, 0xFF]

def send_airbag(can, airbag_enabled: bool):
    """
    Envia mensagem do airbag via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        airbag_enabled (bool): True se airbag está ativo (não envia frame).
    """
    if not airbag_enabled:
        can.send_message(channel=1, can_id=f"{CAN_BUS_ID_AIRBAG:03X}", data=_airbag_frame)
        _airbag_frame[0] = (_airbag_frame[0] + 1) & 0xFF