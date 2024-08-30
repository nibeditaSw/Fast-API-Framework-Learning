from fastapi import HTTPException, Path, Body
from pydantic import BaseModel
from typing import Optional
from pokemon_load_data import SessionLocal, Pokemon, app
import uvicorn

# Define Pydantic models
class PokemonCreate(BaseModel):
    number: int
    name: str
    type_1: Optional[str] = None
    type_2: Optional[str] = None
    total: Optional[int] = 0
    hp: Optional[int] = 0
    attack: Optional[int] = 0
    defense: Optional[int] = 0
    sp_atk: Optional[int] = 0
    sp_def: Optional[int] = 0
    speed: Optional[int] = 0
    generation: Optional[int] = 0
    legendary: Optional[bool] = False

class PokemonResponse(PokemonCreate):
    pokemon_id: int


# Endpoints
@app.get("/pokemon/{number}", response_model=PokemonResponse)
def read_pokemon(number: int = Path(description="The number of the Pokémon to retrieve")):
    db = SessionLocal()
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == number).first()
    db.close()
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return db_pokemon

@app.delete("/pokemon/{number}", response_model=PokemonResponse)
def delete_pokemon(number: int = Path(description="The number of the Pokémon to delete")):
    db = SessionLocal()
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == number).first()
    if db_pokemon is None:
        db.close()
        raise HTTPException(status_code=404, detail="Pokémon not found")
    db.delete(db_pokemon)
    db.commit()
    db.close()
    return db_pokemon

@app.post("/pokemon/", response_model=PokemonResponse)
def create_pokemon(pokemon: PokemonCreate = Body(...)):
    db = SessionLocal()
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == pokemon.number, Pokemon.name == pokemon.name).first()

    if db_pokemon:
        db.close()
        raise HTTPException(status_code=400, detail="Pokémon with this number and name already exists")

    new_pokemon = Pokemon(
        number=pokemon.number,
        name=pokemon.name,
        type_1=pokemon.type_1,
        type_2=pokemon.type_2,
        total=pokemon.total,
        hp=pokemon.hp,
        attack=pokemon.attack,
        defense=pokemon.defense,
        sp_atk=pokemon.sp_atk,
        sp_def=pokemon.sp_def,
        speed=pokemon.speed,
        generation=pokemon.generation,
        legendary=pokemon.legendary
    )

    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    db.close()

    return new_pokemon



def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
