from fastapi import APIRouter, HTTPException
from typing import List
from models.response import Pokemon, PokemonName 
from utils.Logger import Logger
from handler.pokemon_handler import get_pokemon_handler, get_pokemons_by_type_handler, get_water_pokemons_handler

router = APIRouter()
logger = Logger()

@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    pokemon = get_pokemon_handler(id)
    if "error" in pokemon:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(**pokemon)

@router.get("/type/{type_name}", response_model=List[PokemonName])
async def get_pokemon_by_type(type_name: str):
    pokemons = get_pokemons_by_type_handler(type_name)
    if not pokemons:
        logger.add_to_log("error", f"No se encontraron Pokémon del tipo {type_name}")
        raise HTTPException(status_code=404, detail=f"No se encontraron Pokémon del tipo {type_name}")
    return [PokemonName(name=name) for name in pokemons]

@router.get("/water-pokemons", response_model=List[PokemonName])
async def get_water_pokemons():
    logger.add_to_log("info", "Solicitud recibida en /water-pokemons")
    pokemons = get_water_pokemons_handler()
    if not pokemons:
        logger.add_to_log("error", "No se encontraron Pokémon de tipo agua")
        raise HTTPException(status_code=404, detail="No se encontraron Pokémon de tipo agua")
    return [PokemonName(name=name) for name in pokemons]