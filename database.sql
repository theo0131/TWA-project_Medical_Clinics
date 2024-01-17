--  

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'medical_network';

DROP DATABASE IF EXISTS medical_network;

CREATE DATABASE medical_network;
\c medical_network;

CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE medical_network TO postgres;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    user_password VARCHAR(20) NOT NULL,
    user_type VARCHAR(20) NOT NULL
);

INSERT INTO users (first_name, last_name, email, user_password, user_type)
VALUES ('Jane', 'Doe', 'jane.doe@email.com', 'pwd', 'pacient');
INSERT INTO users (first_name, last_name, email, user_password, user_type)
VALUES ('John', 'Doe', 'john.doe@email.com', 'pwd', 'pacient');
INSERT INTO users (first_name, last_name, email, user_password, user_type)
VALUES ('Mary', 'Jack', 'mary.jack@email.com', 'pwd', 'doctor');
INSERT INTO users (first_name, last_name, email, user_password, user_type)
VALUES ('Zack', 'Donner', 'zack.donner@email.com', 'pwd', 'doctor');
INSERT INTO users (first_name, last_name, email, user_password, user_type)
VALUES ('Cody', 'Choy', 'cody.choy@email.com', 'pwd', 'doctor');

CREATE TABLE pacients (
    pacient_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    gender VARCHAR(1) NOT NULL,
    age INT NOT NULL,
    medical_history VARCHAR(200)
);

INSERT INTO pacients (user_id, gender, age, medical_history)
VALUES (1, 'F', 25, ' ');
INSERT INTO pacients  (user_id, gender, age, medical_history)
VALUES (2, 'M', 35, ' ');

CREATE TABLE medics (
    medic_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    specialization VARCHAR(50)
);

INSERT INTO medics (user_id, specialization)
VALUES (3, 'Oftalmology');
INSERT INTO medics  (user_id, specialization)
VALUES (4, 'Dermatology');
INSERT INTO medics  (user_id, specialization)
VALUES (5, 'GP');

CREATE TABLE specializations (
    sp_id SERIAL PRIMARY KEY,
    sp_name VARCHAR(50)
);

INSERT INTO specializations 
VALUES (1, 'Oftalmology');
INSERT INTO specializations 
VALUES (2, 'Dermatology');
INSERT INTO specializations 
VALUES (3, 'ORL');
INSERT INTO specializations 
VALUES (4, 'GP');
INSERT INTO specializations 
VALUES (5, 'Logopedy');
INSERT INTO specializations 
VALUES (6, 'Oncology');
INSERT INTO specializations 
VALUES (7, 'Cardiology');
INSERT INTO specializations 
VALUES (8, 'Endocrinology');
INSERT INTO specializations 
VALUES (9, 'Immunology');
INSERT INTO specializations 
VALUES (10, 'Emergency Medicine');

CREATE TABLE locations (
    address_id SERIAL PRIMARY KEY,
    address_name VARCHAR(50)
);

INSERT INTO locations
VALUES (1, 'Militari');

CREATE TABLE appointments (
    appmt_id SERIAL PRIMARY KEY,
    pacient_id INT REFERENCES pacients(pacient_id),
    medic_id INT REFERENCES medics(medic_id),
    user_id INT REFERENCES users(user_id),
    sp_id INT REFERENCES specializations(sp_id),
    address_id INT REFERENCES locations(address_id),
    appmt_timestamp VARCHAR(500),
    reason VARCHAR(500),
    diagnostic VARCHAR(500)
);

INSERT INTO appointments 
(pacient_id, medic_id, sp_id, address_id, reason)
VALUES (1, 1, 1, 1, 'Nu vreau sa stau acasa');
