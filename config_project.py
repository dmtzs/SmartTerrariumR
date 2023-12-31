"""
config_project
=================
This module contains the methods that are used to configure the project.
:copyrigth: (c) 2023, Diego Martinez Sanchez
:license: Personal license, see the LICENSE file for more details.
"""

import os
import shutil
import zipfile
import platform
import traceback
import wget


def local_libs() -> None:
    """
    Method that downloads the external front end libraries needed in the project.

    Args:
    - None

    Returns:
    - None
    """
    libs_directory = "./resources/Flask/app/static/libraries/"
    local_libs_url = "https://github.com/dmtzs/SmartTerrariumR/releases/download/Local_libraries/localLibraries.zip"
    file_to_unzip = f"{libs_directory}localLibraries.zip"

    if os.path.isdir(libs_directory):
        folders = [
            "bootstrap",
            "fontawesome",
            "jquery",
            "popper",
            "sweetalert"
        ]
        aux = []
        
        for folder in folders:
            if os.path.isdir(f"{libs_directory}{folder}/"):
                pass

            else:
                aux.append(folder)

        folders = aux
        del aux

        if len(folders) > 0:
            wget.download(local_libs_url, out=libs_directory)
        
            with zipfile.ZipFile(file_to_unzip, "r") as uzip:
                for file in uzip.namelist():
                    for fold in folders:
                        if file.startswith(f"{fold}/"):
                            uzip.extract(file, libs_directory)
            
            os.remove(file_to_unzip)
        else:
            pass
    else:
        os.mkdir(libs_directory)
        wget.download(local_libs_url, out=libs_directory)

        with zipfile.ZipFile(file_to_unzip, "r") as uzip:
            uzip.extractall(libs_directory)

        os.remove(file_to_unzip)

def content_init_app_and_sh_files(arch_content: list[str], name_arch: str, turn) -> None:
    """
    Method that creates a file neccessary for init in an automatic mode the application
    of the smart terrarium and also the content of the sh file.

    Args:
    - arch_content(str): Content of the file to create.
    - name_arch: Name of the file to create.

    Returns:
    - None
    """
    with open(name_arch, "wt") as fp:
        for elem in arch_content:
            fp.write(elem)
    
    if turn== 0:
        os.system("chmod +x startTerra.sh")
    else:
        pass

def strings_exe_flask(local_flag: str) -> tuple(str, str):
    """
    Method that returns strings with ; or : according to its operating system in which the script is running.

    Args:
    - local_flag(str): Flag that indicates the operating system in which the script is running.

    Returns:
    - tuple(str, str): Returns a tuple with two strings,
    the first one is the string with the static folder and the second one is the string with the templates folder.
    """
    if local_flag == "w":
        return "./resources/Flask/app;app/", "./resources/Flask/TerrariumLib;TerrariumLib/"
        
    elif local_flag == "l":
        return "./resources/Flask/app:app/", "./resources/Flask/TerrariumLib:TerrariumLib/"

def loop_exe_flask(assets: list[tuple[str]]) -> None:
    """
    Method that runs a for loop in order to delete the folders and files that are not neccessary in the production environment.

    Args:
    - assets(list[tuple[str]]): List of tuples with the folders and files to delete.

    Returns:
    - None
    """
    for h in range(len(assets)):
        for folder in assets[h]:
            if h== 0:
                shutil.rmtree(f"./{folder}")
            else:
                rmArchs= f"./{folder}"
                os.remove(rmArchs)

def files_and_folders(system: str) -> None:
    """
    Method that runs a for loop in order to be executed only if the script is been running in a windows or linux environment.

    Args:
    - system(str): Flag that indicates the operating system in which the script is running.

    Returns:
    - None
    """
    mainFolders= (".vscode", "dist", "build", "resources", "node_modules", ".git", "TerrariumApp", "WikiAssets")
    archsNo= (".gitattributes", ".gitignore", "package-lock.json", "package.json", "README.md", "requirements.txt", "index.js", "Server.spec")
    mainFoldersWin= ("dist", "build")
    
    rmFoldersLin= [mainFolders, archsNo]
    rmFoldersWin= [mainFoldersWin, ("Server.spec",)]

    if system == "Windows":
        loop_exe_flask(rmFoldersWin)
    else:
        loop_exe_flask(rmFoldersLin)
    global flag_prd
    flag_prd = 1

def exe_flask(system: str) -> None:
    """
    Method that creates the executable file in order to protect more the code of the flask and also to create the package of the electron including all code.

    Args:
    - system(str): Flag that indicates the operating system in which the script is running.

    Returns:
    - None
    """
    banderasPyinstaller= "--noconfirm --onefile --windowed"
    nomApp= '--name "Server"'
    icono= '--icon "./resources/Imgs/serverIco.ico"'
    archPrinFlask= "./resources/Flask/main.py"

    if system== "Windows":
        static, templates = strings_exe_flask("w")
        comPyinstaller = f'pyinstaller {banderasPyinstaller} {nomApp} {icono} --add-data "{static}" --add-data "{templates}" "{archPrinFlask}"'
        os.system(comPyinstaller)
        os.system("npm run dist")
        shutil.move("./dist/Server.exe", "./TerrariumApp/win-unpacked/Server.exe")#Falta revisar la forma en que los crea en windows
        files_and_folders(system)

    elif system == "Linux":
        static, templates = strings_exe_flask("l")
        actUsu = os.getenv("USER")
        actPath = os.path.realpath("./")
        auxActPath = actPath.split("/")
        auxActPath = auxActPath[3]
        pathEval = f"/home/{actUsu}/.config/autostart/"
        comPyinstaller = f'pyinstaller {banderasPyinstaller} {nomApp} {icono} --add-data "{static}" --add-data "{templates}" "{archPrinFlask}"'
        shFileContent = [f"#!/bin/bash\n\n", f"cd ~/{auxActPath}/SmartTerrariumR\n", "exec ./SmartTerra.AppImage"]
        initFileContent = ["[Desktop Entry]\n",
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
        shInitFiles = [shFileContent, initFileContent]
        fileNames = ["./startTerra.sh", f"{pathEval}startTerra.sh.desktop"]

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
        
        files_and_folders(system)

        os.mkdir("./resources/")
        shutil.move("./appData.json", "./resources/")

        for turn in range(2):
            content_init_app_and_sh_files(shInitFiles[turn], fileNames[turn], turn)

        print("Verifica si se creo el archivo de inicio, reinicia el sistema operativo y agrega manualmente la variable de entorno que funcionará como llave secreta para la desencripción de AES")
    
    else:
        print("No se puede ejecutar el programa en ambientes que no sean windows o linux")


if __name__ == "__main__":
    try:
        exe_flask(platform.system())
        local_libs()
    except Exception:
        print("Ocurrió un error al ejecutar el programa:")
        traceback.print_exc()
