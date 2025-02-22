""" Задание 3. Тема 9: Продвинутые функции. Декораторы """
# Функция из библиотеки для вычисления произведения всех чисел
from math import prod
# Библиотека, чтобы указать тип данных - функция.
from typing import Callable
# Библиотека для замера времени
import time
# Библиотека для работы с системой
import sys


# Устанавливаем расширение на размер чисел больше
sys.set_int_max_str_digits(999999999)


# Декоратор для счёта времени функции
def time_it(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)

        return result


    return wrapper


# Вычисление "факториала"
@time_it
def factorial(n: int) -> int:
    return prod(range(1, n+1))


print(factorial(10000))