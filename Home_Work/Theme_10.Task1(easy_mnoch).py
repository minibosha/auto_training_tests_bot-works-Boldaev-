def prime_factors(n):
    # Перебираем все простые числа
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            yield divisor
            n = n // divisor
        divisor += 1

    # Если n > 1, то n само является простым числом
    if n > 1:
        yield n


# Чтение входных данных
N = int(input())

# Получение простых множителей
factors = list(prime_factors(N))

# Запись результата в выходной файл
print("*".join(map(str, factors)))
