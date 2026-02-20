-- Used Claude Code as reference 

DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TYPE IF EXISTS status CASCADE;

CREATE TYPE status AS ENUM('pending', 'rejected', 'offered', 'applied', 'interview');

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
    UNIQUE(name)
);
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_id INTEGER REFERENCES company(id) ON DELETE CASCADE,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_status status DEFAULT 'applied',
    position_title VARCHAR(255)
);


CREATE INDEX idx_application_status ON applications(application_status);
CREATE INDEX idx_application_company ON applications(company_id);

--

