"""
modules/lightning.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module provides a function to send vehicle lighting states 
    via CAN bus to the dashboard.

    Supported lights:
        - Side lights
        - Dip beam (low beam)
        - Main beam (high beam)
        - Front fog lights
        - Rear fog lights

    The lighting state is encoded into a CAN frame where each bit 
    represents a specific light. The frame is sent periodically 
    to update the dashboard indicators.
"""

CAN_BUS_ID_LIGHTNING = 0x21A

# Bits das luzes
SIDE       = 0x01
DIP        = 0x02
MAIN       = 0x04
FRONT_FOG  = 0x08
REAR_FOG   = 0x10

# Frame fixo com byte 2 sempre F7
lightning_frame = [0x00, 0x00, 0xF7]

def send_lightning(
    can,
    g_lights_side=False,
    g_lights_dip=False,
    g_lights_main=False,
    g_lights_front_fog=False,
    g_lights_rear_fog=False
):
    """
    Envia o estado das luzes para o painel via CAN.
    """
    lights = 0

    if g_lights_side:
        lights |= SIDE
    if g_lights_dip:
        lights |= DIP
    if g_lights_main:
        lights |= MAIN
    if g_lights_front_fog:
        lights |= FRONT_FOG
    if g_lights_rear_fog:
        lights |= REAR_FOG

    lightning_frame[0] = lights

    can.send_message(channel=1, can_id=f"{CAN_BUS_ID_LIGHTNING:03X}", data=lightning_frame)
