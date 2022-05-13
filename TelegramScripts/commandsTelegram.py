# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

API_TOKEN = "5397598254:AAGQtp5cBytl8J8uSEYRXTDI7-UEjRQyQik"

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "This is an alert bot to know raspberry status\nTo execute commands write in the chat an / and you will see the list of commands available")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.infinity_polling()