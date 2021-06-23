try:
    import time
    from flask import Flask, render_template, redirect, url_for
    from datetime import datetime
except Exception as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

app= Flask(__name__)#Se crea la app, se instancia el framework para poder usarse.
app.secret_key= "clave_secreta_flask"

#Context processor
@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

#Endpoints
@app.route('/')#Ruta inicial del proyecto
def index():
    return render_template('index.html', dato1= "valor", dato2= "valor2", lista= ["uno", "dos", "tres"])

#Manda error porque lo estoy convirtiendo en entero.
@app.route('/informacion')
@app.route('/informacion/<string:nombre>')
@app.route('/informacion/<string:nombre>/<ape>')#Otra ruta para recibir parámetros con lo que dice nombre en este caso y con validaciones
def informacion(nombre= None, ape= None):#El parámetro se debe llamar forzosamente igual a como lo nombre arriba entre las <>
    texto= ""
    if nombre!= None and ape!= None:
        texto= f"Bienvenido, {nombre} {ape}"
    return render_template('informacion.html', textohtml= texto)

@app.route('/contacto')
@app.route('/contacto/<redireccion>')
def contacto():
    return render_template('contacto.html', Nom= Nombre)

if __name__== "__main__":
    app.run(debug= True)#Con esto hacemos que el servidor de flasjk al arrancar y haya cambios en el código se registren los cambios, algo como django.