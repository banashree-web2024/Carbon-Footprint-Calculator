py import sqlite3

conn = sqlite3.connect("users.db")   # <-- Your actual DB
cur = conn.cursor()

# Add missing columns one by one
columns = [
    ("total_kg", "REAL"),
    ("breakdown_json", "TEXT"),
    ("recommendations", "TEXT")
]

for column, dtype in columns:
    try:
        cur.execute(f"ALTER TABLE carbon_results ADD COLUMN {column} {dtype};")
        print(f"Added column: {column}")
    except Exception as e:
        print(f"Column {column} already exists or error: {e}")

conn.commit()
conn.close()

print("carbon_results table fix completed!")

