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