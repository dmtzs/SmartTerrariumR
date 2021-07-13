try:
    import os, platform
except ImportError as eImp:
    print(f"The following import error ocurred: {eImp}")


def limpShell():
    sistema = platform.system()

    if sistema == "Windows":
        return "cls"
    else:
        return "clear"


def main():
    #Pensar si incluir: "sudo apt install florence -y", "sudo apt install at-spi2-core -y"
    comandos = ["sudo apt install python3-pip", "pip3 install -r requirements.txt", "sudo apt install nodejs",
                "sudo apt install npm", "npm install electron", "npm install wait-port", "sudo usermod -a -G dialout $USER"]

    for comm in comandos:
        os.system(comm)
    # Pensar si ejecutar desde aquí el programa de electron.


if __name__ == "__main__":
    try:
        os.system(limpShell())
        main()
    except Exception as ex:
        print(f"The following error ocurred: {ex}")
