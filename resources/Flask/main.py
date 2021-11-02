#@File: main.py
#@Author: Diego Martínez Sánchez and Guillermo Ortega Romo.
#@Description: This file just run all the complete server builded with flask, in order to separate and have more order in the code thats why the-
#              functionality is separated in different files so we can manage more friendly the server if its required.
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