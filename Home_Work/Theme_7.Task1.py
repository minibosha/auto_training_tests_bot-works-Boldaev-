""" Задание 1. Тема 7: Принципы ООП """


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

    def __repr__(self):
        return str(self.point)

# Создаём класс вектора
class Vector(Point):
    def find_distance(self):
        other_point = Point([0, 0])
        return math.sqrt((self.point[0] - other_point.point[0]) ** 2 + (self.point[1] - other_point.point[1]) ** 2)

    def __add__(self, other_point):
        new_coords = [a + b for a, b in zip(self.point, other_point.point)]
        return Vector(new_coords)

    def __sub__(self, other_point):
        new_coords = [a - b for a, b in zip(self.point, other_point.point)]
        return Vector(new_coords)

    def __mul__(self, other_point):
        new_coords = [coord * other_point for coord in self.point]
        return Vector(new_coords)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def scalar(self, other_point):
        return sum(a * b for a, b in zip(self.point, other_point.point))


v1 = Vector([0, 5])
print(v1.find_distance())

v2 = Vector([3, 6])
print(v2.find_distance())

v3 = v1 + v2
print(v3)

v4 = v1 - v2
print(v4)

v5 = v1 * 3
print(v5)

scalar = v1.scalar(v2)
print(scalar)