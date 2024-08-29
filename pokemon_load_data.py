from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    url = "https://coralvanda.github.io/pokemon_data.json"
    response = requests.get(url)
    data = response.json()

    session = SessionLocal()

    for entry in data:
        pokemon = Pokemon(
            number=entry.get("#"),  
            name=entry.get("Name"),
            type_1=entry.get("Type 1"),
            type_2=entry.get("Type 2") if entry.get("Type 2") else None,  
            total=entry.get("Total", 0),
            hp=entry.get("HP", 0),
            attack=entry.get("Attack", 0),
            defense=entry.get("Defense", 0),
            sp_atk=entry.get("Sp. Atk", 0),
            sp_def=entry.get("Sp. Def", 0),
            speed=entry.get("Speed", 0),
            generation=entry.get("Generation", 0),
            legendary=entry.get("Legendary", False)
        )
        session.add(pokemon)
        session.commit()

    session.close()
