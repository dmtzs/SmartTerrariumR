#@File: updateApp.py
#@Author: Diego Martínez Sánchez.
#@Description: This file will be used to update the production app if its neccessary like the program of the arduino, the flask server-
#              and the rest of the files like the appData if its the case that we should add more functionalities in the app.

try:
    # Native python libraries and local libraries.
    import os
    import platform
    from updateLib import * # Module imported: upCommands
except ImportError as eImp:
    print(f"Ocurrió el siguiente error de importación: {eImp}")

#@Description: Method that returns the system and a shell command in order to clean the terminal in which this program is executed.
def ShellAndSystem():
    sistema= platform.system()

    if sistema == "Windows":
        return "cls", sistema
    else:
        return "clear", sistema

if __name__ == "__main__":
    try:
        comm, sis= ShellAndSystem()
        if sis== "Linux":
            coreFile= upCommands.UpdateMethods(comm, sis)
            os.system(comm)
            coreFile.coreUpdate()
        else:
            print("This script should be only executed in a production environment and only in linux systems")
    except Exception as ex:
        print(f"Ocurrió el siguiente error: {ex}")
    except KeyboardInterrupt:
        print("Se presiono Ctrl+C, finalizando programa con ejecución incorrecta")
    finally:
        print("Finalizando ejecución de programa")