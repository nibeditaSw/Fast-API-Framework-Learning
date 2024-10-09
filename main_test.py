import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base


TEST_DATABASE_URL = "postgresql://postgres:nehububu@localhost:5432/test_pokemon_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    response = client.post("/pokemon/load")
    assert response.status_code == 200
    assert response.json()["message"] == "Data successfully stored in the database"

def test_read_pokemon():
    response = client.get("/pokemon/?sort_by=name&sort_order=asc&search_column=name&keyword=Bulbasaur&page=1&limit=10")
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0
    assert response.json()["results"][0]["name"] == "Bulbasaur"

def test_create_pokemon():
    pokemon_data = {
        "number": 999,
        "name": "Testmon",
        "type_1": "Grass",
        "type_2": "Poison",
        "total": 300,
        "hp": 60,
        "attack": 60,
        "defense": 60,
        "sp_atk": 60,
        "sp_def": 60,
        "speed": 60,
        "generation": 1,
        "legendary": False,
    }
    response = client.post("/pokemon/", json=pokemon_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Testmon"

def test_update_pokemon():
    pokemon_update = {
        "attack": 80,
        "speed": 80
    }
    response = client.put("/pokemon/999", json=pokemon_update)
    assert response.status_code == 200
    assert response.json()["attack"] == 80
    assert response.json()["speed"] == 80

def test_delete_pokemon():
    response = client.delete("/pokemon/999")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.json()}"
    assert response.json()["name"] == "Testmon"

    response = client.get("/pokemon/?sort_by=number&keyword=999")
    assert response.status_code == 404, f"Unexpected status code after deletion: {response.status_code}, Response: {response.json()}"

