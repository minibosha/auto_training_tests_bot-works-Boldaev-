""" Задачи на реализацию """

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
