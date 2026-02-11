-- Used Claude Code as reference 

DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS company CASCADE;

CREATE TYPE status AS ENUM('pending','rejected','offered','applied');

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company INTEGER REFERENCES company(id) ON DELETE CASCADE,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_status status DEFAULT 'applied'
);


CREATE INDEX idx_application_status ON applications(application_status);
CREATE INDEX idx_application_company ON applications(company);

