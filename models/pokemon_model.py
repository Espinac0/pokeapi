from typing import List, Optional, Dict, Any
import requests

def fetch_data(url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def get_water_type_url() -> Optional[str]:
    url = "https://pokeapi.co/api/v2/type/"
    data = fetch_data(url)
    if data:
        for pokemon_type in data.get("results", []):
            if pokemon_type.get("name") == "water":
                return pokemon_type.get("url")
    return None

def fetch_water_pokemons() -> List[str]:
    water_type_url = get_water_type_url()
    if not water_type_url:
        return []
    data = fetch_data(water_type_url)
    if data:
        return [pokemon.get("pokemon", {}).get("name") for pokemon in data.get("pokemon", []) if pokemon.get("pokemon")]
    else:
        return []
    
def fetch_pokemon_by_id(pokemon_id: int) -> dict:
    """Obtiene la información de un Pokémon por su ID desde la PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Pokémon no encontrado"}