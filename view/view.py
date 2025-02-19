from fastapi import APIRouter, HTTPException
from typing import List
import requests
from utils.Logger import Logger

logger = Logger()
router = APIRouter()

@router.get("/water-pokemons", response_model=List[str])
async def get_water_pokemons():
    logger.add_to_log("info", "Solicitud recibida en /water-pokemons")
    
    try:
        # Obtener pokémon de tipo agua de la PokeAPI
        response = requests.get("https://pokeapi.co/api/v2/type/11")  # 11 es el ID del tipo agua
        if response.status_code == 200:
            data = response.json()
            water_pokemons = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
            return water_pokemons
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener datos de PokeAPI")
    except Exception as e:
        logger.add_to_log("error", f"Error al obtener pokémon de tipo agua: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))