""" Скачивание библиотек """
# Создание и настройка бота
import telebot
from dotenv import load_dotenv
from os import getenv

import math

import json
import requests

import base64 # Библиотека для создания hash
import re


""" Подгрузка токена бота и его создание """
load_dotenv()
token = getenv('token')

# Создание бота
Bot = telebot.TeleBot(token, parse_mode=None)


# Сделать скролл всех тестов, сделать вывод статистики (/test_statistics ...) и добавление в json файл (Statistics.add_statistics())


""" Функции """
# Функция для возвращения json файла
def show_data():
    # Считываем данные из файла
    with open('files\\data.json', 'r', encoding='utf-8') as file:
        return json.load(file)


# Функция проверки и исправление ввода
def check_message(command, n):
    # Убираем частые ошибки в сообщениях (точки и регистр)
    user_object = command.text
    user_object = user_object.replace('.', '')
    user_object = user_object.lower()

    # Проверяем что у нас нужное количество данных
    txt = user_object.split()
    if len(txt) < n:
        return False

    # Возвращаем лист значений которые мы получаем
    return txt[1:]


# Функция шифровки чисел в hash.
def encoder(line):
    # Преобразуем информацию в строку
    line = str(line)

    # Преобразование строки в байты
    byte_string = line.encode('utf-8')

    # Кодирование в Base64
    encoded_string = base64.b64encode(byte_string)

    return encoded_string


# Функция расшифровки чисел из hash
def decoder(b64):
    # Декодирование из Base64
    decoded_bytes = base64.b64decode(b64)

    # Преобразование байтов обратно в строку
    decoded_string = decoded_bytes.decode('utf-8')

    # Регулярное выражение для поиска чисел, включая научные обозначения
    pattern = r'[\d]+(?:\.\d+)?(?:\^\d+)?'

    # Находим все числа в строке
    matches = re.findall(pattern, decoded_string)

    # Преобразуем найденные строки в числа
    numbers = []
    for match in matches:
        if '^' in match:
            base, exponent = match.split('^')
            number = float(base) * (10 ** int(exponent))
        else:
            number = float(match)
        numbers.append(number)

    return numbers


""" Классы """
# Класс для тестов по математике
class Tests:
    def __init__(self):
        pass

    # Функция для тестов по математике
    def math(self, name):
        pass

    # Функция для тестов по физике
    def physics(self, name):
        pass





class Math:
    def __init__(self):
        self.name = ''
        self.answers = []

    def start_test(self, name):
        self.name = name





# Вывод функций выводящий подробные действия решения и помогающие программе
class User_formulas:
    pass


# Класс выводящий разную статистику и информацию из json файлов
class Statistics:
    @staticmethod
    def get_tests(message):
        data = show_data()

        # Показываем варианты по названию
        if message[0] in ('math', 'математика'):
            return data["math"]
        elif message[0] in ('physics', 'физика', 'phys'):
            return data["physics"]
        else:
            return "Неизвестное сообщение или неправильный ввод."

    @staticmethod
    def get_statistics(message, id):
        # Извлекаем предмет и название теста
        subject = message[0]
        test_name = message[1]

        # Если дан индекс задачи то ищем название по индексу
        if isinstance(test_name, int):
            test_name = Statistics.find_name(subject, test_name)

        # Выводим статистику
        data = show_data()
        if not test_name:
            return "Неизвестное сообщение или неправильный ввод."
        elif subject not in ('math', 'математика', 'physics', 'физика', 'phys'):
            return "Неизвестное сообщение или неправильный ввод."
        else:
            # Получаем статистику
            result = data.get(id, {}).get(subject, {}).get(test_name)
            if result is not None:
                return result
            else:
                return "Неизвестное сообщение или неправильный ввод."

    @staticmethod
    def find_name(subject, index):
        data = show_data()

        # Возвращаем название теста по индексу
        if subject in ('math', 'математика'):
            if 0 <= index < len(data["math"]):
                return data["math"][index]
        elif subject in ('physics', 'физика', 'phys'):
            if 0 <= index < len(data["physics"]):
                return data["physics"][index]


""" Команды бота и ответы на них """
# Вывод при команде старт
@Bot.message_handler(commands=['start'])
def start(message):
    Bot.send_message(message.chat.id, 'Здравствуйте! Вы обратились к чат-боту с тестами. Я чат-бот для подготовки к тестам. Имеющий автоматическое создание примеров на тему теста. Чтобы узнать мой функционал, напишите "/help".')


# Вывод информации для помощи пользователю
@Bot.message_handler(commands=['help'])
def help_for_user(message):
    # Вывод при команде help и таблица команд
    COMMANDS_FOR_USER_HELP = [
        ['Команда', 'Что делает команда.', 'Параметры (если есть).'],
        ['/start', 'Выдаёт краткое описание бота и предметы по которым можно выбрать тест.', '-'],
        ['/help', 'Выдаёт список всех команд чат-бота и как правильно вводить ответы на задачу.', '-'],
        ['/tests object', 'просмотр тем тестов.', 'object - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
        ['/start_test name object', 'начать решение теста.', 'name - Название теста или его номер.'],
        ['/test_statistics name', 'выводит статистику теста (Количество попыток, лучший балл, баллы на первой попытке, баллы на последней попытке).', 'name - Название теста или его номер; object - Выбор предмета из возможных (math, математика; physics, физика, phys).'],
        ['/answer task answer или */an* task answer',  'Дать ответ после начала решения.', 'task - Номер задачи в тесте; answer - ответ на задачу (правила записи ответа выводятся при вводе команды /help).'],
        ['/end', 'заканчивает тест', '-', ]]

    table_str = ""
    change = True
    for row in COMMANDS_FOR_USER_HELP:
        for word in row:
            if change:
                table_str += "| " + word
                table_str += ' ' * (41 - len(word))
                change = False
            else:
                table_str += "| " + word
                table_str += ' ' * (112 - len(word))
        table_str += '\n\n'
        change = True

    Bot.send_message(message.chat.id,'Ссылка-описание на гит хабе: https://github.com/aip-python-tech-2024/works-Boldaev')

    Bot.send_message(message.chat.id, 'Команды:')
    Bot.send_message(message.chat.id, f"```\n{table_str}```", parse_mode='MarkdownV2')

    Bot.send_message(message.chat.id, 'Правила ввода ответов:\nПоявиться позже...')


# Вывод возможных тестов
@Bot.message_handler(commands=['tests'])
def subject(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 2)

    # Получение результата в зависимости от ответа
    Bot.send_message(message.chat.id, Statistics.get_tests(user_message))


# Вывод статистики
@Bot.message_handler(commands=['test_statistics'])
def show_statistics(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3)

    #Bot.send_message(message.chat.id, Statistics.get_statistics(message))


# testik
@Bot.message_handler(commands=['testiki'])
def nothing(message):
    #statistics[message.from_user.id] = message.text[9:] if message.text[8] == ' '  else message.text[8:]
    print(message, message.from_user.id, message.text)

    if message.text == 'aboba':
        return

    Bot.register_next_step_handler(message, nothing)


""" Запуск бота """
Bot.infinity_polling()









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