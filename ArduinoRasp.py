import time, serial, os

def Core():
    #os.system("clear")#Para linux.
    os.system("cls")#Para windows.
    print("Iniciando comunicacion con arduino")

    # Abrimos la conexión con Arduino
    try:
        #arduino = serial.Serial('/dev/ttyACM0', 9600)#Escucha en puerto serial linux mio.
        arduino = serial.Serial('COM6', 9600)#Para windows mio
        time.sleep(2)
    except Exception as e:
        print(f"Ocurrió el ERROR: {e}")

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
                #os.system("clear")
                os.system("cls")
                print("Termino del programa por Ctrl+c presionado")
                arduino.close()
                break
            except Exception as e:
                #os.system("clear")
                os.system("cls")
                print(f"Ocurrió el ERROR: {e}")
                break

if __name__== "__main__":
    Core()