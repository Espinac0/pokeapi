from fastapi import HTTPException
import requests
import redis
from typing import List
from models.pokemon_model import fetch_water_pokemons
from config.redis_config import redis_client, check_redis_connection
from pydantic import BaseModel
from utils.Logger import Logger

logger = Logger()

def get_pokemon_handler(pokemon_id: int) -> dict:
    """Manejador que obtiene la información del Pokémon y la estructura."""
    pokemon_data = fetch_pokemon_by_id(pokemon_id)
    if "error" in pokemon_data:
        return {"error": "Pokémon no encontrado"}
    return {
        "id": pokemon_data["id"],
        "name": pokemon_data["name"],
        "height": pokemon_data["height"],
        "weight": pokemon_data["weight"],
        "types": [t["type"]["name"] for t in pokemon_data["types"]]
    }

def fetch_pokemon_by_id(pokemon_id: int) -> str:
    """Obtiene un Pokémon por su número (ID)."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["name"]  # Devuelve solo el nombre del Pokémon
    except Exception as e:
        logger.add_to_log("error", f"Error al obtener el Pokémon con ID {pokemon_id}: {e}")
        return ""