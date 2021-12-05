try:
    from app import app
    from flask import render_template
except ImportError as eImp:
    print(f"En el archivo {__file__} currió el error de importación: {eImp}")

#----------------------------Error Handlers------------------------------------#

# @Description: Endpoint to verify error 500 if its the case.
@app.route("/error500")
def error():
    return render_template('errorHandlers/error500.html')