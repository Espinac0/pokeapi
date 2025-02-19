from fastapi import HTTPException
from typing import List
from models.pokemon_model import fetch_water_pokemons

def get_water_pokemons_handler() -> List[str]:
    pokemons = fetch_water_pokemons()
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Water-type Pokémon found")
    return pokemons