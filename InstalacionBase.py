try:
    import os
    import platform
    import sys
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

def installBase(sistema):
    # @Description: Variables that contains commands according to the operative system that the program is being executed
    comandosLinux= ["sudo apt update", "sudo apt upgrade", "sudo apt install python3-pip", "pip3 install -r requirements.txt", "sudo apt install nodejs",
                    "sudo apt install npm", "npm install electron wait-port --save -prod", "sudo usermod -a -G dialout $USER"]
    
    comandosWindows= ["pip install -r requirements.txt", "npm install electron wait-port --save -prod"]

    if sistema== "Windows":
        execComands(comandosWindows)
    elif sistema== "Linux":
        execComands(comandosLinux)
    else:
        print("This program can be executed only in Windows and Linux operative systems")

def help(sistema):
    os.system("clear")
    cadeInstall= "Para instalar todas las dependencias necesarias del programa"
    cadeExe= "Para crear el ejecutable con pyinstaller para el back end de flask"
    commPython= ""

    if sistema== "Windows":
        commPython= "python"
    else:
        commPython= "python3"

    print(f"\n\n\n{commPython} InstalacionBase.py --install: {cadeInstall}")
    print(f"\n{commPython} InstalacionBase.py --exeFlask: {cadeExe}")
    print(f"\n{commPython} InstalacionBase.py --help: Para mostrar el presente panel de ayuda\n")

def main(sistema):
    lenargv= len(sys.argv)

    if lenargv== 2:
        if sys.argv[1]== "--install":
            installBase(sistema)
        elif sys.argv[1]== "--exeFlask":
            print("Aquí ejecutar el comando necesario para poder hacer el ejecutable del flask")
        elif sys.argv[1]== "--help":
            help(sistema)
        else:
            print("No ingresaste ningún comando válido")
            if sistema== "Windows":
                print("Ingresa python InstalacionesBase.py --help para ver la ayuda disponible")
            else:
                print("Ingresa python3 InstalacionesBase.py --help para ver la ayuda disponible")
    else:
        print("Solo se puede recibir un argumento, no más y no menos")

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
        print("Finalizando ejecución de programa")
