try:
    pass
except ImportError as eImp:
    print(f"Ocurrió el siguiente error de importación: {eImp}")

class extraMethods():
    pass

class UpdateMethods(extraMethods):
    def __init__(self, command, system):
        self.command= command
        self.system= system

    def coreUpdate(self):
        pass