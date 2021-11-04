try:
    import sys
    import json
except ImportError as eImp:
    print(f"Ocurrió el siguiente error de importación: {eImp}")

class extraMethods():
    def helpMessages(self):
        print("--updateArduino: Updates the arduino with the .hex file that is in the release part of the github project")
        print("--updateServer: Updates the flask server with the .exe file of the flask server that is in the release part of the github project")
        print("--updateElectron: Updates the electron .AppImage app that is in the release part of the github project")
        print("--help: show this help screen")

class UpdateMethods(extraMethods):
    def __init__(self, command, system):
        self.command= command
        self.system= system

    def coreUpdate(self):
        lenargv= len(sys.argv)

        if lenargv== 2:
            if sys.argv[1]== "--updateArduino":
                print("Aún en desarrollo")

            if sys.argv[1]== "--updateServer":
                print("Aún en desarrollo")

            if sys.argv[1]== "--updateElectron":
                print("Aún en desarrollo")

            if sys.argv[1]== "--help":
                self.helpMessages()

            else:
                print("No ingresaste ningún comando válido")
                if self.system== "Windows":
                    print("Ingresa python InstalacionesBase.py --help para ver la ayuda disponible")
                else:
                    print("Ingresa python3 InstalacionesBase.py --help para ver la ayuda disponible")
        
        else:
            print("Solo se puede recibir un argumento, no más y no menos")
            if self.system== "Windows":
                print("Intenta con python updateApp.py --help")
            else:
                print("Intenta con python3 updateApp.py --help")