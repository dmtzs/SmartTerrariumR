#@File: updates.py
#@Author: Diego Martínez Sánchez.
#@Description: This file is in charge to validate if there are updates for the executables in this project so if yes, the it will download from box cloud all the updated assets.
try:
    import requests
    import platform
    from boxsdk import JWTAuth, Client
except ImportError as eImp:
    print(f"En el archivo {__file__} ocurrió el siguiente error de importación: {eImp}")

class ExtraMethods():
    #@Description: Method that returns the system and a shell command in order to clean the terminal in which this program is executed.
    def validate_os(self, action=None):
        sistema = platform.system()

        if action == "install":
            arqui= platform.machine()

            if sistema == "Windows":
                return "cls", sistema, arqui
            else:
                return "clear", sistema, arqui

        elif action == "validate_only":
            if sistema == "Linux":
                return True
            else:
                return False

class CheckUpdates(ExtraMethods):
    # Primero usar API para verificar versiones actuales en la bd
    # Comparar resultados de la API contra las versiones guardadas en el json local.
    # Si es diferente otro método que procese en caso de descargar algunos assets (usar box para realizar esta descarga)
    #   Cubriendo el mismo punto arriba ver de qué manera guardar las credenciales de manera segura. Crear un endpoint que regrese la secret key para desenmcriptar
    #   las credenciales cifradas en formato AES.
    # Los métodos que aquí estarán corresponden a descargar los archvios pertinentes para el caso de avrdude cada vez que se deba actualizar el arduino se deberá-
    # descargar el release de avrdude para actualizar el código de arduino que se descargo desde box. Crear cuenta de GDCode para box.

    # Para lo de box primero hacer request para obtener las credenciales cifradas en formato AES.
    # Después hacer request para obtener la llave secreta y desencriptar esas credenciales obtenidas del endpoint anterior.
    pass