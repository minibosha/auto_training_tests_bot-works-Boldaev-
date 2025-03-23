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

""" Подгрузка токена бота и его создание """
load_dotenv()
token = getenv('token')

# Создание бота
Bot = telebot.TeleBot(token, parse_mode=None)

""" Функции """


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
def check_message(command, n, user_command=None, strict=False, none_lower=False):
    # Убираем частые ошибки в сообщениях (точки и регистр)
    user_object = command.text
    user_object = user_object.replace('.', '')
    if none_lower:
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

        # Добавляем запятые в конец строк
        for ind in range(len(unencrypted_str)):
            unencrypted_str[ind] += ' ,'

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


# Класс для тестов по математике
class Math:
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
                answers, symbol = User_formulas.equation_solver(["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"], {'a': (1, 1), 'b': (-20, 20), 'c': (-20, 20)}, normal_check=True, after_point=0)

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
                self.tasks.append(f'1) Решите полное приведённое квадратное уравнение: {other}. В ответ введите корни в порядке возрастания без пробелов (минусы и нули учитываются).\n')

                # 2. Полное квадратное уравнение.
                # Создаём уравнение
                equations = ["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"]
                answers, symbol = User_formulas.equation_solver(["b^2-4*a*c=D", "((-b) - sqrt(D)) / (2*a)", "((-b) + sqrt(D)) / (2*a)"], {'a': (-20, 20), 'b': (-20, 20), 'c': (-20, 20)}, normal_check=True, after_point=0, exception=['-1', '0', '1'], not_in_exc=('D',))

                # Создаём полное уравнение
                other = UserFormulas.show_task_eq("ax^2 bx c", a=symbol["a"], b=symbol["b"], c=symbol["c"]) + ' = 0'

                # Проверяем что дискриминант не ноль
                if answers[0]:
                    self.solve.append(UserFormulas.create_solve_txt(2, other, ['Находим дискриминант, т.к. дискриминант больше нуля => 2 корня', 'Вычисляем первый корень', 'Вычисляем второй корень'], equations, answers))
                else:
                    self.solve.append(UserFormulas.create_solve_txt(2, other, ['Находим дискриминант, т.к. дискриминант равен нулю => 1 корень', 'Вычисляем корень'], equations[:-1], answers))

                # Добавляем ответ
                equations = sorted(answers[1:])
                answers = ''
                for an in equations:
                    answers += str(int(an))
                self.answers.append(answers)

                # Создаём первый вопрос
                self.tasks.append(f'2) Решите полное квадратное уравнение: {other}. В ответ введите ответ введите корни возрастания без пробелов (минусы и нули учитываются).')
            case "сложение":
                # Создаём три простых задачи и добавляем нужное по ним
                self.solve.append('Чтобы найти ответ нужно сложить два числа, чтобы это сделать воспользуйтесь калькулятором. Делается в одно действие')

                for ind in range(3):
                    answers, symbol = User_formulas.equation_solver(['a + b'], {'a': (0, 100), 'b': (0, 100)}, normal_check=True, after_point=0)
                    equations.append(UserFormulas.show_task_eq('a b', a=symbol["a"], b=symbol["b"])[2:])
                    self.answers.append(str(int(sum(answers))))

                self.tasks.append(f'Решите три примера:\n1. {equations[0]}\n2. {equations[1]}\n3. {equations[2]}')

        # Получаем hash
        self.program_hash = User_formulas.get_hash()
        print(self.program_hash)

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


# Вывод функций выводящий подробные действия решения и помогающие программе
class UserFormulas:
    def __init__(self, user_nums: list):
        self.program_hash = Hash()
        self.user_nums = user_nums  # Числа, который нужны при создании тестов, от пользователя

    # Функция для вычисления уравнений
    def equation_solver(self, eqs, ranges, normal_check=False, after_point=4, round_check=False, exception: list[str] = (), not_in_exc: list[str] = ()):
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

                print(numbers, self.user_nums)
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
                                print(ranges.values(), start, stop + 1, list(range(start, stop + 1)), num, num not in range(start, stop + 1))  # Добавляем 1 к stop
                                if num not in range(start, stop + 1):  # Включаем верхнюю границу
                                    self.user_nums = ''
                                    break
                        # Если все числа прошли проверку, обновляем numbers и dop_vars
                        numbers = update_dicts_with_array(numbers, user_numbers)
                    else:
                        self.user_nums = ''
                        continue

                print(numbers, dop_vars)
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
                    if any(results):
                        # Сохраняем числа для hash.
                        self.program_hash.add(list(map(int, numbers.values())))
                        if self.user_nums:
                            self.user_nums = self.user_nums[1:]

                        # Возвращаем результат
                        return results, numbers

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
        ['/tests subject', 'просмотр тем тестов.',
         'subject - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
        ['/start_test name subject', 'начать решение теста.',
         'name - Название теста или его номер; subject - Выбор предмета из возможных (math, математика; physics, физика, phys).'],
        ['/test_statistics subject name	',
         'выводит статистику теста (Количество попыток, средний балл, лучший балл, баллы на первой попытке, баллы на последней попытке).',
         'name - Название теста или его номер; subject - Выбор предмета из возможных (math, математика; physics, физика, phys)'],
        ['/answer task answer или /an task answer', 'Дать ответ после начала решения.',
         'task - Номер задачи в тесте; answer - ответ на задачу (правила записи ответа выводятся при вводе команды /help).'],
        ['/end', 'заканчивает тест', '-', ],
        ['/find subject name', 'Находит топ-5 похожих тестов по строке',
         'subject - Выбор предмета из возможных (math, математика; physics, физика, phys); name - строка, по которой вы ищете тест']]

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

    Bot.send_message(message.chat.id, 'Ссылка-описание на гит хабе: https://github.com/aip-python-tech-2024/works-Boldaev')

    Bot.send_message(message.chat.id, 'Команды которые нужно посылать программе:')
    Bot.send_message(message.chat.id, f"```\n{table_str}```", parse_mode='MarkdownV2')

    Bot.send_message(message.chat.id,
                     'Правила ввода ответов:\nВвод команд может показаться странным для многих пользователей.\nТакой стиль выбран специально для уменьшения вопросов от программы (предмет, номер, переспрашивание...).\nКак отправлять программе команды? Вот что нужно для этого: в таблице (показывается при команде "/help") указана команда и данные которые ей нужны (параметры). Данные вводятся после команды (/команда) через пробел в порядке указанном в таблице. Например: "/start"; "/start_test math 1"; "/an 1 -0-4"; "/find math полные квадратные уравнения".\nКогда просят ввести название (name) можно вводить его с пробелами.\nТакже хотелось упомянуть что пунктуация и точки исправляются (но не надо эти злоупотреблять!).\nЖелаем приятного пользования! Советуем посмотреть пример разговора (на гитхабе, посмотреть можно при команде "/help") для более понятного понимания возможностей программы и правильного разговора с ней.')


# Вывод возможных тестов
user_test_indexes = {}  # Хранение индекса на котором остановился человек


@Bot.message_handler(commands=['tests'])
def show_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 2, user_command='/tests', strict=True)

    # Проверка, что сообщение правильное
    if not isinstance(user_message, bool):
        user_answer = Statistics.get_tests(user_message)
    else:
        user_answer = 'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /tests subject.\nКоманда для помощи: "/help".'

    # Получение результата в зависимости от ответа
    if user_answer == 'Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /tests subject.\nКоманда для помощи: "/help".':
        Bot.send_message(message.chat.id, user_answer)
    elif len(user_answer) >= 20:
        Bot.send_message(message.chat.id, array_for_message(user_answer,
                                                            omissions="index") + "\nНапишите /next для вывода тестов дальше.")
    else:
        Bot.send_message(message.chat.id, array_for_message(user_answer, omissions="index"))

    # Сохраняем человека, для продолжения просмотра тестов
    if message.chat.id not in user_test_indexes.keys():
        user_test_indexes[message.chat.id] = [0, user_message]


# Функция для продолжения просмотра тестов
@Bot.message_handler(commands=['next'])
def next_tests(message):
    # Убираем факторы, которые могу быть причиной неизвестного сообщения
    user_message = check_message(message, 1, user_command='/next')

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
    message_text = check_message(message, 2, user_command='/test_statistics')

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

        Bot.send_message(message.chat.id, statistics)
    else:
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод. \nВозможно вы хотели ввести: /test_statistics subject name.\nКоманда для помощи: '/help'.")


@Bot.message_handler(commands=['find'])
def find_similar(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3, user_command='/find')

    if isinstance(message_text, bool):
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /find subject name.\nКоманда для помощи: '/help'.")
        return False

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
    message_text = check_message(message, 3, user_command='/start_test', strict=True)

    # Проверяем что правильное сообщение
    if isinstance(message_text, bool) or len(message_text) == 1:
        Bot.send_message(message.chat.id,
                         "Неизвестное сообщение или неправильный ввод.\nВозможно вы хотели ввести: /start_test subject name.\nКоманда для помощи: '/help'.")
        return False

    # Проверяем что есть такой тест по его названию или индексу
    if message_text[1].isdigit():
        test_name = Statistics.find_name(message_text[0], int(message_text[1]))
        if test_name is None:
            Bot.send_message(message.chat.id, 'Такого номера теста нет.')
        else:
            Bot.send_message(message.chat.id, f"Вы хотите начать тест по имени: '{test_name}'? (да/нет; yes/no; y/n)")
            user_tests[message.chat.id] = test_name

            Bot.register_next_step_handler(message, check_for_start)
    else:
        test_name = ' '.join(message_text[1:])
        if test_name in Statistics.get_tests(message_text):
            Bot.send_message(message.chat.id, f"Вы хотите начать тест по имени: '{test_name}'? (да/нет; yes/no; y/n)")
            user_tests[message.chat.id] = test_name

            Bot.register_next_step_handler(message, check_for_start)
        else:
            Bot.send_message(message.chat.id, Statistics.get_tests(message_text[0]))


def check_for_start(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    message_text += check_message(message, 1, strict=True)

    # Проверяем ответ
    if message_text[0] in ('да', 'yes', 'y'):
        Bot.send_message(message.chat.id, 'Вы хотите получить решение? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, check_for_solve)
    elif message_text[0] in ('нет', 'no', 'n'):
        Bot.send_message(message.chat.id, 'Тест не начался.')
        del user_tests[message.chat.id]
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.')
        del user_tests[message.chat.id]

        # Очищаем следующий шаг
        Bot.clear_step_handler_by_chat_id(message.chat.id)
        return True
    else:
        Bot.send_message(message.chat.id,
                         'Некорректный ввод, будет считаться что вы ввели "нет".')
        del user_tests[message.chat.id]


# Данные которые нужны для создания теста
need_for_create_solve = False
user_hash = ''


def check_for_solve(message):
    # Подключаем глобальные переменные
    global need_for_create_solve
    global user_hash

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    message_text += check_message(message, 1, strict=True)

    # Проверяем ответ
    if message_text[0] in ('да', 'yes', 'y'):
        need_for_create_solve = True
        Bot.send_message(message.chat.id, 'Хорошо, мы сделаем решение.\nУ вас есть хэш? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, ask_for_hash)
    elif message_text[0] in ('нет', 'no', 'n'):
        Bot.send_message(message.chat.id, 'Решение теста не будет.\nУ вас есть хэш? (да/нет; yes/no; y/n)')
        Bot.register_next_step_handler(message, ask_for_hash)
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.')
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
    message_text += check_message(message, 1, strict=True)

    # Проверяем ответ
    if message_text[0] in ('да', 'yes', 'y'):
        need_for_create_solve = True
        Bot.send_message(message.chat.id, 'Введите hash.')
        Bot.register_next_step_handler(message, get_hash)
    elif message_text[0] in ('нет', 'no', 'n'):
        get_hash_and_start_test(message)
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.')
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
    message_text += check_message(message, 1, strict=True, none_lower=False)

    # Сохраняем hash
    if message_text:
        user_hash = message_text[0]
    else:
        user_hash = []
    print(message_text, user_hash)

    get_hash_and_start_test(message)


def get_hash_and_start_test(message):
    # Подключаем глобальные переменные
    global need_for_create_solve
    global user_hash

    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = []
    message_text += check_message(message, 1, strict=True)

    # Проверяем ответ
    if user_hash:
        Bot.send_message(message.chat.id, 'Тест начат, ваш хэш принят.\nНачалось создание теста...')
        create_test(message, need_for_create_solve, user_hash=user_hash)
    elif message_text[0] in ('нет', 'no', 'n'):
        Bot.send_message(message.chat.id, 'Началось создание теста...')
        create_test(message, need_for_create_solve)
    elif message_text[0] == '/end':
        Bot.send_message(message.chat.id, 'Создание теста прекращено.')
        del user_tests[message.chat.id]

        # Очищаем следующий шаг
        Bot.clear_step_handler_by_chat_id(message.chat.id)
        return True
    else:
        Bot.send_message(message.chat.id, 'Некорректный ввод, будет считаться что вы ввели "нет".')
        create_test(message, need_for_create_solve)


noth = [0]  # Массив для сохранения проверки


def create_test(message, need_solve: bool, user_hash=''):
    # Добавляем класс теста к человеку
    user_tests[message.chat.id] = Math(user_tests[message.chat.id], need_solve, user_hash)

    # Создаём тест
    user_tests[message.chat.id].create_test()

    # Выводим hash
    Bot.send_message(message.chat.id, f'Hash для повторного прохождения теста: {user_tests[message.chat.id].show_hash()}')

    # Выводим правила ввода ответов
    Bot.send_message(message.chat.id, 'Можете начать отправлять ответы.\nПравила ввода ответов:\nВвод команд может показаться странным для многих пользователей.\nТакой стиль выбран специально для уменьшения вопросов от программы (предмет, номер, переспрашивание...).\nКак отправлять программе команды? Вот что нужно для этого: в таблице (показывается при команде "/help") указана команда и данные которые ей нужны (параметры). Данные вводятся после команды (/команда) через пробел в порядке указанном в таблице. Например: "/start"; "/start_test math 1"; "/an 1 -0-4"; "/find math полные квадратные уравнения".\nКогда просят ввести название (name) можно вводить его с пробелами.\nТакже хотелось упомянуть что пунктуация и точки исправляются (но не надо эти злоупотреблять!).\nЖелаем приятного пользования! Советуем посмотреть пример разговора (на гитхабе, посмотреть можно при команде "/help") для более понятного понимания возможностей программы и правильного разговора с ней.')

    # Выводим тест
    tasks_txt, noth[0] = user_tests[message.chat.id].show_test()
    Bot.send_message(message.chat.id, tasks_txt)

    # Заходим в петлю проверки ответов
    Bot.register_next_step_handler(message, save_answers)


def save_answers(message):
    # Убираем факторы, которые могут быть причиной неизвестного сообщения
    message_text = check_message(message, 3, user_command='/answer')
    if check_message(message, 3, user_command='/an'):
        message_text = check_message(message, 3, user_command='/an')
    elif check_message(message, 0, user_command='/end'):
        message_text = ['/end']
    elif check_message(message, 0, user_command='/help'):
        message_text = ['/help']
    elif not any([message_text]):
        message_text = [False]

    # Проверка сообщения
    if message_text[0] == '/end':
        show_results(message)
    elif message_text[0] == '/help':
        help_for_user(message)
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)
    elif isinstance(message_text[0], int):
        Bot.send_message(message.chat.id,
                         "Вы некорректно ввели ответ. Формат ответа: /an task answer.\nЧтобы закончить тест введите '/end'.")
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)
    elif int(message_text[0]) <= int(noth[0]):
        user_tests[message.chat.id].add_answer(noth[0], int(message_text[0]), message_text[1])
        Bot.send_message(message.chat.id, f"Ответ {message_text[1]} на {message_text[0]} вопрос: принят.")
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)
    else:
        Bot.send_message(message.chat.id,
                         "Вы некорректно ввели ответ. Формат ответа: /an task answer.\nЧтобы закончить тест введите '/end'.")
        # Ждём ответы дальше
        Bot.register_next_step_handler(message, save_answers)


def show_results(message):
    # Очищаем следующий шаг
    Bot.clear_step_handler_by_chat_id(message.chat.id)

    if len(user_tests[message.chat.id].user_answers) == 0:
        Bot.send_message(message.chat.id, 'Вы не дали ни одного ответа, результат теста не будет засчитан.')
        return True
    else:
        # Выводим решения (если нужно)
        Bot.send_message(message.chat.id, user_tests[message.chat.id].show_solve())

        # Выводим проверку ответов
        Bot.send_message(message.chat.id, user_tests[message.chat.id].check_answers())

        # Выводим статистику
        Statistics.add_statistics(user_tests[message.chat.id].get_point(), 'math', message.chat.id,
                                  user_tests[message.chat.id].name_test)

    # Удаляем человека из памяти
    del user_tests[message.chat.id]

    return True


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
