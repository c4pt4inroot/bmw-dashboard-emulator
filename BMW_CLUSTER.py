"""
BMW Cluster Simulation - Main Control Script

Author: Leeo Santos
Created: June 2025
GitHub: https://github.com/c4pt4inroot

Description:
    This is the main script for simulating a BMW instrument cluster via the CAN bus.
    It uses a serial CAN interface to send simulated signals such as ignition,
    RPM, speed, engine temperature, handbrake, seatbelt, indicator lights,
    time/date, and dashboard lighting.

    The script runs in a timed loop, executing different signal functions based
    on a cyclic counter to simulate real-time vehicle behavior.

Dependencies:
    - usb_can.py (CANInterface class)
    - Custom modules in /modules (ignition, lightning, rpm, etc.)

Usage:
    Run this script directly with Python to start the CAN simulation:
        python BMW_CLUSTER.py
"""

from usb_can import CANInterface
from modules.ignition import send_ignition
from modules.lightning import send_lightning
from modules.rpm import send_rpm
from modules.speed import send_speed
from modules.abs import send_abs
from modules.airbag import send_airbag
from modules.enginetemperature import send_engine_temperature
from modules.fuel import send_fuel
from modules.handbrake import send_handbrake
from modules.seatbelt import send_seatbelt
from modules.indicators import IndicatorController
from modules.time import send_time
import time

def main():
    can = CANInterface(port="COM3")
    can.setup_channel(channel=1, baudrate=100)

    indicators = IndicatorController()

    previous = 0        # Inicializa o timer
    counter = 0         # Contador para ciclos
    current_speed = 0   # Velocidade inicial
    step = 1            # Incremento da velocidade

    try:
        while True:
            current = time.time() * 1000  # tempo atual em ms

            if current - previous >= 10:
                send_ignition(can, ignition_on=True)  # Sempre ligado
                send_lightning(can, g_lights_main=True,)
                
                send_rpm(can, 4000)  # Valor fixo para teste
                
                if counter % 7 == 0:
                    send_speed(can, current_speed)
                    current_speed += step
                    if current_speed >= 280 or current_speed <= 0:
                        step *= -1
                
                if counter % 20 == 0:
                    send_abs(can, abs_enabled=False)
                    send_airbag(can, airbag_enabled=False)
                    send_engine_temperature(can, temp_celsius=100)
                    send_fuel(can, fuel_percent=50)
                    send_handbrake(can, handbrake_active=True)
                    send_seatbelt(can, seatbelt_fastened=False)
                    indicators.send_indicators(can, indicator_state=3)
                
                if counter % 100 == 0:
                    send_time(
                        can,
                        hour=14,
                        minute=35,
                        second=12,
                        day=21,
                        month=6,
                        year=2025
                    )

                counter += 1
                previous = current
            time.sleep(0.001)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
