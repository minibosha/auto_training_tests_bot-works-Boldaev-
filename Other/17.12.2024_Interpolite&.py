""" Записи с уроков"""




# 17.12.2024
# Интерполяция
""" Обычный  код с балансом который очень легко менять за классом.
class Client:
    def __init__(self, initial_balance):
        self.balance = initial_balance

me = Client(100)
friend = Client(200)

me.balance -= 50
friend.balance += 50

print(me.balance)
print(friend.balance)
"""

""" Добавляем интерполяцию
class Client:
    def __init__(self, initial_balance):
        self.__balance = initial_balance # Используем интерполяция

me = Client(100)
friend = Client(200)

me.balance -= 50 # Нельзя изменить ивне (даже через me.__balance)
friend.balance += 50

print(me.balance)
print(friend.balance)
"""

'''
class Client:
    def __init__(self, initial_balance, name):
        self.__name = name
        self.__balance = initial_balance # Используем интерполяция

    def __repr__(self):
        return f"У {self.__name} столько мани: {self.__balance}"

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            return False

        # Убираем начальные и конечные пробелы
        name = name.strip()

        if name == '':
            return False

        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if not isinstance(name, str):
            return False

        # Убираем начальные и конечные пробелы
        name = name.strip()

        if name == '':
            return False

        self.__name = name


    def get_balance(self):
        return self.__balance

    def send_to(self, receiver, amount): # использовать __balance можно только в функциях класса
        if not isinstance(receiver, Client):
            return False

        if amount > self.__balance:
            # В идеале выкинуть ошибку raise
            return False

        self.__balance -= amount
        receiver.__balance += amount


me = Client(100, 'me')
friend = Client(200, 'alex')
print(me, friend)

me.send_to(friend, 150)
print(me, friend)

friend.send_to(me, 150)
print(me, friend)

print(me.get_balance())
print(friend.get_balance())


me.set_name('  TEST  ')
print(me)

me.set_name(me.name + ' Andreev')
friend.set_name(friend.get_name() + ' Andreev')
print(me.name, friend.name)

# me.name (2. Срабатывает сеттер) = me.name (1. Срабатывает геттер + ' Andreev'
me.name += ' Andrucha'

print(me.name, friend.name)


# Полиморфизм
class Dog:
    def greet(self):
        print('Bark!')


class Cat:
    def greet(self):
        print('Meow!')

class Person:
    def greet(self):
        print('Hello!')


finn = Dog()
murr = Cat()
me = Person()

for mammal in (finn, murr, me):
    mammal.greet()
'''



