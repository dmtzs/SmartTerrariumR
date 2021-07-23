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

# Inits arduino connection
conn = ArduinoConnection()
conn.startCommunication()

# Variables for reading operation mode
sem = threading.Semaphore()
firstTime = True
modo = ""
lightMode = ""

# JSON read
jsonMain = jsonObject()

# Creation of the flask app.
app = Flask(__name__)
app.secret_key = "clave_secreta_flask"


@app.context_processor  # Context processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

#---------------------------------Endpoints------------------------------------#


def firstTimeLoad():
    global jsonMain, modo, lightMode, rangoResAgua, rangoTerrario, rangoHum

    jsonMain.readData()
    modo = jsonMain.jsonData['configuracion']['modo']
    lightMode = jsonMain.jsonData['configuracion']['dia-noche']
    rangoResAgua = jsonMain.jsonData['configuracion']['temperaturas-rangos']['rangoResAgua']
    rangoTerrario = jsonMain.jsonData['configuracion']['temperaturas-rangos']['rangoTempDHT']
    rangoHum = jsonMain.jsonData['configuracion']['humedad-rango']['rangoHumedad']

    number = 1 if modo == "true" or modo == 1 else 0
    text = "auto{}".format(str(number))
    sem.acquire()
    _ = conn.communication(text)
    sem.release()

    number = 1 if lightMode == "true" or lightMode == 1 else 0
    text = "lght{}".format(str(number))
    sem.acquire()
    _ = conn.communication(text)
    sem.release()


@app.route('/')  # Initial route of the project.
def index():
    global firstTime

    if firstTime:
        firstTimeLoad()
        firstTime = False
        return render_template('bienvenida.html', dato1=modo, pushed=modo, lightmode=lightMode, offButton=1, dis="hidden")

    if modo == 'true' or modo == 1:
        return render_template('automatico.html', autoLightMode="disabled", autoLight="disabled")
    if modo == 'false' or modo == 0:
        return render_template('manual.html')


@app.route("/listen")
def listen():

    def respond_to_client():
        while True:
            sem.acquire()
            succes = conn.communication("strm")
            sem.release()
            # print(conn.receivedData)
            if not succes:
                pass
            yield f"id: 1\ndata: {conn.receivedData}\nevent: online\n\n"
            # DO NOT QUIT: This time sleep is for initialize the electron.
            time.sleep(2)
    return Response(respond_to_client(), mimetype='text/event-stream')


@app.route('/indexevents', methods=["POST"])
def indexEvents():
    global modo, lightMode

    if request.method == "POST" and "modoOperacion" in request.form:
        receivedMode = request.form.get("modoOperacion")
        if receivedMode != modo:
            modo = receivedMode
            jsonMain.readData()
            jsonMain.writeData_changeMode(modo)
            number = 1 if modo == "true" or modo == 1 else 0
            text = "auto{}".format(str(number))
            sem.acquire()
            succes = conn.communication(text)
            if not succes:
                return "error"
            sem.release()
        return "mode changed"

    if request.method == "POST" and "lighMode" in request.form:
        receivedMode = request.form.get("lighMode")
        if receivedMode != lightMode:
            lightMode = receivedMode
            jsonMain.readData()
            jsonMain.writeData_changeLightMode(lightMode)
            number = 1 if lightMode == "true" or lightMode == 1 else 0
            text = "lght{}".format(str(number))
            sem.acquire()
            succes = conn.communication(text)
            if not succes:
                return "error"
            sem.release()
        return "light mode changed"

    if request.method == "POST" and "lightStatus" in request.form:
        onoffLight = request.form.get("lightStatus")
        if onoffLight:
            text = "bulb"
            sem.acquire()
            succes = conn.communication(text)
            if not succes:
                return "error"
            sem.release()
            return "changeLight"
    return "error"


@app.route('/configuracion', methods=["POST", "GET"])
def configuracion():
    global rangoResAgua, rangoTerrario, rangoHum

    if request.method == "POST":
        TempAgua = request.form['TempAguaReserva']
        TempTerra = request.form['TempTerrario']
        Hum = request.form['Humedad']
        if rangoResAgua != TempAgua:
            rangoResAgua = TempAgua
            jsonMain.readData()
            jsonMain.writeData_changeRanges(TempAgua, 0)

        elif rangoTerrario != TempTerra:
            rangoTerrario = TempTerra
            jsonMain.readData()
            jsonMain.writeData_changeRanges(TempTerra, 1)

        elif rangoHum != Hum:
            rangoHum = Hum
            jsonMain.readData()
            jsonMain.writeData_changeRanges(Hum, 2)
        # Mandar también las variables al arduino y de igual manera actualizar el archivo json con los nuevos valores.
        return render_template('configuracion.html', rango1=f"{TempAgua}", rango2=f"{TempTerra}", rango3=f"{Hum}", exito="Datos actualizados con éxito")
    return render_template('configuracion.html', rango1=f"{rangoResAgua}", rango2=f"{rangoTerrario}", rango3=f"{rangoHum}")


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/help')
def help():
    return render_template('bienvenida.html', status="hidden")


@app.route('/closeApp', methods=['POST'])
def closeAll():
    msg = request.form.get("closeMsg")
    if msg == "closeAll":
        conn.closeConnection()
    return "closed"

#----------------------------Error Handlers------------------------------------#


@app.route("/error500")
def error():
    return render_template('errorHandlers/error500.html')


#-------------------------------Execute----------------------------------------#

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
