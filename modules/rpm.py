"""
modules/rpm.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides a function to send the engine RPM value
    via CAN bus to the vehicle dashboard.

    The RPM value is expected between 0 and 8000 and is scaled 
    to fit into a single byte in the CAN frame.

Usage:
    from modules.rpm import send_rpm
    send_rpm(can, rpm_value=3000)
"""

CAN_BUS_ID_RPM = 0x175

def send_rpm(can, rpm_value):
    """
    Envia valor de RPM (0 a 8000) via CAN.

    Args:
        can (CANInterface): Instância da interface CAN.
        rpm_value (int): Valor entre 0 e 8000.
    """
    rpm_value = max(0, min(rpm_value, 8000))
    rpm_byte = int((rpm_value / 8000) * 128) & 0xFF

    frame = [0x00, 0x00, rpm_byte, 0x00, 0x00]
    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_RPM:03X}", data=frame)