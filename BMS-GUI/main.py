import sys
from PySide2.QtCore import QTimer,Signal
from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit, QTableWidgetItem, QPushButton
from ui import Ui_MainWindow
import serial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # Initialize a list to store thermistor data with placeholders for 160 thermistors
        self.thermistor_data = [None] * 160  # Array to hold temperature values

        # Open the serial connection to BMS
        try:
            self.arduino = serial.Serial("com23", 9600, timeout=1)
            print("Serial connection established")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            sys.exit(1)

        # Timer to check for updates every 100 milliseconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(0)  # Update every 100 milliseconds


    def update_ui(self):
        # Check if data is available from BMS
       if self.arduino.inWaiting() > 0:
            # Read and decode the message
            received_message = self.arduino.readline().decode('utf-8').strip()
            print(f"Received message: {received_message}")

            # Process voltage data
            if received_message.startswith('a,'):
                self.process_voltage_data(received_message)
            # Process thermistor data
            elif received_message.startswith('b,'):
                self.process_thermistor_data(received_message)
            # Process current data
            elif received_message.startswith('c,'):
                self.process_current_data(received_message)
            # Process voltage error flag data
            elif received_message.startswith('d,'):
                self.process_error_data(received_message)
            # Process TOTAL VOLTAGE data
            elif received_message.startswith('e,'):
                self.process_tv_data(received_message)
            # Process charging voltage data
            elif received_message.startswith('f,'):
                self.process_cv_data(received_message)
            # Process charging current data
            elif received_message.startswith('g,'):
                self.process_cc_data(received_message)
            # Process charger status data
            elif received_message.startswith('h,'):
                self.process_st_data(received_message)
            # Process temperature error flag data
            elif received_message.startswith('j,'):
                self.process_errort_data(received_message)
            # Process current error flag data
            elif received_message.startswith('k,'):
                self.process_errorc_data(received_message)
            # Process charger control bit data
            elif received_message.startswith('z,'):
                self.process_crc_data(received_message)
            # Process commanded charging voltage data
            elif received_message.startswith('y,'):
                self.process_commv_data(received_message)
            # Process commanded charging current data
            elif received_message.startswith('x,'):
                self.process_commc_data(received_message)

    def process_voltage_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 4:  # Example format: 'a,ic,cell,voltage'
                ic_number = int(parts[1])  # Extract IC number
                cell_number = int(parts[2])  # Extract cell number
                voltage = float(parts[3])  # Extract voltage

                line_edit_name = f"l{ic_number}{cell_number}"
                line_edit = self.findChild(QLineEdit, line_edit_name)

                if line_edit:
                    line_edit.setText(f"{voltage:.3f} V")
                    print(f"Updated {line_edit_name} with voltage: {voltage:.2f} V")
                else:
                    print(f"No QLineEdit found with name: {line_edit_name}")

            else:
                print(f"Message format incorrect for voltage: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing voltage message: {message}, error: {e}")

    def process_thermistor_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 3:  # Example format: 'b,thermistor_number,temperature'
                thermistor_number = int(parts[1])
                temperature = float(parts[2])

                if 1 <= thermistor_number <= 160:
                    self.thermistor_data[thermistor_number - 1] = temperature
                    self.ui.tableWidget.setItem(thermistor_number - 1, 0, QTableWidgetItem(str(thermistor_number)))
                    self.ui.tableWidget.setItem(thermistor_number - 1, 1, QTableWidgetItem(str(f"{temperature:.2f} °C")))
                    print(f"Thermistor {thermistor_number} updated with temperature: {temperature:.2f} °C")
                else:
                    print(f"Received invalid thermistor number: {thermistor_number}")

            else:
                print(f"Message format incorrect for thermistor: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing thermistor message: {message}, error: {e}")

    def process_current_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'c,current_value'
                current = float(parts[1])

                # Find the QLineEdit widget named 'lc' and update it
                line_edit = self.findChild(QLineEdit, 'lc')
                if line_edit:
                    line_edit.setText(f"{current:.3f} A")  # Format the current to 3 decimal places
                    print(f"Updated 'lc' with current: {current:.3f} A")
                else:
                    print("No QLineEdit found with name: 'lc'")

            else:
                print(f"Message format incorrect for current: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing current message: {message}, error: {e}")

    def process_error_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'd,error'
                error = float(parts[1])

                # Find the QLineEdit widget named 'ER' and update it
                line_edit = self.findChild(QLineEdit, 'ER')
                if line_edit:
                    line_edit.setText(f"{error:.3f}")  # Format the ERROR FLAG to 3 decimal places
                    print(f"Updated 'ER' with error: {error:.3f} ")
                else:
                    print("No QLineEdit found with name: 'ER'")

            else:
                print(f"Message format incorrect for error: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing error message: {message}, error: {e}")

    def process_tv_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'e,totalvoltage'
                totalvoltage = float(parts[1])

                # Find the QLineEdit widget named 'TV' and update it
                line_edit = self.findChild(QLineEdit, 'TV')
                if line_edit:
                    line_edit.setText(f"{totalvoltage:.3f}")  # Format the total voltage to 3 decimal places
                    print(f"Updated 'TV' with total voltage: {totalvoltage:.3f} ")
                else:
                    print("No QLineEdit found with name: 'TV'")

            else:
                print(f"Message format incorrect for totalvoltage: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing totalvoltage message: {message}, error: {e}")

    def process_cv_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'f,chargingvoltage'
                chargingvoltage = float(parts[1])

                # Find the QLineEdit widget named 'CV' and update it
                line_edit = self.findChild(QLineEdit, 'CV')
                if line_edit:
                    line_edit.setText(f"{chargingvoltage:.3f}")  # Format the charging voltage to 3 decimal places
                    print(f"Updated 'CV' with voltage: {chargingvoltage:.3f} ")
                else:
                    print("No QLineEdit found with name: 'CV'")

            else:
                print(f"Message format incorrect for charging voltage: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing chargingvoltage message: {message}, error: {e}")

    def process_cc_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'g,chargingcurrent'
                chargingcurrent = float(parts[1])

                # Find the QLineEdit widget named 'CC' and update it
                line_edit = self.findChild(QLineEdit, 'CC')
                if line_edit:
                    line_edit.setText(f"{chargingcurrent:.3f}")  # Format the chargingcurrent to 3 decimal places
                    print(f"Updated 'CC' with chargingcurrent: {chargingcurrent:.3f} ")
                else:
                    print("No QLineEdit found with name: 'CC'")

            else:
                print(f"Message format incorrect for chargingcurrent: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing chargingcurrent message: {message}, error: {e}")

    def process_st_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'h,status'
                status = float(parts[1])

                # Find the QLineEdit widget named 'ST' and update it
                line_edit = self.findChild(QLineEdit, 'ST')
                if line_edit:
                    line_edit.setText(f"{status:.3f}")  # Format the status to 3 decimal places
                    print(f"Updated 'ST' with status: {status:.3f} ")
                else:
                    print("No QLineEdit found with name: 'ST'")

            else:
                print(f"Message format incorrect for status: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing status message: {message}, error: {e}")

    def process_errort_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'j,errort'
                errort = float(parts[1])

                # Find the QLineEdit widget named 'ERT' and update it
                line_edit = self.findChild(QLineEdit, 'ERT')
                if line_edit:
                    line_edit.setText(f"{errort:.3f}")  # Format the temp error flag to 3 decimal places
                    print(f"Updated 'ERT' with error: {errort:.3f} ")
                else:
                    print("No QLineEdit found with name: 'ERT'")

            else:
                print(f"Message format incorrect for errort: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing errort message: {message}, error: {e}")

    def process_errorc_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'k,errorc'
                errorc = float(parts[1])

                # Find the QLineEdit widget named 'ERC' and update it
                line_edit = self.findChild(QLineEdit, 'ERC')
                if line_edit:
                    line_edit.setText(f"{errorc:.3f}")  # Format the error current flag to 3 decimal places
                    print(f"Updated 'ERC' with error: {errorc:.3f} ")
                else:
                    print("No QLineEdit found with name: 'ERC'")

            else:
                print(f"Message format incorrect for errorc: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing errorc message: {message}, error: {e}")

    def process_crc_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'z,crc'
                crc = float(parts[1])

                # Find the QLineEdit widget named 'crc' and update it
                line_edit = self.findChild(QLineEdit, 'CRC')
                if line_edit:
                    line_edit.setText(f"{crc:.3f}")  # Format the charger control bit to 3 decimal places
                    print(f"Updated 'CRC' with control bit value: {crc:.3f} ")
                else:
                    print("No QLineEdit found with name: 'CRC'")

            else:
                print(f"Message format incorrect for crc: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing crc message: {message}, error: {e}")

    #send charger start control bit to BMS
    def start(self):

        start = 0
        self.arduino.write(b"a")
        self.arduino.write(bytes([start]))  # Convert integer to bytes
        print("started")

    # send charger stop control bit to BMS
    def stop(self):
        stop = 1
        self.arduino.write(b"a")
        self.arduino.write(bytes([stop]))
        print("stopped")

    def charger(self):
        line_edit = self.findChild(QLineEdit, 'charv')  # Voltage input
        voltage = int(float(line_edit.text()) * 10)  # Multiply by 10 to scale the input

        line_edit = self.findChild(QLineEdit, 'charc')  # Current input
        current = int(float(line_edit.text()) * 10)  # Multiply by 10 to scale the input

        # High and low bytes for voltage (4500)
        volthi = (voltage >> 8) & 0xFF  # High byte
        voltlo = voltage & 0xFF  # Low byte

        # High and low bytes for current (40)
        currhi = (current >> 8) & 0xFF  # High byte
        currlo = current & 0xFF  # Low byte

        # Send the commanded volatge and current data to BMS master
        self.arduino.write(b"b")
        self.arduino.write(bytes([volthi]))
        self.arduino.write(bytes([voltlo]))
        self.arduino.write(bytes([currhi]))
        self.arduino.write(bytes([currlo]))

        print(f"Voltage: {volthi} {voltlo}, Current: {currhi} {currlo}")

    def process_commv_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'y,commv'
                commv = float(parts[1])

                # Find the QLineEdit widget named 'commv' and update it
                line_edit = self.findChild(QLineEdit, 'commv')
                if line_edit:
                    line_edit.setText(f"{commv:.3f}")  # Format the commanded charging voltage to 3 decimal places
                    print(f"Updated 'commv' with volatge: {commv:.3f} ")
                else:
                    print("No QLineEdit found with name: 'commv'")

            else:
                print(f"Message format incorrect for commv: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing commvmessage: {message}, error: {e}")

    def process_commc_data(self, message):
        try:
            parts = message.split(',')
            if len(parts) == 2:  # Example format: 'x,commc'
                commc = float(parts[1])

                # Find the QLineEdit widget named 'commc' and update it
                line_edit = self.findChild(QLineEdit, 'commc')
                if line_edit:
                    line_edit.setText(f"{commc:.3f}")  # Format the commanded charger current to 3 decimal places
                    print(f"Updated 'commc' with current: {commc:.3f} ")
                else:
                    print("No QLineEdit found with name: 'commc'")

            else:
                print(f"Message format incorrect for commc: {message}")

        except (ValueError, IndexError) as e:
            print(f"Error processing commcmessage: {message}, error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.ui.START.clicked.connect(window.start)
    window.ui.STOP.clicked.connect(window.stop)
    window.ui.send.clicked.connect(window.charger)

    sys.exit(app.exec_())