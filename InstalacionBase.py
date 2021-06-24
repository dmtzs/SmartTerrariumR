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
    os.system("sudo apt install python3-pip")
    os.system("pip3 install -r requirements.txt")
    #Pensar si ejecutar desde aquí el programa de electron y el servidor de flask

if __name__== "__main__":
    try:
        comandoShell= limparShell()
        os.system(comandoShell)
        main()
    except Exception as ex:
        print(f"The following error ocurred: {ex}")