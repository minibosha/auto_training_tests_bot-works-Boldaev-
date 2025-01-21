""" Задание 2. Тема 7: Принципы ООП """

# Скачиваем библиотеку для вычислений
import math


# Создаём класс вектора
class Vector:
    def __init__(self, point):
        self.point = point

    def find_distance(self):
        other_point = [0, 0]
        return math.sqrt((self.point[0] - other_point[0]) ** 2 + (self.point[1] - other_point[1]) ** 2)

    def __add__(self, other):
        new_cords = [a + b for a, b in zip(self.point, other.point)]
        return Vector(new_cords)

    def __getitem__(self, index):
        return self.point[index]

    def to_tuple(self):
        return tuple(self.point)  # Возвращает координаты как кортеж

    def __repr__(self):
        return f"{self.point[0]} {self.point[1]}"


# Создаём класс, который описывает средство передвижения
class Vehicle:
    def __init__(self, point):
        self.position = Vector(point)
        self.route = []
        self.record_route = True

    def get_rout(self):
        return self.route

    def move(self, n):
        # Вычисляем новую позицию
        new_position = Vector([
            self.position[0] + self.position[0] * n,
            self.position[1] + self.position[1] * n])

        # Обновляем позицию
        self.position = new_position

        # Записываем маршрут, если флаг установлен
        if self.record_route:
            self.route.append(self.position.to_tuple())

        return self.route

    def toggle_record_route(self):
        self.record_route = not self.record_route

    def __repr__(self):
        return f"{self.position[0]} {self.position[1]}"


class Car(Vehicle):
    def __init__(self, fuel_efficiency, point):
        super().__init__(point)
        self.point = point
        self.fuel_efficiency = fuel_efficiency
        self.fuel = 0

    def show_fuel(self):
        return self.fuel

    def add_fuel(self, amount):
        self.fuel += amount

    def set_fuel_efficiency(self, efficiency):
        self.fuel_efficiency = efficiency

    def move(self, n):
        # Вычисляем длину вектора движения
        distance = math.sqrt(self.position[0] ** 2 + self.position[1] ** 2) * n

        # Проверяем, достаточно ли бензина для перемещения
        required_fuel = distance * self.fuel_efficiency
        if required_fuel < self.fuel:
            # Перемещаемся если есть бензин
            super().move(n)

            # Уменьшаем количество бензина
            self.fuel -= required_fuel

        return self.route


# Пример использования класса Vehicle
v1 = Vehicle([0, 1])
print(v1.move(2))
print(v1.move(8))

v1.toggle_record_route()
print(v1.move(2))
print(v1, '\n')

# Пример использования класса Car
car = Car(0.3, [0, 3])
car.add_fuel(100)

print(car.move(2), car.show_fuel())
print(car.move(2), car.show_fuel())
print(car.move(3), car.show_fuel())

car.toggle_record_route()
print(car.move(1), car.show_fuel())
print(car)
