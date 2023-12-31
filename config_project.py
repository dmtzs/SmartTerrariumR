import os
import zipfile
import wget


def local_libs():
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

if __name__ == "__main__":
    local_libs()
