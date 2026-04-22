import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Add full_name if missing
try:
    cur.execute("ALTER TABLE users ADD COLUMN full_name TEXT;")
    print("Added: full_name")
except:
    print("full_name already exists")

# Add email if missing
try:
    cur.execute("ALTER TABLE users ADD COLUMN email TEXT;")
    print("Added: email")
except:
    print("email already exists")

conn.commit()
conn.close()

print("Fix completed!")
