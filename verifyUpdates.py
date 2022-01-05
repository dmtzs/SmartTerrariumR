try:
    from updateLib import updates
except ImportError as eImp:
    print(f"En el archivo {__file__} ocurrió el siguiente error de importación: {eImp}")

def main_flow():
    methods = updates.CheckUpdates()
    flag = methods.validate_os()

    if flag:# Crear archivo local de log para la ejecución de este programa y así verificar si se ejecutó correctamente o no.
        # Hacer cosas
        pass
    else:
        pass

if __name__ == "__main__":
    try:
        # Si en el json no viene nada la primera entonces borrar este archivo pue ssignifica que es opensource la version que tienen.
        # En el appData.json viene un parte de updates con los nombres de los assets, esto para usar esos nombres en caso de ser necesario para hacer el request a box cloud por esos assets.
        main_flow()
    except Exception as ex:
        # Hacer que el resultado se imprima en log local, poner mensaje: f"En el archivo {__file__} ocurrió el siguiente error: {ex}"
        pass