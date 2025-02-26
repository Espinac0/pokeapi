import requests
import os
import redis
from typing import List
from utils.Logger import Logger

# Configuración de Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

# Diccionario para mapear el tipo de Pokémon a su ID
type_to_id = {
    "normal": 1, "fighting": 2, "flying": 3, "poison": 4, "ground": 5, "rock": 6,
    "bug": 7, "ghost": 8, "steel": 9, "fire": 10, "water": 11, "grass": 12,
    "electric": 13, "psychic": 14, "ice": 15, "dragon": 16, "dark": 17, "fairy": 18
}

# Función para obtener los Pokémon por tipo
def fetch_pokemons_by_type(type_name: str) -> List[str]:
    type_id = type_to_id.get(type_name.lower(), None)
    if not type_id:
        return []

    cached_data = redis_client.get(type_name)
    if cached_data:
        return cached_data.split(',')

    url = f"https://pokeapi.co/api/v2/type/{type_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemons = [pokemon["pokemon"]["name"] for pokemon in data["pokemon"]]

        redis_client.setex(type_name, 3600, ','.join(pokemons))  # Guarda los resultados en caché
        return pokemons
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error obtaining pokemon type {type_name}: {e}")
        return []

# Función para obtener los Pokémon de tipo agua usando la de tipo
def fetch_water_pokemons() -> List[str]:
    return fetch_pokemons_by_type("water")

# Función para obtener un Pokémon por su ID
def fetch_pokemon_by_id(pokemon_id: int) -> str:
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

    cached_data = redis_client.get(str(pokemon_id))
    if cached_data:
        return cached_data
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        redis_client.setex(str(pokemon_id), 3600, data["name"])  # Guarda en caché
        return data["name"]
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error obtaining pokemon whit ID {pokemon_id}: {e}")
        return ""