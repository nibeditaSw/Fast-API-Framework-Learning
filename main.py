import uvicorn
import requests
from fastapi import FastAPI, Depends, HTTPException, Path, Body, Query, status
from typing import Optional, Literal
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Pokemon
from database import SessionLocal
from schemas import (
    PokemonPostPutInputSchema,
    PokemonPatchInputSchema,
    PokemonGetAllOutputSchema,
    PokemonPostPatchPutOutputSchema,
)
from authorization import role_required
from constants import SORTABLE_FIELDS, int_columns, bool_columns, string_columns, ADMIN_ROLE, USER_ROLE

# Load JSON Data
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/pokemon/load")
def fetch_and_store(db: Session = Depends(get_db), role: str = Depends(role_required([ADMIN_ROLE]))):
    # Fetch the JSON data from the URL
    response = requests.get("https://coralvanda.github.io/pokemon_data.json")
    data = response.json()

    print(f"Data fetched: {len(data)} entries")

    # Collect all existing Pokémon numbers from the database
    existing_numbers = {pokemon.number for pokemon in db.query(Pokemon.number).all()}

    # Collect Pokémon data for bulk insert
    pokemon_data = []

    for entry in data:
        original_number = entry.get("#")
        number = original_number

        # Find the next available unique number
        while number in existing_numbers or any(p['number'] == number for p in pokemon_data):
            number += 1
        
        # If the number was incremented, log the change
        if number != original_number:
            print(f"Duplicate number {original_number} found. Assigning new number {number}.")

        # Create a dictionary of Pokémon data for bulk insert
        pokemon_data.append({
            'number': number,
            'name': entry.get("Name"),
            'type_1': entry.get("Type 1"),
            'type_2': entry.get("Type 2") if entry.get("Type 2") else None,
            'total': entry.get("Total", 0),
            'hp': entry.get("HP", 0),
            'attack': entry.get("Attack", 0),
            'defense': entry.get("Defense", 0),
            'sp_atk': entry.get("Sp. Atk", 0),
            'sp_def': entry.get("Sp. Def", 0),
            'speed': entry.get("Speed", 0),
            'generation': entry.get("Generation", 0),
            'legendary': entry.get("Legendary", False)
        })

        # Add the new unique number to the set of existing numbers
        existing_numbers.add(number)

    # Perform bulk insert using bulk_insert_mappings
    try:
        db.bulk_insert_mappings(Pokemon, pokemon_data)
        db.commit()
        return {
            "message": "Authorized and Data successfully stored in the database",
            "inserted": len(pokemon_data),
        }
    except SQLAlchemyError as e:
        db.rollback()  
        return {"error": str(e)}


@app.get("/pokemon/", response_model=PokemonGetAllOutputSchema)
def read_pokemon(
    sort_by: SORTABLE_FIELDS = Query(default="pokemon_id", description="Column to sort by"),
    sort_order: Literal["asc", "desc"] = Query(default="asc", description="Sort order: 'asc' or 'desc'"),
    search_column: Literal["name", "type_1", "type_2", "total", "hp", "attack", "defense", "sp_atk", "sp_def", "speed", "generation", "legendary"] = Query(default="name", description="Column to search in"),
    keyword: Optional[str] = Query(None, description="Keyword to search for"),
    page: int = Query(default=1, description="Page number to retrieve, starts at 1"),
    limit: int = Query(default=10, description="Number of results per page"),
    db: Session = Depends(get_db),
    role: str = Depends(role_required([ADMIN_ROLE, USER_ROLE]))
):
    query = db.query(Pokemon)

    if keyword:
        search_column_attr = getattr(Pokemon, search_column, None)
        if search_column_attr is None:
            raise HTTPException(status_code=400, detail=f"Invalid search column: {search_column}")

        # Validate integer columns
        if search_column in int_columns:
            if not keyword.isdigit():
                raise HTTPException(status_code=400, detail=f"Keyword must be an integer for the {search_column} column")
            query = query.filter(search_column_attr == int(keyword))

        # Validate boolean columns
        elif search_column in bool_columns:
            if keyword.lower() not in ['true', 'false']:
                raise HTTPException(status_code=400, detail=f"Keyword must be 'true' or 'false' for the {search_column} column")
            query = query.filter(search_column_attr == (keyword.lower() == 'true'))

        # Convert non-integer inputs to string for string columns
        elif search_column in string_columns:
            query = query.filter(search_column_attr.ilike(f"%{keyword}%"))
        else:
            raise HTTPException(status_code=400, detail=f"Search not supported for column: {search_column}")

    # Sorting
    if sort_order == "asc":
        query = query.order_by(asc(sort_by))
    else:
        query = query.order_by(desc(sort_by))

    # Pagination
    offset = (page - 1) * limit
    db_pokemon = query.offset(offset).limit(limit).all()

    if not db_pokemon:
        raise HTTPException(status_code=404, detail="No Pokémon found")

    return {"results": db_pokemon}


@app.delete("/pokemon/{number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pokemon(number: int = Path(description="The number of the Pokémon to delete"), db: Session = Depends(get_db), role: str = Depends(role_required([ADMIN_ROLE, USER_ROLE]))):
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == number).first()
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    db.delete(db_pokemon)
    db.commit()
    # return db_pokemon

@app.post("/pokemon/", response_model=PokemonPostPatchPutOutputSchema)
def create_pokemon(pokemon: PokemonPostPutInputSchema = Body(...), db: Session = Depends(get_db), role: str = Depends(role_required([ADMIN_ROLE, USER_ROLE]))):
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == pokemon.number, Pokemon.name == pokemon.name).first()

    if db_pokemon:
        raise HTTPException(status_code=400, detail="Pokémon with this number and name already exists")

    new_pokemon = Pokemon(**pokemon.dict())

    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)

    return new_pokemon


@app.put("/pokemon/{number}", response_model=PokemonPostPatchPutOutputSchema)
def update_pokemon(number: int, pokemon: PokemonPatchInputSchema = Body(...), db: Session = Depends(get_db), role: str = Depends(role_required([ADMIN_ROLE, USER_ROLE]))):
    db_pokemon = db.query(Pokemon).filter(Pokemon.number == number).first()

    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon not found")

    for key, value in pokemon.dict(exclude_unset=True).items():
        setattr(db_pokemon, key, value)

    db.commit()
    db.refresh(db_pokemon)

    return db_pokemon


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

if __name__ == "__main__":
    main()
