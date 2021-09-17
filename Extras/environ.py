import os

#print(os.getenv("SHELL"))
#print(os.getenv("SESSION_MANAGER"))

#Esto en linux no setea realmente la variable de entorno porque se debe de ejecutar el programa para que esto sirva
#os.environ["PRUEBA"]= "/bin/bash"
os.environ.setdefault("PRUEBA", "Nuevo_valor")
print(os.environ["PRUEBA"])

if "PRUEBA" in os.environ:
    print("Existe")
else:
    print("No existe")

print("Borrando variable")
os.environ.pop("PRUEBA")