"""
arduino_connection
=====================
This module manages the connections with the arduino so we can do all the interaction
needed in order to perform the functionality of the terrarium to do it smart.

This module contains the following classes:
    - ArduinoConnection: This class manages the connection with the arduino and the-
    communication with the same arduino.

This module contains the following methods:
    - get_arduino_ports: This method detects the serial ports in use and if there are
    more than one the program will use the first serial-port available to be used.
    - init_connection: This method inits the connection to the Arduino more specifically
    for checking is there's an Arduino available for been used in to the app.
    - read_arduino: This method is used for reading the data that comes from the Arduino
    in order to be showed in the raspberry app to the user.
    - write_arduino: This method is for sending the instructions to the Arduino, so the
    Arduino will know what to do with the rest of the components installed in the terrarrium.
    - clean_shell: This method is for cleaning the shell of the app according to the OS.
    - close_connection: Just for closing the connection with the Arduino.
    - start_communication: Inits the communication with the Arduino to start the main
    functionality of the same Arduino.
    - communication: The method that do the stream of the temperatures, humidity and all
    data that comes from the Arduino and also send the instructions to the arduino to do things.
"""
try:
    import os
    import time
    import serial
    import platform
    import warnings
    import serial.tools.list_ports
except ImportError as err_imp:
    print(f"In file: {__file__} the following import error ocurred: {err_imp}")


class ArduinoConnection():
    """
    This class manages the connection with the arduino and the communication with the same arduino
    and all functionalities related to the arduino.

    #### Attributes:
    - this_system(str): The OS in which the app is running.
    - baudrate(int): The baudrate for the serial communication with the Arduino.
    - timeout(float): The timeout for the serial communication with the Arduino.
    - buffersize(int): The buffer size for the serial communication with the Arduino.
    - tries(int): The number of tries for the serial communication with the Arduino.
    - connection(serial.Serial): The connection with the Arduino.
    - send_data(str): The data to be sent to the Arduino.
    - received_data(str): The data received from the Arduino.
    - receiving(bool): The status of the communication with the Arduino.

    #### Methods:
    - get_arduino_ports: This method detects the serial ports in use and if there are
    more than one the program will use the first serial-port available to be used.
    - init_connection: This method inits the connection to the Arduino more specifically
    for checking is there's an Arduino available for been used in to the app.
    - read_arduino: This method is used for reading the data that comes from the Arduino
    in order to be showed in the raspberry app to the user.
    - write_arduino: This method is for sending the instructions to the Arduino, so the
    Arduino will know what to do with the rest of the components installed in the terrarrium.
    - clean_shell: This method is for cleaning the shell of the app according to the OS.
    - close_connection: Just for closing the connection with the Arduino.
    - start_communication: Inits the communication with the Arduino to start the main
    functionality of the same Arduino.
    - communication: The method that do the stream of the temperatures, humidity and all
    data that comes from the Arduino and also send the instructions to the arduino to do things.
    """
    this_system = platform.system()
    baudrate = 115200
    timeout = 1.5
    buffersize = 64
    tries = 0

    # @description: Init the attributes of the class.
    def __init__(self):
        self.connection = None
        self.send_data = ""
        self.received_data = ""
        self.receiving = True

        if self.this_system == "Windows":
            shell_command = "cls"
        else:
            shell_command = "clear"
        os.system(shell_command)
    
    # @Description: Detect the serial ports in use and if there are more than one the program will use the first serial-
    #               port available to be used.
    def get_arduino_ports(self) -> str:
        """
        This method detects the serial ports in use and if there are more than one,
        the program will use the first serial port available to be used.
        """
        if self.this_system == "Windows":
            arduino_ports = [
                p.device
                for p in serial.tools.list_ports.comports()
                # may need tweaking to match new arduinos
                if "Arduino" in p.description or "Dispositivo" in p.description
            ]
        else:
            arduino_ports = [
                p.device
                for p in serial.tools.list_ports.comports()
                # may need tweaking to match new arduinos
            ]
        if not arduino_ports:
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            warnings.warn('Multiple Arduinos found - using the first')
        
        return arduino_ports[0]

    def init_connection(self) -> None:
        """
        This method inits the connection to the Arduino more specifically for checking is there's an Arduino available-
        for been used in to the app.

        Args:
        - None

        Returns:
        - None
        """
        try:
            arduino_detected = self.get_arduino_ports()
            self.connection = serial.Serial(arduino_detected, self.baudrate, timeout=self.timeout)
            self.receiving = True
        except Exception as e:
            print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")
            self.receiving = False

    def read_arduino(self) -> None:
        """
        This method is used for reading the data that comes from the Arduino in order to be shown-
        in the raspberry app to the user.

        Args:
        - None

        Returns:
        - None
        """
        rawstring = self.connection.read(
            self.buffersize).decode('utf-8').rstrip()
        if not rawstring:
            self.tries = self.tries + 1
        else:
            self.receiving = False
            self.received_data = rawstring

    def write_arduino(self, data: str) -> None:
        """
        This method is for sending the instructions to the Arduino, so the Arduino will know what-
        to do with the rest of the components installed in the terrarrium.

        Args:
        - data(str): The string to be sent to the Arduino.

        Returns:
        - None
        """
        self.send_data = data + "\n"
        self.send_data = self.send_data.encode('utf-8')
        self.connection.write(self.send_data)
        self.send_data = self.send_data.decode('utf-8').rstrip()

    def clean_shell(self) -> tuple[str, ...]:
        """
        This method is for cleaning the shell of the app according to the OS.

        Args:
        - None

        Returns:
        - tuple[str, ...]: Returns a tuple with the shell command and the OS in which the app is running.
        """
        if self.this_system == "Windows":
            return "cls", self.this_system
        else:
            return "clear", self.this_system

    # @Description: Just for closing the connection with the Arduino.
    def close_connection(self) -> None:
        self.connection.close()

    # @Description: Inits the communication with the Arduino to start the main functionality of the same Arduino.
    def start_communication(self) -> None:
        self.init_connection()
        self.tries = 0
        while self.receiving is False and self.tries <= 5:
            self.init_connection()
            self.tries = self.tries + 1
        time.sleep(2)

    # @Description: The method that do the stream of the temperatures, humidity and all data that comes
    #               from the Arduino and also send the instructions to the arduino to do things.
    def communication(self, text: str) -> bool:
        if self.connection:
            self.clean_shell()
            self.receiving = True

            time.sleep(.1)
            self.write_arduino(text)
            time.sleep(.1)
            self.read_arduino()
            time.sleep(.1)
            return True
        else:
            return False
