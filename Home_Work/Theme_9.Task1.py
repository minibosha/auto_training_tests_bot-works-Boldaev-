""" Задание 1. Тема 9: Продвинутые функции. Декораторы """
# Функция из библиотеки для вычисления произведения всех чисел
from math import prod


# Функция для счёта произведения неизвестного кол-ва чисел
def product(*args):
    return prod(args)


# Делаем тест функции
print(product(1, 2, 3, 4, 5))
print(product(1, 4, 6, 9))
