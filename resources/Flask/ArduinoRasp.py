try:
    import os
    import time
    import serial
    import Metodos
    import warnings
    import serial.tools.list_ports
except ImportError as error:
    print(f"\n\n\t\t\t\tOcurrió el ERROR: {error}")


def Core():
    metos = Metodos.ColeccionMetodos()
    comandoShell, plataforma = metos.limparShell()
    os.system(comandoShell)
    print("\n\n\t\t\t\tIniciando comunicacion con arduino")

    # Abrimos la conexión con Arduino
    try:
        if plataforma == "Windows":
            arduino_ports = [
                p.device
                for p in serial.tools.list_ports.comports()
                if 'Arduino' in p.description  # may need tweaking to match new arduinos
            ]
            if not arduino_ports:
                raise IOError("No Arduino found")
            if len(arduino_ports) > 1:
                warnings.warn('Multiple Arduinos found - using the first')

            arduino = serial.Serial(arduino_ports[0], 9600)
        else:
            serial_port = "/dev/" + \
                os.popen(
                    "dmesg | egrep ttyACM | cut -f3 -d: | tail -n1").read().strip()
            arduino = serial.Serial(serial_port, baudrate=9600, timeout=3)

        # if plataforma == "Windows":
        #     arduino = serial.Serial('COM6', 9600)  # Para windows mio
        # else:  # Checar que regresa al ejecutarse en la raspberry, si dice otra cosa que no es linux entonces elif
        #     # Escucha en puerto serial linux mio.
        #     arduino = serial.Serial('/dev/ttyACM0', 9600)
        bande = 0
        time.sleep(2)
    except Exception as e:
        print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")
        bande = 1
    finally:
        if bande == 0:
            with arduino:
                while True:
                    try:
                        metos.writeArduino(arduino, "hola")
                        metos.readArduino(arduino)

                        # ApagarBuzzer()#Para mandar por el puerto serial que se presiono el botón y apagar el buzzer.
                    except KeyboardInterrupt:
                        print(
                            "\n\n\t\t\t\tTermino del programa por Ctrl+c presionado")
                        arduino.close()
                        break
                    except Exception as e:
                        print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")
                        arduino.close()
                        break
        else:
            print(
                "\n\n\t\t\t\tNo se puede ejecutar el resto del programa debido al/los errores anteriores.")
            print("\n\n\t\t\t\tFinalizando programa.")


if __name__ == "__main__":
    try:
        Core()
    except Exception as e:
        print(f"Ocurrió el error: {e}")
