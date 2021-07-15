try:
    import time
    import json
    import os
except Exception as eImp:
    print(f"Ocurrió el error de importación: {eImp}")


class jsonObject():
    filename = 'resources/appData.json'

    def __init__(self):
        self.jsonData = None

    def readData(self):
        with open(os.path.abspath(self.filename), 'r') as jsonFile:
            self.jsonData = json.load(jsonFile)
            jsonFile.close()

    def writeData_changeMode(self, newMode):
        if newMode == 'true':
            self.jsonData['configuracion']['modo'] = 1
        if newMode == 'false':
            self.jsonData['configuracion']['modo'] = 0

        self.jsonData = json.dumps(self.jsonData, indent=4)
        with open(os.path.abspath(self.filename), 'w') as jsonFile:
            jsonFile.write(self.jsonData)
            jsonFile.close()
