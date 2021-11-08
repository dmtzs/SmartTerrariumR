#@File: jsonObject.py
#@Author: Diego Martínez Sánchez and Guillermo Ortega Romo.
#@Description: This module manages the data stored in the appData json file that is used to configure the app at the moment we init the raspberry-
#              so everything will stay with all the configuration added even if the raspberry turns off in a anormal way.
try:
    import os
    import json
except ImportError as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

# @Description: Class for manage the json appData in order to be used in the app or to update the same json file.
#               In this class are all the methods to read, write and update the data of the json file
class jsonObject():
    filename= "resources/appData.json"
    filename2= "../appData.json"

    # @Description: Init the attributes for the class.
    def __init__(self):
        self.jsonData = None

    # @Description: Method to read the data from the json file.
    def readData(self):
        auxFile= ""

        if os.path.isfile(self.filename):
            auxFile= self.filename
        else:
            auxFile= self.filename2

        try:
            with open(auxFile, 'r') as jsonFile:
                self.jsonData = json.load(jsonFile)
                #jsonFile.close()
        except Exception:
            print("No se encontró el archivo appData.json en ninguna de las rutas")

    # @Description: Method to write all the data in the json file.
    def writeData(self):
        auxFile= ""
        self.jsonData = json.dumps(self.jsonData, indent=4)

        if os.path.isfile(self.filename):
            auxFile= self.filename
        else:
            auxFile= self.filename2

        try:
            with open(auxFile, 'w') as jsonFile:
                jsonFile.write(self.jsonData)
                #jsonFile.close()
        except Exception:
            print("No se encontró el archivo appData.json en ninguna de las rutas")

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

    # @Description: Method that needs to update the day stored in the appData.json file in order to be used in the endpoint to verify-
    #               if there`s any available update for the production assets of the app.
    def write_data_day_update(self, dia):
        self.jsonData["updates"]["dia"]= dia

        self.writeData()
        #We still need to review this method, maybe we need to add more things to make them work.