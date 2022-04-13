# Script que solo se ejecutará por fatherFile.py y creará un crontab de prueba.
import os
from crontab import CronTab

usu = os.getenv("USER")

my_cron = CronTab(user=usu)
print(type(my_cron))# Regresa una clase, checar si el for debajo funcionaría

# # Para mostrar crons creados
# for job in my_cron:
#     print(job)

# exe_file_from_cron = os.path.dirname(__file__)
# # print(exe_file_from_cron)

# file_to_execute = "python3 " + exe_file_from_cron + "/testCron.py"
# # Debajo pone el comando: cd /home/diego/Documentos/pruebas/crons && python3 /home/diego/Documentos/pruebas/crons/testCron.py
# job = my_cron.new(command=f"cd {exe_file_from_cron} && {file_to_execute}")
# job.minute.every(1)
# my_cron.write()

# Comandos para crontab en terminal
# Para ver los crontab actuales del usuario actual: crontab -l
# Para borrar todos los crontab: crontab -r
# Para ver las ultimas lineas de los logs creados por la ejecución del crontab: tail -f /var/log/syslog | grep cron -i
# Falta investigar como poner el contrab con python para que se ejecute cada mes o cada semana, dependiendo de cómo se defina.