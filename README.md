# BMS-GUI
A Python-based graphical interface for monitoring and controlling a comprehensive Battery Management System utilizing Analog Devices LTC6813

 ![Image Alt](https://github.com/chithrinesh/BMS-GUI/blob/main/GUI%20WITH%20DATA.png?raw=true)
Features
Real-time monitoring of 424 cell voltages
Real-time monitoring of 160 thermistor temperatures
Current monitoring
Charger control with voltage and current setting
Start/stop charging capability
Error flag monitoring
Total voltage display

The system uses PySide2 for the GUI and serial communication to interface with the BMS master controller, which in turn communicates with LTC6813 slave devices and an Elcon charger via CAN bus.

Hardware Architecture
The BMS hardware architecture consists of:
BMS Master Controller: Arduino-based controller that interfaces with the GUI via serial communication
LTC6813 Slave Devices: 6 LTC6813 chips monitoring 106 cell taps via IsoSPI-SPI
Thermistor Modules: CAN-based modules monitoring 160 thermistors
Elcon Charger: Controlled via CAN bus communications

Communication Protocol:
Serial Communication (GUI ↔ BMS)
The GUI communicates with the BMS master controller via serial communication with the following protocol formats:

Cell Voltage Data: a,ic,cell,voltage
Thermistor Data: b,thermistor_number,temperature
Current Data: c,current_value
Error Flags: d,error, j,errort, k,errorc
Total Voltage: e,totalvoltage
Charger Data: f,chargingvoltage, g,chargingcurrent, h,status, z,crc
Commanded Values: y,commv, x,commc

CAN Communication (BMS ↔ Charger)
The BMS communicates with the Elcon charger using CAN protocol based on the Elcon CAN Specification:

BMS to Charger (ID: 0x1806E5F4):

Max Allowable Charging Terminal Voltage (0.1V/byte)
Max Allowable Charging Current (0.1A/byte)
Control Bit (0: Start charging, 1: Stop charging)


Charger to BMS (ID: 0x18FF50E5):

Output Voltage (0.1V/byte)
Output Current (0.1A/byte)
Status Flags (Hardware Failure, Temperature, Input Voltage, Communication State, Operation Mode)

Installation
1.install python 3.9
2.Clone this repository
3.install the packages given in requirements.txt

Usage:

Connection Setup:

The application will automatically attempt to connect to the BMS master on COM23 at 9600 baud
If your BMS master is connected to a different port, modify the port in the code


Monitoring Battery Cells:

All cell voltages are displayed in real-time on the GUI
Any voltage errors will be flagged in the error display


Temperature Monitoring:

The tableWidget displays readings from up to 160 thermistors


Charger Control:

Set desired charging voltage and current in the input fields
Click "Send" to transmit the desired values to the charger
Click "START" to begin charging (sends control bit 0)
Click "STOP" to stop charging (sends control bit 1)

A Python-based graphical user interface for monitoring and controlling a Battery Management System (BMS) based on Analog Devices LTC6813 chips and Elcon charger using CAN communication.

Overview

This application provides a comprehensive interface for battery management in electric vehicle applications. It enables real-time monitoring of:

Individual cell voltages

Temperature readings from 160 thermistors

Battery pack current

Charging control

Error detection

The system uses PySide2 for the GUI and serial communication to interface with the BMS master controller, which in turn communicates with LTC6813 slave devices and an Elcon charger via CAN bus.

Hardware Architecture

The BMS hardware architecture consists of:

BMS Master Controller: Arduino-based controller that interfaces with the GUI via serial communication

LTC6813 Slave Devices: 6 LTC6813 chips monitoring 107 cell taps via IsoSPI-SPI

Thermistor Modules: CAN-based modules monitoring 160 thermistors

Elcon Charger: Controlled via CAN bus communications

The design is based on Analog Devices's LTC Series LTC6813 Demo Boards (DC2350B).

Communication Protocol

Serial Communication (GUI ↔ BMS)

The GUI communicates with the BMS master controller via serial communication with the following protocol formats:

Data Type

Format Example

Cell Voltage

a,ic,cell,voltage

Thermistor

b,thermistor_number,temperature

Current

c,current_value

Error Flags

d,error, j,errort, k,errorc

Total Voltage

e,totalvoltage

Charger Data

f,chargingvoltage, g,chargingcurrent, h,status, z,crc

Commanded Values

y,commv, x,commc

CAN Communication (BMS ↔ Charger)

The BMS communicates with the Elcon charger using CAN protocol based on the Elcon CAN Specification:

BMS to Charger (ID: 0x1806E5F4)

Max Allowable Charging Terminal Voltage (0.1V/byte)

Max Allowable Charging Current (0.1A/byte)

Control Bit (0: Start charging, 1: Stop charging)

Charger to BMS (ID: 0x18FF50E5)

Output Voltage (0.1V/byte)

Output Current (0.1A/byte)

Status Flags (Hardware Failure, Temperature, Input Voltage, Communication State, Operation Mode)

Features

Real-time monitoring of 107 cell voltages

Real-time monitoring of 160 thermistor temperatures

Current monitoring

Charger control with voltage and current setting

Start/stop charging capability

Error flag monitoring

Total voltage display

Installation

Clone this repository:

git clone https://github.com/yourusername/bms-gui.git
cd bms-gui

Install required dependencies:

pip install PySide2 pyserial

Connect the BMS master controller to your computer via USB

Run the application:

python main.py

Usage

Connection Setup:

The application will automatically attempt to connect to the BMS master on COM23 at 9600 baud

If your BMS master is connected to a different port, modify the port in the code

Monitoring Battery Cells:

All cell voltages are displayed in real-time on the GUI

Any voltage errors will be flagged in the error display

Temperature Monitoring:

The tableWidget displays readings from up to 160 thermistors

Charger Control:

Set desired charging voltage and current in the input fields

Click "Send" to transmit the desired values to the charger

Click "START" to begin charging (sends control bit 0)

Click "STOP" to stop charging (sends control bit 1)

Technical Details

Charger Control Protocol

When the user clicks "Send" button after entering voltage and current values:

Input values are scaled by a factor of 10 to match the CAN protocol (0.1V/byte, 0.1A/byte)

Values are split into high and low bytes

Bytes are transmitted to BMS master using the following format:

'b' + volthi + voltlo + currhi + currlo

BMS master formats these values into the appropriate CAN message (ID: 0x1806E5F4) and sends to the charger

Start/Stop Control

The START and STOP buttons send simple control commands:

START: Sends 'a' + 0 (Control bit 0 = Start charging)

STOP: Sends 'a' + 1 (Control bit 1 = Stop charging)

Code Structure

main.py: Main application and window initialization

ui.py: Generated UI file (not shown in the provided code)

process_*_data(): Methods to handle different types of data received from the BMS master

start(), stop(), charger(): Control functions for the charger

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements

Based on Analog Devices's LTC Series LTC6813 Demo Boards (DC2350B)

LTC6813 Datasheet

DC2350B Evaluation Board
