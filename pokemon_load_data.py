import requests
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Setup Database
DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/pokemon_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Models
class Pokemon(Base):
    __tablename__ = "pokemon"
    pokemon_id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type_1 = Column(String)  
    type_2 = Column(String)  
    total = Column(Integer)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_atk = Column(Integer)
    sp_def = Column(Integer)
    speed = Column(Integer)
    generation = Column(Integer)
    legendary = Column(Boolean)


# Create Tables
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Load JSON Data
app = FastAPI()

@app.on_event("startup")
async def load_data():
    # Fetch the JSON data from the URL
    url = "https://coralvanda.github.io/pokemon_data.json"
    response = requests.get(url)
    data = response.json()

    session = SessionLocal()

    # Collect all existing Pokémon numbers from the database
    existing_numbers = {pokemon.number for pokemon in session.query(Pokemon.number).all()}

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
        session.bulk_insert_mappings(Pokemon, pokemon_data)
        session.commit()
        print("Data inserted successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred: {str(e)}")
    finally:
        session.close()
