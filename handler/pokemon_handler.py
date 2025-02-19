from fastapi import HTTPException
from typing import List
from models.pokemon_model import fetch_water_pokemons

def get_water_pokemons_handler() -> List[str]:
    pokemons = fetch_water_pokemons()
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Water-type Pokémon found")
    return pokemons

def fetch_pokemon_by_id(pokemon_id: int) -> str:
    """Obtiene un Pokémon por su número (ID)."""
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
        logger.add_to_log("error", f"Error al obtener el Pokémon con ID {pokemon_id}: {e}")
        sentry_sdk.capture_exception(e)  # Captura errores en Sentry
        return ""