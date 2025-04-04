""" Скачивание библиотек """
import difflib
import json
import random
import re
from os import getenv

# Создание и настройка бота
import telebot
from dotenv import load_dotenv
from sympy import symbols, sympify
from telebot import types  # для создания кнопок

""" Подгрузка токена бота и его создание """
load_dotenv()
token = getenv('token')

# Создание бота
Bot = telebot.TeleBot(token, parse_mode=None)

""" Переменные """

SUBJECTS = ['math', 'математика', 'physics', 'физика', 'phys']
MATH_SUB = ['math', 'математика']
PHYS_SUB = ['physics', 'физика', 'phys']

""" Функции """


# Функция, для создания шаблонных кнопок
def easy_markup(*args):
    # Создание кнопок команд (для обычных задач)
    # Создание объекта кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Добавление кнопок
    for btn in args:
        markup.add(types.KeyboardButton(btn))

    # Возвращения объекта кнопок
    return markup


# Обновляет значения в словарях dict1 и dict2 на основе массива array.
def update_dicts_with_array(dict1: dict, array: list):
    index = 0  # Индекс для перебора массива

    # Обновляем первый словарь
    for key in dict1:
        if index < len(array):
            dict1[key] = array[index]
            index += 1
        else:
            break  # Если массив закончился, выходим

    return dict1


# Проверка языка для расшифровки
def detect_language(char):
    return 'а' <= char.lower() <= 'я' or char == 'ё'


# Проверка, что строка это число
def is_number(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


# Функция переделывающая положительные числа в шестнадцатеричную систему
def make_hex(number: float) -> str:
    if number.is_integer():
        return hex(int(number))[2:].upper()
    else:
        # Для дробных чисел преобразуем целую и дробную части отдельно
        integer_part = int(number)
        fractional_part = int(str(number).split('.')[-1])  # Ограничиваем дробную часть двумя знаками
        return f"{hex(integer_part)[2:].upper()}.{hex(fractional_part)[2:].upper()}"


# Функция, которая преобразует число в 16-ричный формат.
def to_hex(number: float) -> str:
    # Проверяем число на минус
    if '-' in str(number):
        return '-' + make_hex(float(str(number)[1:]))
    else:
        return make_hex(number)


# Проверка, можно ли представить число как степень десятки.
def is_power_of_ten(number: float) -> bool | None:
    if number == 0:
        return False
    if number < 0:
        number = abs(number)
    if number < 1000:
        return False
    # Делим число на 10, пока оно не станет равным 1
    while number != 1:
        if number % 10 != 0:  # Если остаток от деления на 10 не равен 0
            return False
        number = number // 10  # Делим число на 10

    return True


# Функция сжимания числа, выбирая наиболее короткое представление.
def compress_number(number: float) -> str:
    hex_representation = to_hex(number)

    # Проверяем, можно ли представить число как степень десятки
    if is_power_of_ten(number):
        if hex_representation[0] == '-':
            power = len(str(int(number))[1:]) - 1
            power_representation = f"-10^{power}"
        else:
            power = len(str(int(number))[1:])
            power_representation = f"10^{power}"

        # Выбираем более короткое представление
        if len(power_representation) < len(hex_representation):
            return power_representation

    return hex_representation


# Функция обработки строки с числами, разделенными знаком (например, '/' или '*').
def process_numbers(input_str: str) -> str:
    if '/' in input_str:
        numbers = input_str.split('/')
        separator = '/'
    elif '*' in input_str:
        numbers = input_str.split('*')
        separator = '*'
    else:
        # Если нет разделителя, обрабатываем как одно число
        return compress_number(float(input_str))

    # Обрабатываем каждое число
    compressed_numbers = []
    for num in numbers:
        compressed_numbers.append(compress_number(float(num)))

    # Возвращаем сжатую строку с тем же разделителем
    return separator.join(compressed_numbers)


def counter():
    count = 0
    while True:
        yield count
        count += 1


# Функция разделения по языкам
def split_by_language(input_str: str) -> list:
    result = []
    current_group = []
    current_lang = None  # Текущий язык ('rus' или 'eng')
    has_lower = False  # Есть ли в группе символы в нижнем регистре

    for char in input_str:
        if char.isalpha():
            # Определяем язык и регистр символа
            lang = 'rus' if detect_language(char) else 'eng'
            is_lower = char.islower()

            # Если язык или регистр изменились, завершаем текущую группу
            if (lang != current_lang) or (is_lower != has_lower):
                if current_group:
                    # Добавляем группу с минусом, если есть символы в нижнем регистре
                    result.append(('-' if has_lower else '') + ''.join(current_group))
                    current_group = []
                    has_lower = False
                current_lang = lang

            # Обновляем флаг нижнего регистра
            if is_lower:
                has_lower = True

            # Добавляем шестнадцатеричный знак
            current_group.append(char)
        else:
            # Если символ — разделитель, завершаем текущую группу
            if char in {' ', ','}:
                if current_group:
                    result.append(('-' if has_lower else '') + ''.join(current_group))
                    current_group = []
                    current_lang = None
                    has_lower = False
                result.append(char)
            else:
                # Если символ не разделитель, добавляем его в текущую группу
                if current_group:
                    current_group.append(char)
                else:
                    # Если группы нет, добавляем символ как есть
                    result.append(char)

    # Добавляем последнюю группу, если она есть
    if current_group:
        result.append(('-' if has_lower else '') + ''.join(current_group))

    # Объединяем последовательные разделители
    merged_result = []
    for item in result:
        if merged_result and item in {' ', ','} and merged_result[-1] in {' ', ','}:
            merged_result[-1] += item
        else:
            merged_result.append(item)

    return merged_result


def to_tenth(string: list[str]) -> list[str]:
    unencrypted = []
    # Проверяем каждое число на наличие символов
    char = ''
    factor = 0
    for index, num in enumerate(string):
        minus = False
        # Проверяем число на символы, если их нет то просто переделываем число
        if '-' in num:
            # Добавляем минус в конечное расшифрованное число, а для расшифровки убираем его
            char += '-'
            num = num[1:]
            minus = True
        if '*' in num:
            # Указываем что есть множитель и убираем его на время
            num = num.split('*')
            factor = int(num[-1])
            num = num[0]
        if '.' in num:
            # Расшифровываем дробное число
            num = num.split('.')
            num = str(int(num[0], 16)) + '.' + str(int(num[1], 16))
            # Проверяем что нет множителя чтобы не переходить дальше
            if not factor:
                char += num
                char += ' '
                continue
        if '^' in num:
            # Возводим число в степень
            num = num.split('^')
            num = str(int(num[0]) ** int(num[1]))
            # Проверяем что нет множителя чтобы не переходить дальше
            if not factor:
                char += num
                char += ' '
                continue
        if factor:
            # Добавляем числа по множителю
            for ind in range(factor):
                # Проверяем что нет минуса
                if minus and ind != 0:
                    char += '-'
                char += num
                char += ' '
            # Обнуляем множитель и переходим дальше
            factor = 0
            continue
        if ' ,' == num:
            # Переходи на следующую задачу
            char += ' ,'
            unencrypted.append(char)
            char = ''
        else:
            # Если не прошло проверки, значит это обычное шестнадцатеричное число
            char += str(int(num, 16))

        char += ' '

    return unencrypted


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
def check_message(command, n, user_command=None, strict=False, none_lower=False, answer=False):
    # Убираем частые ошибки в сообщениях (точки и регистр)
    user_object = command.text
    if not answer:
        user_object = user_object.replace('.', '')
    if not none_lower:
        user_object = user_object.lower()

    # Разграничиваем текст
    txt = user_object.split()

    # Проверяем что введённая команда верная
    if user_command:
        if user_command != txt[0]:
            return False

    # Проверяем что у нас нужное количество данных
    if strict:
        if len(txt) != n:
            return False
    else:
        if len(txt) < n:
            return False

    # Возвращаем лист значений которые мы получаем
    if n == 0 or strict == True and n == 1:
        return txt
    else:
        return txt[1:]


""" Классы """


# Класс для хэша
class Hash:
    def __init__(self):
        self.string = []  # Список для хранения строк
        self.encrypted = ''  # Переменная для хранения зашифрованной строки

    # Функция расшифровки
    def transcriber(self) -> bool | list:
        ENG_SYMBOLS = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                       'w']  # Константы для постановки знаков
        RUSS_SYMBOLS = ['э', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'х', 'ч']
        HEX_RUSS = {'а': 'A', 'б': 'B', 'в': 'C', 'г': 'D', 'д': 'E', 'е': 'F'}
        unencrypted_str = self.encrypted.split(',')  # Разделяем строки по запятым
        result = []
        print(self.string, self.encrypted)
        # Добавляем запятые в конец строк
        for ind in range(len(unencrypted_str)):
            unencrypted_str[ind] += ' ,'
        print(result)

        # Разделяем символы
        for stroke in unencrypted_str:
            result += split_by_language(stroke)

        # Очищаем результат чтобы не использовать много памяти и сохраняем результат в другой массив
        unencrypted_str = result
        result = []

        # Меняем все буквы в числа
        # Проверяем, что строка не разделитель перехода на новое задание
        for stroke in unencrypted_str:
            if stroke == ' ,':
                result.append(' ,')
                continue
            else:
                # Заменяем каждый символ на цифру (если символ это цифра)
                chars = ''
                for symbol in stroke:
                    if symbol.isalpha() or symbol == 'ё':
                        try:
                            symbol = symbol.lower()
                            # Проверка, что символ не шестнадцатеричной буквой
                            if 'a' <= symbol <= 'f':
                                chars += symbol.upper()
                            # Проверка, что это неизменённая шестнадцатеричная буква
                            elif symbol in HEX_RUSS.keys():
                                chars += HEX_RUSS[symbol]
                            else:
                                # По языку определяем цифру
                                if detect_language(symbol):
                                    chars += str(RUSS_SYMBOLS.index(symbol))
                                else:
                                    chars += str(ENG_SYMBOLS.index(symbol))
                        except ValueError as e:
                            print(e, stroke, symbol)
                            return False
                    else:
                        chars += symbol

                # Добавляем шестнадцатеричное число в результат
                result.append(chars)

        # Обновляем значения строки
        unencrypted_str = result

        # Возвращаем числа из шестнадцатеричной системы в десятеричную
        unencrypted_str = to_tenth(unencrypted_str)

        # Возвращаем расшифрованную строку
        return unencrypted_str

    def read(self, hash_str: str):
        # Расшифровываем hash, если этого не делали
        if not self.string:
            self.encrypted = hash_str
            self.string = self.transcriber()

        # Проверка, что не было ошибок
        if not self.string:
            return 'Error'

        # Выдаём коэффициенты задачи
        return self.string

    # Функция зашифровки чисел
    def string_for_show(self) -> list:
        string = [''] * len(self.string)
        # 1 Шаг: Подготовка строки к шифрованию
        for ind, nums in enumerate(self.string):
            # Разбиваем строку на числа и преобразуем их в список
            nums = list(map(float, nums.split()[:-1]))

            # Формируем результат, проверяя повторы
            index = 0
            count = 0
            result = []
            while index <= len(nums) - 1:
                number = nums[index]

                # Находим повторы
                while index <= len(nums) - 1 and number == nums[index]:
                    count += 1
                    index += 1

                # Проверяем на повторы и добавляем в результат для изменения
                if count >= 3:
                    if number.is_integer():
                        result.append(f"{int(number)}*{count}")
                    else:
                        result.append(f"{number}*{count}")
                else:
                    if number.is_integer():
                        for _ in range(count):
                            result.append(int(number))
                    else:
                        for _ in range(count):
                            result.append(number)
                count = 0  # Обнуляем счётчик

            # Переделываем результат в строку для дальнейшего использования
            nums = result
            result = []  # Очищаем, чтобы не тратить память

            # Переделываем все числа в шестнадцатеричную. Меняем дробные и создаём степени по возможности.
            for num in nums:
                result.append(process_numbers(str(num)))

            # Сохраняем изменения
            string[ind] = ' '.join(result)

        # Возвращаем строку
        return string

    # Функция для зашифровки числа и его вывода
    def show(self):
        # 2 Шаг: Смена знаков
        ENG_SYMBOLS = 'ghijklmnopqrstuvw'  # Константы для постановки знаков
        RUSS_SYMBOLS = 'эжзийклмнопрстухч'
        HEX_RUSS = {'A': 'а', 'B': 'б', 'C': 'в', 'D': 'г', 'E': 'д', 'F': 'е'}

        encoded_str = ''
        russ = True
        # Проверяем каждое число и переделываем в буквы
        for string in self.string_for_show():
            encoded_str += ','  # Добавляем разделитель новой задачи
            string = string.split()

            # Проверка каждого числа
            for num in string:
                # Проверка на отрицательное число
                minus = False

                # Заменяем каждый символ и проверяем на минус
                for symbol in num:
                    # Проверяем что это числа, а не символ
                    if is_number(symbol):
                        # Проверяем что число положительное
                        if minus:
                            # Проверяем язык
                            if russ:
                                encoded_str += RUSS_SYMBOLS[int(symbol)]
                            else:
                                encoded_str += ENG_SYMBOLS[int(symbol)]
                        else:
                            # Проверяем язык
                            if russ:
                                encoded_str += RUSS_SYMBOLS[int(symbol)].upper()
                            else:
                                encoded_str += ENG_SYMBOLS[int(symbol)].upper()
                    # Проверяем что число шестнадцатеричное
                    elif symbol in HEX_RUSS.keys():
                        # Добавляем по языку
                        if russ:
                            # Проверяем положительное ли число
                            if minus:
                                encoded_str += HEX_RUSS[symbol].lower()
                            else:
                                encoded_str += HEX_RUSS[symbol].upper()
                        else:
                            # Проверяем положительное ли число
                            if minus:
                                encoded_str += symbol.lower()
                            else:
                                encoded_str += symbol.upper()
                    else:
                        # Если отрицательное число, то меняем его знак
                        if symbol == '-':
                            minus = True
                        else:
                            # Проверяем что число положительное или отрицательное
                            if minus:
                                encoded_str += symbol.lower()
                            else:
                                encoded_str += symbol.upper()
                # Меняем язык
                russ = not russ

        # Возвращаем зашифрованную строку
        self.encrypted = encoded_str[1:]
        return self.encrypted

    # Функция добавления коэффициентов задачи
    def add(self, num) -> None:
        # Меняем массив если это числа или строки, но не одной строкой
        if type(num) is list:
            num = ' '.join(map(str, num))

        # Добавляем строку в список
        num += ' ,'
        self.string.append(num)


# Класс для предмета
class Subject:
    def __init__(self, name_test, need_solve, user_hash):
        # Данные пользователя
        self.user_answers: list[str] = []
        self.user_hash = Hash()
        # Если hash есть, то создаём расшифрованный объект hash-a
        print(self.user_hash)
        if user_hash:
            try:
                print(self.user_hash)
                self.user_hash = self.user_hash.read(user_hash)
                for ind, text_of_test in enumerate(list(self.user_hash)):
                    print(self.user_hash)
                    if 'Error' in text_of_test:
                        self.user_hash = []
                        break
                    else:
                        if ',' in text_of_test:
                            self.user_hash[ind] = text_of_test[:-3]
            except (TypeError, ValueError):
                self.user_hash = []
        else:
            self.user_hash = []
        print(self.user_hash)

        # Данные для компьютера
        self.tasks: list[str] = []  # Задачи
        self.solve: list[str] = []  # Решения на задачи
        self.answers: list[str] = []  # Ответы на задачи
        self.program_hash = Hash()

        self.name_test: str = name_test
        self.need_solve: bool = need_solve

    # Выводим hash
    def show_hash(self):
        return self.program_hash

    # Вывод номеров теста
    def show_test(self):
        return array_for_message(self.tasks), len(self.answers)

    # Сохранение ответа
    def add_answer(self, n: int, task: int, ans: str):
        if len(self.user_answers) != 0:
            self.user_answers[task - 1] = ans
        else:
            self.user_answers = [''] * n
            self.user_answers[task - 1] = ans

    # Выводим решение
    def show_solve(self):
        if self.need_solve:
            return array_for_message(self.solve)
        else:
            return False

    # Проверяем ответы
    def check_answers(self):
        ans = ''
        m = 0
        for ind in range(len(self.answers)):
            ans += f'Задача №{ind + 1}.\nВаш ответ: {self.user_answers[ind]}.\nПравильный ответ: {self.answers[ind]}.\nВердикт: '

            # Вердикт
            if self.user_answers[ind] == self.answers[ind]:
                ans += 'Правильно\n'
                m += 1
            else:
                ans += 'Неправильно\n'

        # Результат
        ans += f'Итог: {m}/{len(self.answers)} ({int(m / len(self.answers) * 100)}%) правильных.'

        return ans

    # Выводим кол-во правильных ответов
    def get_point(self):
        n = 0
        for ind in range(len(self.answers)):
            if self.user_answers[ind] == self.answers[ind]:
                n += 1

        return n


# Класс для тестов по математике
class Math(Subject):
    # Нахождение и начало теста
    def create_test(self):
        # Переменные которые могут пригодиться при создании теста
        equations = []
        answers = []
        symbol = []
        other = []

        # Создаём класс UserFormulas с хэшом
        User_formulas = UserFormulas(self.user_hash)

        # Создаём тест
        match self.name_test:
            case 'полные квадратные уравнения':
                # 1. Полное приведённое квадратное уравнение.
                # Создаём уравнение
                equations = ["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"]
                answers, symbol = User_formulas.equation_solver(
                    ["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"],
                    {'a': (1, 1), 'b': (-20, 20), 'c': (-20, 20)}, normal_check=True, after_point=0,
                    exception=['0'], not_in_exc=['D'])

                # Создаём уравнение в целом
                other = UserFormulas.show_task_eq("x^2 bx c", a=symbol["a"], b=symbol["b"], c=symbol["c"]) + ' = 0'

                # Проверяем что дискриминант не ноль
                if answers[0]:
                    self.solve.append(UserFormulas.create_solve_txt(1, other, [
                        'Находим дискриминант (можно решить Виета), т.к. дискриминант больше нуля => 2 корня',
                        'Вычисляем первый корень', 'Вычисляем второй корень'], equations, answers))
                else:
                    self.solve.append(UserFormulas.create_solve_txt(1, other, [
                        'Находим дискриминант, т.к. дискриминант равен нулю => 1 корень', 'Вычисляем корень'],
                                                                    equations[:-1], answers))

                # Добавляем ответ
                equations = sorted(answers[1:])
                answers = ''
                for an in equations:
                    answers += str(int(an))
                self.answers.append(answers)

                # Создаём первый вопрос
                self.tasks.append(
                    f'1) Решите полное приведённое квадратное уравнение: {other}. В ответ введите корни в порядке возрастания без пробелов (минусы и нули учитываются).\n')

                # 2. Полное квадратное уравнение.
                # Создаём уравнение
                equations = ["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"]
                answers, symbol = User_formulas.equation_solver(
                    ["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"],
                    {'a': (-20, 20), 'b': (-20, 20), 'c': (-20, 20)}, normal_check=True, after_point=0,
                    exception=['-1', '0', '1'], not_in_exc=['D', ])

                # Создаём полное уравнение
                other = UserFormulas.show_task_eq("ax^2 bx c", a=symbol["a"], b=symbol["b"], c=symbol["c"]) + ' = 0'

                # Проверяем что дискриминант не ноль
                if answers[0]:
                    self.solve.append(UserFormulas.create_solve_txt(2, other, [
                        'Находим дискриминант, т.к. дискриминант больше нуля => 2 корня', 'Вычисляем первый корень',
                        'Вычисляем второй корень'], equations, answers))
                else:
                    self.solve.append(UserFormulas.create_solve_txt(2, other, [
                        'Находим дискриминант, т.к. дискриминант равен нулю => 1 корень', 'Вычисляем корень'],
                                                                    equations[:-1], answers))

                # Добавляем ответ
                equations = sorted(answers[1:])
                answers = ''
                for an in equations:
                    answers += str(int(an))
                self.answers.append(answers)

                # Создаём первый вопрос
                self.tasks.append(
                    f'2) Решите полное квадратное уравнение: {other}. В ответ введите ответ введите корни возрастания без пробелов (минусы и нули учитываются).')
            case "сложение":
                # Создаём три простых задачи и добавляем нужное по ним
                self.solve.append(
                    'Чтобы найти ответ нужно сложить два числа, чтобы это сделать воспользуйтесь калькулятором. Делается в одно действие')

                for ind in range(3):
                    answers, symbol = User_formulas.equation_solver(['a + b'], {'a': (0, 100), 'b': (0, 100)},
                                                                    normal_check=True, after_point=0)
                    equations.append(UserFormulas.show_task_eq('a b', a=symbol["a"], b=symbol["b"])[2:])
                    self.answers.append(str(int(sum(answers))))

                self.tasks.append(f'Решите три примера:\n1. {equations[0]}\n2. {equations[1]}\n3. {equations[2]}')

        # Получаем hash
        self.program_hash = User_formulas.get_hash()

    @staticmethod
    def get_subject():
        return 'math'


# Класс для тестов по физике
class Phys(Subject):
    # Нахождение и начало теста
    def create_test(self):
        # Переменные которые могут пригодиться при создании теста
        equations = []
        answers = []
        symbol = []
        other = []

        # Создаём класс UserFormulas с хэшом
        User_formulas = UserFormulas(self.user_hash)

        # Создаём тест
        match self.name_test:
            case 'закон ома':
                # Создаём решение
                self.solve.append(
                    'Для решения задачи нужен закон Ома: I = U / R\n из которой получаем U = I * R, R = U / I, где I - Сила тока, U - напряжение, R - сопротивление.')

                # Создаём первую задачу
                answers, symbol = User_formulas.equation_solver(
                    ['U / R'],
                    {'U': (1, 100), 'R': (1, 220)}, normal_check=True, after_point=5,
                    exception=['0'])

                self.solve.append(
                    '1) Подставляем в формулу и получаем: ' + str(symbol['U']) + '/' + str(symbol['R']) + ' = ' + str(
                        answers[0]))

                self.answers.append(str(answers[0]))
                self.tasks.append('1) Найдите силу тока в цепи и напишите её, если в цепи напряжение равно ' +
                                  str(symbol["U"]) + ' В    , а сопротивление лампы равно ' + str(symbol["R"]) + ' Ом')

                print(answers, self.answers, symbol, self.solve, self.tasks)

                # Создаём вторую задачу
                answers, symbol = User_formulas.equation_solver(
                    ['U1 / I1'],
                    {'U1': (1, 100), 'I1': (1, 100)}, normal_check=True, after_point=5,
                    exception=['0'])

                self.solve.append(f'2) Подставляем в формулу и получаем: ' + str(symbol['U1']) + '/' + str(
                    symbol['I1']) + ' = ' + str(answers[0]))

                self.answers.append(str(answers[0]))
                print(answers, self.answers, symbol)
                self.tasks.append('2) Найдите сопротивление лампы и напишите его, если сила тока в цепи ' + str(
                    symbol['I1']) + ' A, напряжение в цепи ' + str(symbol['U1']) + ' В')

                # Создаём третью задачу
                answers, symbol = User_formulas.equation_solver(
                    ['U1 / ((R1 * R2) / (R1 + R2))'],
                    {'U1': (1, 100), 'R1': (1, 220), 'R2': (1, 220)}, normal_check=True, after_point=5,
                    exception=['0'])

                self.solve.append(
                    f'3) Для расчёта нам нужна формула расчёта сопротивления двух параллельных резисторов: ((R1 * R2) / (R1 + R2)).\nСопротивление подставляем в закон ома и получим формулу: U / ((R1 * R2) / (R1 + R2)) = ' + str(
                        answers[0]))

                self.answers.append(str(answers[0]))
                print(answers, self.answers, symbol)
                self.tasks.append('3) Найдите силу тока в цепи и напишите её, если напряжение равно ' + str(
                    symbol['U1']) + ' В, и два резистора параллельного подключения ' + str(symbol['R1']) + ' и ' + str(
                    symbol['R2']) + ' Ом')

        # Получаем hash
        self.program_hash = User_formulas.get_hash()

    @staticmethod
    def get_subject():
        return 'phys'


# Вывод функций выводящий подробные действия решения и помогающие программе
class UserFormulas:
    def __init__(self, user_nums: list):
        self.program_hash = Hash()
        self.user_nums = user_nums  # Числа, который нужны при создании тестов, от пользователя

    # Функция для вычисления уравнений
    def equation_solver(self, eqs, ranges, normal_check=False, after_point=4, round_check=False,
                        exception: list[str] = (), not_in_exc: list[str] = ()):
        while True:
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

                # Проверяем расшифровку hash от пользователя
                if self.user_nums:
                    user_numbers = self.user_nums[0].split()  # Разделяем числа пользователя
                    if len(numbers) + len(dop_vars) == len(user_numbers):
                        for ind, num in enumerate(user_numbers):
                            # Проверяем, что индекс не выходит за пределы ranges
                            if ind > len(ranges):
                                print(f"Ошибка: индекс {ind} выходит за пределы ranges.")
                                self.user_nums = ''
                                break

                            # Проверяем, является ли num числом
                            try:
                                num = int(num)  # Пробуем преобразовать в число
                            except ValueError:
                                # Если num не является числом, пропускаем проверку диапазона
                                continue

                            # Получаем диапазон и проверяем число
                            range_values = list(ranges.values())
                            if ind < len(range_values):
                                start, stop = range_values[ind]
                                if num > stop or num < start:  # Включаем верхнюю границу
                                    self.user_nums = ''
                                    break
                        # Если все числа прошли проверку, обновляем numbers и dop_vars
                        if self.user_nums:
                            numbers = update_dicts_with_array(numbers, user_numbers)
                        else:
                            self.user_nums = ''
                    else:
                        self.user_nums = ''

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

                # Проверяем, что коэффициенты не в исключении и это не коэффициент который в него не попадает
                if exception:
                    num_for_exs = []
                    for exc in numbers:
                        if exc in not_in_exc:
                            pass
                        else:
                            num_for_exs.append(numbers.get(exc))
                    for number in num_for_exs:
                        if number in exception:
                            if self.user_nums:
                                self.user_nums = ''
                            continue
                # Округляем числа если это нужно
                if round_check:
                    results = UserFormulas.round_nums(results, after_point)

                # Проверяем что числа в нужном диапазоне (до n знаков после запятой).
                if normal_check:
                    if len(results) == len(equations):
                        if UserFormulas.normal(results, after_point):
                            # Сохраняем числа для hash.
                            self.program_hash.add(list(map(int, numbers.values())))
                            if self.user_nums:
                                self.user_nums = self.user_nums[1:]

                            # Возвращаем результат
                            return results, numbers
                        else:
                            if self.user_nums:
                                self.user_nums = ''
                    else:
                        if self.user_nums:
                            self.user_nums = ''
                else:
                    if any(results):
                        # Сохраняем числа для hash.
                        self.program_hash.add(list(map(int, numbers.values())))
                        if self.user_nums:
                            self.user_nums = self.user_nums[1:]

                        # Возвращаем результат
                        return results, numbers
                    else:
                        if self.user_nums:
                            self.user_nums = ''

                # Удаляем результаты
                results.clear()

    # Функция для получения hash-a
    def get_hash(self):
        return self.program_hash.show()

    # Проверка, что у чисел не больше after_point знаков после запятой
    @staticmethod
    def normal(nums, after_point):
        # Регулярное выражение для проверки числа с не более чем n цифрами после запятой
        if after_point == 0:
            pattern = False
        else:
            pattern = r'^\d+(\.\d{1,' + str(after_point) + '})?$'

        # Проверяем все числа на нормальность
        res = []
        if pattern:
            for num in nums:
                num = abs(num)
                res.append(bool(re.match(pattern, str(num))))
        else:
            for num in nums:
                res.append(num.is_integer())

        # Выводим ответ после проверки всех чисел
        return all(res)

    # Округление числа до указанного значения
    @staticmethod
    def round_nums(nums, digits):
        res = []
        for num in nums:
            res.append(round(num, digits))

        return res

    # Функция заменяющая все символы на цифры в уравнении
    @staticmethod
    def show_task_eq(equation, **symbol):
        # Заменяем указатели на значения из symbols
        for key, value in symbol.items():
            # Делаем значение - числом
            value = int(value)
            # Определяем знак для значения
            sign = '+' if value >= 0 else '-'
            # Форматируем строку с пробелом перед знаком
            equation = equation.replace(key, f"{sign} {abs(value)}")

        # Убираем лишний пробел перед первым знаком, если он есть
        equation = equation.replace(' + ', ' + ').replace(' - ', ' - ')

        return equation

    # Функция для создания текста для решения
    @staticmethod
    def create_solve_txt(num: int, eq: str, explanation: list, activity: list, answer: list, sign="="):
        solve_txt = ''

        # Подставляем номер задачи
        solve_txt += f'Задача №{num}: {eq}\n'
        # Подставляем значения и сохраняем текст
        for ind in range(len(explanation)):
            if "=" in activity[ind]:
                solve_txt += f'{ind + 1}) {explanation[ind]}: {activity[ind][:activity[ind].index("=")]} {sign} {answer[ind]}.\n'
            else:
                solve_txt += f'{ind + 1}) {explanation[ind]}: {activity[ind]} {sign} {answer[ind]}.\n'

        # Возвращаем текст
        return solve_txt


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
            return "Вашей статистики на этот тест нет."
        elif subject not in ('math', 'математика', 'physics', 'физика', 'phys'):
            return "Неизвестное сообщение или неправильный ввод."
        else:
            # Преобразуем предмет для его вывода
            if subject in ('math', 'математика'):
                subject = "math"
            elif subject in ('physics', 'физика', 'phys'):
                subject = "physics"

            # Получаем статистику
            result = data.get(str(user_id), {}).get(subject, {}).get(test_name)
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
    def add_statistics(point: int, subject: str, user_id: str, name: str):
        # Меняем id на строчку
        user_id = str(user_id)

        # Путь к JSON-файлу
        file_path = "files\\data.json"

        # Чтение JSON-файла
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Добавление данных
        if user_id not in data:
            data[user_id] = {}  # Создаём запись для пользователя, если её нет

        if subject not in data[user_id]:
            data[user_id][subject] = {}  # Создаём запись для предмета, если её нет

        if name not in data[user_id][subject]:
            data[user_id][subject][name] = []  # Создаём запись для теста, если её нет

        # Добавляем новое значение
        data[user_id][subject][name].append(point)

        # Запись обновлённых данных обратно в JSON-файл
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


""" Команды бота и ответы на них """


# Вывод при команде старт
@Bot.message_handler(commands=['start'])
def start(message):
    # Вывод описания и кнопок
    Bot.send_message(message.chat.id,
                     'Здравствуйте! Вы обратились к чат-боту с тестами. Я чат-бот для подготовки к тестам. Имеющий автоматическое создание примеров на тему теста. Чтобы узнать мой функционал, напишите "/help".\nЧтобы узнать какие есть тесты напишите /tests.',
                     reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))


# Вывод информации для помощи пользователю
@Bot.message_handler(commands=['help'])
def help_for_user(message):
    # Вывод при команде help и таблица команд
    COMMANDS_FOR_USER_HELP = [
        ['Команда и то что она попросит', 'Что делает команда.', 'Параметры (если есть).'],
        ['/start', 'Выдаёт краткое описание бота и предметы по которым можно выбрать тест.', '-'],
        ['/help', 'Выдаёт список всех команд чат-бота и как правильно вводить ответы на задачу.', '-'],
        ['/tests subject', 'просмотр тем тестов.',
         'subject - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
        ['/start_test subject name ', 'начать решение теста.',
         'name - Название теста или его номер; subject - Выбор предмета из возможных (math, математика; physics, физика, phys).'],
        ['/test_statistics subject name	',
         'выводит статистику теста (Количество попыток, средний балл, лучший балл, баллы на первой попытке, баллы на последней попытке).',
         'name - Название теста или его номер; subject - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
        ['/answer task answer или /an task answer', 'Дать ответ после начала решения.',
         'task - Номер задачи в тесте; answer - ответ на задачу (правила записи ответа выводятся при вводе команды /help).'],
        ['/end', 'заканчивает тест', '-', ],
        ['/find subject name', 'Находит топ-5 похожих тестов по строке',
         'subject - Выбор предмета из возможных (math, математика; physics, физика, phys); name - строка, по которой вы ищете тест']]

    # Создание таблицы для вывода информации
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

    # Ссылка и переход для гит-хаба
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт гит-хаба", url='https://github.com/aip-python-tech-2024/works-Boldaev')
    markup.add(button1)
    Bot.send_message(message.chat.id,
                     'Ссылка-описание на гит хабе: https://github.com/aip-python-tech-2024/works-Boldaev',
                     reply_markup=markup)

    # Вывод таблицы команд для пользователя
    Bot.send_message(message.chat.id,
                     'Таблица команд и данных которая она будет спрашивать в дальнейшем.\nКоманды которые нужно посылать программе:')
    Bot.send_message(message.chat.id, f"```\n{table_str}```", parse_mode='MarkdownV2')

    # Вывод правил ввода ответов
    Bot.send_message(message.chat.id,
                     'Правила ввода ответов:\nВ основном все вопросы выбираются на кнопках или вводятся если их нет.\nЕсли кнопки не появились, то проверьте есть ли справа от места ввода сообщения квадрат с 4-я кружочками. Если да, то нажмите на него и появятся кнопки.\nЕсли их нет, то введите команду /start или /help для их появления, если чат-бот не спрашивает о том, что нужно вводить.\nЕсли чат-бот просит ввести, то можно вводить сообщения больше чем одно слово.',
                     reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))


# Вывод возможных тестов
user_test_indexes = {}  # Хранение индекса на котором остановился человек


@Bot.message_handler(commands=['tests'])
def show_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 1, user_command='/tests', strict=True)

    # Проверка, что сообщение правильное
    if not isinstance(user_message, bool):
        # Вывод сообщения и ожидания предмета
        Bot.send_message(message.chat.id, 'Введите предмет (математика, физика)',
                         reply_markup=easy_markup("Математика", "Физика"))

        Bot.register_next_step_handler(message, get_subject_and_show_tests)
    else:
        Bot.send_message(message.chat.id,
                         'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /tests.\nКоманда для помощи: "/help".',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))


def get_subject_and_show_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 1, strict=True)

    # Проверка, что сообщение правильное
    if not isinstance(user_message, bool):

        # Проверка, что предметы в нужном диапазоне
        if user_message[0] not in SUBJECTS:
            Bot.send_message(message.chat.id,
                             f'Такого предмета пока нет. Выберите предмет на кнопке или из списка при следующей попытке: {SUBJECTS}',
                             reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                      "/start_test"))
            return False

        user_answer = Statistics.get_tests(user_message)
    else:
        user_answer = 'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /tests.\nКоманда для помощи: "/help".'

    # Получение результата в зависимости от ответа
    if user_answer == 'Неизвестное сообщение или неправильный ввод.' or user_answer == 'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /tests.\nКоманда для помощи: "/help".':
        Bot.send_message(message.chat.id, user_answer,
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False
    elif len(user_answer) >= 20:
        Bot.send_message(message.chat.id, array_for_message(user_answer,
                                                            omissions="index") + "\nНапишите /next для вывода тестов дальше.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
    else:
        Bot.send_message(message.chat.id, array_for_message(user_answer, omissions="index"),
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))

        Bot.send_message(message.chat.id,
                         "Если вы хотите начать тест по этому предмету, то сейчас введите его номер или название.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))

        Bot.register_next_step_handler(message, check_for_easy_start_test, user_message[0])

    # Сохраняем человека, для продолжения просмотра тестов
    if message.chat.id not in user_test_indexes.keys():
        user_test_indexes[message.chat.id] = [0, user_message]


# Функция для продолжения просмотра тестов
@Bot.message_handler(commands=['next'])
def next_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 1, user_command='/next', strict=True)

    if not user_message:
        Bot.send_message(message.chat.id,
                         'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /next.\nКоманда для помощи: "/help".',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    # Сохраняем и добавляем просмотр к человеку
    if message.chat.id not in user_test_indexes.keys():
        Bot.send_message(message.chat.id,
                         "Напишите команду '/tests', чтобы программа поняла предмет который вам нужен.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False
    else:
        user_test_indexes[message.chat.id][0] += 20

    # Выводим человеку тесты
    user_answer = Statistics.get_tests(user_test_indexes[message.chat.id][1])
    user_answer = array_for_message(user_answer, omissions="index", start_ind=user_test_indexes[message.chat.id][0],
                                    end=user_test_indexes[message.chat.id][0] + 20)

    if len(user_answer.split()) // 2 >= 20:
        Bot.send_message(message.chat.id, user_answer + "\nНапишите /next для вывода тестов дальше.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
    elif 0 < len(user_answer.split()) // 2 < 20:
        Bot.send_message(message.chat.id, user_answer,
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
    else:
        Bot.send_message(message.chat.id,
                         "Вы просмотрели все тесты, если вам нужно начать сначала, то снова напишите команду '/tests'.")

        # Проверка, что человек смотрел больше 20 тестов
        if len(user_answer.split()) >= 20:
            Bot.send_message(message.chat.id,
                             "Если вы хотите начать тест по этому предмету, то сейчас введите его номер или название.",
                             reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))
            subject = user_test_indexes[message.chat.id][1]

            del user_test_indexes[message.chat.id]

            Bot.register_next_step_handler(message, check_for_easy_start_test, subject)

        del user_test_indexes[message.chat.id]


# Проверка, что пользователь решил ввести число
def check_for_easy_start_test(message, subject):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 0)
    if not message_text:
        return False

    message_text = message_text[0]  # Оставляем только сообщение
    if message_text == '/start':
        start(message)
    elif message_text == '/help':
        help_for_user(message)
    elif message_text == '/tests':
        show_tests(message)
    elif message_text == '/next':
        next_tests(message)
    elif message_text == '/test_statistics':
        show_statistics(message)
    elif message_text == '/find':
        find_similar(message)
    elif message_text == '/start_test':
        start_test(message)
    else:
        get_ind_for_start_test(message, [subject])


# Вывод статистики
@Bot.message_handler(commands=['test_statistics'])
def show_statistics(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 1, user_command='/test_statistics', strict=True)

    # Выводим сообщение
    if message_text:
        Bot.send_message(message.chat.id, 'Введите предмет (математика, физика)',
                         reply_markup=easy_markup("Математика", "Физика"))

        Bot.register_next_step_handler(message, get_subject_for_show_statistics)
    else:
        Bot.send_message(message.chat.id,
                         'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /test_statistics.\nКоманда для помощи: "/help".',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))


def get_subject_for_show_statistics(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 1, strict=True)

    if message_text:
        # Проверка, что предметы в нужном диапазоне
        if message_text[0] not in SUBJECTS:
            Bot.send_message(message.chat.id,
                             f'Такого предмета пока нет. Выберите предмет на кнопке или из списка при следующей попытке: {SUBJECTS}',
                             reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                      "/start_test"))
            return False

        Bot.send_message(message.chat.id, 'Введите номер или название теста',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод. \nВозможно вы хотели ввести: /test_statistics.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    Bot.register_next_step_handler(message, get_index_of_test_for_show_statistics, message_text)


def get_index_of_test_for_show_statistics(message, subject):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 0)

    # Соединяем в сообщение
    if not isinstance(message_text, bool):
        message_text = subject + message_text

    # Получаем статистику
    if message_text:
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

        Bot.send_message(message.chat.id, statistics,
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
    else:
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод. \nВозможно вы хотели ввести: /test_statistics.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))


@Bot.message_handler(commands=['find'])
def find_similar(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 1, user_command='/find', strict=True)

    if isinstance(message_text, bool):
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /find subject name.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    # Спрашиваем предмет
    Bot.send_message(message.chat.id, f'Выберите предмет на кнопке или напишите из списка: {SUBJECTS}.',
                     reply_markup=easy_markup("Математика", "Физика"))

    # Ждём предмет
    Bot.register_next_step_handler(message, get_subject_to_find_similar)


def get_subject_to_find_similar(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 1, strict=True)

    # Проверяем что правильный вывод
    if isinstance(message_text, bool):
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /find.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    # Проверка, что предметы в нужном диапазоне
    if message_text[0] not in SUBJECTS:
        Bot.send_message(message.chat.id,
                         f'Такого предмета пока нет. Выберите предмет на кнопке или из списка при следующей попытке: {SUBJECTS}',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    # Спрашиваем текст
    Bot.send_message(message.chat.id, 'Введите текст для поиска.',
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    # Ждём текст
    Bot.register_next_step_handler(message, get_text_to_find_similar, message_text)


def get_text_to_find_similar(message, get_subject):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 0)

    # Проверяем то правильный вывод
    if isinstance(message_text, bool):
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /find.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    # Доделываем сообщение
    message_text = get_subject + message_text

    # Находим топ-5 похожих слов
    try:
        similar = find_similar_words(message_text[0], ' '.join(message_text[1:]))
    except UnboundLocalError:
        Bot.send_message(message.chat.id, "Ваша строка некорректна",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    # Проверка, что мы получили массив слов
    if not isinstance(similar, str):
        similar = array_for_message(similar)

    Bot.send_message(message.chat.id, 'топ-5 похожих тестов по запросу:\n' + similar,
                     reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))


# Функция для начала тестов
user_tests = {}  # Словарь для сохранения тестов


@Bot.message_handler(commands=['start_test'])
def start_test(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 1, user_command='/start_test', strict=True)

    # Проверяем что правильное сообщение
    if isinstance(message_text, bool):
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /start_test subject name.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    Bot.send_message(message.chat.id, 'Введите предмет (математика/физика)',
                     reply_markup=easy_markup('Математика', 'Физика'))

    Bot.register_next_step_handler(message, get_subject_for_start_test)


def get_subject_for_start_test(message):
    # Сохраняем предмет для создания теста под предмет
    global subject

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 1, strict=True)

    if isinstance(message_text, bool) or message_text[0] not in SUBJECTS:
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /start_test.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    if message_text[0] in MATH_SUB:
        subject = 'math'
    elif message_text[0] in PHYS_SUB:
        subject = 'phys'
    else:
        return False

    Bot.send_message(message.chat.id, 'Введите название или номер задачи (задачи можно узнать по команде /tests)',
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    Bot.register_next_step_handler(message, get_ind_for_start_test, message_text)


def get_ind_for_start_test(message, get_subject):
    # Сохраняем предмет для создания теста под предмет
    global subject

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 0)

    # Сохраняем предмет пользователя
    if get_subject[0] in MATH_SUB:
        subject = 'math'
    elif get_subject[0] in PHYS_SUB:
        subject = 'phys'
    else:
        return False

    if message_text == ['/tests']:
        Bot.send_message(message.chat.id, 'Прохождение теста окончено, напишите команду /tests снова',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    if isinstance(message_text, bool):
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /start_test.\nКоманда для помощи: '/help'.",
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return False

    message_text = get_subject + message_text

    # Проверяем что есть такой тест по его названию или индексу
    if message_text[1].isdigit():
        test_name = Statistics.find_name(message_text[0], int(message_text[1]))
        if test_name is None:
            Bot.send_message(message.chat.id, 'Такого номера теста нет.',
                             reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                      "/start_test"))
        else:
            Bot.send_message(message.chat.id, f"Вы хотите начать тест по имени: '{test_name}'? (да/нет; yes/no; y/n)",
                             reply_markup=easy_markup('Да', 'Нет'))
            user_tests[message.chat.id] = test_name

            Bot.register_next_step_handler(message, check_for_start)
    else:
        test_name = ' '.join(message_text[1:])
        if test_name in Statistics.get_tests(message_text):
            Bot.send_message(message.chat.id, f"Вы хотите начать тест по имени: '{test_name}'? (да/нет; yes/no; y/n)",
                             reply_markup=easy_markup('Да', 'Нет'))
            user_tests[message.chat.id] = test_name

            Bot.register_next_step_handler(message, check_for_start)
        else:
            Bot.send_message(message.chat.id, Statistics.get_tests(message_text[0]),
                             reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                      "/start_test"))


def check_for_start(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    if check_message(message, 1, strict=True):
        message_text += check_message(message, 1, strict=True)
    else:
        message_text = [False]

    # Проверяем ответ
    if message_text[0] in ('да', 'yes', 'y'):
        Bot.send_message(message.chat.id, 'Вы хотите получить решение? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, check_for_solve)
    elif message_text[0] in ('нет', 'no', 'n'):
        Bot.send_message(message.chat.id, 'Тест не начался.',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        del user_tests[message.chat.id]
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        del user_tests[message.chat.id]

        # Очищаем следующий шаг
        Bot.clear_step_handler_by_chat_id(message.chat.id)
        return True
    else:
        Bot.send_message(message.chat.id,
                         'Некорректный ввод, будет считаться что вы ввели "нет".',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        del user_tests[message.chat.id]


# Данные которые нужны для создания теста
need_for_create_solve = False
user_hash = ''
subject = ''


def check_for_solve(message):
    # Подключаем глобальные переменные
    global need_for_create_solve
    global user_hash

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    if check_message(message, 1, strict=True):
        message_text += check_message(message, 1, strict=True)
    else:
        message_text = [False]

    # Проверяем ответ
    if message_text[0] in ('да', 'yes', 'y'):
        need_for_create_solve = True
        Bot.send_message(message.chat.id, 'Хорошо, мы сделаем решение.\nУ вас есть хэш? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, ask_for_hash)
    elif message_text[0] in ('нет', 'no', 'n'):
        Bot.send_message(message.chat.id, 'Решение теста не будет.\nУ вас есть хэш? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, ask_for_hash)
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        del user_tests[message.chat.id]

        # Очищаем следующий шаг
        Bot.clear_step_handler_by_chat_id(message.chat.id)
        return True
    else:
        Bot.send_message(message.chat.id,
                         'Некорректный ввод, будет считаться что вы ввели "нет".\nУ вас есть хэш? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, get_hash_and_start_test)


def ask_for_hash(message):
    # Подключаем глобальные переменные
    global need_for_create_solve
    global user_hash

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    if check_message(message, 1, strict=True):
        message_text += check_message(message, 1, strict=True)
    else:
        message_text = [False]

    # Проверяем ответ
    if message_text[0] in ('да', 'yes', 'y'):
        need_for_create_solve = True
        Bot.send_message(message.chat.id, 'Введите hash.', reply_markup=telebot.types.ReplyKeyboardRemove())
        Bot.register_next_step_handler(message, get_hash)
    elif message_text[0] in ('нет', 'no', 'n'):
        get_hash_and_start_test(message)
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        del user_tests[message.chat.id]

        # Очищаем следующий шаг
        Bot.clear_step_handler_by_chat_id(message.chat.id)
        return True
    else:
        get_hash_and_start_test(message)


def get_hash(message):
    # Подключаем глобальные переменные
    global need_for_create_solve
    global user_hash

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    if check_message(message, 1, strict=True, none_lower=True):
        message_text += check_message(message, 1, strict=True, none_lower=True)
    else:
        message_text = [False]

    # Сохраняем hash
    if message_text[0]:
        user_hash = message_text[0]
    else:
        user_hash = []

    get_hash_and_start_test(message)


def get_hash_and_start_test(message):
    # Подключаем глобальные переменные
    global need_for_create_solve
    global user_hash

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    if check_message(message, 1, strict=True, none_lower=True):
        message_text += check_message(message, 1, strict=True, none_lower=True)
    else:
        message_text = [False]

    if message_text[-1] == '.':
        message_text = message_text[:-1]

    # Проверяем ответ
    if user_hash:
        Bot.send_message(message.chat.id, 'Тест начат, ваш хэш принят.\nНачалось создание теста...')
        create_test(message, need_for_create_solve, user_hash=user_hash)
    elif message_text[0] in ('нет', 'no', 'n', 'Нет', 'НЕТ', 'No', 'NO', 'N', 'Н'):
        Bot.send_message(message.chat.id, 'Началось создание теста...')
        create_test(message, need_for_create_solve)
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        del user_tests[message.chat.id]

        # Очищаем следующий шаг
        Bot.clear_step_handler_by_chat_id(message.chat.id)
        return True
    else:
        Bot.send_message(message.chat.id,
                         'Некорректный ввод, будет считаться что вы ввели "нет" или ваш hash недействителен.')
        create_test(message, need_for_create_solve)


check = 0


def create_test(message, need_solve: bool, user_hash=''):
    # Подключаем переменную для проверки
    global check
    global subject

    # Добавляем класс теста к человеку
    if subject in MATH_SUB:
        user_tests[message.chat.id] = Math(user_tests[message.chat.id], need_solve, user_hash)
    elif subject in PHYS_SUB:
        user_tests[message.chat.id] = Phys(user_tests[message.chat.id], need_solve, user_hash)
    else:
        return False

    # Создаём тест
    user_tests[message.chat.id].create_test()

    # Выводим правила ввода ответов
    Bot.send_message(message.chat.id,
                     'Правила ввода ответов:\nВ основном все вопросы выбираются на кнопках или вводятся если их нет.\nЕсли кнопки не появились, то проверьте есть ли справа от места ввода сообщения квадрат с 4-я кружочками. Если да, то нажмите на него и появятся кнопки.\nЕсли их нет, то введите команду /start или /help для их появления, если чат-бот не спрашивает о том, что нужно вводить.\nЕсли чат-бот просит ввести, то можно вводить сообщения больше чем одно слово.')

    # Выводим hash с HTML-разметкой
    Bot.send_message(
        message.chat.id,
        f"Hash для повторного прохождения теста: `{user_tests[message.chat.id].show_hash()}`",
        parse_mode="MARKDOWN")

    # Выводим тест
    tasks_txt, check = user_tests[message.chat.id].show_test()
    Bot.send_message(message.chat.id, tasks_txt, reply_markup=easy_markup('/answer', '/end', '/help'))

    # Заходим в петлю проверки ответов
    Bot.register_next_step_handler(message, save_answers)


def save_answers(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения и собираем сообщение
    message_text = check_message(message, 1, user_command='/answer', strict=True)
    if check_message(message, 1, user_command='/an', strict=True) or message_text:
        Bot.send_message(message.chat.id, 'Введите номер задачи.', reply_markup=telebot.types.ReplyKeyboardRemove())

        Bot.register_next_step_handler(message, get_num_of_task_for_save_answer)
    elif check_message(message, 1, user_command='/end', strict=True):
        message_text = ['/end']
        check_message_text(message, message_text)
    elif check_message(message, 1, user_command='/help', strict=True):
        message_text = ['/help']
        check_message_text(message, message_text)
    elif not any([message_text]):
        message_text = [False]
        check_message_text(message, message_text)
    elif isinstance(message_text, bool):
        message_text = [False]
        check_message_text(message, message_text)


def get_num_of_task_for_save_answer(message):
    message_text = check_message(message, 1, strict=True)

    if isinstance(message_text, bool):
        message_text = [False]
        check_message_text(message, message_text)

    Bot.send_message(message.chat.id, 'Введите ваш ответ.', reply_markup=telebot.types.ReplyKeyboardRemove())

    Bot.register_next_step_handler(message, get_answer_for_task_for_save_answer, message_text)


def get_answer_for_task_for_save_answer(message, num):
    message_text = check_message(message, 0, answer=True)

    if isinstance(message_text, bool):
        message_text = [False]
        check_message_text(message, message_text)

    message_text[0] = message_text[0].replace(',', '.')

    check_message_text(message, num + message_text)


def check_message_text(message, message_text):
    # Переменная для проверки
    global check

    # Проверка сообщения
    if message_text[0] == '/end':
        show_results(message)
    elif message_text[0] == '/help':
        help_for_user(message)
        Bot.send_message(message.chat.id,
                         'Продолжайте решать задачи по команде /answer. Для выхода из задач введите /end.',
                         reply_markup=easy_markup('/answer', '/end', '/help'))
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)
    elif isinstance(message_text[0], int):
        Bot.send_message(message.chat.id,
                         "Вы некорректно ввели ответ. Формат ответа: /answer.\nЧтобы закончить тест введите '/end'.",
                         reply_markup=easy_markup('/answer', '/end', '/help'))
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)
    elif int(message_text[0]) <= int(check):
        user_tests[message.chat.id].add_answer(check, int(message_text[0]), message_text[1])
        Bot.send_message(message.chat.id, f"Ответ {message_text[1]} на {message_text[0]} вопрос: принят.",
                         reply_markup=easy_markup('/answer', '/end', '/help'))
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)
    else:
        Bot.send_message(message.chat.id,
                         "Вы некорректно ввели ответ. Формат ответа: /answer.\nЧтобы закончить тест введите '/end'.",
                         reply_markup=easy_markup('/answer', '/end', '/help'))
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)


def show_results(message):
    # Очищаем следующий шаг
    Bot.clear_step_handler_by_chat_id(message.chat.id)

    if len(user_tests[message.chat.id].user_answers) == 0:
        Bot.send_message(message.chat.id, 'Вы не дали ни одного ответа, результат теста не будет засчитан.',
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))
        return True
    else:
        # Выводим решения (если нужно)
        solve = user_tests[message.chat.id].show_solve()
        if solve:
            Bot.send_message(message.chat.id, solve)

        # Выводим проверку ответов
        Bot.send_message(message.chat.id, user_tests[message.chat.id].check_answers(),
                         reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find",
                                                  "/start_test"))

        # Выводим статистику
        Statistics.add_statistics(user_tests[message.chat.id].get_point(), user_tests[message.chat.id].get_subject(),
                                  message.chat.id,
                                  user_tests[message.chat.id].name_test)

    # Удаляем человека из памяти
    del user_tests[message.chat.id]

    return True


# Ответ на все неизвестные собщения
@Bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    Bot.send_message(message.chat.id,
                     'Такой команды у бота нет, для помощи введите команду /help или выберите на кнопке!',
                     reply_markup=easy_markup("/help", "/tests", "/next", "/test_statistics", "/find", "/start_test"))


# testiki
taps = {}


@Bot.message_handler(commands=['testiki'])
def nothing(message):
    if not taps.get(str(message.chat.id), False):
        msg = Bot.send_message(message.chat.id, 'Счётчик: 0')

        from time import sleep
        for i in range(1, 11):
            Bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=str(i))
            sleep(1)

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
