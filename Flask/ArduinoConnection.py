try:
    import os
    import time
    import serial
    import warnings
    import platform
    import serial.tools.list_ports
except ImportError as eImp:
    print(f"The following error import ocurred: {eImp}")


class ArduinoConnection():
    thisSystem = platform.system()

    def __init__(self):
        self.connection = None
        self.sendData = ""
        self.receivedData = ""

        if self.thisSystem == "Windows":
            comandoShell = "cls"
        else:
            comandoShell = "clear"
        os.system(comandoShell)

    def initConnection(self):
        try:
            if self.thisSystem == "Windows":
                arduino_ports = [
                    p.device
                    for p in serial.tools.list_ports.comports()
                    if 'Arduino' in p.description  # may need tweaking to match new arduinos
                ]
                if not arduino_ports:
                    raise IOError("No Arduino found")
                if len(arduino_ports) > 1:
                    warnings.warn('Multiple Arduinos found - using the first')

                self.connection = serial.Serial(arduino_ports[0], 9600)
            else:
                serial_port = "/dev/" + \
                    os.popen(
                        "dmesg | egrep ttyACM | cut -f3 -d: | tail -n1").read().strip()
                self.connection = serial.Serial(
                    serial_port, baudrate=9600, timeout=3)
        except Exception as e:
            print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")

    def readArduino(self):
        rawstring = self.connection.readline()
        if not rawstring:
            pass
        else:
            rawstring = rawstring.rstrip(b'\r\n')
            rawstring = str(rawstring)
            aux = len(rawstring)
            aux -= 1
            rawstring = rawstring[2:aux]
            # arre= rawstring.strip("\n")#Este toma lo último después del último caracter en el rstrip
            arre = rawstring.split("\n")
            # Ya comprobe que en efecto ahora es una cadena lo que obtengo del serial con arduino
            self.receivedData = rawstring
            # print(rawstring)
            #print(f"Arreglo: {arre}")
            # print(type(rawstring))

    def writeArduino(self, Data):
        self.sendData = Data
        self.connection.writeline(b'{}'.format(self.sendData))

    def limparShell(self):
        if self.thisSystem == "Windows":
            return "cls", self.thisSystem
        else:
            return "clear", self.thisSystem

    def closeConnection(self):
        self.connection.close()
