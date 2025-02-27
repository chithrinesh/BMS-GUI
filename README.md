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

Communication Protocol
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
