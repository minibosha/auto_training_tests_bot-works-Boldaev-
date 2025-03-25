import requests
from typing import Generator, Union
from functools import lru_cache
from base_pokemon import BasePokemon
from pokemon import Pokemon
from pokeerror import PokeError
from pokemonstats import PokemonStats


class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    @classmethod
    @lru_cache(maxsize=None)
    def get_pokemon(cls, identifier: Union[str, int]) -> Pokemon:
        try:
            response = requests.get(f"{cls.BASE_URL}{identifier}")
            response.raise_for_status()
            data = response.json()

            # Отсекам нужную статистику
            stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}

            return Pokemon(
                id=data["id"],
                name=data["name"],
                height=data["height"],
                weight=data["weight"],
                stats=PokemonStats(
                    hp=stats["hp"],
                    attack=stats["attack"],
                    defense=stats["defense"],
                    special_attack=stats["special-attack"],
                    special_defense=stats["special-defense"],
                    speed=stats["speed"]))
        except requests.exceptions.RequestException as e:
            raise PokeError(f"Ошибка запроса: {str(e)}")

    @classmethod
    def get_all(cls, get_full: bool = False) -> Generator[Union[BasePokemon, Pokemon], None, None]:
        next_url = cls.BASE_URL  # Начинаем с первого URL

        while next_url:
            try:
                response = requests.get(next_url)
                response.raise_for_status()
                data = response.json()

                for item in data["results"]:
                    if get_full:
                        yield cls.get_pokemon(item["name"])
                    else:
                        yield BasePokemon(name=item["name"])

                next_url = data.get("next")  # Получаем следующий URL из API
            except requests.exceptions.RequestException as e:
                raise PokeError(f"Ошибка запроса: {str(e)}")