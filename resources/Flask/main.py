#@File: main.py
#@Author: Diego Martínez Sánchez and Guillermo Ortega Romo.
#@Description: This file starts all the complete server builded with flask, this code has only the way the app should be executed.
#              Which means if the server should be executed in development mode or production.
try:
    from app import app
    from gevent.pywsgi import WSGIServer
except ImportError as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

#-------------------------------Execute----------------------------------------#
if __name__ == "__main__":
    try:
        # -----------------Dev mode-----------------
        #app.run(host="127.0.0.1", port=5000, debug=True)

        # -----------------Prod mode----------------
        appServer=  WSGIServer(("127.0.0.1", 5000), app)
        appServer.serve_forever()
    except KeyboardInterrupt:
        print("Se presionó Ctrl + C")
        print("Apagando servidor...")
    except Exception as err:
        print(f"Ocurrió el siguiente error: {err}")