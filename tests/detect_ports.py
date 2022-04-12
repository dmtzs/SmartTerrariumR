try:
    import os
    import time
    import serial
    import platform
    import warnings
    import serial.tools.list_ports
except ImportError as eImp:
    print(f"The following error import ocurred: {eImp}")

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