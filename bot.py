""" Скачивание библиотек """
# Создание и настройка бота
import telebot
from dotenv import load_dotenv
from os import getenv

import random
from sympy import symbols, sympify

import math

import json

import base64  # Библиотека для создания hash
import re

import difflib

""" Подгрузка токена бота и его создание """
load_dotenv()
token = getenv('token')

# Создание бота
Bot = telebot.TeleBot(token, parse_mode=None)


""" Функции """


# Нахождение топ-5 самых похожих слов по запросу
def find_similar_words(subject, input_word):
    # Загружаем названия тестов
    data = show_data()

    # Проверка, что правильно введён предмет
    if subject in ('math', 'математика', 'physics', 'физика', 'phys'):
        # Преобразуем предмет для его вывода
        if subject in ('math', 'математика'):
            subject = "math"
        elif subject in ('physics', 'физика', 'phys'):
            subject = "physics"

        # Находим массив тестов
        word_list = data[subject]
    else:
        "Неизвестное сообщение или неправильный ввод."

    # Используем SequenceMatcher для нахождения похожих слов
    similar_words = difflib.get_close_matches(input_word, word_list, n=5, cutoff=0.0)
    return similar_words


# Функция для показа массива
def array_for_message(array, omissions='\n', start_ind=0, end=20):
    if omissions != "index":
        return omissions.join(map(str, array))
    else:
        array = array[start_ind:end]
        message = ''
        for ind, obj in enumerate(array, start=start_ind):
            message += f'{ind + 1}) {obj}\n'
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
class Math:
    def __init__(self):
        # Данные пользователя
        self.user_answers = []

        # Данные для компьютера
        self.name_test = ''
        self.answers = []
        self.equations = []
        self.solve = []

    # Нахождение и начало теста
    def start_test(self, name):
        self.name_test = name


# Вывод функций выводящий подробные действия решения и помогающие программе
class UserFormulas:
    # Проверка, что у чисел не больше after_point знаков после запятой
    @staticmethod
    def normal(nums, after_point):
        # Регулярное выражение для проверки числа с не более чем n цифрами после запятой
        pattern = r'^\d+(\.\d{1,' + str(after_point) + '})?$'

        # Проверяем все числа на нормальность
        res = []
        for num in nums:
            num = abs(num)
            res.append(bool(re.match(pattern, str(num))))

        # Выводим ответ после проверки всех чисел
        return all(res)

    # Округление числа до указанного значения
    @staticmethod
    def round_nums(nums, digits):
        res = []
        for num in nums:
            res.append(round(num, digits))

        return res

    # Функция для вычисления уравнений
    @staticmethod
    def equation_solver(eqs, ranges, normal_check=False, after_point=4, round_check=False):
        # Создание нужных ячеек памяти
        results = []
        numbers = {}

        # Пытаемся рандомно подобрать значение, но если много операций то переходим дальше
        for _ in range(1000000):

            # Проверяем что нет доп. переменных
            equations = []  # Массив для уравнений
            dop_vars = {}  # Массив для добавочных переменных

            for ind, eq in enumerate(eqs):
                if '=' in eq:
                    ind_sym = eq.index('=')
                    if ind_sym:
                        dop_vars[ind] = eq[ind_sym + 1:]
                        equations.append(eq[:ind_sym])
                else:
                    equations.append(eq)

            # Создаём рандомные числа
            for ind, obj in enumerate(ranges.keys()):
                numbers[obj] = random.randint(ranges[obj][0], ranges[obj][1])

            # Заранее определяем массив переменных
            symbols_list = list(numbers.keys())  # Преобразуем в список
            symbols_list.extend(list(dop_vars.values()))  # Добавляем доп. переменные

            # Создаем символы из списка
            variables = {var: symbols(var) for var in symbols_list}

            # Проверяем числа на уравнениях
            for ind, equation in enumerate(equations):
                # Создаём уравнение
                expr = sympify(equation.strip())

                # Назначаем переменной значение
                values = {variables[var]: value for var, value in numbers.items() if var in variables}

                # Вычисляем результат (Проверка, что число не комплексное)
                try:
                    res = float(expr.subs(values))
                    results.append(res)

                    # Добавляем доп. переменные
                    val = dop_vars.get(ind, False)
                    if val:
                        numbers[val] = res

                except TypeError:
                    results.clear()
                    break

            # Округляем числа если это нужно
            if round_check:
                print(results)
                results = UserFormulas.round_nums(results, after_point)

            # Проверяем что числа в нужном диапазоне (до n знаков после запятой).
            if normal_check:
                if len(results) == len(equations):
                    if UserFormulas.normal(results, after_point):
                        return results, numbers
            else:
                return results, numbers

            # Удаляем результаты
            results.clear()


# Класс выводящий разную статистику и информацию из json файлов
class Statistics:
    # Получение всех названий тестов по предмету
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

    # Получение статистики человека по его id
    @staticmethod
    def get_statistics(message, user_id):
        # Извлекаем предмет и название теста
        subject = message[0]
        test_name = ' '.join(message[1:])

        # Если дан индекс задачи, то ищем название по индексу. Если нет, то переделываем сообщение
        if test_name.isdigit():
            test_name = Statistics.find_name(subject, int(test_name))

        # Выводим статистику
        data = show_data()
        if not test_name:
            return "Неизвестное сообщение или неправильный ввод."
        elif subject not in ('math', 'математика', 'physics', 'физика', 'phys'):
            return "Неизвестное сообщение или неправильный ввод."
        else:
            # Преобразуем предмет для его вывода
            if subject in ('math', 'математика'):
                subject = "math"
            elif subject in ('physics', 'физика', 'phys'):
                subject = "physics"

            # Получаем статистику
            result = data.get("id", {}).get(subject, {}).get(test_name)  # Удалить "id", заменить на переменную!!!
            if result is not None:
                return result
            else:
                return "Вашей статистики на этот тест нет."

    # Нахождение имя теста по его индексу и предмету
    @staticmethod
    def find_name(subject, index):
        data = show_data()
        index -= 1

        # Возвращаем название теста по индексу
        if subject in ('math', 'математика'):
            if 0 <= index < len(data["math"]):
                return data["math"][index]
        elif subject in ('physics', 'физика', 'phys'):
            if 0 <= index < len(data["physics"]):
                return data["physics"][index]

    # Добавление статистики
    @staticmethod
    def add_statistics(point, subject, user_id, name):
        data = show_data()

        # Инициализируем структуру данных, если она не существует
        if user_id not in data:
            data[user_id] = {}
        if subject not in data[user_id]:
            data[user_id][subject] = {}
        if name not in data[user_id][subject]:
            data[user_id][subject][name] = []

        # Если длина списка больше или равна 100, очищаем его
        if len(data[user_id][subject][name]) >= 100:
            data[user_id][subject][name] = []

        # Добавляем балл на тест
        data[user_id][subject][name].append(point)

        # Если больше 100 прохождений теста (возможно спам), то обновляем результаты теста
        if len(data[user_id][subject][name]) > 100:
            data[user_id][subject][name] = []

        # Добавляем балл на тест
        data[user_id][subject][name].append(point)

        # Сохраняем изменения обратно в файл
        with open('files\\data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


""" Команды бота и ответы на них """


# Вывод при команде старт
@Bot.message_handler(commands=['start'])
def start(message):
    Bot.send_message(message.chat.id,
                     'Здравствуйте! Вы обратились к чат-боту с тестами. Я чат-бот для подготовки к тестам. Имеющий автоматическое создание примеров на тему теста. Чтобы узнать мой функционал, напишите "/help".')


# Вывод информации для помощи пользователю
@Bot.message_handler(commands=['help'])
def help_for_user(message):
    # Вывод при команде help и таблица команд
    COMMANDS_FOR_USER_HELP = [
        ['Команда', 'Что делает команда.', 'Параметры (если есть).'],
        ['/start', 'Выдаёт краткое описание бота и предметы по которым можно выбрать тест.', '-'],
        ['/help', 'Выдаёт список всех команд чат-бота и как правильно вводить ответы на задачу.', '-'],
        ['/tests object', 'просмотр тем тестов.',
         'object - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
        ['/start_test name object', 'начать решение теста.', 'name - Название теста или его номер.'],
        ['/test_statistics name',
         'выводит статистику теста (Количество попыток, лучший балл, баллы на первой попытке, баллы на последней попытке).',
         'name - Название теста или его номер; object - Выбор предмета из возможных (math, математика; physics, физика, phys).'],
        ['/answer task answer или */an* task answer', 'Дать ответ после начала решения.',
         'task - Номер задачи в тесте; answer - ответ на задачу (правила записи ответа выводятся при вводе команды /help).'],
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

    Bot.send_message(message.chat.id,
                     'Ссылка-описание на гит хабе: https://github.com/aip-python-tech-2024/works-Boldaev')

    Bot.send_message(message.chat.id, 'Команды:')
    Bot.send_message(message.chat.id, f"```\n{table_str}```", parse_mode='MarkdownV2')

    Bot.send_message(message.chat.id, 'Правила ввода ответов:\nПоявиться позже...')


# Вывод возможных тестов
user_test_indexes = {}  # Хранение индекса на котором остановился человек


@Bot.message_handler(commands=['tests'])
def show_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 2)

    # Сохраняем человека, для продолжения просмотра тестов
    if message.chat.id not in user_test_indexes.keys():
        user_test_indexes[message.chat.id] = [0, user_message]

    # Получение результата в зависимости от ответа
    user_answer = Statistics.get_tests(user_message)
    if user_answer == 'Неизвестное сообщение или неправильный ввод.':
        Bot.send_message(message.chat.id, user_answer)
    elif len(user_answer) >= 20:
        Bot.send_message(message.chat.id, array_for_message(user_answer,
                                                            omissions="index") + "\nНапишите /next для вывода тестов дальше.")
    else:
        Bot.send_message(message.chat.id, array_for_message(user_answer, omissions="index"))


# Функция для продолжения просмотра тестов
@Bot.message_handler(commands=['next'])
def next_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 1)

    # Сохраняем и добавляем просмотр к человеку
    if message.chat.id not in user_test_indexes.keys():
        Bot.send_message(message.chat.id,
                         "Напишите команду '/tests subject', чтобы программа поняла предмет который вам нужен.")
        return
    else:
        user_test_indexes[message.chat.id][0] += 20

    # Выводим человеку тесты

    user_answer = Statistics.get_tests(user_test_indexes[message.chat.id][1])
    user_answer = array_for_message(user_answer, omissions="index", start_ind=user_test_indexes[message.chat.id][0],
                                    end=user_test_indexes[message.chat.id][0] + 20)

    if len(user_answer.split()) // 2 >= 20:
        Bot.send_message(message.chat.id, user_answer + "\nНапишите /next для вывода тестов дальше.")
    elif 0 < len(user_answer.split()) // 2 < 20:
        Bot.send_message(message.chat.id, user_answer)
    else:
        Bot.send_message(message.chat.id,
                         "Вы просмотрели все тесты, если вам нужно начать сначала, то снова напишите команду '/tests subject'.")
        del user_test_indexes[message.chat.id]

        # Вывод статистики


@Bot.message_handler(commands=['test_statistics'])
def show_statistics(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3)

    # Получаем статистику
    statistics = Statistics.get_statistics(message_text, message.chat.id)

    # Проверка, что мы получили массив статистики, и преобразуем его в понятную информацию
    if not isinstance(statistics, str):
        answer = [0, 0, 0, 0, 0]
        answer[0] = f"Количество попыток - {len(statistics)}"
        answer[1] = f"Средний балл - {sum(statistics) / len(statistics)}"
        answer[2] = f"Лучший балл - {max(statistics)}"
        answer[3] = f"Баллы на первой попытке - {statistics[0]}"
        answer[4] = f"Баллы на последней попытке - {statistics[-1]}"

        statistics = array_for_message(answer)

    Bot.send_message(message.chat.id, statistics)


@Bot.message_handler(commands=['find'])
def find_similar(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3)

    # Находим топ-5 похожих слов
    similar = find_similar_words(message_text[0], ' '.join(message_text[1:]))

    # Проверка, что мы получили массив слов
    if not isinstance(similar, str):
        similar = array_for_message(similar)

    Bot.send_message(message.chat.id, 'топ-5 похожих тестов по запросу:\n' + similar)


# Функция для начала тестов
user_tests = {}  # Словарь для сохранения тестов


@Bot.message_handler(commands=['start_test'])
def start_test(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3)

    # Проверяем что есть такой тест по его названию или индексу
    if message_text[1].isdigit():
        test_name = Statistics.find_name(message_text[0], int(message_text[1]))
        Bot.send_message(message.chat.id, f"Вы хотите начать тест по имени: '{test_name}'?")
    else:
        test_name = ' '.join(message_text[1:])
        if test_name in Statistics.get_tests(message_text):
            pass                                                # Доработать!!!
        else:
            Bot.send_message(message.chat.id, Statistics.get_tests(message_text[0]))


# testiki
taps = {}


@Bot.message_handler(commands=['testiki'])
def nothing(message):
    chat_id = str(message.chat.id)
    taps_count = taps.get(chat_id, -1)

    if taps_count == -1:
        Bot.send_message(message.chat.id,
                         'Нам запретили тапать хомяка, так что я сделал его пародию. Напишите "тап", чтобы начать!')
        taps[chat_id] = 0  # Инициализируем счетчик тапов
        Bot.register_next_step_handler(message, nothing)
    else:
        if message.text.lower() == 'тап':
            taps[chat_id] += 1
            Bot.send_message(message.chat.id,
                             f'Вы тапнули хомяка {taps[chat_id]} раз(а). Продолжайте тапать или напишите что-то другое, чтобы остановиться.')
            Bot.register_next_step_handler(message, nothing)
        else:
            Bot.send_message(message.chat.id,
                             f'Вы закончили игру. Вы тапнули хомяка {taps[chat_id]} раз(а). Напишите /testiki, чтобы начать заново.')
            del taps[chat_id]  # Удаляем запись о пользователе, чтобы начать заново


""" Запуск бота """
try:
    Bot.infinity_polling()
except KeyboardInterrupt:
    print('The program is stopped...')
