import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# ---------------- USERS TABLE ---------------- #
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Insert example login user (optional)
cur.execute("""
INSERT OR IGNORE INTO users (username, email, password) 
VALUES (?, ?, ?)
""", ("admin", "admin@example.com", "1234"))

# ---------------- CARBON RESULTS TABLE ---------------- #
cur.execute("""
CREATE TABLE IF NOT EXISTS carbon_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_kg REAL,
    breakdown_json TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database with users & carbon_results table created successfully!")
