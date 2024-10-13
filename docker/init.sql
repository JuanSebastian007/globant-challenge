CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    department VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    job VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    datetime TIMESTAMP WITHOUT TIME ZONE,
    department_id INTEGER,
    job_id INTEGER
);