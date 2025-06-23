"""
modules/handbrake.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides functionality to send the handbrake status
    over the CAN bus to the vehicle dashboard.

    The send_handbrake function sends a CAN message indicating whether
    the handbrake is engaged (active) or released.

Usage:
    from modules.handbrake import send_handbrake

    send_handbrake(can, handbrake_active=True)
"""

CAN_BUS_ID_HANDBRAKE = 0x34F
_handbrake_frame = [0xFE, 0xFF]

def send_handbrake(can, handbrake_active: bool):
    """
    Envia o estado do freio de mão via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        handbrake_active (bool): True se o freio de mão está puxado, False se está solto.
    """
    _handbrake_frame[0] = 0xFE if handbrake_active else 0xFD
    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_HANDBRAKE:03X}", data=_handbrake_frame)
