try:
    import os
    import platform
    from crontab import CronTab
except ImportError as eImp:
    print(f"En el archivo {__file__} ocurrió el siguiente error de importación: {eImp}")

def validate_os():
    sistema = platform.system()

    if sistema == "Linux":
        return True
    else:
        return False

def main_flow():
    actual_user = os.getenv("USER")

    my_cron = CronTab(user=actual_user)

    print(my_cron)

if __name__ == "__main__":
    try:
        flag = validate_os()

        if flag:
            main_flow()
        else:
            print("Solo se puede ejecutar este script en sistemas linux")

    except Exception as ex:
        print(f"En el archivo {__file__} ocurrió el siguiente error: {ex}")
    finally:
        print("Finalizando ejecución de script")