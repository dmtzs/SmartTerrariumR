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
    message_to_send = """Este es un bot en el que puedes ejecutar acciones desde telegram, solo agregas un /comando 
    para que puedas ejecutar uno de los comandos disponibles que salen como opciones en el canal donde el bot está 
    instalado. De igual manera es un bot que notifica si está abajo el servidor o se a reiniciado la raspberry, etc."""
    bot.reply_to(message, message_to_send)

@bot.message_handler(commands=["reboot"])
def reboot_rasp(message):
    message_to_send = "Reiniciando raspberry"
    bot.reply_to(message, message_to_send)
    subprocess.Popen('reboot', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    bot.infinity_polling()