"""
usb_can.py

Author: Leeo Santos  
Created: June 2025  
GitHub: https://github.com/c4pt4inroot  

Description:
    This module provides a Python interface for sending and receiving CAN messages
    through a USB-to-CAN serial adapter. It wraps configuration and communication
    logic into a single class: CANInterface.

    The CANInterface class allows you to:
    - Connect to a USB serial port
    - Configure CAN channels with specific baudrates
    - Send standard and extended CAN frames
    - Receive and decode incoming CAN messages (ignores timestamp suffix if present)

    This abstraction simplifies the process of sending and receiving CAN messages 
    to vehicle components, such as BMW instrument clusters, for testing, simulation, 
    or diagnostics.

Dependencies:
    - pyserial (serial)

Usage Example:
    from usb_can import CANInterface

    can = CANInterface(port="COM3")
    can.setup_channel(channel=1, baudrate=100)
    can.send_message(channel=1, can_id="1A6", data=[0x01, 0x02, 0x03])
    message = can.receive_message()
    if message:
        print(message)
"""
import serial
import time

class CANInterface:
    BAUD_RATE_COMMANDS = {
        10:  "1",
        50:  "3",
        100: "6",
        125: "7",
        250: "8",
        400: "9",
        500: "A",
        800: "B",
        900: "C",
    }
    #---------------------------------------------------------------------------------------------------------
    def __init__(self, port, serial_baudrate=115200, timeout=1):
        """
        Inicializa a interface CAN via porta serial.

        Args:
            port (str): Porta serial (ex: 'COM3').
            serial_baudrate (int): Baudrate da serial.
            timeout (float): Timeout da porta serial.
        """
        try:
            self.ser = serial.Serial(port, serial_baudrate, timeout=timeout)
            print(f"[OK] Conectado à porta {port}")
        except Exception as e:
            print(f"[ERRO] Não foi possível abrir a porta {port}: {e}")
            self.ser = None
    #---------------------------------------------------------------------------------------------------------
    def is_connected(self):
        return self.ser is not None and self.ser.is_open
    #---------------------------------------------------------------------------------------------------------
    def _send_command(self, command, description=""):
        if not self.is_connected():
            print("[ERRO] Porta serial não conectada.")
            return

        self.ser.write(command.encode())
        print(f"Send: {command.strip()} ({description})")
        time.sleep(0.1)
    #---------------------------------------------------------------------------------------------------------
    def setup_channel(self, channel, baudrate):
        """
        Configura um canal CAN com a taxa desejada.

        Args:
            channel (int): Canal (1 ou 2).
            baudrate (int): Baudrate CAN em kbps.
        """
        try:
            if baudrate not in self.BAUD_RATE_COMMANDS:
                raise ValueError(f"Baudrate inválido: {baudrate}")

            baud_char = self.BAUD_RATE_COMMANDS[baudrate]
            baud_command = f"S{channel}{baud_char}\r"
            enable_command = f"O{channel}0\r"

            self._send_command(baud_command, f"{baudrate} kbps para CAN{channel}")
            self._send_command(enable_command, f"Habilita CAN{channel}")

            response = self.ser.readline().decode(errors="ignore").strip()
            if response:
                print(f"Response: {response}")

        except Exception as e:
            print(f"[ERRO] Falha ao configurar CAN{channel}: {e}")
    #---------------------------------------------------------------------------------------------------------
    def send_message(self, channel, can_id, data):
        """
        Envia uma mensagem CAN no canal especificado.

        Args:
            channel (int): Canal CAN (1 ou 2).
            can_id (str): ID CAN em hexadecimal (ex: '26E' ou '1ABCDE12').
            data (list[int]): Lista com até 8 bytes (0-255).
        """
        try:
            if not self.is_connected():
                raise Exception("Porta serial não conectada.")

            if not (1 <= channel <= 2):
                raise ValueError("Canal deve ser 1 ou 2.")

            if len(data) > 8:
                raise ValueError("Mensagem CAN deve ter até 8 bytes.")

            can_id_str = can_id.upper()

            # Define padrão ou estendido
            extended = len(can_id_str) > 3
            cmd_type = 'T' if extended else 't'

            dlc = len(data)
            data_str = ''.join(f"{byte:02X}" for byte in data)

            cmd = f"{cmd_type}{channel}{can_id_str}{dlc}{data_str}\r"
            self.ser.write(cmd.encode())
            # print(f"Sent: {cmd.strip()}")

        except Exception as e:
            print(f"[ERRO] Falha ao enviar mensagem CAN: {e}")
    #---------------------------------------------------------------------------------------------------------
    def receive_message(self):
        """
        Recebe e decodifica uma mensagem CAN recebida pela serial.

        Retorna:
            dict | None: Um dicionário com 'channel', 'can_id', 'data', ou None se nada válido for lido.
        """
        try:
            if not self.is_connected():
                raise Exception("Serial port not connected.")

            line = self.ser.readline().decode(errors="ignore").strip()

            if not line:
                return None

            # Verifica tipo da mensagem
            if line.startswith("t") or line.startswith("T"):
                extended = line[0] == "T"
                channel = int(line[1])
                id_len = 8 if extended else 3
                can_id = line[2:2 + id_len]
                dlc_index = 2 + id_len
                dlc = int(line[dlc_index], 16)
                data_start = dlc_index + 1
                data_end = data_start + dlc * 2
                data_raw = line[data_start:data_end]

                data = [int(data_raw[i:i+2], 16) for i in range(0, len(data_raw), 2)]

                return {
                    "channel": channel,
                    "can_id": can_id,
                    "data": data
                }

            return None  # Ignora linhas que não são CAN
        except Exception as e:
            print(f"[ERRO] Falha ao receber mensagem CAN: {e}")
            return None