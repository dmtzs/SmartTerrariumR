try:
    import os
    import platform
    import sys
    import shutil
except ImportError as eImp:
    print(f"Ocurrió el siguiente error de importación: {eImp}")

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

# @Description: Method for install all the dependencies we need in order to make the program work in the way its supposed to be.
def installBase(sistema):
    # @Description: Variables that contains commands according to the operative system that the program is being executed
    comandosLinux= ["sudo apt update", "sudo apt upgrade", "sudo apt install python3-pip", "pip3 install -r requirements.txt", "sudo apt install curl",
                    "curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -", "cat /etc/apt/sources.list.d/nodesource.list", "sudo apt install -y nodejs",
                    "npm install wait-port --save-prod", "npm install electron electron-builder --save-dev", "sudo usermod -a -G dialout $USER"]
    
    comandosWindows= ["pip install -r requirements.txt", "npm install electron wait-port --save-prod"]

    if sistema== "Windows":
        execComands(comandosWindows)
    elif sistema== "Linux":
        execComands(comandosLinux)
    else:
        print("This program can be executed only in Windows and Linux operative systems")

# @Description: Method in which you can see the help in order to know how to use the present program in the correct way.
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
    print(f"\n{commPython} InstalacionBase.py --exes: {cadeExe}")
    print(f"\n{commPython} InstalacionBase.py --help: Para mostrar el presente panel de ayuda\n")

# Description: A complementary method for the ExeFlask method that returns strings with ; or : according to its operating system in which the script is running.
def cadesExeFlask(bandeLocal):
    if bandeLocal== "w":
        return "./resources/Flask/static;static/", "./resources/Flask/templates;templates/"
        
    elif bandeLocal== "l":
        return "./resources/Flask/static:static/", "./resources/Flask/templates:templates/"

# Description: A complementary method for the ExeFlask method that runs a for loop in order to be executed only if the script is been running in a windows or linux environment.
def loopForExeFlask():
    resFolders= ("RaspSerial", "Flask", "Imgs")
    mainFolders= ("Extras", ".vscode", "dist")
    archsNo= (".gitattributes", ".gitignore", "LICENSE.md", "package-lock.json", "package.json", "README.md", "requirements.txt")
    rmFolders= [resFolders, mainFolders, archsNo]

    for h in range(len(rmFolders)):
        for folder in rmFolders[h]:
            if h== 0:
                shutil.rmtree(f"./resources/{folder}")
            elif h== 1:
                shutil.rmtree(f"./{folder}")
            else:
                rmArchs= f"./resources/{folder}"
                if os.path.isfile(rmArchs):
                    os.remove(rmArchs)
                else:
                    rmArchs= f"./{folder}"
                    os.remove(rmArchs)

# Description: Method to create the executable file in order to protect more the code of the flask and also to create the package of the electron including all code.
def ExeFlask(sistema):
    banderasPyinstaller= "--noconfirm --onefile --windowed"
    nomApp= '--name "Server"'
    icono= '--icon "./resources/Imgs/serverIco.ico"'
    archPrinFlask= "./resources/Flask/main.py"

    if sistema== "Windows":
        static, templates= cadesExeFlask("w")
        comPyinstaller= f'pyinstaller {banderasPyinstaller} {nomApp} {icono} --add-data "{static}" --add-data "{templates}" "{archPrinFlask}"'
        os.system(comPyinstaller)
        os.system("npm run dist")
        shutil.move("./dist/Server.exe", "./TerrariumApp/win-unpacked/Server.exe")#Falta revisar la forma en que los crea en windows
        loopForExeFlask()

    elif sistema== "Linux":
        static, templates= cadesExeFlask("l")
        comPyinstaller= f'pyinstaller {banderasPyinstaller} {nomApp} {icono} --add-data "{static}" --add-data "{templates}" "{archPrinFlask}"'
        os.system(comPyinstaller)
        os.system("npm run dist")
        shutil.move("./dist/Server", "./TerrariumApp/linux-unpacked/Server")#If its in linux the icon should be a png of 256x256
        loopForExeFlask()
    
    else:
        print("No se puede ejecutar el programa en ambientes que no sean windows o linux")

# @Description: Method which calls all the other methods of this script, this is like the brain.
def main(sistema):
    lenargv= len(sys.argv)

    if lenargv== 2:
        if sys.argv[1]== "--install":
            installBase(sistema)

        elif sys.argv[1]== "--exes":
            ExeFlask(sistema)

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
        if sistema== "Windows":
            print("Intenta con python InstalacionesBase.py --help")
        else:
            print("Intenta con python3 InstalacionesBase.py --help")

if __name__ == "__main__":
    try:
        comShell, sistema= ShellAndSystem()
        os.system(comShell)
        main(sistema)
    except Exception as ex:
        print(f"Ocurrió el siguiente error: {ex}")
    except KeyboardInterrupt:
        print("Se presiono Ctrl+C, finalizando programa con ejecución incorrecta")
    finally:
        print("Finalizando ejecución de programa")
