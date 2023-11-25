CREATE DATABASE medical_network;
\c medical_network; -- Connect to the database

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    user_password VARCHAR(20) NOT NULL,
    user_type VARCHAR(20) NOT NULL
);

CREATE TABLE pacients (
    pacient_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    sex VARCHAR(1) NOT NULL,
    age INT NOT NULL,
    medical_history VARCHAR(200)
);

CREATE TABLE medics (
    medic_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    specialization VARCHAR(50)
);

CREATE TABLE specializations (
    sp_id SERIAL PRIMARY KEY,
    sp_name VARCHAR(50)
);

CREATE TABLE locations (
    address_id SERIAL PRIMARY KEY,
    address_name VARCHAR(50)
);

CREATE TABLE appointments (
    appmt_id SERIAL PRIMARY KEY,
    pacient_id INT REFERENCES pacients(pacient_id),
    medic_id INT REFERENCES medics(medic_id),
    user_id INT REFERENCES users(user_id),
    sp_id INT REFERENCES specializations(sp_id),
    address_id INT REFERENCES locations(address_id),
    appmt_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    diagnostic VARCHAR(200)
);
