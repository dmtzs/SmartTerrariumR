try:
    import os
    import time
    import serial
    import warnings
    import platform
    import serial.tools.list_ports
except ImportError as eImp:
    print(f"The following error import ocurred: {eImp}")

# @Description: Class for manage all the arduino connection from the app of the raspberry to the arduino.
class ArduinoConnection():
    thisSystem = platform.system()
    baudrate = 115200
    timeout = 1.5
    buffersize = 64
    tries = 0

    # @description: Init the attributes of the class.
    def __init__(self):
        self.connection = None
        self.sendData = ""
        self.receivedData = ""
        self.recieving = True

        if self.thisSystem == "Windows":
            comandoShell = "cls"
        else:
            comandoShell = "clear"
        os.system(comandoShell)

    # @Description: Inits the connection to the Arduino more specifically for checking is there´s an Arduino available-
    #               for been used in to the app.
    def initConnection(self):
        try:
            if self.thisSystem == "Windows":
                arduino_ports = [
                    p.device
                    for p in serial.tools.list_ports.comports()
                    # may need tweaking to match new arduinos
                    if "Arduino" in p.description or "Dispositivo" in p.description
                ]
                if not arduino_ports:
                    raise IOError("No Arduino found")
                if len(arduino_ports) > 1:
                    warnings.warn('Multiple Arduinos found - using the first')

                self.connection = serial.Serial(
                    arduino_ports[0], self.baudrate, timeout=self.timeout)
            else:
                serial_port = "/dev/" + \
                    os.popen(
                        "dmesg | egrep ttyACM | cut -f3 -d: | tail -n1").read().strip()
                self.connection = serial.Serial(
                    serial_port, baudrate=self.baudrate, timeout=self.timeout)
            self.recieving = True
        except Exception as e:
            print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")
            self.recieving = False

    # @Description: This method is used for reading the data that comes from the Arduino in order to be showed-
    #               in the raspberry app to the user.
    def readArduino(self):
        rawstring = self.connection.read(
            self.buffersize).decode('utf-8').rstrip()
        if not rawstring:
            self.tries = self.tries + 1
        else:
            self.recieving = False
            self.receivedData = rawstring

    # @Description: This method is for sending the instructions to the Arduino, so the Arduino will know what-
    #               to do with the rest of the components installed in the terrarrium.
    def writeArduino(self, Data):
        self.sendData = Data + "\n"
        self.sendData = self.sendData.encode('utf-8')
        self.connection.write(self.sendData)
        self.sendData = self.sendData.decode('utf-8').rstrip()

    # @Description: A method to know the OS in which the app is running and the return of a shell command.
    def limpiarShell(self):
        if self.thisSystem == "Windows":
            return "cls", self.thisSystem
        else:
            return "clear", self.thisSystem

    # @Description: Just for closing the connection with the Arduino.
    def closeConnection(self):
        self.connection.close()

    # @Description: Inits the communication with the Arduino to start the main functionality of the same Arduino.
    def startCommunication(self):
        self.initConnection()
        self.tries = 0
        while self.recieving is False and self.tries <= 5:
            self.initConnection()
            self.tries = self.tries + 1
        time.sleep(2)

    # @Description: The method that do the stream of the temperatures, humidity and all data that comes
    #               from the Arduino and also send the instructions to the arduino to do things.
    def communication(self, text):
        if self.connection:
            self.limpiarShell()
            self.recieving = True

            time.sleep(.1)
            self.writeArduino(text)
            time.sleep(.1)
            self.readArduino()
            time.sleep(.1)
            return True
        else:
            return False
