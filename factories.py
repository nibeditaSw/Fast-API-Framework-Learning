import factory
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base  
from models import Pokemon  


# Set up the test database session
TEST_DATABASE_URL = "postgresql://postgres:nehububu@localhost:5432/test_pokemon_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

fake = Faker()

class PokemonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Pokemon
        sqlalchemy_session = TestingSessionLocal()  

    number = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda x: fake.name())
    type_1 = factory.LazyAttribute(lambda x: fake.random_element(elements=("Grass", "Fire", "Water", "Poison")))
    type_2 = factory.LazyAttribute(lambda x: fake.random_element(elements=("Flying", "Bug", "Electric", "Fairy", None)))
    total = factory.LazyAttribute(lambda x: fake.random_int(min=200, max=700))
    hp = factory.LazyAttribute(lambda x: fake.random_int(min=20, max=100))
    attack = factory.LazyAttribute(lambda x: fake.random_int(min=20, max=100))
    defense = factory.LazyAttribute(lambda x: fake.random_int(min=20, max=100))
    sp_atk = factory.LazyAttribute(lambda x: fake.random_int(min=20, max=100))
    sp_def = factory.LazyAttribute(lambda x: fake.random_int(min=20, max=100))
    speed = factory.LazyAttribute(lambda x: fake.random_int(min=20, max=100))
    generation = factory.LazyAttribute(lambda x: fake.random_int(min=1, max=8))
    legendary = factory.LazyAttribute(lambda x: fake.boolean())
