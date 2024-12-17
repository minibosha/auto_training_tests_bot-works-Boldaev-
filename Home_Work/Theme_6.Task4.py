""" Задачи на реализацию """

# Задание 4
# Прыжки в длину
# Изменение в задаче: последняя строка - вывод топа произвольного размера спортсменов
# Класс для вывода результата
class Result:
    @staticmethod
    def check_participants(jumps):
        # Преобразуем прыжки в список, игнорируя "x"
        valid_jumps = [float(jump) for jump in jumps if jump != 'x']

        if valid_jumps:
            return valid_jumps


    @staticmethod
    def filter_participants(participants):
        return participants.sort(key=lambda p: sorted(p[3], reverse=True), reverse=True)

    @staticmethod
    def get_top(participants, number):
        if not participants:
            return "No results."
        else:
            top = []
            for i in range(min(number, len(participants))):
                country, name, surname, jumps = participants[i]
                top.append([country, name, surname, max(jumps)])

            return top


# Класс для вывода таблиц и сохранения результата
class Table:
    def __init__(self):
        self.participants = []

    def add_participant(self, country, name, surname, valid_jumps):
        self.participants.append([country, name, surname, valid_jumps])


# Создаём объект класса для таблицы
table = Table()

# Ввод данных
for _ in range(int(input())):
    line = input().strip()
    parts = line.split()
    country = parts[0]
    name = parts[1]
    surname = parts[2]
    jumps = parts[3:]

    # Проверяем и добавляем участников
    valid_jumps = Result.check_participants(jumps)
    if valid_jumps:
        table.add_participant(country, name, surname, valid_jumps)

# Сортируем таблицу
Result.filter_participants(table.participants)

# Выводим участников
n = int(input())
top_table = Result.get_top(table.participants, n)
if top_table == 'No results.':
    print(top_table)
else:
    for ind, top in enumerate(top_table, start=1):
        print(f'{ind})', *top)
