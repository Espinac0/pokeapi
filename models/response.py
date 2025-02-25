from pydantic import BaseModel

class PokemonName(BaseModel):
    name: str