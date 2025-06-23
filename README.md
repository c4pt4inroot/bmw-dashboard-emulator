# 🚘 BMW Dashboard Emulator

A Python-based emulator that communicates with BMW instrument clusters via CAN bus, enabling simulation of ignition, RPM, speed, fuel level, ABS, airbag, indicators, lights, and more.

> ⚙️ Built for developers, hardware hackers, and enthusiasts who want to interact with BMW dashboards outside the vehicle.

---

## 📦 Features

- ✅ Ignition state (on/off)
- 🕹 RPM and speed simulation
- 🛑 ABS and airbag warning lights
- 💡 Indicators, fog lights, main lights, and side lights
- ⛽ Fuel level simulation
- 🌡 Engine temperature
- 🕒 Date and time injection
- 🧷 Handbrake and seatbelt status
- 📤 Real CAN frame transmission via serial CAN adapter
- 🔧 Modular and readable code

---

## 🛠 Requirements

- Python 3.7+
- A USB-to-CAN serial adapter (compatible with 8N1 command protocol)
- [pyserial](https://pypi.org/project/pyserial/)

Install dependencies:

```bash
pip install pyserial
