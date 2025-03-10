def list_to_sqrt(N):
    a = 1
    while a ** 2 <= N:
        yield a ** 2
        a += 1


# Ввод данных
N = int(input())

# Вычисляем квадраты
sqrts = list(list_to_sqrt(N))

# Выводим квадраты до N
print(' '.join(map(str, sqrts)))
