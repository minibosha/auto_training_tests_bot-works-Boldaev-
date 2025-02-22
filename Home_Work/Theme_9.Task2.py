""" Задание 2. Тема 9: Продвинутые функции. Декораторы """
# Скачиваем библиотеку для вычислений
import math


# Создаём класс для точки
class Point:
    def __init__(self, point: list) -> None:
        self.point = point

    def copy_point(self) -> 'Point':
        return Point(self.point.copy())

    def find_distance(self, other_point: 'Point') -> float:
        return math.sqrt((self.point[0] - other_point.point[0]) ** 2 + (self.point[1] - other_point.point[1]) ** 2)

    def __repr__(self) -> str:
        return str(self.point)


# Длина отрезка
X1, Y1, X2, Y2 = map(int, input().split())

p1 = Point([X1, Y1])
p2 = Point([X2, Y2])
print(p1.find_distance(p2))
