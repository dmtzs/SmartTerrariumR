"""
This file starts all the complete server builded with flask, this code has only the way the app should be executed.
Which means if the server should be executed in development mode or production.

This file is part of SmartTerrariumRpi.

SmartTerrariumRpi - A project to control a terrarium with a Raspberry Pi, for now only tested in rpi 4.

This project is licensed under the MIT License. See LICENSE.md file for more information.

Diego Martínez Sánchez and Guillermo Ortega Romo - 2021
"""
try:
    import traceback
    from app import app
    from gevent.pywsgi import WSGIServer
except ImportError as err_imp:
    print(f"Ocurrió el error de importación en el archivo {__file__}: {err_imp}")

#-------------------------------Execute----------------------------------------#
if __name__ == "__main__":
    try:
        # -----------------Dev mode-----------------
        # app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)

        # -----------------Prod mode----------------
        app_server =  WSGIServer(("127.0.0.1", 5000), app)
        app_server.serve_forever()
    except KeyboardInterrupt:
        print("Se presionó Ctrl + C")
        print("Apagando servidor...")
    except Exception as err:
        print(f"Ocurrió el siguiente error: {err}")
        print(f"Error completo: \n{traceback.format_exc()}")
    else:
        print("\nReiniciando servidor")