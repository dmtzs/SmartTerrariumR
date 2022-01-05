#@File: createCrontab.py
#@Author: Diego Martínez Sánchez.
#@Description: This file is in charge to create a crontab in order to execute a script that will be on charge to update the assets for this application.
try:
    import os
    from crontab import CronTab
    from updateLib import updates
except ImportError as eImp:
    print(f"En el archivo {__file__} ocurrió el siguiente error de importación: {eImp}")

def main_flow():
    actual_user = os.getenv("USER")
    exe_file_from_cron = os.path.dirname(__file__)
    file_to_execute = "python3 " + exe_file_from_cron + "/verifyUpdates.py"

    with CronTab(user=actual_user) as my_cron:
        job = my_cron.new(command=f"cd {exe_file_from_cron} && {file_to_execute}")
        job.minute.on(0)
        job.hour.on(10)
        job.day.on(14, 28)

if __name__ == "__main__":
    try:
        methods = updates.ExtraMethods()
        flag = methods.validate_os()

        if flag:
            main_flow()
        else:
            print("Solo se puede ejecutar este script en sistemas linux")

    except Exception as ex:
        print(f"En el archivo {__file__} ocurrió el siguiente error: {ex}")
    finally:
        print("Finalizando ejecución de script createCrontab.py")