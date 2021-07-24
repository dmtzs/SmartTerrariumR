try:
    import os
    import platform
except ImportError as eImp:
    print(f"The following import error ocurred: {eImp}")


def limpShellSystem():
    sistema = platform.system()

    if sistema == "Windows":
        return "cls", sistema
    else:
        return "clear", sistema


def main(sistema):
    #Pensar si incluir: "sudo apt install florence -y", "sudo apt install at-spi2-core -y"
    comandosLinux= ["sudo apt update", "sudo apt upgrade", "sudo apt install python3-pip", "pip3 install -r requirements.txt", "sudo apt install nodejs",
                    "sudo apt install npm", "npm install electron wait-port electron-alert", "sudo usermod -a -G dialout $USER"]
    
    comandosWindows= "npm install electron wait-port electron-alert"

    if sistema== "Windows":
        os.system(comandosWindows)
    elif sistema== "Linux":
        for comm in comandosLinux:
            os.system(comm)
    else:
        print("Solo se puede ejecutar en linux y windows")
    # Pensar si ejecutar desde aquí el programa de electron.


if __name__ == "__main__":
    try:
        comShell, sistema= limpShellSystem()
        os.system(comShell)
        main(sistema)
    except Exception as ex:
        print(f"The following error ocurred: {ex}")
    finally:
        print("Finalizando ejecución de programa de instalaciones base")
