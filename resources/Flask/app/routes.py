#@File: routes.py
#@Author: Diego Martínez Sánchez and Guillermo Ortega Romo.
#@Description: This file has all the endpoints that are defined in order to perfrom all the functionality of the project to make the terrarrium-
#              smart like is the main purpose of this project, more description per endpoint below.
try:
    import csv
    import time
    import threading
    from TerrariumLib import *#All these modules imported: ArduinoConnection, jsonObject
    from datetime import datetime
    from app import app
    from flask import render_template, Response, request
    from gevent import monkey
    import datetime as dt 
    import pytz
    monkey.patch_all()
except ImportError as eImp:
    print(f"En el archivo {__file__} currió el error de importación: {eImp}")

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



#---------------------------------Context processor for the date------------------------------------#
# @Description: Context proccessor used to get the actual calendar date.
@app.context_processor
def date_now():
    return {
        'now': datetime.now()
    }

#---------------------------------Endpoints------------------------------------#

# @Description: This function loads the data of the appData json file in which are defined all the automatic parameters, user information, etc in order to be used-
#               in the aplication for its correct functionality. The functions creates global variables in order to manage the parameters of the json file so it can-
#               be used in all the program for the endpoints that requires this information.
def firstTimeLoad():
    global jsonMain, modo, lightMode, onOff, rangoResAgua, rangoTerrario, rangoHum, correoGDCode, nomL, nomApp, versionApp, descripcionApp, timeZone, now, timeDia, timeNoche

    jsonMain.readData()
    modo = jsonMain.jsonData["configuracion"]["modo"]
    lightMode = jsonMain.jsonData["configuracion"]["dia-noche"]
    onOff = 0
    rangoResAgua = jsonMain.jsonData["configuracion"]["temperaturas-rangos"]["rangoResAgua"]
    rangoTerrario = jsonMain.jsonData["configuracion"]["temperaturas-rangos"]["rangoTempDHT"]
    rangoHum = jsonMain.jsonData["configuracion"]["humedad-rango"]["rangoHumedad"]
    correoGDCode = jsonMain.jsonData["correo"]
    nomL = jsonMain.jsonData["usuario"]["usuario-nl"]
    nomApp = jsonMain.jsonData["nombre-app"]
    versionApp = jsonMain.jsonData["version"]
    descripcionApp = jsonMain.jsonData["descripcion-app"]
    timeZone = jsonMain.jsonData["configuracion"]["time-zone"]
    timeDia = jsonMain.jsonData["configuracion"]["horarios"]["dia"]
    timeNoche = jsonMain.jsonData["configuracion"]["horarios"]["noche"]
    now = dt.datetime.now(pytz.timezone(timeZone)).time()

    number = 1 if modo == "true" or modo == 1 else 0
    text = f"auto{str(number)}"
    sem.acquire()
    _ = conn.communication(text)
    sem.release()

    if modo == "true" or modo == 1:
        text = f"bulb1"
        sem.acquire()
        _ = conn.communication(text)
        sem.release()

    if modo == "false" or modo == 0:
        number = 1 if lightMode == "true" or lightMode == 1 else 0
        text = f"lght{str(number)}"
        sem.acquire()
        _ = conn.communication(text)
        sem.release()

    text = f"conf{rangoResAgua},{rangoTerrario},{rangoHum}"
    sem.acquire()
    _ = conn.communication(text)
    sem.release()


# @Description: This endpoint will be used for the welcome html template at the first time the application is executed. After this page is changed this endpoint will-
#               be used to serve the other templates of the automatic and manual mode. This is also the initial endpoint of the project.
@app.route("/")  # Initial route of the project.
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


# @Description: Validates if actual time is inside the bounds of day or night to
#   change the bulbs in automatic mode
def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime


# @Description: This endpoint is just for the stream of the temperatures and humidity measured in the arduino and sended from the arduino to the raspberry in order to be-
#               showed in the app in the raspberry.
@app.route("/listen")
def listen():
    def respond_to_client():
        global streamData, now 
        while True:
            if modo == 'true' or modo == 1:
                # TODO: Only day and night bulbs all day
                # I need to implement the part here in which we can turn on or off the day and night ligh-
                # all day only in the automatic mode. Ask Memo if here is going to be a good idea to implement-
                # that specific part in this endpoint or should be in another way
                # Also we need to use ranges of day and night so we can know when to turn on the noght or day light.
                # modo-dia-noche in automatic mode should be use for know if take in consideration the temperature-
                # ranges or only the day and night ranges for maintain turned on all lights
                now = dt.datetime.now(pytz.timezone(timeZone)).time()
                
                horaDia = timeDia.split(":")
                horaNoche = timeNoche.split(":")

                if(isNowInTimePeriod(dt.time(int(horaDia[0]),int(horaDia[1])), dt.time(int(horaNoche[0]),int(horaNoche[1])), now)):
                    number = 1
                else:
                    number = 0

                text = f"lght{str(number)}"
              
                sem.acquire()
                _ = conn.communication(text)
                sem.release()
            
            sem.acquire()
            succes = conn.communication("strm")
            sem.release()
            # print(conn.receivedData)
            if not succes:
                pass
            reader = csv.reader(conn.receivedData.splitlines())
            streamData = list(reader)
            # print(streamData)
            # Read here the flag of the appData json file that is: modo-dia-noche. In order to send what automatic function do.
            yield f"id: 1\ndata: {conn.receivedData}\nevent: online\n\n"
            # DO NOT QUIT: This time sleep is for initialize the electron.
            time.sleep(5)
    return Response(respond_to_client(), mimetype= "text/event-stream")

# @Description: In this endpoint are managed all the buttons of the manual mode, in order to activate all the components that the arduino will be managing. So with this-
#               the users can be in complete control of all the functionality that will have this app.
@app.route("/indexevents", methods=["POST"])
def indexEvents():
    global modo, lightMode, onOff

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

            if number == 1:
                text = f"bulb{str(number)}"
                sem.acquire()
                succes = conn.communication(text)
                sem.release()

            if number == 0:
                text = f"bulb{str(onOff)}"
                sem.acquire()
                succes = conn.communication(text)
                sem.release()
                
                text = f"lght{str(lightMode)}"
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
            number = 1 if onoffLight == "true" or onoffLight == 1 else 0
            onOff = number
            text = f"bulb{str(number)}"
            # text = "bulb"
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
@app.route("/configuracion", methods=["POST", "GET"])
def configuracion():
    global rangoResAgua, rangoTerrario, rangoHum, timeDia, timeNoche

    if request.method == "POST":
        TempAgua = request.form['TempAguaReserva']
        TempTerra = request.form['TempTerrario']
        Hum = request.form['Humedad']
        horaDia = request.form['timeDia']
        horaNoche = request.form['timeNoche']
        
        if horaDia == "" or horaDia == timeDia:
            pass
        elif timeDia != horaDia:
            timeDia = horaDia
            jsonMain.readData()
            jsonMain.write_data_hour_range(timeDia, "dia")
            
        if horaNoche == "" or horaNoche == timeNoche:
            pass
        elif timeNoche != horaNoche:
            timeNoche = horaNoche
            jsonMain.readData()
            jsonMain.write_data_hour_range(timeNoche, "noche")

        if TempAgua == "" or TempAgua == rangoResAgua:
            pass
        elif rangoResAgua != TempAgua:
            rangoResAgua = TempAgua
            jsonMain.readData()
            jsonMain.writeData_changeRanges(TempAgua, "temperaturas-rangos", "rangoResAgua")

        if TempTerra == "" or TempTerra == rangoTerrario:
            pass
        elif rangoTerrario != TempTerra:
            rangoTerrario = TempTerra
            jsonMain.readData()
            jsonMain.writeData_changeRanges(TempTerra, "temperaturas-rangos", "rangoTempDHT")

        if Hum == "" or Hum == rangoHum:
            pass
        elif rangoHum != Hum:
            rangoHum = Hum
            jsonMain.readData()
            jsonMain.writeData_changeRanges(Hum, "humedad-rango", "rangoHumedad")

        # Preguntar a memo si así es como ya quedaría la comunicación con el arduino para actualizar los rangos.
        text = f"conf{rangoResAgua},{rangoTerrario},{rangoHum}"
        sem.acquire()
        succes = conn.communication(text)
        sem.release()
        if not succes:
            return "error"

        return render_template('configuracion.html', rango1=f"{rangoResAgua}", rango2=f"{rangoTerrario}", rango3=f"{rangoHum}", rango4=f"{timeDia}", rango5=f"{timeNoche}", bandeSuccess=True)
    return render_template('configuracion.html', rango1=f"{rangoResAgua}", rango2=f"{rangoTerrario}", rango3=f"{rangoHum}", rango4=f"{timeDia}", rango5=f"{timeNoche}")


# @Description: Endpoint that is used for show contact information with us.
@app.route("/contacto")
def contacto():
    global correoGDCode, nomApp, versionApp, descripcionApp

    return render_template('contacto.html', correo=correoGDCode, nombreApp=nomApp, versionDeApp=versionApp, decApp=descripcionApp)


# @Description: Endpoint that is used for show QRCodes that shows you english and spanish manuals.
@app.route("/help")
def help():
    return render_template('ManUsu.html', status="hidden")


# @Description: Endpoint that is used for closing the app according to the operative system.
@app.route("/closeApp", methods=['POST'])
def closeAll():
    msg = request.form.get("closeMsg")
    if msg == "closeAll":
        conn.closeConnection()
    return "closed"