try:
    import time
    import json
    import os
except Exception as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

# @Description: Class for manage the json appData in order to be used in the app or to update the same json file.
#               In this class are all the methods to read, write and update the data of the json file
class jsonObject():
    filename = 'resources/appData.json'

    # @Description: Init the attributes for the class.
    def __init__(self):
        self.jsonData = None

    # @Description: Method to read the data from the json file.
    def readData(self):
        with open(os.path.abspath(self.filename), 'r') as jsonFile:
            self.jsonData = json.load(jsonFile)
            jsonFile.close()

    # @Description: Method to write all the data in the json file.
    def writeData(self):
        self.jsonData = json.dumps(self.jsonData, indent=4)
        with open(os.path.abspath(self.filename), 'w') as jsonFile:
            jsonFile.write(self.jsonData)
            jsonFile.close()

    # @Description: Method to update in the json file the parameter of the state of the operation mode of the app.
    def writeData_changeMode(self, newMode):
        text = 1 if newMode == "true" else 0
        self.jsonData['configuracion']['modo'] = text

        self.writeData()

    # @Description: Method to update in the json file the parameter of the state of the lightmode of the app.
    def writeData_changeLightMode(self, newMode):
        if newMode == 'true':
            self.jsonData['configuracion']['dia-noche'] = 1
        if newMode == 'false':
            self.jsonData['configuracion']['dia-noche'] = 0

        self.writeData()

    # @Description: Method to update the ranges for the humidity and temperatures that the automatic mode will be managing.
    def writeData_changeRanges(self, rangoRecibido, bande):
        if bande== 0:
            self.jsonData['configuracion']['temperaturas-rangos']['rangoResAgua']= rangoRecibido
        elif bande== 1:
            self.jsonData['configuracion']['temperaturas-rangos']['rangoTempDHT']= rangoRecibido
        elif bande== 2:
            self.jsonData['configuracion']['humedad-rango']['rangoHumedad']= rangoRecibido

        self.writeData()