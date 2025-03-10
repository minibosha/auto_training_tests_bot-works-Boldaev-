def find_roots(A, B, C, D):
    x = -100
    while x != 101:
        if A * x ** 3 + B * x ** 2 + C * x + D == 0:
            yield x
        x += 1


# Чтение входных данных
A, B, C, D = map(int, input().split())

# Поиск корней с использованием генератора
roots = sorted(set(find_roots(A, B, C, D)))

# Вывод результата
print(" ".join(map(str, roots)))
