#@File: InstalacionBase.py
#@Author: Diego Martínez Sánchez.
#@Description: This file contains all the methods that are used in order to install and create the production app for the terrarium.

#---------------------------Methods---------------------------
# @Description: Method used to execute the commands that were sent by the main method
def execComands(comandsExec):
    for comm in comandsExec:
        os.system(comm)

# @Description: Method for dowloading through wget the local libraries we need in order to load all the styles and other functionalities
#               of the electron project, etc.
def localLibs():
    libsDirectory= "./resources/Flask/app/static/libraries/"
    localLibsUrl= "https://github.com/dmtzs/dmtzs/releases/download/temporal/localLibraries.zip"
    fileToUnzip= f"{libsDirectory}localLibraries.zip"

    if os.path.isdir(libsDirectory):
        folders= ["bootstrap", "fontawesome", "jquery", "popper", "sweetalert"]
        aux= []
        
        for folder in folders:
            if os.path.isdir(f"{libsDirectory}{folder}/"):
                pass

            else:
                aux.append(folder)

        folders= aux
        del aux

        if len(folders) > 0:
            wget.download(localLibsUrl, out= libsDirectory)
        
            with zipfile.ZipFile(fileToUnzip, 'r') as uzip:
                for file in uzip.namelist():
                    for fold in folders:
                        if file.startswith(f"{fold}/"):
                            uzip.extract(file, libsDirectory)
            
            os.remove(fileToUnzip)
        else:
            pass
    else:
        os.mkdir(libsDirectory)
        wget.download(localLibsUrl, out= libsDirectory)

        with zipfile.ZipFile(fileToUnzip, 'r') as uzip:
            uzip.extractall(libsDirectory)

        os.remove(fileToUnzip)

# @Description: Method for install all the dependencies we need in order to make the program work in the way its supposed to be.
def installBase(sistema):
    # @Description: Variables that contains commands according to the operative system that the program is being executed
    # comandosLinux= ["sudo apt update", "sudo apt upgrade -y", "sudo apt install python3-pip", "pip3 install -r requirements.txt", "sudo apt install curl",
    #                 "curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -", "cat /etc/apt/sources.list.d/nodesource.list", "sudo apt install -y nodejs",
    #                 "npm install wait-port --save-prod", "npm install electron electron-builder --save-dev", "sudo usermod -a -G dialout $USER"]
    comandosLinux= ["pip3 install -r requirements.txt", "sudo apt install curl", "curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -",
                    "cat /etc/apt/sources.list.d/nodesource.list", "sudo apt install -y nodejs","npm install wait-port --save-prod",
                    "npm install electron electron-builder --save-dev"]
    
    comandosWindows= ["pip install -r requirements.txt", "npm install electron wait-port --save-prod", "npm install electron electron-builder --save-dev"]

    localLibs()
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

# @Description: A complementary method for the ExeFlask method that returns strings with ; or : according to its operating-
#               system in which the script is running.
def cadesExeFlask(bandeLocal):
    if bandeLocal== "w":
        return "./resources/Flask/app;app/", "./resources/Flask/TerrariumLib;TerrariumLib/"
        
    elif bandeLocal== "l":
        return "./resources/Flask/app:app/", "./resources/Flask/TerrariumLib:TerrariumLib/"

# @Description: A complementary method for the ExeFlask method that runs a for loop in order to be executed only if the script-
#               is been running in a windows or linux environment.
def ArchYFolders(sistema):
    mainFolders= (".vscode", "dist", "build", "resources", "node_modules", ".git", "TerrariumApp", "WikiAssets")
    archsNo= (".gitattributes", ".gitignore", "package-lock.json", "package.json", "README.md", "requirements.txt", "index.js", "Server.spec")
    mainFoldersWin= ("dist", "build")
    
    rmFoldersLin= [mainFolders, archsNo]
    rmFoldersWin= [mainFoldersWin, ("Server.spec",)]

    if sistema== "Windows":
        loopForExeFlask(rmFoldersWin)
    else:
        loopForExeFlask(rmFoldersLin)
    global bandeProd
    bandeProd= 1

# @Description: A method that just deletes uneccessary files and folders after we create the production environment.
def loopForExeFlask(assets):
    for h in range(len(assets)):
        for folder in assets[h]:
            if h== 0:
                shutil.rmtree(f"./{folder}")
            else:
                rmArchs= f"./{folder}"
                os.remove(rmArchs)

# @Description: Creation of a method that creates a file neccessary for init in an automatic mode the application-
#               of the smart terrarium and also the content of the sh file.
def contentInitAppAndShFiles(archContent, nameArch, turn):
    with open(nameArch, "wt") as fp:
        for elem in archContent:
            fp.write(elem)
    
    if turn== 0:
        os.system("chmod +x startTerra.sh")
    else:
        pass

# @Description: Method to create the executable file in order to protect more the code of the flask and also to create-
#               the package of the electron including all code.
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
        ArchYFolders(sistema)

    elif sistema== "Linux":
        static, templates= cadesExeFlask("l")
        actUsu= os.getenv("USER")
        actPath= os.path.realpath("./")
        auxActPath= actPath.split("/")
        auxActPath= auxActPath[3]
        pathEval= f"/home/{actUsu}/.config/autostart/"
        comPyinstaller= f'pyinstaller {banderasPyinstaller} {nomApp} {icono} --add-data "{static}" --add-data "{templates}" "{archPrinFlask}"'
        shFileContent= [f"#!/bin/bash\n\n", f"cd ~/{auxActPath}/SmartTerrariumR\n", "exec ./SmartTerra.AppImage"]
        initFileContent= ["[Desktop Entry]\n",
                  "Type=Application\n",
                  f"Exec={actPath}/startTerra.sh\n",
                  "Hidden=false\n",
                  "NoDisplay=false\n",
                  "X-GNOME-Autostart-enabled=true\n",
                  "Name[es]=Smart Terrarium\n",
                  "Name=Smart Terrarium\n",
                  "Comment[es]=Inits the application of the smart terrarium\n",
                  "Comment=Inits the application of the smart terrarium\n",
                  "X-GNOME-Autostart-Delay= 3"]
        shInitFiles= [shFileContent, initFileContent]
        fileNames= ["./startTerra.sh", f"{pathEval}startTerra.sh.desktop"]

        if os.path.isdir(pathEval):
            pass
        else:
            os.mkdir(pathEval)

        os.system(comPyinstaller)
        os.system("npm run dist")
        
        try:
            shutil.move("./TerrariumApp/TerrariumApp-1.0.0.AppImage", "./SmartTerra.AppImage")
        except:
            shutil.move("./TerrariumApp/TerrariumApp-1.0.0-arm64.AppImage", "./SmartTerra.AppImage")

        shutil.move("./resources/appData.json", "./")
        shutil.move("./dist/Server", "./")
        
        ArchYFolders(sistema)

        os.mkdir("./resources/")
        shutil.move("./appData.json", "./resources/")

        for turn in range(2):
            contentInitAppAndShFiles(shInitFiles[turn], fileNames[turn], turn)

        print("Verifica si se creo el archivo de inicio, reinicia el sistema operativo y agrega manualmente la variable de entorno que funcionará como llave secreta para la desencripción de AES")
    
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
            exec(open("createCrontab.py").read())
            os.remove("createCrontab.py")
            print("Crontab creado correctamente")

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
        # Native python libraries
        import os
        import sys
        import shutil
        import zipfile

        # My own libraries
        from update_lib import updates

        # Not native python libraries
        import wget
    except ImportError as eImp:
        print(f"En el archivo {__file__} ocurrió el siguiente error de importación: {eImp}")
        print("Instalando todas las bibliotecas de pyhton3")
        methods = updates.ExtraMethods()
        comShell, sistema, arch = methods.validate_os("install")
        del arch

        if sistema== "Linux":
            os.system("pip3 install -r requirements.txt")
        
        else:
            print("El script solo se puede ejecutar en entornos Linux")
        
        print("Bibliotecas faltantes instaladas.")
        print("Por favor vuelve a ejecutar este programa con el mismo comando.")
        
    else:
        methods = updates.ExtraMethods()
        comShell, sistema, arch = methods.validate_os("install")

        if sistema== "Linux":
            del arch

            global bandeProd
            bandeProd= 0
            try:
                os.system(comShell)
                main(sistema)
            except Exception as ex:
                print(f"Ocurrió el siguiente error: {ex}")
            except KeyboardInterrupt:
                print("Se presiono Ctrl+C, finalizando programa con ejecución incorrecta")
            finally:
                print("Finalizando ejecución de programa")
                if bandeProd== 0:
                    pass
                elif bandeProd!= 0 and sistema== "Linux":
                    os.remove("InstalacionBase.py")

        else:
            print("El script solo se puede ejecutar en entornos Linux")