try:
    import os, platform
except ImportError as eImp:
    print(f"The following import error ocurred: {eImp}")

def limparShell():
    sistema= platform.system()

    if sistema== "Windows":
        return "cls"
    else:
        return "clear"

def main():
    os.system("pip3 install -r requirements.txt")
    #Va el git clone

    """
    Para la parte de dht22 con el raspberry
    temporal: https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/
    temporal2: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ --> se ve mejor este
    """

if __name__== "__main__":
    try:
        comandoShell= limparShell()
        os.system(comandoShell)
        main()
    except Exception as ex:
        print(f"The following error ocurred: {ex}")