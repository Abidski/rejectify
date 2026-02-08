-- Used Claude Code as reference 

DROP TABLE IF EXIST applications CASCADE;
DROP TABLE IF EXIST companies CASCADE;

CREATE TYPE status AS ENUM('pending','rejected','offered','applied')

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company INTEGER REFERENCES company(id) ON DELETE CASCADE,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    aplication_status status DEFAULT 'applied'
);

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
    from VARCHAR(255) NOT NULL
    subject VARCHAR(255) NOT NULL
);

CREATE INDEX idx_application_status ON applications(status)
CREATE INDEX idx_application_company ON applications(company)
CREATE INDEX idx_application_status ON applications(status)

