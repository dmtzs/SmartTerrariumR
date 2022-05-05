import telebot

token = "5397598254:AAGQtp5cBytl8J8uSEYRXTDI7-UEjRQyQik"
bot = telebot.TeleBot(token)
bot.config["api-key"] = token

bot.send_message(5222776919, "prueba telegram bot api")