try:
    import time
    import csv
    import threading
    from gevent.pywsgi import WSGIServer
    from TerrariumLib import ArduinoConnection, jsonObject
    from flask import Flask, Response, stream_with_context, request, render_template, redirect, url_for
    from datetime import datetime
    from gevent import monkey
    monkey.patch_all()
except ImportError as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

#---------------------------------Variables and objects------------------------------------#
# Inits arduino connection
conn = ArduinoConnection.ArduinoConnection()
conn.startCommunication()

# Variables for reading operation mode
sem = threading.Semaphore()
firstTime = True
modo = ""
lightMode = ""


# Keeps the data received from the arduino´s stream
streamData = []

# JSON read
jsonMain = jsonObject.jsonObject()

# Creation of the flask app.
app = Flask(__name__)
app.secret_key = "clave_secreta_flask"

#---------------------------------Context processor for the date------------------------------------#


@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

#---------------------------------Endpoints------------------------------------#

# @Description: This function loads the data of the appData json file in which are defined all the automatic parameters, user information, etc in order to be used-
#               in the aplication for its correct functionality. The functions creates global variables in order to manage the parameters of the json file so it can-
#               be used in all the program for the endpoints that requires this information.


def firstTimeLoad():
    global jsonMain, modo, lightMode, rangoResAgua, rangoTerrario, rangoHum, correoGDCode, nomL, nomApp, versionApp, descripcionApp

    jsonMain.readData()
    modo = jsonMain.jsonData['configuracion']['modo']
    lightMode = jsonMain.jsonData['configuracion']['dia-noche']
    rangoResAgua = jsonMain.jsonData['configuracion']['temperaturas-rangos']['rangoResAgua']
    rangoTerrario = jsonMain.jsonData['configuracion']['temperaturas-rangos']['rangoTempDHT']
    rangoHum = jsonMain.jsonData['configuracion']['humedad-rango']['rangoHumedad']
    correoGDCode = jsonMain.jsonData['correo']
    nomL = jsonMain.jsonData['usuario']['usuario-nl']
    nomApp = jsonMain.jsonData['nombre-app']
    versionApp = jsonMain.jsonData['version']
    descripcionApp = jsonMain.jsonData['descripcion-app']

    number = 1 if modo == "true" or modo == 1 else 0
    # text = "auto{}".format(str(number))
    text = f"auto{str(number)}"  # Try and if not uncomment the above line.
    sem.acquire()
    _ = conn.communication(text)
    sem.release()

    number = 1 if lightMode == "true" or lightMode == 1 else 0
    # text = "lght{}".format(str(number))
    text = f"lght{str(number)}"  # Try and if not uncomment the above line.
    sem.acquire()
    _ = conn.communication(text)
    sem.release()

# @Description: This endpoint will be used for the welcome html template at the first time the application is executed. After this page is changed this endpoint will-
#               be used to serve the other templates of the automatic and manual mode. This is also the initial endpoint of the project.


@app.route('/')  # Initial route of the project.
def index():
    global firstTime, nomL, nomApp

    if firstTime:
        firstTimeLoad()
        firstTime = False
        return render_template('bienvenida.html', pushed=modo, lightmode=lightMode, offButton=1, dis="hidden", nl=nomL, nomRealApp=nomApp)

    if modo == 'true' or modo == 1:
        return render_template('automatico.html', autoLightMode="disabled", autoLight="disabled")
    if modo == 'false' or modo == 0:
        return render_template('manual.html')

# @Description: This endpoint is just for the stream of the temperatures and humidity measured in the arduino and sended from the arduino to the raspberry in order to be-
#               showed in the app in the raspberry.


@app.route("/listen")
def listen():
    def respond_to_client():
        global streamData
        while True:
            sem.acquire()
            succes = conn.communication("strm")
            sem.release()
            # print(conn.receivedData)
            if not succes:
                pass
            reader = csv.reader(conn.receivedData.splitlines())
            streamData = list(reader)
            # print(streamData)
            yield f"id: 1\ndata: {conn.receivedData}\nevent: online\n\n"
            # DO NOT QUIT: This time sleep is for initialize the electron.
            time.sleep(5)
    return Response(respond_to_client(), mimetype='text/event-stream')

# @Description: In this endpoint are managed all the buttons of the manual mode, in order to activate all the components that the arduino will be managing. So with this-
#               the users can be in complete control of all the functionality that will have this app.


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
            # text = "auto{}".format(str(number))
            # Try and if not uncomment the above line.
            text = f"auto{str(number)}"
            sem.acquire()
            succes = conn.communication(text)
            sem.release()
            if not succes:
                return "error"
        return "mode changed"

    if request.method == "POST" and "lighMode" in request.form:
        receivedMode = request.form.get("lighMode")
        if receivedMode != lightMode:
            lightMode = receivedMode
            jsonMain.readData()
            jsonMain.writeData_changeLightMode(lightMode)
            number = 1 if lightMode == "true" or lightMode == 1 else 0
            # text = "lght{}".format(str(number))
            # Try and if not uncomment the above line.
            text = f"lght{str(number)}"
            sem.acquire()
            succes = conn.communication(text)
            sem.release()
            if not succes:
                return "error"
        return "light mode changed"

    if request.method == "POST" and "lightStatus" in request.form:
        onoffLight = request.form.get("lightStatus")
        if onoffLight:
            text = "bulb"
            sem.acquire()
            succes = conn.communication(text)
            sem.release()
            if not succes:
                return "error"
            return "changeLight"

    if request.method == "POST" and "rellenar" in request.form:
        rellenar = request.form.get("rellenar")
        if rellenar:
            # text = "bwtr{}".format(str(rellenar))
            # Try and if not uncomment the above line.
            text = f"bwtr{str(rellenar)}"
            sem.acquire()
            succes = conn.communication(text)
            sem.release()
            if not succes:
                return "error"
        return "rellenando"

    if request.method == "POST" and "humedecer" in request.form:
        hmd = request.form.get("humedecer")
        if hmd:
            text = "hmdf"
            sem.acquire()
            succes = conn.communication(text)
            sem.release()
            if not succes:
                return "error"
        return "humedecido"

    return "error"

# @Description: For managing all the ranges for the automatic mode so the arduino will know when to do somethign like turn on or off the biulbs, to know if-
#               the night or day bulb should be on or off, turn on the water bomb to humidify the terrarrium, to refill the drinker when its almost empty, etc.


@app.route('/configuracion', methods=["POST", "GET"])
def configuracion():
    global rangoResAgua, rangoTerrario, rangoHum

    if request.method == "POST":
        TempAgua = request.form['TempAguaReserva']
        TempTerra = request.form['TempTerrario']
        Hum = request.form['Humedad']

        if TempAgua == "" or TempAgua == rangoResAgua:
            pass
        elif rangoResAgua != TempAgua:
            rangoResAgua = TempAgua
            jsonMain.readData()
            jsonMain.writeData_changeRanges(TempAgua, 0)

        if TempTerra == "" or TempTerra == rangoTerrario:
            pass
        elif rangoTerrario != TempTerra:
            rangoTerrario = TempTerra
            jsonMain.readData()
            jsonMain.writeData_changeRanges(TempTerra, 1)

        if Hum == "" or Hum == rangoHum:
            pass
        elif rangoHum != Hum:
            rangoHum = Hum
            jsonMain.readData()
            jsonMain.writeData_changeRanges(Hum, 2)

        # Preguntar a memo si así es como ya quedaría la comunicación con el arduino para actualizar los rangos.
        text = f"conf{rangoResAgua}{rangoTerrario}{rangoHum}"
        sem.acquire()
        succes = conn.communication(text)
        sem.release()
        if not succes:
            return "error"

        return render_template('configuracion.html', rango1=f"{rangoResAgua}", rango2=f"{rangoTerrario}", rango3=f"{rangoHum}", bandeSuccess=True)
    return render_template('configuracion.html', rango1=f"{rangoResAgua}", rango2=f"{rangoTerrario}", rango3=f"{rangoHum}")


@app.route('/contacto')
def contacto():
    global correoGDCode, nomApp, versionApp, descripcionApp

    return render_template('contacto.html', correo=correoGDCode, nombreApp=nomApp, versionDeApp=versionApp, decApp=descripcionApp)


@app.route('/help')
def help():
    return render_template('ManUsu.html', status="hidden")


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
