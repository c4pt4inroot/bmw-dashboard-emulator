"""
modules/time.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module sends date and time information to the vehicle dashboard via CAN bus.
    The send_time function encodes hour, minute, second, day, month, and year into a
    CAN data frame and transmits it through the given CANInterface instance.

Usage:
    from modules.time import send_time
    send_time(can, hour=14, minute=35, second=12, day=21, month=6, year=2025)
"""

CAN_BUS_ID_TIME = 0x39E
_time_frame = [0x0B, 0x10, 0x00, 0x0D, 0x1F, 0xDF, 0x07, 0xF2]

def send_time(can, hour, minute, second, day, month, year):
    """
    Envia data e hora via CAN para o painel.

    Args:
        can (CANInterface): Instância da interface CAN.
        hour (int): Horas (0–23)
        minute (int): Minutos (0–59)
        second (int): Segundos (0–59)
        day (int): Dia do mês (1–31)
        month (int): Mês (1–12)
        year (int): Ano (ex: 2025)
    """
    _time_frame[0] = hour & 0xFF
    _time_frame[1] = minute & 0xFF
    _time_frame[2] = second & 0xFF
    _time_frame[3] = day & 0xFF
    _time_frame[4] = ((month << 4) & 0xF0) | 0x0F
    _time_frame[5] = year & 0xFF
    _time_frame[6] = (year >> 8) & 0xFF

    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_TIME:03X}", data=_time_frame)
