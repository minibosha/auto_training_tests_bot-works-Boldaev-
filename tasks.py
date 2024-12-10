""" Решение задач. Тема 6. ООП """


""" Задачи на анализ """

# Задача 1
'''
1. Класс books:
    - Вывод всех книг которые можно взять 
    - Вывод у кого находиться книга по её названию (кол-во имеющихся экземпляров)
    - Вывод характеристики книги (ISBN, год создания, название, автора, количество имеющихся экземпляров)
    - Удаление книги из базы данных
    - Просмотр взятых книг
2. Класс user:
    - Выдача книги пользователю
    - Просмотр читательского билета (уникальный номер билета, ФИО человека, взятые книги и х сроки, его адрес и контактные данные)
    - Возврат книги от пользователя с показом штрафа если он просрочил время.
'''

# Задача 2
'''
1. Класс articles:
    - Просмотр статей
    - Возможность поставить реакцию на статью
    - Чтение определённой статьи
    - Нахождение статьей интересные пользователю
2. Класс user:
    - Регистрация
    - Добавление статьей
    - Удаление статьей
    - Изменение статьей
    - Создание категорий на статьи
'''

# Задача 3
'''
Чат-бот для подготовки к тестам. Имеющий автоматическое создание задач на тему теста и показа решения на задачи. 

Возможности:
- Решение теста, созданного программой.
- Смотреть статистику по решению теста.
- Смотреть решение и ответы на задачи в тесте.
- Возможность пройти тест снова по хэшу.

## Проектирование:
Тесты:

Нахождение теста по указанному предмету;

Запуск теста по его названию на определённую тему;

Быстрое создание тестов на тему (из-за имеющихся функций в программе);

Решения:
    
Функции для вывода последовательного решения для пользователя (например дискриминант);

Функции упрощающие внутренние вычисления;

Статистика и ответы (информация о тестах):

Вывод статистики человека на задачу;

Нахождение информации о статистике из json файла;
'''


""" Задачи на реализацию """

# Задание 1
'''
# Класс гонщиков
class Driver:
    # Создаём словарь картеров
    drivers = {}

    def add_driver(self, name, circle_times):
        time = sum(circle_times)
        self.drivers[name] = [circle_times, time]

    def sort_drivers(self):
        sorted_drivers = sorted(self.drivers.items(), key=lambda item: item[1][1])
        return sorted_drivers


# Ввод данных
n, m = map(int, input().split())
driver_instance = Driver()  # Создаем экземпляр класса Driver

# Вводим имена и сохраняем их
for _ in range(n):
    name = input()
    circle_times = list(map(int, input().split()))

    driver_instance.add_driver(name, circle_times)  # Добавляем гонщика

# Сортируем гонщиков и выводим результат
sorted_drivers = driver_instance.sort_drivers()
print(sorted_drivers[0][0])
'''

# Задание 2
'''
# Скачиваем библиотеку для вычислений
import math

# Создаём класс для точки
class Point:
    def __init__(self, point):
        self.point = point

    def copy_point(self):
        return Point(self.point.copy())  # Возвращаем новый объект Point

    def find_distance(self, other_point):
        return math.sqrt((self.point[0] - other_point.point[0]) ** 2 + (self.point[1] - other_point.point[1]) ** 2)

# Класс для треугольника
class Triangle:
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    def find_perimeter(self):
        return (self.point1.find_distance(self.point2) +
                self.point2.find_distance(self.point3) +
                self.point3.find_distance(self.point1))

    def find_area(self):
        # Используем формулу Герона
        a = self.point1.find_distance(self.point2)
        b = self.point2.find_distance(self.point3)
        c = self.point3.find_distance(self.point1)
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

    def is_point_inside(self, point):
        # Используем метод площадей
        area1 = Triangle(point, self.point2, self.point3).find_area()
        area2 = Triangle(self.point1, point, self.point3).find_area()
        area3 = Triangle(self.point1, self.point2, point).find_area()
        return math.isclose(self.find_area(), area1 + area2 + area3)

    def show_points(self):
        return [self.point1, self.point2, self.point3]

# Создаём класс для создания круга
class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def circumference(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def is_point_inside(self, point):
        return self.center.find_distance(point) < self.radius

    def has_common_points(self, other):
        distance_between_centers = self.center.find_distance(other.center)
        return distance_between_centers <= (self.radius + other.radius) and distance_between_centers >= abs(self.radius - other.radius)


# Ввод и вывод ответов на задачи

# Длина отрезка
X1, Y1, X2, Y2 = map(int, input().split())

p1 = Point([X1, Y1])
p2 = Point([X2, Y2])
print(p1.find_distance(p2))

# Площадь треугольника
x1, y1, x2, y2, x3, y3 = map(int, input().split())
p1 = Point([x1, y1])
p2 = Point([x2, y2])
p3 = Point([x3, y3])
triangle = Triangle(p1.copy_point(), p2.copy_point(), p3.copy_point())

print(triangle.find_area())

# Две окружности
x1, y1, r1 = map(int, input().split())
x2, y2, r2 = map(int, input().split())

circle1 = Circle(Point([x1, y1]), r1)
circle2 = Circle(Point([x2, y2]), r2)

print("YES" if circle1.has_common_points(circle2) else "NO")

# Треугольник и точка
x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
x3, y3 = map(int, input().split())
x4, y4 = map(int, input().split())

p1 = Point([x1, y1])
p2 = Point([x2, y2])
p3 = Point([x3, y3])
p4 = Point([x4, y4])

triangle = Triangle(p1.copy_point(), p2.copy_point(), p3.copy_point())

print("In" if triangle.is_point_inside(p4) else "Out")

# Развлечения с измерителем
points = []
for _ in range(int(input())):
    x, y = map(int, input().split())
    points.append(Point([x, y]))

answer = []
for point in points:
    for p in points:
        answer.append(point.find_distance(p))

answer = sorted(set(answer))[1:]
print(len(answer))
for s in answer:
    print(s)
'''

# Задание 3
'''
# Сотовые связь в большом городе

# Класс для работы с абонентом
class Operator:
    def __init__(self):
        self.mobile_operators = {}

    # Функция добавление станции
    def add_station(self, name, x, y, r):
        self.mobile_operators.setdefault(name, []).append(Circle(Point([x, y]), r))

    def show_stations(self):
        return self.mobile_operators.keys()

    def check_connection(self, other, operator):
        return len([True for operator in self.mobile_operators[operator] if operator.is_point_inside(other)])


# Ввод данных
# Сохраняем операторов
operators = Operator()
for _ in range(int(input())):
    name = input()
    x, y, r = map(int, input().split())
    operators.add_station(name, x, y, r)

# Ввод координаты абонента
x1, y1 = map(int, input().split())
subscriber_point = Point([x1, y1])

# Проверка количества точек в радиусе
answer = []
for operator in operators.show_stations():
    answer.append([operator, operators.check_connection(subscriber_point, operator)])

# Выводим ответ
print(len(answer))
for a in answer:
    print(*a)
'''

# Задание 4
'''
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
'''