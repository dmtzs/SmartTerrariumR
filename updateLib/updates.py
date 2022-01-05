try:
    import requests
    import platform
except ImportError as eImp:
    print(f"En el archivo {__file__} ocurrió el siguiente error de importación: {eImp}")

class ExtraMethods():
    def validate_os(self):
        sistema = platform.system()

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