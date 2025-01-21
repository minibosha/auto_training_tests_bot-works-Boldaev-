""" Задачи на реализацию """


# Задание 1
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
driver_instance = Driver()

# Вводим имена и сохраняем их
for _ in range(n):
    name = input()
    circle_times = list(map(int, input().split()))

    driver_instance.add_driver(name, circle_times)

# Сортируем гонщиков и выводим результат
sorted_drivers = driver_instance.sort_drivers()
print(sorted_drivers[0][0])
