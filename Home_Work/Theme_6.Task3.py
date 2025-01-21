""" Задачи на реализацию """

# Задание 2 (Забираем классы)
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
        return distance_between_centers <= (self.radius + other.radius) and distance_between_centers >= abs(
            self.radius - other.radius)


# Задание 3
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
