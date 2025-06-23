"""
modules/indicators.py

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This module defines the IndicatorController class to manage
    the state of vehicle turn signals and send the corresponding
    CAN messages to the dashboard.

    Supported indicator states:
        0 = Off
        1 = Left indicator on
        2 = Right indicator on
        3 = Hazard (all indicators on)

    The controller handles timing and toggling the indicator lights
    based on the requested state and sends periodic CAN frames.

Usage:
    from modules.indicators import IndicatorController

    indicators = IndicatorController()
    indicators.send_indicators(can, indicator_state=1)  # Left indicator on
"""

import time

CAN_BUS_ID_INDICATORS = 0x1F6

class IndicatorController:
    def __init__(self):
        self._frame = [0x80, 0xF0]
        self._last_indicator = 0
        now = self._current_millis()
        self._last_indicator_time = now
        self._last_frame_time = now

    def _current_millis(self):
        return int(time.time() * 1000)

    def send_indicators(self, can, indicator_state: int):
        """
        Envia o estado das setas via CAN.
        
        Args:
            can (CANInterface): Instância da interface CAN.
            indicator_state (int): 
                0 = desligado,
                1 = esquerda,
                2 = direita,
                3 = alerta
        """
        current = self._current_millis()
        light_indicator = self._last_indicator

        if indicator_state == 0:
            if current - self._last_indicator_time >= 600:
                light_indicator = 0
        else:
            light_indicator = indicator_state
            self._last_indicator_time = current

        if (self._last_indicator != light_indicator) or (current - self._last_frame_time >= 600):
            if light_indicator != 0:
                self._frame[0] = {
                    1: 0x91,  # esquerda
                    2: 0xA1,  # direita
                    3: 0xB1   # alerta
                }.get(light_indicator, 0x80)

                self._frame[1] = 0xF1 if self._last_indicator == light_indicator else 0xF2
            else:
                self._frame = [0x80, 0xF0]

            self._last_indicator = light_indicator
            self._last_frame_time = current

            can.send_message(channel=1, can_id=f"{CAN_BUS_ID_INDICATORS:03X}", data=self._frame)
