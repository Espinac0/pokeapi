from fastapi import HTTPException
from typing import Dict
import json
import redis
from models.pokemon_model import fetch_pokemon_by_id
from config.redis_config import redis_client, check_redis_connection
from pydantic import BaseModel
from utils.Logger import Logger

<<<<<<< HEAD
logger = Logger()

def get_pokemon_handler(pokemon_id: int) -> dict:
    """Manejador que obtiene la información del Pokémon y la estructura."""
    pokemon_data = fetch_pokemon_by_id(pokemon_id)
    if "error" in pokemon_data:
        return {"error": "Pokémon no encontrado"}
    return {
=======
def get_pokemon_handler(pokemon_id: int) -> Dict:
    """Manejador que obtiene la información del Pokémon y la estructura."""
    cache_key = f"pokemon_{pokemon_id}"
    
    # Intentar obtener de Redis si está disponible
    if check_redis_connection():
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    
    # Si no está en caché, obtener de la PokeAPI
    pokemon_data = fetch_pokemon_by_id(pokemon_id)
    if "error" in pokemon_data:
        return {"error": "Pokémon no encontrado"}
    
    # Estructurar los datos
    structured_data = {
>>>>>>> 0a459b546b902fb91737c7f7098dc8163c457646
        "id": pokemon_data["id"],
        "name": pokemon_data["name"],
        "height": pokemon_data["height"],
        "weight": pokemon_data["weight"],
        "types": [t["type"]["name"] for t in pokemon_data["types"]]
    }
<<<<<<< HEAD

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
=======
    
    # Guardar en caché si Redis está disponible
    if check_redis_connection():
        try:
            redis_client.setex(cache_key, 3600, json.dumps(structured_data))
        except redis.RedisError as e:
            print(f"Error al guardar en Redis: {e}")
    
    return structured_data
>>>>>>> 0a459b546b902fb91737c7f7098dc8163c457646
