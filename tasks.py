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

