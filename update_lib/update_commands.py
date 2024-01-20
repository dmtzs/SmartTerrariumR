try:
    import os
    import sys
    import wget
    import json
    import zipfile as zp
except ImportError as eImp:
    print(f"Ocurrió el siguiente error de importación: {eImp}")

class MoreMethods():
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

        self.avrdude= self.jsonData["releases"]["avrdude"]
        self.arduinoLink= self.jsonData["releases"]["arduino"]
        self.serverLink= self.jsonData["releases"]["server"]
        self.electronLink= self.jsonData["releases"]["electron"]

    def updateServer(self):
        os.remove("Server")
        wget.download(self.serverLink)
        print("Server updated")

    def updateElectron(self):
        os.remove("SmartTerra.AppImage")
        wget.download(self.electronLink)
        print("Electron app updated")

    def updateArduino(self):
        trashFiles= ["builtin_tools_versions.txt", "RaspSerial.ino.hex"]

        wget.download(self.arduinoLink)
        os.system(self.avrdudeCommand)# Maybe I still need to do dynamically the paths included in the command

        for i in trashFiles:
            os.remove(i)

        print("Arduino updated")

    def downAvr(self):
        wget.download(self.avrdude)

        with zp.ZipFile("./avr.zip", "r") as av:
            av.extractall("./avr/")

        os.remove("avr.zip")
        print("Avrdude downloaded")

    def firstFunctions(self):
        os.system('pkill -xf "./Server"')
        os.system('pkill -xf "./SmartTerra.AppImage"')
        
        coreRuta= os.path.realpath(__file__)
        coreRuta= coreRuta[:-23]
        restOfFlags= "-v -patmega328p -carduino -P/dev/ttyACM0 -b115200 -D -Uflash:w:RaspSerial.ino.hex:i"
        self.avrdudeCommand= f"{coreRuta}avr/bin/avrdude -C{coreRuta}avr/etc/avrdude.conf {restOfFlags}"

        self.jsonDataMet()

        if os.path.isdir("avr"):
            pass
        else:
            self.downAvr()

class UpdateMethods(MoreMethods):
    avrdudeCommand= None
    serverLink= None
    electronLink= None
    arduinoLink= None
    avrdude= None
    jsonData= None

    def __init__(self, command, system):
        self.command= command
        self.system= system

    def coreUpdate(self):
        self.firstFunctions()

        lenargv= len(sys.argv)

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