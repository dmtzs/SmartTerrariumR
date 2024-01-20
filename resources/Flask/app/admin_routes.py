"""
admin_routes
====================
Routes for admin users, this file contains the routes for the admin users.

Diego Martinez Sanchez
"""
try:
    import pytz
    from http import HTTPStatus
    from datetime import datetime as dt
    from app import app
    from flask import make_response, jsonify, abort, request
except ImportError as err_imp:
    print(f"In file: {__file__} the following import error ocurred: {err_imp}")

# ------------------Admin routes------------------
@app.route("/status", methods=["GET"])
def status():
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        abort(make_response(jsonify({"error": "Unauthorized"}), HTTPStatus.UNAUTHORIZED))
    response = {
        "status": "OK",
        "date": dt.now(pytz.timezone("America/Mexico_City")).strftime("%d/%m/%Y %H:%M:%S")
    }
    return make_response(jsonify(response), HTTPStatus.OK)
