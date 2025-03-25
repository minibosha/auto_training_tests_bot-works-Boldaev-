# Базовый класс покемона с названием
class BasePokemon:
    def __init__(self, name: str) -> None:
        self._name = name

    # Вывод имени
    @property
    def name(self) -> str:
        return self._name

    # Вывод имен при указании класса
    def __str__(self) -> str:
        return f"BasePokemon(name={self.name})"