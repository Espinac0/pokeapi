from fastapi import APIRouter, HTTPException
from typing import List
import requests
import json
import redis
import os
from handler.pokemon_handler import *
from pydantic import BaseModel

# Configuración de Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
CACHE_EXPIRATION = 3600  # 1 hora en segundos

# Conexión a Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
router = APIRouter()

# Modelo Pydantic para la respuesta
class Pokemon(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]

@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon_name = fetch_pokemon_by_id(id)  # Usa fetch_pokemon_by_id
    if not pokemon_name:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")  # Log de error
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(name=pokemon_name)  # Devuelve solo el nombre

@router.get("/water-pokemons", response_model=List[str])
async def get_water_pokemons():
    """Obtiene la lista de Pokémon de tipo agua."""
    cache_key = "water_pokemons"
    
    # Intentar obtener de Redis si está disponible
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    
    # Si no está en caché, obtener de la PokeAPI
    response = requests.get("https://pokeapi.co/api/v2/type/11")  # 11 es el ID del tipo agua
    if response.status_code == 200:
        data = response.json()
        water_pokemons = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
        
        # Guardar en caché si Redis está disponible
        if redis_client:
            try:
                redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(water_pokemons))
            except redis.RedisError as e:
                print(f"Error al guardar en Redis: {e}")
        
        return water_pokemons
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener datos de PokeAPI")

@router.get("/redis-health")
async def check_redis_health():
    """Verifica el estado de Redis."""
    try:
        redis_client.ping()
        return {"status": "healthy", "message": "Redis está funcionando correctamente"}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis no está disponible: {str(e)}")