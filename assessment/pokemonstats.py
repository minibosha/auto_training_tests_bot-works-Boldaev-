from dataclasses import dataclass


# Дополнительна статистика покемона
@dataclass(frozen=True)
class PokemonStats:
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    def __str__(self) -> str:
        return (
            f"Stats(hp={self.hp}, attack={self.attack}, "
            f"defense={self.defense}, sp_attack={self.special_attack}, "
            f"sp_defense={self.special_defense}, speed={self.speed})")