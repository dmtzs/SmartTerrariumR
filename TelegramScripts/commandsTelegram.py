try:
    import telebot
    import subprocess
except ImportError as eImp:
    print(f"The following import ERROR occurred in {__file__}: {eImp}")

API_TOKEN = "5397598254:AAGQtp5cBytl8J8uSEYRXTDI7-UEjRQyQik"

bot = telebot.TeleBot(API_TOKEN)

# @bot.message_handler(commands=['help', 'start'])
@bot.message_handler(commands=["help"])
def send_welcome(message):
    first_part = "Este es un bot en el que puedes ejecutar acciones desde telegram, "
    second_part = "solo agregas un /comando para que puedas ejecutar uno de los comandos disponibles que salen como opciones en el canal "
    last_part = "donde el bot está instalado. De igual manera es un bot que notifica si está abajo el servidor o se a reiniciado la raspberry, etc."
    message_to_send = first_part + second_part + last_part
    bot.reply_to(message, message_to_send)

@bot.message_handler(commands=["rebootrasp"])
def reboot_rasp(message):
    message_to_send = "Reiniciando raspberry"
    bot.reply_to(message, message_to_send)
    subprocess.Popen('reboot', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@bot.message_handler(commands=["iprasp"])
def ip_rasp(message):
    command = subprocess.Popen('hostname -I', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = command.communicate()[0]
    result = result.decode("ascii")
    bot.reply_to(message, result)

if __name__ == '__main__':
    bot.infinity_polling()