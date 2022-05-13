try:
    import sys
    import time
    import pytz
    import telebot
    import subprocess
    from datetime import datetime as dt
except ImportError as eImp:
    print(f"The following import ERROR occurred in {__file__}: {eImp}")

def telegram_message(message, modo):
    now = dt.now(pytz.timezone("America/Mexico_City"))#TODO: Usar después API de timezone
    date_time = now.strftime('%d/%B/%Y %I:%M:%S')

    token = "your_telegram_token"
    bot = telebot.TeleBot(token)
    #bot.config["api_key"] = token

    if modo == "normal":
        final_message = f"------------{date_time}------------" + "\n" + message + "\n" + "------------------------------------------------------------"
    elif modo == "alert":
        final_message = f"------------{date_time}------------" + "\n" + message[0] + "\n" + message[1] + "\n" + "------------------------------------------------------------"

    if modo == "alert" or modo == "normal":
        bot.send_message(-1001752301611, final_message)# chat id de mi grupo: -1001752301611, chat id de mi mismo: 5222776919

def core_method():
    lenargv = len(sys.argv)
    args = sys.argv
    print("Entrando core method")

    if lenargv == 2:
        if args[1] == "--rebootRasp":
            message = "Raspberry se ha reiniciado"
            time.sleep(8)
            print("ENtrando a funcion mandar telegram")
            telegram_message(message, "normal")

        elif args[1] == "--verifyApps":
            # TODO: Necesito usar otro método para validar si la app está corriendo o no, tal vez de manera separada si el servidor está corriendo si el electron también, etc
            # PAra este caso el cron debe mandar con la bandera de verifyApps y tal vez internamente mandar mensaje en caso de que solo esté abajo el servidor o el electron o ambos.
            result_command = subprocess.Popen('ps aux | grep python3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)# TODO: Todo este bloque separarlo en una función
            output_result = str(result_command.stdout.read())
            result_command.stdout.close()
            result_command.wait()
            message_array = []
            flag_alert = ""

            if "Flask" in output_result:
                message_array.append("Ambiente corriendo: DEV")
                message_array.append("Servidor arriba")
                flag_alert = "OK"
            # elif "Server" in output_result:#TODO: Se debe de correr de nuevo subprocess buscando server
            #     message_array.append("Ambiente corriendo: PRD")
            #     message_array.append("Servidor arriba")
            else:
                message_array.append("Ambiente corriendo por última vez: DEV")# TODO: Para este caso poner aquí un txt que lea el último ambiente que se corrió, tal vez ese mismo archivo lo podamos escribir desde el index.js que se corre en electron, es decir, que el electron identifique si es dev o prd y escriba eso en el archivo que después lo leerá este mismo
                message_array.append("Servidor abajo")
                flag_alert = "alert"

            # result_command = subprocess.Popen('ps aux | grep "sh -c electron"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)# TODO: Todo este bloque separarlo en una función
            # output_result = str(result_command.stdout.read())
            # result_command.stdout.close()
            # result_command.wait()
            # if "sh -c electron" in output_result:
            #     message_array.append("Electron arriba")
            # else:
            #     message_array.append("Electron abajo")

            telegram_message(message_array, flag_alert)
    else:
        telegram_message("Se intentó correr el script sin argumento", "normal")

if __name__ == "__main__":
    try:
        core_method()
    except Exception as ex:
        title_toast = "Error"
        body_toast = f"The following ERROR ocurred: {ex}"


# Para mas de subprocess ver el siguiente enlace con info: https://stackoverflow.com/questions/38056/how-to-check-if-a-process-is-still-running-using-python-on-linux#:~:text=on%20linux%2C%20you%20can%20look,exists%2C%20the%20process%20is%20running.
# Documentación de telegram bot api: https://core.telegram.org/bots/api

# TODO: Ver la manera de mandar a más de un chat la alerta, como a mi y a un grupo, etc
