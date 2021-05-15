try:
    import os, time, serial
except ImportError as error:
    print(f"\n\n\t\t\t\tOcurrió el ERROR: {error}")

def Core():
    #os.system("clear")#Para linux.
    os.system("cls")#Para windows.
    print("\n\n\t\t\t\tIniciando comunicacion con arduino")

    # Abrimos la conexión con Arduino
    try:
        #arduino = serial.Serial('/dev/ttyACM0', 9600)#Escucha en puerto serial linux mio.
        arduino = serial.Serial('COM6', 9600)#Para windows mio
        bande= 0
        time.sleep(2)
    except Exception as e:
        print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")
        bande= 1
    finally:
        if bande== 0:
            with arduino:
                while True:
                    try:
                        rawstring= arduino.readline()
                        if not rawstring:
                            pass
                        else:
                            rawstring= rawstring.rstrip(b'\r\n')
                            rawstring= str(rawstring)
                            aux= len(rawstring)
                            aux-= 1
                            rawstring= rawstring[2:aux]
                            #arre= rawstring.strip("\n")#Este toma lo último después del último caracter en el rstrip
                            arre= rawstring.split("\n")
                            print(rawstring)#Ya comprobe que en efecto ahora es una cadena lo que obtengo del serial con arduino
                            print(f"Arreglo: {arre}")
                            #print(type(rawstring))
                    except KeyboardInterrupt:
                        print("\n\n\t\t\t\tTermino del programa por Ctrl+c presionado")
                        arduino.close()
                        break
                    except Exception as e:
                        print(f"\n\n\t\t\t\tOcurrió el ERROR: {e}")
                        arduino.close()
                        break
        else:
            print("\n\n\t\t\t\tNo se puede ejecutar el resto del programa debido al/los errores anteriores.")
            print("\n\n\t\t\t\tFinalizando programa.")

if __name__== "__main__":
    Core()