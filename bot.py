# Скачивание библиотек
import telebot
from dotenv import load_dotenv
from os import getenv

import requests


# Подгрузка токена бота
load_dotenv()
token = getenv('token')

# Создание бота
bot = telebot.TeleBot(token, parse_mode=None)


# Команды бота и ответы на них
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bot not ready yet... \nwait for full version)))")


@bot.message_handler(command=['games'])
def send_games(message):
    url = 'https://search.nintendo-europe.com/en/select?fq=type%3AGAME+AND+system_type%3Anintendoswitch*+AND+product_code_txt%3A*&q=*&sort=change_date+desc&start=0&wt=json&rows=10'
    data = requests.get(url).json()
    response = '\n'.join([game['title'] for game in data['response']['docs']])
    bot.send_message(message.chat.id, response)


# Запуск бота
bot.infinity_polling()