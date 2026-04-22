CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS carbon_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_kg REAL,
    breakdown_json TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
