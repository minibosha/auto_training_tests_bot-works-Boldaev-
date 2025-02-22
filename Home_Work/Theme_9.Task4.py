""" Задание 4. Тема 9: Продвинутые функции. Декораторы """
# Указатель типа - функции
from typing import Callable


# Функция для кэша
def cache(func: Callable) -> Callable:
    cached_results = {}  # Словарь для хранения кэшированных результатов

    def wrapper(*args, **kwargs):
        # Создаём ключ на основе всех аргументов
        key = (args, frozenset(kwargs.items()))  # frozenset для неизменяемости

        # Если результат уже есть в кэше, возвращаем его
        if key in cached_results:
            print(f"Результат для {key} взят из кэша")
            return cached_results[key]

        # Иначе вычисляем результат и сохраняем его в кэше
        result = func(*args, **kwargs)
        cached_results[key] = result
        print(f"Результат для {key} вычислен и сохранён в кэше")
        return result

    return wrapper


# Функция суммы двух чисел
@cache
def add(a: int, b: int) -> int:
    return a + b


# Функция приветствия
@cache
def greet(name: str, greeting="Hello") -> str:
    return f"{greeting}, {name}!"


# Тестируем
print(add(2, 3))  # Вычисляется и кэшируется
print(add(2, 3))  # Берётся из кэша
print(add(3, 2))  # Вычисляется и кэшируется (аргументы в другом порядке)
print(greet("Alice"))  # Вычисляется и кэшируется
print(greet("Alice", greeting="Hi"))  # Вычисляется и кэшируется (другой greeting)
print(greet("Alice"))  # Берётся из кэша