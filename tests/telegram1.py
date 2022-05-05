import telebot

token = ""
bot = telebot.TeleBot(token)
bot.config["api_key"] = token

bot.send_message(5222776919, "prueba telegram bot api")