# Базовое исключение для ошибок PokéAPI
class PokeError(Exception):
    def __init__(self, message: str = "Ошибка при работе с PokéAPI"):
        self.message = message
        super().__init__(self.message)
