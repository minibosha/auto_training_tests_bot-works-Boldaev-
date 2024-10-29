# Скачивание библиотек
import telebot
from dotenv import load_dotenv
from os import getenv

# Подгрузка токена бота
load_dotenv()
token = getenv('token')

# Создание бота
bot = telebot.TeleBot(token, parse_mode=None)


# Команды бота и ответы на них
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# Запуск бота
bot.infinity_polling()