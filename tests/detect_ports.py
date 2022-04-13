try:
    import os
    import serial
    import warnings
    import platform
    import subprocess
    import serial.tools.list_ports
except ImportError as eImp:
    print(f"El siguiente error de importación ocurrió en el archivo {__file__}: {eImp}")


def ports():
    baudrate = 115200
    timeout = 1.5

    try:
        if platform.system() == "Windows":
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

            connection = serial.Serial(arduino_ports[0], baudrate, timeout=timeout)
        else:
            arduino_ports = [
                p.device
                for p in serial.tools.list_ports.comports()
                # may need tweaking to match new arduinos
            ]

            # print(f"Puertos serial detectados: {serial_port}")
            print(f"Puertos serial detectados: {arduino_ports[0]}")

            connection = serial.Serial("/dev/ttyAMA0", baudrate=baudrate, timeout=timeout)
            print(f"Connection: {connection}")
            connection.close()
    except Exception as ex:
        print(f"\n\n\t\t\t\tOcurrió el ERROR: {ex}")

if __name__ == "__main__":
    ports()