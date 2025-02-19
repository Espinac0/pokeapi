from handler.pokemon_handler import (
    fetch_water_pokemons,
    fetch_pokemon_by_id
)

def test_fetch_pokemon_by_id():
    assert fetch_pokemon_by_id(1) == "bulbasaur"

