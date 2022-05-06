try:
    import sys
    import pytz
    import telebot
    import subprocess
    from datetime import datetime as dt
except ImportError as eImp:
    print(f"The following import ERROR occurred in {__file__}: {eImp}")

def telegram_message(message, modo):
    now = dt.now(pytz.timezone("America/Mexico_City"))#TODO: Usar después API de timezone
    date_time = now.strftime('%d/%B/%Y %I:%M:%S')

    token = ""
    bot = telebot.TeleBot(token)
    bot.config["api_key"] = token

    if modo == "normal":
        final_message = f"-------------{date_time}-------------" + "\n" + message + "\n" + "--------------------------------------------------------------"
    elif modo == "verify":
        final_message = f"-------------{date_time}-------------" + "\n" + message[0] + "\n" + message[1] + "\n" + message[2] + "\n" + "--------------------------------------------------------------"

    bot.send_message(5222776919, final_message)

def core_method():
    lenargv = len(sys.argv)
    args = sys.argv

    if lenargv == 2:
        if args[1] == "--rebootRasp":
            message = "Raspberry se ha reiniciado"
            telegram_message(message, "normal")

        elif args[1] == "--verifyApps":
            # TODO: Necesito usar otro método para validar si la app está corriendo o no, tal vez de manera separada si el servidor está corriendo si el electron también, etc
            # PAra este caso el cron debe mandar con la bandera de verifyApps y tal vez internamente mandar mensaje en caso de que solo esté abajo el servidor o el electron o ambos.
            result_command = subprocess.Popen('ps aux | grep python3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)# TODO: Todo este bloque separarlo en una función
            output_result = str(result_command.stdout.read())
            result_command.stdout.close()
            result_command.wait()
            message_array = []

            if "Flask" in output_result:
                message_array.append("Ambiente corriendo: DEV")
                message_array.append("Servidor arriba")
            # elif "Server" in output_result:#TODO: Se debe de correr de nuevo subprocess buscando server
            #     message_array.append("Ambiente corriendo: PRD")
            #     message_array.append("Servidor arriba")
            else:
                message_array.append("Ambiente corriendo por última vez: DEV")# TODO: Para este caso poner aquí un txt que lea el último ambiente que se corrió, tal vez ese mismo archivo lo podamos escribir desde el index.js que se corre en electron, es decir, que el electron identifique si es dev o prd y escriba eso en el archivo que después lo leerá este mismo
                message_array.append("Servidor abajo")

            result_command = subprocess.Popen('ps aux | grep electron', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)# TODO: Todo este bloque separarlo en una función
            output_result = str(result_command.stdout.read())
            result_command.stdout.close()
            result_command.wait()
            if "/home/diego/Documents/SmartTerrariumR/node_modules/electron/dist/electron --type=broker" in output_result:
                message_array.append("Electron arriba")
            else:
                message_array.append("Electron abajo")

            telegram_message(message_array, "verify")
    else:
        telegram_message("Se intentó correr el script sin argumento", "normal")

if __name__ == "__main__":
    try:
        core_method()
    except Exception as ex:
        title_toast = "Error"
        body_toast = f"The following ERROR ocurred: {ex}"

# Para mas de subprocess ver el siguiente enlace con info: https://stackoverflow.com/questions/38056/how-to-check-if-a-process-is-still-running-using-python-on-linux#:~:text=on%20linux%2C%20you%20can%20look,exists%2C%20the%20process%20is%20running.