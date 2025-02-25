from fastapi import APIRouter, HTTPException
from typing import List
from models import Pokemon  # Modelo de respuesta
from utils.Logger import Logger  # Logger para agregar logs
from handler.pokemon_handler import get_pokemon_handler, get_pokemons_by_type_handler, get_water_pokemons_handler

router = APIRouter()
logger = Logger()

@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon = get_pokemon_handler(id)
    if "error" in pokemon:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(**pokemon)

@router.get("/type/{type_name}", response_model=List[Pokemon])
async def get_pokemon_by_type(type_name: str):
    """Obtiene Pokémons de un tipo específico."""
    pokemons = get_pokemons_by_type_handler(type_name)
    if not pokemons:
        logger.add_to_log("error", f"No se encontraron Pokémon del tipo {type_name}")
        raise HTTPException(status_code=404, detail=f"No se encontraron Pokémon del tipo {type_name}")
    return [Pokemon(name=name) for name in pokemons]

@router.get("/water-pokemon", response_model=List[Pokemon])
async def get_water_pokemons():
    """Obtiene Pokémons de tipo agua."""
    pokemons = get_water_pokemons_handler()
    if not pokemons:
        logger.add_to_log("error", "No se encontraron Pokémon de tipo agua")
        raise HTTPException(status_code=404, detail="No se encontraron Pokémon de tipo agua")
    return [Pokemon(name=name) for name in pokemons]
