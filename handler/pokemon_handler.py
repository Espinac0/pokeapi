from models.pokemon_model import fetch_pokemon_by_id, fetch_pokemons_by_type, fetch_water_pokemons

def get_pokemon_handler(pokemon_id: int) -> dict:
    pokemon_name = fetch_pokemon_by_id(pokemon_id)
    if not pokemon_name:
        return {"error": "Pokémon notfound"}
    return {"id": pokemon_id, "name": pokemon_name}

def get_pokemons_by_type_handler(type_name: str) -> list:
    return fetch_pokemons_by_type(type_name)

def get_water_pokemons_handler() -> list:
    return fetch_water_pokemons()