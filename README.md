
# Project Title

A Python-based graphical user interface for monitoring and controlling a Battery Management System (BMS) based on Analog Devices LTC6813 chips and Elcon charger using CAN communication.


## Features
Real-time monitoring of 106 cell voltages

Real-time monitoring of 160 thermistor temperatures

Current monitoring

Charger control with voltage and current setting

Start/stop charging capability

Error flag monitoring

Total voltage display
## Messag format:

The GUI communicates with the BMS master controller via serial communication with the following protocol formats:

Cell Voltage Data: a,ic,cell,voltage

Thermistor Data: b,thermistor_number,temperature

Current Data: c,current_value

Error Flags: d,error, j,errort, k,errorc

Total Voltage: e,totalvoltage

Charger Data: 

f,chargingvoltage

g,chargingcurrent

h,status

z,crc

Commanded Values: 

y,commandedvoltage

x,commandedcurrent
## Example format for sending data to GUI:
Serial.print("f,");

Serial.println(chargingvoltage);

It sends the charging voltage read from charger to GUI
## START AND STOP BUTTON:
The bms needs to sent control bit as 0 for charger to start.This can be set by pressing start button in gui and it send message to bms in the below format.

START:

a 0

STOP:

a 1
## COMMANDE VOLTAGE AND COMMANDED CURRENT

To set charging voltage as 450.1 V it needs to be multiplied by 10 and converted to high and low byte same for current.

On pressing send button the python code multiples the input then converts it into two 8 bytes and send to BMS in below format

b volthighbyte voltlobyte currenthibyte currentlobyte
## BMS CODE TO READ CHARGER CONTROL DATA FROM GUI:
 if (Serial.available() > 0) 
    {

        char command1 = Serial.read();

        if (command1 == 'a') 
     {

        int command = Serial.read();

        if (command == 0) 
        {

            // Start action

            control=0;

            Serial.println("Received start command");

        }

        else if (command == 1) 
         {

            // Start action

            control=1;

            Serial.println("Received start command");

         }

      }

if (Serial.available() >= 5) 
      {

        char command2 = Serial.read();

        if (command2 == 'b') 
      {

       volthi = Serial.read(); 

       voltlo = Serial.read();  

       currhi = Serial.read();  

       currlo = Serial.read(); 

      }

      }
    }


## Deployment

To deploy this project run

```bash
  
  pip install PySide2 pyserial
```

