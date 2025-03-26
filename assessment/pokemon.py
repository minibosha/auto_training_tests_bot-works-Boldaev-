from dataclasses import dataclass

from base_pokemon import BasePokemon
from pokemonstats import PokemonStats


# Класс с полной информацией о покемоне
@dataclass(frozen=True)
class Pokemon(BasePokemon):
    id: int
    height: int
    weight: int
    stats: PokemonStats

    def __str__(self) -> str:
        return (
            f"Pokemon(id={self.id}, name={self.name}, "
            f"height={self.height}, weight={self.weight})")
