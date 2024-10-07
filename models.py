from sqlalchemy import Column, Integer, String, Boolean
from database import Base, engine

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
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
