-- pokemon_database_creation.sql
CREATE DATABASE pokemon_db;

-- pokemon_table_creation.sql
CREATE TABLE pokemon (
    pokemon_id SERIAL PRIMARY KEY, 
    number INTEGER UNIQUE NOT NULL,
    name VARCHAR(40) NOT NULL,
    type_1 VARCHAR(40) NOT NULL,
    type_2 VARCHAR(40),
    total INTEGER NOT NULL,
    hp INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    sp_atk INTEGER NOT NULL,
    sp_def INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    generation INTEGER NOT NULL,
    legendary BOOLEAN NOT NULL
);

-- pokemon_table_insert.sql
INSERT INTO pokemon (number, name, type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary)
VALUES
    (1, 'Bulbasaur', 'Grass', 'Poison', 318, 45, 49, 49, 65, 65, 45, 1, false),
    (25, 'Pikachu', 'Electric', NULL, 320, 35, 55, 40, 50, 50, 90, 1, false)

-- pokemon_table_delete_by_pokemon_id.sql
DELETE FROM pokemon WHERE pokemon_id = 1;
DELETE FROM pokemon WHERE name = 'Pikachu';