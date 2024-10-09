from pydantic import BaseModel
from typing import Optional, List


# Input Schemas
class PokemonPostPutInputSchema(BaseModel):
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
    pokemon_id: int


class PokemonGetAllOutputSchema(BaseModel):
    results: List[PokemonGetOutputSchema]


class PokemonPostPatchPutOutputSchema(PokemonGetOutputSchema):
    pass
