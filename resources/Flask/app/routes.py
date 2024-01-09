"""
routes
=====================
This file has all the endpoints that are defined in order to perform
all the functionality of the project to make the terrarrium smart like
is the main purpose of this project, more description per endpoint below.

Diego Martínez Sánchez and Guillermo Ortega Romo.
"""
try:
    import csv
    import time
    import pytz
    import threading
    from datetime import datetime as dt
    from app import app
    from gevent import monkey
    from flask import Response, render_template, request
    from terrarium_lib import json_object, arduino_connection
except ImportError as err_imp:
    print(f"In file: {__file__} the following import error ocurred: {err_imp}")


# TODO: Verificar camel case para las variables y en general el color azul que sale en este archivo
#---------------------------------Variables and objects------------------------------------#
# Inits arduino connection
monkey.patch_all()
conn = arduino_connection.ArduinoConnection()
conn.start_communication()

# Variables for reading operation mode
sem = threading.Semaphore()
first_time = True
mode = ""
light_mode = ""

# Keeps the data received from the arduino's stream
stream_data = []

# JSON read
json_main = json_object.JsonObject()
#---------------------------------Endpoints------------------------------------#

# @Description: This function loads the data of the appData json file in which are defined all the automatic parameters, user information, etc in order to be used-
#               in the aplication for its correct functionality. The functions creates global variables in order to manage the parameters of the json file so it can-
#               be used in all the program for the endpoints that requires this information.
def first_time_load():
    global json_main, mode, light_mode, on_off, water_range_res, terrarium_range, humidity_range, gdcode_email, large_name, app_name, app_version, app_description, time_zone, now, time_day, time_night

    json_main.read_data()
    mode = json_main.json_data["configuracion"]["modo"]
    light_mode = json_main.json_data["configuracion"]["dia-noche"]
    on_off = 0
    water_range_res = json_main.json_data["configuracion"]["temperaturas-rangos"]["rangoResAgua"]
    terrarium_range = json_main.json_data["configuracion"]["temperaturas-rangos"]["rangoTempDHT"]
    humidity_range = json_main.json_data["configuracion"]["humedad-rango"]["rangoHumedad"]
    gdcode_email = json_main.json_data["correo"]
    large_name = json_main.json_data["usuario"]["usuario-nl"]
    app_name = json_main.json_data["nombre-app"]
    app_version = json_main.json_data["version"]
    app_description = json_main.json_data["descripcion-app"]
    time_zone = json_main.json_data["configuracion"]["time-zone"]
    time_day = json_main.json_data["configuracion"]["horarios"]["dia"]
    time_night = json_main.json_data["configuracion"]["horarios"]["noche"]
    # now = dt.datetime.now(pytz.timezone(time_zone)).time()# Checar si no afecta que se quede de esta manera

    number = 1 if mode == "true" or mode == 1 else 0
    text = f"auto{str(number)}"
    sem.acquire()
    _ = conn.communication(text)
    sem.release()

    if mode == "true" or mode == 1:
        text = f"bulb1"
        sem.acquire()
        _ = conn.communication(text)
        sem.release()

    if mode == "false" or mode == 0:
        number = 1 if light_mode == "true" or light_mode == 1 else 0
        text = f"lght{str(number)}"
        sem.acquire()
        _ = conn.communication(text)
        sem.release()

    text = f"conf{water_range_res},{terrarium_range},{humidity_range}"
    sem.acquire()
    _ = conn.communication(text)
    sem.release()

#---------------------------------Context processor for the date------------------------------------#
# @Description: Context proccessor used to get the actual calendar date.
@app.context_processor
def date_now():
    return {
        "now": dt.now(pytz.timezone(time_zone))
    }


# @Description: This endpoint will be used for the welcome html template at the first time the application is executed. After this page is changed this endpoint will-
#               be used to serve the other templates of the automatic and manual mode. This is also the initial endpoint of the project.
@app.route("/")  # Initial route of the project.
def index():
    global first_time, large_name, app_name

    if first_time:
        first_time_load()
        first_time = False
        return render_template('bienvenida.html', pushed=mode, lightmode=light_mode, offButton=1, dis="hidden", nl=large_name, nomRealApp=app_name)

    if mode == 'true' or mode == 1:
        return render_template('automatico.html', autolightMode="disabled", autoLight="disabled")
    if mode == 'false' or mode == 0:
        return render_template('manual.html')


# @Description: Validates if actual time is inside the bounds of day or night to change the bulbs in automatic mode
def isnow_intime_period(startTime, endTime, nowTime):#Tla vez sea buena idea pasarla a terrarium lib aunque no entraría ni en json ni en arduino, evaluar eso
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
        global stream_data, now 
        while True:
            if mode == 'true' or mode == 1:
                now = dt.now(pytz.timezone(time_zone)).time()
                
                horaDia = time_day.split(":")
                horaNoche = time_night.split(":")

                if(isnow_intime_period(dt.time(int(horaDia[0]),int(horaDia[1])), dt.time(int(horaNoche[0]),int(horaNoche[1])), now)):
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
            # print(conn.received_data)
            if not succes:
                pass
            reader = csv.reader(conn.received_data.splitlines())
            stream_data = list(reader)
            # print(stream_data)
            # Read here the flag of the appData json file that is: modo-dia-noche. In order to send what automatic function do.
            yield f"id: 1\ndata: {conn.received_data}\nevent: online\n\n"
            # DO NOT QUIT: This time sleep is for initialize the electron.
            time.sleep(5)
    return Response(respond_to_client(), mimetype= "text/event-stream")

# @Description: In this endpoint are managed all the buttons of the manual mode, in order to activate all the components that the arduino will be managing. So with this-
#               the users can be in complete control of all the functionality that will have this app.
@app.route("/indexevents", methods=["POST"])
def index_events():
    global mode, light_mode, on_off

    if request.method == "POST" and "modoOperacion" in request.form:
        receivedMode = request.form.get("modoOperacion")
        if receivedMode != mode:
            mode = receivedMode
            json_main.read_data()
            json_main.write_data_change_mode(mode)
            number = 1 if mode == "true" or mode == 1 else 0
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
                text = f"bulb{str(on_off)}"
                sem.acquire()
                succes = conn.communication(text)
                sem.release()
                
                text = f"lght{str(light_mode)}"
                sem.acquire()
                succes = conn.communication(text)
                sem.release()

            if not succes:
                return "error"
        return "mode changed"

    if request.method == "POST" and "lighMode" in request.form:
        receivedMode = request.form.get("lighMode")
        if receivedMode != light_mode:
            light_mode = receivedMode
            json_main.read_data()
            json_main.write_data_change_light_mode(light_mode)
            number = 1 if light_mode == "true" or light_mode == 1 else 0
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
            on_off = number
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
def configuration():
    global water_range_res, terrarium_range, humidity_range, time_day, time_night

    if request.method == "POST":
        TempAgua = request.form['TempAguaReserva']
        TempTerra = request.form['TempTerrario']
        Hum = request.form['Humedad']
        horaDia = request.form['timeDia']
        horaNoche = request.form['timeNoche']
        
        if horaDia == "" or horaDia == time_day:
            pass
        elif time_day != horaDia:
            time_day = horaDia
            json_main.read_data()
            json_main.write_data_hour_range(time_day, "dia")
            
        if horaNoche == "" or horaNoche == time_night:
            pass
        elif time_night != horaNoche:
            time_night = horaNoche
            json_main.read_data()
            json_main.write_data_hour_range(time_night, "noche")

        if TempAgua == "" or TempAgua == water_range_res:
            pass
        elif water_range_res != TempAgua:
            water_range_res = TempAgua
            json_main.read_data()
            json_main.write_data_change_ranges(TempAgua, "temperaturas-rangos", "rangoResAgua")

        if TempTerra == "" or TempTerra == terrarium_range:
            pass
        elif terrarium_range != TempTerra:
            terrarium_range = TempTerra
            json_main.read_data()
            json_main.write_data_change_ranges(TempTerra, "temperaturas-rangos", "rangoTempDHT")

        if Hum == "" or Hum == humidity_range:
            pass
        elif humidity_range != Hum:
            humidity_range = Hum
            json_main.read_data()
            json_main.write_data_change_ranges(Hum, "humedad-rango", "rangoHumedad")

        # Preguntar a memo si así es como ya quedaría la comunicación con el arduino para actualizar los rangos.
        text = f"conf{water_range_res},{terrarium_range},{humidity_range}"
        sem.acquire()
        succes = conn.communication(text)
        sem.release()
        if not succes:
            return "error"

        return render_template('configuracion.html', rango1=f"{water_range_res}", rango2=f"{terrarium_range}", rango3=f"{humidity_range}", rango4=f"{time_day}", rango5=f"{time_night}", bandeSuccess=True)
    return render_template('configuracion.html', rango1=f"{water_range_res}", rango2=f"{terrarium_range}", rango3=f"{humidity_range}", rango4=f"{time_day}", rango5=f"{time_night}")


# @Description: Endpoint that is used for show contact information with us.
@app.route("/contacto")
def contact():
    global gdcode_email, app_name, app_version, app_description

    return render_template('contacto.html', correo=gdcode_email, nombreApp=app_name, versionDeApp=app_version, decApp=app_description)


# @Description: Endpoint that is used for show QRCodes that shows you english and spanish manuals.
@app.route("/help")
def help():
    return render_template('ManUsu.html', status="hidden")


# @Description: Endpoint that is used for closing the app according to the operative system.
@app.route("/closeApp", methods=['POST'])
def close_all():
    msg = request.form.get("closeMsg")
    if msg == "closeAll":
        conn.close_connection()
    return "closed"
