import requests
from typing import Generator, Union
from base_pokemon import BasePokemon
from pokemon import Pokemon


class PokeAPI:
    # Сайт для получения API
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    # Функция, для получения данных о покемоне
    @classmethod
    def get_pokemon(cls, identifier: Union[str, int]) -> Pokemon:
        response = requests.get(f"{cls.BASE_URL}{identifier}")
        response.raise_for_status()
        data = response.json()

        return Pokemon(
            id_=data["id"],
            name=data["name"],
            height=data["height"],
            weight=data["weight"])

    # Итератор для, получение разных данных
    @classmethod
    def get_all(cls, get_full: bool = False) -> Generator[Union[BasePokemon, Pokemon], None, None]:
        lim = 1
        while True:
            response = requests.get(f"{cls.BASE_URL}{lim}")
            response.raise_for_status()
            data = response.json()

            if get_full:
                yield cls.get_pokemon(data["name"])
                lim += 1
            else:
                yield BasePokemon(name=data["name"])
                lim += 1