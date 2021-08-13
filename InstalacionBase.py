try:
    import os
    import platform
except ImportError as eImp:
    print(f"The following import error ocurred: {eImp}")

# @Description: Method that returns the system and a shell command in order to clean the terminal in which this program is executed.
def ShellAndSystem():
    sistema = platform.system()

    if sistema == "Windows":
        return "cls", sistema
    else:
        return "clear", sistema
# @Description: Method used to execute the commands that were sent by the main method
def execComands(comandsExec):
    for comm in comandsExec:
        os.system(comm)

def main(sistema):
    # @Description: Variables that contains commands according to the operative system that the program is being executed
    comandosLinux= ["sudo apt update", "sudo apt upgrade", "sudo apt install python3-pip", "pip3 install -r requirements.txt", "sudo apt install nodejs",
                    "sudo apt install npm", "npm install electron wait-port", "sudo usermod -a -G dialout $USER"]
    
    comandosWindows= ["pip install -r requirements.txt", "npm install electron wait-port electron-alert"]

    if sistema== "Windows":
        execComands(comandosWindows)
    elif sistema== "Linux":
        execComands(comandosLinux)
    else:
        print("This program can be executed only in Windows and Linux operative systems")

if __name__ == "__main__":
    try:
        comShell, sistema= ShellAndSystem()
        os.system(comShell)
        main(sistema)
    except Exception as ex:
        print(f"The following error ocurred: {ex}")
    except KeyboardInterrupt:
        print("Se presiono Ctrl+c, finalizando programa con ejecución incorrecta")
    finally:
        print("Finalizando ejecución de programa de instalaciones base")
