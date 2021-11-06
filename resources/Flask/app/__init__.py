try:
    from flask import Flask
except ImportError as eImp:
    print(f"Ocurrió el error de importación: {eImp}")

# Creation of the flask app.
app = Flask(__name__)
app.secret_key = "clave_secreta_flask"

from app import routes, admin_routes