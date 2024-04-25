DROP SCHEMA IF EXISTS goat;
DROP TABLE IF EXISTS animal CASCADE;
DROP TABLE IF EXISTS session_animal CASCADE;

CREATE SCHEMA goat;

CREATE TABLE animal (
    tag varchar(16),
    animal_id SERIAL PRIMARY KEY,
    sex varchar(13),
    status varchar(8),
    dam varchar(16)
);

CREATE TABLE session_animal (
    session_id SERIAL,
    animal_id SERIAL REFERENCES animal(animal_id),
    birth_weight float,
    observations varchar(30),
    milk_rating varchar(30),
    kid_ease varchar(30),
    num_of_kids varchar(30),
    mother_score varchar(30),
    mothering varchar(30),
    PRIMARY KEY (session_id, animal_id)
);