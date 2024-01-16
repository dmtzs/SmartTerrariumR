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
    from datetime import datetime as dt, time as dt_time
    from app import app
    from gevent import monkey
    from flask import Response, render_template, request
    from terrarium_lib import json_object, arduino_connection
except ImportError as err_imp:
    print(f"In file: {__file__} the following import error ocurred: {err_imp}")


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
def first_time_load() -> None:
    """
    This function loads the data of the appData json file in which are defined all the automatic parameters, user information, etc in order to be used in the aplication for its correct functionality.
    
    The functions creates global variables in order to manage the parameters of the json file so it can be used in all the program for the endpoints that requires this information.

    Returns:
    - None: This function does not return anything.
    """
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

#---------------------------------Context processor for the date------------------------------------
@app.context_processor
def date_now() -> dict[str, dt]:
    """
    This function is used to get the actual calendar date for now in the context processor.

    Returns:
    - dict[str, dt]: A dictionary with the actual calendar date.
    """
    return {
        "now": dt.now(pytz.timezone(time_zone))
    }

@app.route("/")  # Initial route of the project.
def index() -> str:
    """
    This function is used to render the index.html template.

    Returns:
    - str: The index.html template.
    """
    global first_time, large_name, app_name

    if first_time:
        first_time_load()
        first_time = False
        return render_template('bienvenida.html', pushed=mode, lightmode=light_mode, offButton=1, dis="hidden", nl=large_name, nomRealApp=app_name)

    if mode == 'true' or mode == 1:
        return render_template('automatico.html', autolightMode="disabled", autoLight="disabled")
    if mode == 'false' or mode == 0:
        return render_template('manual.html')

def isnow_intime_period(start_time: dt_time, end_time: dt_time, now_time: dt_time) -> bool:
    """
    This function validates if actual time is inside the bounds of day or night to change the bulbs in automatic mode.

    Args:
    - start_time: Start time of the day or night.
    - end_time: End time of the day or night.
    - now_time: Actual time.

    Returns:
    - bool: True if actual time is inside the bounds of day or night, otherwise False.
    """
    if start_time < end_time:
        return now_time >= start_time and now_time <= end_time
    else:
        #Over midnight:
        return now_time >= start_time or now_time <= end_time

@app.route("/listen")
def listen() -> Response:
    """
    This function is used to listen the data sended from the arduino.

    Returns:
    - Response: The data sended from the arduino.
    """
    def respond_to_client() -> str:
        """
        This function is used to receive the data from the arduino and its sent to the client.

        Returns:
        - str: The data received from the arduino.
        """
        global stream_data, now 
        while True:
            if mode == 'true' or mode == 1:
                now = dt.now(pytz.timezone(time_zone)).time()
                day_hour = time_day.split(":")
                night_hour = time_night.split(":")
                start_time = dt_time(int(day_hour[0]),int(day_hour[1]))
                end_time = dt_time(int(night_hour[0]),int(night_hour[1]))

                if isnow_intime_period(start_time, end_time, now):
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

@app.route("/indexevents", methods=["POST"])
def index_events() -> str:
    """
    This function is used to manage the events that are sended from the index.html template.

    Returns:
    - str: A string that indicates if the event was successful or not.
    """
    global mode, light_mode, on_off

    if request.method == "POST" and "modoOperacion" in request.form:
        received_mode = request.form.get("modoOperacion")
        if received_mode != mode:
            mode = received_mode
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
        received_mode = request.form.get("lighMode")
        if received_mode != light_mode:
            light_mode = received_mode
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
        onoff_light = request.form.get("lightStatus")
        if onoff_light:
            number = 1 if onoff_light == "true" or onoff_light == 1 else 0
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
        refill = request.form.get("rellenar")
        if refill:
            # text = "bwtr{}".format(str(rellenar))
            # Try and if not uncomment the above line.
            text = f"bwtr{str(refill)}"
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

@app.route("/configuracion", methods=["POST", "GET"])
def configuration() -> str:
    """
    For managing all the ranges for the automatic mode so the arduino will know when
    to do somethign like turn on or off the biulbs, to know if the night or day bulb should be on or off,
    turn on the water bomb to humidify the terrarrium, to refill the drinker when its almost empty, etc.

    Returns:
    - str: A string which is ussed to render the html template.
    """
    global water_range_res, terrarium_range, humidity_range, time_day, time_night

    if request.method == "POST":
        water_temperature = request.form['TempAguaReserva']
        terrarium_temperature = request.form['TempTerrario']
        only_humidity = request.form['Humedad']
        day_hour = request.form['timeDia']
        night_hour = request.form['timeNoche']
        
        if day_hour == "" or day_hour == time_day:
            pass
        elif time_day != day_hour:
            time_day = day_hour
            json_main.read_data()
            json_main.write_data_hour_range(time_day, "dia")
            
        if night_hour == "" or night_hour == time_night:
            pass
        elif time_night != night_hour:
            time_night = night_hour
            json_main.read_data()
            json_main.write_data_hour_range(time_night, "noche")

        if water_temperature == "" or water_temperature == water_range_res:
            pass
        elif water_range_res != water_temperature:
            water_range_res = water_temperature
            json_main.read_data()
            json_main.write_data_change_ranges(water_temperature, "temperaturas-rangos", "rangoResAgua")

        if terrarium_temperature == "" or terrarium_temperature == terrarium_range:
            pass
        elif terrarium_range != terrarium_temperature:
            terrarium_range = terrarium_temperature
            json_main.read_data()
            json_main.write_data_change_ranges(terrarium_temperature, "temperaturas-rangos", "rangoTempDHT")

        if only_humidity == "" or only_humidity == humidity_range:
            pass
        elif humidity_range != only_humidity:
            humidity_range = only_humidity
            json_main.read_data()
            json_main.write_data_change_ranges(only_humidity, "humedad-rango", "rangoHumedad")

        # Preguntar a memo si así es como ya quedaría la comunicación con el arduino para actualizar los rangos.
        text = f"conf{water_range_res},{terrarium_range},{humidity_range}"
        sem.acquire()
        succes = conn.communication(text)
        sem.release()
        if not succes:
            return "error"

        return render_template(
            'configuracion.html',
            rango1=f"{water_range_res}",
            rango2=f"{terrarium_range}",
            rango3=f"{humidity_range}",
            rango4=f"{time_day}",
            rango5=f"{time_night}",
            bandeSuccess=True
        )
    return render_template(
        'configuracion.html',
        rango1=f"{water_range_res}",
        rango2=f"{terrarium_range}",
        rango3=f"{humidity_range}",
        rango4=f"{time_day}",
        rango5=f"{time_night}"
    )


# @Description: Endpoint that is used for show contact information with us.
@app.route("/contacto")
def contact() -> str:
    """
    This function is used to render the contacto.html template.

    Returns:
    - str: The contacto.html template.
    """
    global gdcode_email, app_name, app_version, app_description

    return render_template(
        'contacto.html',
        correo=gdcode_email,
        nombreApp=app_name,
        versionDeApp=app_version,
        decApp=app_description
    )


@app.route("/help")
def help() -> str:
    """
    This function is used to render the ayuda.html template.

    It shows QRCodes that shows you english and spanish manuals.

    Returns:
    - str: The ayuda.html template.
    """
    return render_template('ManUsu.html', status="hidden")


@app.route("/closeApp", methods=['POST'])
def close_all() -> str:
    """
    This function is used to close the app according to the operative system.

    Returns:
    - str: A string that indicates if the app was closed or not.
    """
    msg = request.form.get("closeMsg")
    if msg == "closeAll":
        conn.close_connection()
    return "closed"
