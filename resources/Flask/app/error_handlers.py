try:
    from app import app
    from flask import render_template
except ImportError as err_imp:
    print(f"In file: {__file__} the following import error ocurred: {err_imp}")

#----------------------------Error Handlers------------------------------------#

# @Description: Endpoint to verify error 500 if its the case.
@app.route("/error500")
def error() -> str:
    """
    Endpoint to verify error 500 if its the case.

    Returns:
    - str: HTML template with the error 500.
    """
    return render_template('errorHandlers/error500.html')