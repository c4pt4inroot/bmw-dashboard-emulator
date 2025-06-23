"""
modules/abs.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    Module responsible for sending CAN messages related to the ABS (Anti-lock Braking System)
    status to the vehicle's dashboard. When ABS is disabled, it sends specific CAN frames
    to simulate the system state on the cluster.

    The `send_abs` function updates and sends two CAN frames:
    - The main ABS frame with a modified byte indicating system state.
    - A counter frame used for timing control, with increment and masking.

Usage:
    from modules.abs import send_abs

    send_abs(can, abs_enabled=False)
"""

CAN_BUS_ID_ABS = 0x19E
CAN_BUS_ID_ABS_COUNTER = 0x0C0

_abs_frame = [0x00, 0xE0, 0xB3, 0xFC, 0xF0, 0x43, 0x00, 0x65]
_abs_counter_frame = [0xF0, 0xFF]

def send_abs(can, abs_enabled: bool):
    """
    Envia mensagens ABS para o painel, se não estiver ativado.

    Args:
        can (CANInterface): Instância da interface CAN.
        abs_enabled (bool): Indica se o ABS está ativado.
    """
    if not abs_enabled:
        # Atualiza o byte 2 do frame ABS
        value = _abs_frame[2]
        upper = (value >> 4) + 3
        _abs_frame[2] = ((upper << 4) & 0xF0) | 0x03

        # Envia os frames ABS
        can.send_message(channel=1, can_id=f"{CAN_BUS_ID_ABS:03X}", data=_abs_frame)
        can.send_message(channel=1, can_id=f"{CAN_BUS_ID_ABS_COUNTER:03X}", data=_abs_counter_frame)

        # Incrementa o contador com OR em 0xF0
        _abs_counter_frame[0] = ((_abs_counter_frame[0] + 1) & 0x0F) | 0xF0
