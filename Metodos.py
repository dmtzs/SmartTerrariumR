try:
    import platform
except ImportError as eImp:
    print(f"The following error import ocurred: {eImp}")

class ColeccionMetodos():

    def Arduino(self, arduino):
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

    def limparShell(self):
        sistema= platform.system()

        if sistema== "Windows":
            return "cls"
        else:
            return "clear"