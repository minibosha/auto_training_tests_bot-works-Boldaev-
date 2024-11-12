# Создание и настройка бота
# Скачивание библиотек
import telebot
from dotenv import load_dotenv
from os import getenv

import math

import requests

# Подгрузка токена бота
load_dotenv()
token = getenv('token')

# Создание бота
bot = telebot.TeleBot(token, parse_mode=None)


# Классы.
# Переменные и массивы нужные для классов
tests_name_math = ('Полные квадратные уравнения', )
tests_name_phys = ('', )
statistics = {}


# Класс для тестов по математике
class math:
    def __init__(self):
        pass


# Класс для тестов по физике
class physics:
    def __init__(self):
        pass


# Вывод вычислений
class user_formulas:
    def __init__(self):
        pass


# Команды бота и ответы на них
# Вывод при команде старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вы обратились к чат-боту с тестами. Я чат-бот для подготовки к тестам. Имеющий автоматическое создание примеров на тему теста. Чтобы узнать мой функционал, напишите "/help".')


# Вывод при команде help и таблица комманд
commands_for_user_help = [
    ['Команда', 'Что делает команда.', 'Параметры (если есть).'],
    ['/start', 'Выдаёт краткое описание бота и предметы по которым можно выбрать тест.', '-'],
    ['/help', 'Выдаёт список всех команд чат-бота и как правильно вводить ответы на задачу.', '-'],
    ['/tests object', 'просмотр тем тестов.', 'object - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
    ['/start_test name', 'начать решение теста.', 'name - Название теста или его номер.'],
    ['/test_statistics name', 'выводит статистику теста (Количество попыток, лучший балл, баллы на первой попытке, баллы на последней попытке).', 'name - Название теста или его номер.'],
    ['/answer task answer или */an* task answer',  'Дать ответ после начала решения.', 'task - Номер задачи в тесте; answer - ответ на задачу (правила записи ответа выводятся при вводе команды /help).'],
    ['/end', 'заканчивает тест', '-',]
    ]

@bot.message_handler(commands=['help'])
def help_for_user(message):
    table_str = ""
    change = True
    for row in commands_for_user_help:
        for word in row:
            if change:
                table_str += "| " + word
                table_str += ' ' * (41 - len(word))
                change = False
            else:
                table_str += "| " + word
                table_str += ' ' * (112 - len(word))
        table_str += '\n'
        change = True

    bot.send_message(message.chat.id, 'Ссылка-описание на гит хабе: https://github.com/aip-python-tech-2024/works-Boldaev')

    bot.send_message(message.chat.id, 'Команды:')
    bot.send_message(message.chat.id, f"```\n{table_str}```", parse_mode='MarkdownV2')

    bot.send_message(message.chat.id, 'Правила ввода ответов:\nПоявиться позже...')


@bot.message_handler(commands=['tests'])
def math_or_phys(object0):
    # Убираем факторы которые могу быть причиной неизвестного сообщения
    user_object = object0.text
    user_object = user_object.replace('.', '')
    user_object = user_object.lower()

    # Вывод результата в зависимости от ответа
    if user_object in ('/tests math', '/tests математика'):
        math_tests(object0)
    elif user_object in ('/tests physics', '/tests физика', '/tests phys'):
        phys_tests(object0)
    else:
        bot.send_message(object0.chat.id, 'Неизвестное сообщение или неправильный ввод.')


# Вывод тестов по математике
def math_tests(object0):
    for ind, test in enumerate(tests_name_math):
        bot.send_message(object0.chat.id, str(ind+1) + '. ' + test)


# Вывод тестов по физике
def phys_tests(object0):
    for ind, test in enumerate(tests_name_phys):
        bot.send_message(object0.chat.id, str(ind+1) + '. ' + test)

# Запуск бота
bot.infinity_polling()



'''
import telebot
from dotenv import load_dotenv
import requests
from os import getenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOKEN = getenv('TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode='MarkdownV2')

add_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    reply = r'Hi\! This bot will help you to manage your Nintendo Switch games library\. You can:

• Add your games with purchase price\.
• Get some useful information from eShop\.
• Find buddies with same games\.

Detailed instructions are available via /help command\. Enjoy\!'

    bot.reply_to(message, reply)


@bot.message_handler(commands=['help'])
def send_help(message):
    reply = r'Available commands:

• /add new game to your library\. We will ask you some questions about your new game\.
• /find game information from eShop by its name or code \(you can find this code on cartridge\)\.
• /list your games with information\.'

    bot.reply_to(message, reply)


@bot.message_handler(commands=['add'])
def add_game_init(message):
    bot.send_message(message.chat.id, 'Send me *game name*')
    bot.register_next_step_handler(message, add_game_name)


def add_game_name(message):
    global add_data
    add_data[message.chat.id] = [message.text]
    bot.reply_to(message, 'Perfect, now send me purchase price in dollars, for example *59\.99*')
    bot.register_next_step_handler(message, add_game_price)


def add_game_price(message):
    global add_data
    add_data[message.chat.id].append(float(message.text))
    bot.reply_to(message, 'Nice, now check your info')
    info_reply = f'{add_data[message.chat.id][0]}: {add_data[message.chat.id][1]}'.replace('.', r'\.')
    print(info_reply)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('Yes', callback_data='yes'),
        InlineKeyboardButton('No', callback_data='no')
    )

    bot.reply_to(message, info_reply, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'yes':
        bot.answer_callback_query(call.id, 'Answer is Yes')
        bot.send_message(call.message.chat.id, 'Successfully added\!')
    elif call.data == 'no':
        bot.answer_callback_query(call.id, 'Answer is No')
        add_game_init(call.message)


@bot.message_handler(commands=['games'])
def send_games(message):
    url = 'https://search.nintendo-europe.com/en/select?fq=type%3AGAME+AND+system_type%3Anintendoswitch*+AND+product_code_txt%3A*&q=*&sort=change_date+desc&start=0&wt=json&rows=10'
    data = requests.get(url).json()
    response = '\n'.join([game['title'] for game in data['response']['docs']])
    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, 'Cannot proceed this message, try again')


bot.infinity_polling()
'''