try:
    import time
    import json
    import threading
    from gevent.pywsgi import WSGIServer
    from jsonObject import jsonObject
    from ArduinoConnection import ArduinoConnection
    from flask import Flask, Response, stream_with_context, request, render_template, redirect, url_for
    from datetime import datetime
    from gevent import monkey
    monkey.patch_all()
except Exception as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

# Inicia coneccion con arduino
conn = ArduinoConnection()

# variables para leer modo de operacion
sem = threading.Semaphore()
firstTime = True
modo = ""
bombLight = ""

# JSON read
jsonMain = jsonObject()

# Se crea la app, se instancia el framework para poder usarse.
app = Flask(__name__)
app.secret_key = "clave_secreta_flask"


@app.context_processor  # Context processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

#---------------------------------Endpoints------------------------------------#


@app.route('/', methods=["POST", "GET"])  # Ruta inicial del proyecto
def index():
    global firstTime, jsonMain, modo

    if firstTime:
        jsonMain.readData()
        modo = jsonMain.jsonData['configuracion']['modo']
        bombLight = jsonMain.jsonData['configuracion']['dia-noche']
        firstTime = False
        return render_template('bienvenida.html', dato1=modo, pushed=modo)

    sem.acquire()
    if request.method == "POST" and "modoOperacion" in request.form:
        receivedMode = request.form.get("modoOperacion")
        print(modo)
        print(receivedMode)
        if receivedMode != modo:
            modo = receivedMode
            jsonMain.readData()
            jsonMain.writeData_changeMode(modo)

    if request.method == "POST" and "lightStatus" in request.form:
        onoffLight = request.form.get("lightStatus")
        if onoffLight:
            strmData = {"light": onoffLight}
            text = json.dumps(strmData)
            succes = conn.communication(text)
            if not succes:
                return "error"
            return "pito"
    sem.release()

    if modo == 'true':
        return render_template('automatico.html')
    if modo == 'false':
        return render_template('manual.html')


@app.route("/listen")
def listen():

    def respond_to_client():
        while True:
            sem.acquire()
            succes = conn.communication("strm")
            sem.release()
            print(conn.receivedData)
            if not succes:
                pass
            yield f"id: 1\ndata: {conn.receivedData}\nevent: online\n\n"
            # NO QUITAR: Este time sleep es importante para que cargue electron
            time.sleep(5)
    return Response(respond_to_client(), mimetype='text/event-stream')


@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/raspberry')
def raspberry():
    Nombre = "GDCode"
    data = {
        "user": {
            "name": "satyam kumar",
        }
    }
    text = json.dumps(data)
    return render_template('rasp.html', Nom=Nombre, JsonString=text)


@app.route('/raspberry', methods=['POST'])
def my_form_post():
    data = request.form.get("jsonString")
    text = data
    sem.acquire()
    succces = conn.communication(text)
    sem.release()
    if succces:
        return conn.receivedData
    else:
        return "error"


#----------------------------Error Handlers------------------------------------#


@app.route("/error500")
def error():
    return render_template('errorHandlers/error500.html')


#-------------------------------Execute----------------------------------------#

if __name__ == "__main__":
    # Con esto hacemos que el servidor de flasjk al arrancar y haya cambios en el código se registren los cambios, algo como django.
    app.run(host="127.0.0.1", port=5000, debug=False)
