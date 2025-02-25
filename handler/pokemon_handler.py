from fastapi import HTTPException
import requests
import redis
from typing import List
from models.pokemon_model import fetch_water_pokemons
from config.redis_config import redis_client, check_redis_connection
from pydantic import BaseModel
from models.pokemon import fetch_pokemon_by_id

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
        # Intentar obtener de Redis si está disponible
        if check_redis_connection():
            cached_data = redis_client.get(str(pokemon_id))
            if cached_data:
                return cached_data
    except redis.RedisError as e:
        print(f"Error de Redis: {e}")
        # Continuar con la petición a la API si Redis falla

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemon_name = data["name"]

        # Intentar guardar en caché si Redis está disponible
        if check_redis_connection():
            try:
                redis_client.setex(str(pokemon_id), 3600, pokemon_name)
            except redis.RedisError as e:
                print(f"Error al guardar en Redis: {e}")

        return pokemon_name
    except Exception as e:
        print(f"Error al obtener el Pokémon con ID {pokemon_id}: {e}")
        return ""
