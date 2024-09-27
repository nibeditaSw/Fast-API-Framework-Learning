import uvicorn
from fastapi import HTTPException, Path, Body, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import asc, desc
from pokemon_load_data import SessionLocal, Pokemon, app

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

class PokemonUpdate(BaseModel):
    name: str
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


@app.get("/pokemon/", response_model=List[PokemonResponse])
def read_pokemon(
    sort_by: str = Query(default="pokemon_id", description="Column to sort by", regex="^(pokemon_id)$"),
    order: str = Query(default="asc", description="Sort order: 'asc' or 'desc'", regex="^(asc|desc)$"),
    search_column: str = Query(default="name", description="Column to search in"),
    keyword: Optional[str] = Query(None, description="Keyword to search for"),
    page: int = Query(default=1, description="Page number to retrieve, starts at 1"),
    limit: int = Query(default=10, description="Number of results per page")
):
    db = SessionLocal()

    query = db.query(Pokemon)

    # Validate keyword datatype based on the search column
    int_columns = ["total", "hp", "attack", "defense", "sp_atk", "sp_def", "speed", "generation"]
    bool_columns = ["legendary"]
    string_columns = ["name", "type_1", "type_2"]

    if keyword:
        search_column_attr = getattr(Pokemon, search_column, None)
        if search_column_attr is None:
            db.close()
            raise HTTPException(status_code=400, detail=f"Invalid search column: {search_column}")

        # Validate integer columns
        if search_column in int_columns:
            if not keyword.isdigit():
                db.close()
                raise HTTPException(status_code=400, detail=f"Keyword must be an integer for the {search_column} column")
            query = query.filter(search_column_attr == int(keyword))

        # Validate boolean columns
        elif search_column in bool_columns:
            if keyword.lower() not in ['true', 'false']:
                db.close()
                raise HTTPException(status_code=400, detail=f"Keyword must be 'true' or 'false' for the {search_column} column")
            query = query.filter(search_column_attr == (keyword.lower() == 'true'))

        # Convert non-integer inputs to string for string columns
        elif search_column in string_columns:
            query = query.filter(search_column_attr.ilike(f"%{keyword}%"))
        else:
            db.close()
            raise HTTPException(status_code=400, detail=f"Search not supported for column: {search_column}")

    # Sorting
    if order == "asc":
        query = query.order_by(asc(sort_by))
    else:
        query = query.order_by(desc(sort_by))

    # Pagination
    offset = (page - 1) * limit  
    db_pokemon = query.offset(offset).limit(limit).all()

    db.close()

    if not db_pokemon:
        raise HTTPException(status_code=404, detail="No Pokémon found")

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


@app.put("/pokemon/{number}", response_model=PokemonResponse)
def update_pokemon(number: int, pokemon: PokemonUpdate = Body(...)):
    db = SessionLocal()
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == number).first()

    if db_pokemon is None:
        db.close()
        raise HTTPException(status_code=404, detail="Pokémon not found")

    for key, value in pokemon.dict(exclude_unset=True).items():
        setattr(db_pokemon, key, value)

    db.commit()
    db.refresh(db_pokemon)
    db.close()

    return db_pokemon



def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

if __name__ == "__main__":
    main()
