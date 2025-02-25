# Скачиваем библиотеку с указателями
from typing import Iterator, Iterable


# Класс для расчёта числа Фибоначчи.
class Fibonacci(Iterable):
    def __init__(self, value: int) -> None:
        self.value = value + 1
        self.last_num = 0
        self.prev_num = 1

        if self.value == 1:
            self.value = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> int:
        if self.value == 1:
            raise StopIteration
        if self.value == 0:

            return 1

        # Вычисляем следующее число Фибоначчи
        next_num = self.last_num + self.prev_num
        self.last_num, self.prev_num = self.prev_num, next_num
        self.value -= 1
        return self.last_num  # Возвращаем текущее число Фибоначчи


# Пример использования
n = int(input())
print([i for i in Fibonacci(n)][-1])
