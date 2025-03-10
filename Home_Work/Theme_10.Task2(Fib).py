# Библиотеки для указателей
from typing import Iterator, Iterable


# Класс для расчёта числа Фибоначчи.
class Fibonacci(Iterable):
    def __init__(self, value: int) -> None:
        self.value = value  # Количество чисел Фибоначчи, которые нужно вычислить
        self.last_num = 0  # Предыдущее число Фибоначчи
        self.prev_num = 1  # Текущее число Фибоначчи

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> int:
        # Если все числа Фибоначчи вычислены, завершаем итерацию
        if self.value == 0:
            raise StopIteration

        # Вычисляем следующее число Фибоначчи
        next_num = self.last_num + self.prev_num
        self.last_num, self.prev_num = self.prev_num, next_num
        self.value -= 1  # Уменьшаем счётчик оставшихся чисел
        return self.last_num  # Возвращаем текущее число Фибоначчи


# Пример использования
n = int(input())  # Вводим количество чисел Фибоначчи
fib = Fibonacci(n)  # Создаём объект Fibonacci
result = 0  # Переменная для хранения последнего числа Фибоначчи

# Итерируемся по объекту Fibonacci и сохраняем последнее значение
for num in fib:
    result = num

# Выводим результат
print(result)
