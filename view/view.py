from fastapi import APIRouter, HTTPException
from typing import List
from models.response import Pokemon
from utils.Logger import Logger
from handler.pokemon_handler import get_pokemon_handler, get_pokemons_by_type_handler, get_water_pokemons_handler

router = APIRouter()
logger = Logger()

@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    pokemon = get_pokemon_handler(id)
    if "error" in pokemon:
        logger.add_to_log("error", f"Pokémon with ID {id} not found")
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return Pokemon(**pokemon)

@router.get("/type/{type_name}", response_model=List[Pokemon])
async def get_pokemon_by_type(type_name: str):
    pokemons = get_pokemons_by_type_handler(type_name)
    if not pokemons:
        logger.add_to_log("error", f"No Pokemon found whit the type {type_name}")
        raise HTTPException(status_code=404, detail=f"No Pokemon found in {type_name}")
    return [Pokemon(name=name) for name in pokemons]

@router.get("/water-pokemons", response_model=List[Pokemon])
async def get_water_pokemons():
    logger.add_to_log("info", " request received in /water-pokemons")
    pokemons = get_water_pokemons_handler()
    if not pokemons:
        logger.add_to_log("error", "No water Pokemon found")
        raise HTTPException(status_code=404, detail="No water type Pokemon found")
    return [Pokemon(name=name) for name in pokemons]