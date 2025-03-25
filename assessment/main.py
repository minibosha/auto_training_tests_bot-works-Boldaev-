from pokeapi import PokeAPI
from pokemon import Pokemon
import itertools
import time


def get_heaviest_pokemon(generator, max_count: int) -> Pokemon:
    heaviest = None
    # Ограничиваем генератор с помощью itertools.islice
    for pokemon in itertools.islice(generator, max_count):
        print(f"ID: {pokemon.id} | Name: {pokemon.name}")
        if heaviest is None or pokemon.weight > heaviest.weight:
            heaviest = pokemon
    return heaviest


def benchmark(func):
    def wrapper():
        start = time.time()
        result = func()
        print(f"Время выполнения: {time.time() - start:.2f} сек")
        return result

    return wrapper


@benchmark
def first_50_test():
    print("Первые 50 покемонов")
    generator = PokeAPI.get_all(get_full=True)
    return get_heaviest_pokemon(generator, 50)


@benchmark
def first_20_test():
    print("\nПервые 20 покемонов (должно быть быстрее)")
    generator = PokeAPI.get_all(get_full=True)  # Новый генератор начинает с начала
    return get_heaviest_pokemon(generator, 20)


# Получаем покемона ditto
ditto = PokeAPI.get_pokemon("ditto")
print(f"Получен покемон: {ditto}\n")


# Первый тест (50 покемонов)
result_50 = first_50_test()
print(f"Самый тяжёлый: {result_50}\n")

# Второй тест (20 покемонов, используем кэш)
result_20 = first_20_test()
print(f"Самый тяжёлый: {result_20}")