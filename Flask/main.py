try:
    import time
    import sys
    from ArduinoConnection import ArduinoConnection
    from flask import Flask, request, render_template, redirect, url_for
    from datetime import datetime
except Exception as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

# Inicia coneccion con arduino
conn = ArduinoConnection()

# Se crea la app, se instancia el framework para poder usarse.
app = Flask(__name__)
app.secret_key = "clave_secreta_flask"

# Context processor


@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

# Endpoints


@app.route('/')  # Ruta inicial del proyecto
def index():
    return render_template('index.html', dato1="valor", dato2="valor2", lista=["uno", "dos", "tres"])

# Manda error porque lo estoy convirtiendo en entero.


@app.route('/informacion')
@app.route('/informacion/<string:nombre>')
# Otra ruta para recibir parámetros con lo que dice nombre en este caso y con validaciones
@app.route('/informacion/<string:nombre>/<ape>')
# El parámetro se debe llamar forzosamente igual a como lo nombre arriba entre las <>
def informacion(nombre=None, ape=None):
    texto = ""
    if nombre != None and ape != None:
        texto = f"Bienvenido, {nombre} {ape}"
    return render_template('informacion.html', textohtml=texto)


@app.route('/contacto')
@app.route('/contacto/<redireccion>')
def contacto():
    Nombre = "Diego"
    return render_template('contacto.html', Nom=Nombre)


@app.route('/raspberry')
def raspberry():
    Nombre = ""
    return render_template('rasp.html', Nom=Nombre)


@app.route('/raspberry', methods=['POST'])
def my_form_post():
    text = request.form['data']
    conn.initConnection()
    conn.writeArduino(text)
    conn.readArduino()
    processed_text = conn.receivedData
    conn.closeConnection()
    print(processed_text, file=sys.stdout.flush())
    return render_template('rasp.html', send_data=text, received_data=processed_text)


if __name__ == "__main__":
    # Con esto hacemos que el servidor de flasjk al arrancar y haya cambios en el código se registren los cambios, algo como django.
    app.run(host="127.0.0.1", port=5000)
