-- Table definition for the HR attrition database (SQLite)

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id                 INTEGER PRIMARY KEY,
    age                         INTEGER,
    gender                      TEXT,
    marital_status              TEXT,
    education                   TEXT,
    department                  TEXT,
    job_role                    TEXT,
    job_level                   INTEGER,   -- 1 = Junior, 2 = Mid, 3 = Senior
    city                        TEXT,
    distance_from_home_km       INTEGER,
    monthly_income              INTEGER,   -- in INR
    overtime                    TEXT,      -- 'Yes' / 'No'
    job_satisfaction            INTEGER,   -- 1 (low) to 4 (very high)
    work_life_balance           INTEGER,   -- 1 (bad) to 4 (best)
    performance_rating          INTEGER,   -- 2 to 4
    years_at_company            INTEGER,
    years_since_last_promotion  INTEGER,
    training_times_last_year    INTEGER,
    attrition                   TEXT       -- 'Yes' = employee left
);
