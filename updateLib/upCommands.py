try:
    import os
    import sys
    import wget
    import json
except ImportError as eImp:
    print(f"Ocurrió el siguiente error de importación: {eImp}")

class ExtraMethods():
    def helpMessages(self):
        print("--updateArduino: Updates the arduino with the .hex file that is in the release part of the github project")
        print("--updateServer: Updates the flask server with the .exe file of the flask server that is in the release part of the github project")
        print("--updateElectron: Updates the electron .AppImage app that is in the release part of the github project")
        print("--updateAll: Updates complete Smart terrarium app, teh server, the electron app and the arduino")
        print("--help: show this help screen")

    def jsonDataMet(self):
        with open("resources/appData.json", "r") as jsonFile:
            self.jsonData= json.load(jsonFile)

        self.jsonData= self.jsonData["updates"]

        self.arduinoLink= self.jsonData["release-arduino"]
        self.serverLink= self.jsonData["release-server"]
        self.electronLink= self.jsonData["release-electron"]

    def updateServer(self):
        os.remove("Server")
        wget.download(self.serverLink)
        print("Server updated")

    def updateElectron(self):
        os.remove("SmartTerra.AppImage")
        wget.download(self.electronLink)
        print("Electron app updated")

    def updateArduino(self):
        print("Aún en desarrollo")

class UpdateMethods(ExtraMethods):
    serverLink= None
    electronLink= None
    arduinoLink= None
    jsonData= None

    def __init__(self, command, system):
        self.command= command
        self.system= system

    def coreUpdate(self):
        lenargv= len(sys.argv)

        self.jsonDataMet()

        if lenargv== 2:
            if sys.argv[1]== "--updateArduino":
                self.updateArduino()

            if sys.argv[1]== "--updateServer":
                self.updateServer()

            if sys.argv[1]== "--updateElectron":
                self.updateElectron()

            if sys.argv[1]== "--updateAll":
                self.updateElectron()
                self.updateServer()
                self.updateArduino()

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