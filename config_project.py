import os
import zipfile
import wget


def localLibs():
    libsDirectory= "./resources/Flask/app/static/libraries/"
    localLibsUrl= "https://github.com/dmtzs/SmartTerrariumR/releases/download/Local_libraries/localLibraries.zip"
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