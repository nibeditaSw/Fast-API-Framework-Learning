import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from database import Base
from constants import ADMIN_ROLE, USER_ROLE
from factories import PokemonFactory
from factories import TestingSessionLocal, engine

# TEST_DATABASE_URL = "postgresql://postgres:nehububu@localhost:5432/test_pokemon_db"
# engine = create_engine(TEST_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Setup test client
client = TestClient(app)

# Setup and teardown for the test database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create the test database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the test database tables
    Base.metadata.drop_all(bind=engine)

def test_fetch_and_store():
    headers = {"role": ADMIN_ROLE}
    response = client.post("/pokemon/load", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Authorized and Data successfully stored in the database"

def test_read_pokemon():
    pokemon = PokemonFactory(name="Bulbasaur")
    headers = {"role": ADMIN_ROLE}
    
    response = client.get("/pokemon/?sort_by=name&sort_order=asc&search_column=name&keyword=Bulbasaur&page=1&limit=10", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0
    assert response.json()["results"][0]["name"] == "Bulbasaur"

def test_create_pokemon():
    headers = {"role": ADMIN_ROLE}
    pokemon_data = PokemonFactory.build(number=1001)
    
    pokemon_dict = {
        "number": pokemon_data.number,
        "name": pokemon_data.name,
        "type_1": pokemon_data.type_1,
        "type_2": pokemon_data.type_2,
        "total": pokemon_data.total,
        "hp": pokemon_data.hp,
        "attack": pokemon_data.attack,
        "defense": pokemon_data.defense,
        "sp_atk": pokemon_data.sp_atk,
        "sp_def": pokemon_data.sp_def,
        "speed": pokemon_data.speed,
        "generation": pokemon_data.generation,
        "legendary": pokemon_data.legendary,
    }
    
    response = client.post("/pokemon/", json=pokemon_dict, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["name"] == pokemon_data.name


def test_update_pokemon():
    pokemon = PokemonFactory.create()
    headers = {"role": ADMIN_ROLE}
    pokemon_update = {
        "attack": 80,
        "speed": 80
    }
    response = client.put(f"/pokemon/{pokemon.number}", json=pokemon_update, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["attack"] == 80
    assert response.json()["speed"] == 80

def test_delete_pokemon():
    pokemon = PokemonFactory.create()
    headers = {"role": ADMIN_ROLE}
    
    response = client.delete(f"/pokemon/{pokemon.number}", headers=headers)
    assert response.status_code == 204, f"Unexpected status code: {response.status_code}, Response: {response.content}"

