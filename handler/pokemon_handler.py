from fastapi import HTTPException
import requests
import redis
from typing import List
from models.pokemon_model import fetch_water_pokemons
from config.redis_config import redis_client, check_redis_connection

def get_water_pokemons_handler() -> List[str]:
    pokemons = fetch_water_pokemons()
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Water-type Pokémon found")
    return pokemons

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