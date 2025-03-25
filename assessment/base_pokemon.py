from dataclasses import dataclass


# Базовый класс покемона с названием
@dataclass(frozen=True)
class BasePokemon:
    name: str

    def __str__(self) -> str:
        return f"BasePokemon(name={self.name})"