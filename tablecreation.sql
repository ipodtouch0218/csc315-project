CREATE SCHEMA goat;

CREATE TABLE animal (
    animal_id
    sex
    status
    dam
);

CREATE TABLE session_animal (
    session_id
    animal_id
    birth_weight
    observations
    milk_rating
    kid_ease
    num_of_kids
    mother_score
    mothering
    PRIMARY KEY (session_id, animal_id)
);