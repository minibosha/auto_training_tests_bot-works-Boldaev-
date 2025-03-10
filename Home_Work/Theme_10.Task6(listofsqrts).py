def powers_of_two(N):
    exponent = 0
    current = 1
    while current <= N:
        yield current
        exponent += 1
        current = 2 ** exponent  # Вычисляем следующую степень


# Получаем данные
N = int(input())

# Получаем результат генератора
result = list(powers_of_two(N))

# Выводим результат
print(' '.join(map(str, result)))
