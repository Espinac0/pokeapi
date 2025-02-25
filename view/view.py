from fastapi import APIRouter, HTTPException
from typing import List
import requests
from utils.Logger import Logger
import redis
import json
import os
from pydantic import BaseModel
logger = Logger()
router = APIRouter()

class Pokemon(BaseModel):
    name: str

# Configuración de Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
CACHE_EXPIRATION = 3600  # 1 hora en segundos

# Conexión a Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@router.get("/water-pokemons", response_model=List[str])
async def get_water_pokemons():
    logger.add_to_log("info", "Solicitud recibida en /water-pokemons")
    
    try:
        # Intentar obtener datos de la caché
        cache_key = "water_pokemons"
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            logger.add_to_log("info", "Datos obtenidos de la caché de Redis")
            return json.loads(cached_data)
            
        # Si no está en caché, obtener de la PokeAPI
        logger.add_to_log("info", "Datos no encontrados en caché, consultando PokeAPI")
        response = requests.get("https://pokeapi.co/api/v2/type/11")  # 11 es el ID del tipo agua
        if response.status_code == 200:
            data = response.json()
            water_pokemons = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
            
            # Guardar en caché
            try:
                redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(water_pokemons))
                logger.add_to_log("info", "Datos guardados en la caché de Redis")
            except Exception as e:
                logger.add_to_log("error", f"Error al guardar en Redis: {str(e)}")
            
            return water_pokemons
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener datos de PokeAPI")
    except redis.RedisError as e:
        logger.add_to_log("warning", f"Error con Redis: {str(e)}")
        # Si Redis falla, continuamos sin caché
        return await get_water_pokemons_without_cache()
    except Exception as e:
        logger.add_to_log("error", f"Error al obtener pokémon de tipo agua: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Función de respaldo cuando Redis no está disponible
@router.get("/water-pokemons-without-cache", response_model=List[str])
async def get_water_pokemons_without_cache():
    response = requests.get("https://pokeapi.co/api/v2/type/11")
    if response.status_code == 200:
        data = response.json()
        return [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener datos de PokeAPI")
    



@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon = fetch_pokemon_by_id(id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(name=pokemon)


@router.get("/redis-health")
async def check_redis_health():
    try:
        redis_client.ping()
        return {"status": "healthy", "message": "Redis está funcionando correctamente"}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis no está disponible: {str(e)}")
    

    try:
        # Intentar escribir en Redis
        redis_client.set("test_key", "test_value")
        # Leer el valor
        value = redis_client.get("test_key")
        # Obtener todas las claves
        keys = redis_client.keys("*")
        return {
            "status": "success",
            "test_value": value,
            "all_keys": keys
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }