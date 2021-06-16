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

if __name__== "__main__":
    try:
        comandoShell= limparShell()
        os.system(comandoShell)
        main()
    except Exception as e:
        print(f"The following error ocurred: {e}")