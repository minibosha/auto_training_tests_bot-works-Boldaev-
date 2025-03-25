from base_pokemon import BasePokemon


# Класс с полной информацией о покемоне
class Pokemon(BasePokemon):
    def __init__(self, id_: int, name: str, height: int, weight: int) -> None:
        super().__init__(name)
        self._id = id_
        self._height = height
        self._weight = weight

    # Декоратор получения id
    @property
    def id(self) -> int:
        return self._id

    # Декоратор получения высоты
    @property
    def height(self) -> int:
        return self._height

    # Декоратор получения веса
    @property
    def weight(self) -> int:
        return self._weight

    # Вывод данных
    def __str__(self) -> str:
        return (
            f"Pokemon(id={self.id}, name={self.name}, "
            f"height={self.height}, weight={self.weight})")