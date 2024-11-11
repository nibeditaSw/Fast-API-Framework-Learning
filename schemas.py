from pydantic import BaseModel
from typing import Optional, List


# Input Schemas
class PokemonPostPutInputSchema(BaseModel):
    """
    Schema for creating or updating a Pokémon entry via POST or PUT requests.
    
    Attributes:
        number (int): Unique identifier for the Pokémon.
        name (str): Name of the Pokémon.
        type_1 (Optional[str]): Primary type of the Pokémon (e.g., 'Fire', 'Water').
        type_2 (Optional[str]): Secondary type of the Pokémon, if any.
        total (int): Total base stat of the Pokémon.
        hp (int): Pokémon's base HP (Health Points).
        attack (int): Pokémon's base Attack stat.
        defense (int): Pokémon's base Defense stat.
        sp_atk (int): Pokémon's base Special Attack stat.
        sp_def (int): Pokémon's base Special Defense stat.
        speed (int): Pokémon's base Speed stat.
        generation (int): Generation to which the Pokémon belongs.
        legendary (bool): Indicates if the Pokémon is legendary.
    """
    number: int
    name: str
    type_1: Optional[str] = None
    type_2: Optional[str] = None
    total: int = 0
    hp: int = 0
    attack: int = 0
    defense: int = 0
    sp_atk: int = 0
    sp_def: int = 0
    speed: int = 0
    generation: int = 0
    legendary: bool = False


class PokemonPatchInputSchema(BaseModel):
    """
    Schema for partial updates to a Pokémon entry via PATCH requests.
    
    Attributes:
        name (Optional[str]): Name of the Pokémon.
        type_1 (Optional[str]): Primary type of the Pokémon.
        type_2 (Optional[str]): Secondary type of the Pokémon.
        total (Optional[int]): Total base stat of the Pokémon.
        hp (Optional[int]): Pokémon's base HP.
        attack (Optional[int]): Pokémon's base Attack stat.
        defense (Optional[int]): Pokémon's base Defense stat.
        sp_atk (Optional[int]): Pokémon's base Special Attack stat.
        sp_def (Optional[int]): Pokémon's base Special Defense stat.
        speed (Optional[int]): Pokémon's base Speed stat.
        generation (Optional[int]): Generation to which the Pokémon belongs.
        legendary (Optional[bool]): Indicates if the Pokémon is legendary.
    """
    name: Optional[str] = None
    type_1: Optional[str] = None
    type_2: Optional[str] = None
    total: Optional[int] = None
    hp: Optional[int] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    sp_atk: Optional[int] = None
    sp_def: Optional[int] = None
    speed: Optional[int] = None
    generation: Optional[int] = None
    legendary: Optional[bool] = None


# Output Schemas
class PokemonGetOutputSchema(PokemonPostPutInputSchema):
    """
    Schema for retrieving a Pokémon entry, including its unique ID.
    
    Attributes:
        pokemon_id (int): Unique identifier of the Pokémon entry in the database.
    """
    pokemon_id: int


class PokemonGetAllOutputSchema(BaseModel):
    """
    Schema for retrieving a list of Pokémon entries.
    
    Attributes:
        results (List[PokemonGetOutputSchema]): List of Pokémon entries retrieved from the database.
    """
    results: List[PokemonGetOutputSchema]


class PokemonPostPatchPutOutputSchema(PokemonGetOutputSchema):
    """
    Schema for the response after creating, updating, or partially updating a Pokémon entry.
    
    Inherits:
        PokemonGetOutputSchema: Provides a unified schema for responses, containing all Pokémon data.
    """
    pass
