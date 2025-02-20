import pytest
from handler.pokemon_handler import fetch_pokemon_by_id
from config.redis_config import check_redis_connection

def test_fetch_pokemon_by_id():
    # Verificar si Redis está disponible
    redis_available = check_redis_connection()
    
    # Obtener el Pokémon
    result = fetch_pokemon_by_id(1)
    
    # Verificar el resultado
    assert result == "bulbasaur", f"Expected 'bulbasaur', but got '{result}'"
