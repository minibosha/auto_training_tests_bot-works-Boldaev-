from pokeapi import PokeAPI
from pokemon import Pokemon


# Получаем покемона ditto
ditto = PokeAPI.get_pokemon("ditto")
print(f"Получен покемон: {ditto}\n")

# Ищем самого тяжёлого среди первых 50
heaviest: Pokemon = None
for ind, pokemon in enumerate(PokeAPI.get_all(get_full=True)):
    if ind == 50:
        break
    if isinstance(pokemon, Pokemon):
        if heaviest is None or pokemon.weight > heaviest.weight:
            heaviest = pokemon

print(f"Самый тяжёлый покемон: {heaviest}")