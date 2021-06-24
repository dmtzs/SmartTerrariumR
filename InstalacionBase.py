try:
    import os, platform, Metodos
except ImportError as eImp:
    print(f"The following import error ocurred: {eImp}")

def main():
    os.system("sudo apt install python3-pip")
    os.system("pip3 install -r requirements.txt")
    #Pensar si ejecutar desde aquí el programa de electron y el servidor de flask

if __name__== "__main__":
    try:
        limpShell= Metodos.ColeccionMetodos()
        comandoShell= limpShell.limparShell()
        os.system(comandoShell)
        main()
    except Exception as ex:
        print(f"The following error ocurred: {ex}")