"""
modules/seatbelt.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides a function to send the seatbelt status
    via CAN bus to the vehicle dashboard.

    The status indicates whether the seatbelt is fastened or not
    by modifying a specific byte in the CAN frame.

Usage:
    from modules.seatbelt import send_seatbelt
    send_seatbelt(can, seatbelt_fastened=True)
"""

CAN_BUS_ID_SEATBELT = 0x581
_seatbelt_frame = [0x40, 0x4D, 0x00, 0x28, 0xFF, 0xFF, 0xFF, 0xFF]

def send_seatbelt(can, seatbelt_fastened: bool):
    """
    Envia o estado do cinto de segurança via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        seatbelt_fastened (bool): True se o cinto está afivelado, False se não.
    """
    _seatbelt_frame[3] = 0x29 if seatbelt_fastened else 0x28
    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_SEATBELT:03X}", data=_seatbelt_frame)
