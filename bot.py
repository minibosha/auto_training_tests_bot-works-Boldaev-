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


# сделать вывод статистики (/test_statistics ...) и добавление в json файл (Statistics.add_statistics())
# Сделать поиск топ-5 самых похожих тестов по запросу


""" Функции """
# Функция для показа массива
def array_for_message(array, omissions='\n', start_ind=0, end=20):
    if omissions != "index":
        return omissions.join(map(str, array))
    else:
        array = array[start_ind:end]
        message = ''
        for ind, obj in enumerate(array, start=start_ind):
            message += f'{ind+1}) {obj}\n'
        return message



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

        # Если дан индекс задачи, то ищем название по индексу
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
user_test_indexes = {} # Хранение индекса на котором остановился человек
@Bot.message_handler(commands=['tests'])
def show_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 2)

    # Сохраняем человека, для продолжения просмотра тестов
    if message.chat.id not in user_test_indexes.keys():
        user_test_indexes[message.chat.id] = [0, user_message]

    # Получение результата в зависимости от ответа
    user_answer = Statistics.get_tests(user_message)
    if len(user_answer) >= 20:
        Bot.send_message(message.chat.id, array_for_message(user_answer, omissions="index") + "\nНапишите /next для вывода тестов дальше.")
    else:
        Bot.send_message(message.chat.id, array_for_message(user_answer, omissions="index"))

# Функция для продолжения просмотра тестов
@Bot.message_handler(commands=['next'])
def next_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 1)

    # Сохраняем и добавляем просмотр к человеку
    if message.chat.id not in user_test_indexes.keys():
        Bot.send_message(message.chat.id, "Напишите команду '/tests subject', чтобы программа поняла предмет который вам нужен.")
        return
    else:
        user_test_indexes[message.chat.id][0] += 20

    # Выводим человеку тесты

    user_answer = Statistics.get_tests(user_test_indexes[message.chat.id][1])
    user_answer = array_for_message(user_answer, omissions="index", start_ind=user_test_indexes[message.chat.id][0], end=user_test_indexes[message.chat.id][0] + 20)


    if len(user_answer.split())//2 >= 20:
        Bot.send_message(message.chat.id, user_answer + "\nНапишите /next для вывода тестов дальше.")
    elif 0 < len(user_answer.split())//2 < 20:
        Bot.send_message(message.chat.id, user_answer)
    else:
        Bot.send_message(message.chat.id, "Вы просмотрели все тесты, если вам нужно начать сначала, то снова напишите команду '/tests subject'.")
        del user_test_indexes[message.chat.id]


        # Вывод статистики
@Bot.message_handler(commands=['test_statistics'])
def show_statistics(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3)

    #Bot.send_message(message.chat.id, Statistics.get_statistics(message))


# testik
@Bot.message_handler(commands=['testiki'])
def nothing(message):
    Bot.send_message(message.chat.id, array_for_message([1, 2, 3, 'hi']))

    """
    #statistics[message.from_user.id] = message.text[9:] if message.text[8] == ' '  else message.text[8:]
    print(message, message.from_user.id, message.text)

    if message.text == 'aboba':
        return

    Bot.register_next_step_handler(message, nothing)
    """


""" Запуск бота """
Bot.infinity_polling()