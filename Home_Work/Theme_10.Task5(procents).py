# Вычисляем проценты в ФПИ банке
def count_procents(X, P, Y):
    P = 1 + P / 100
    while X < Y:
        X *= P  # Увеличиваем вклад на P процентов и отбрасываем дробную часть
        yield 1


# Получаем вводимые данные
X, P, Y = map(int, input().split())

# Вычисляем время которое нам понадобиться
T = sum(list(count_procents(X, P, Y)))

# Выводим результат
print(T)
