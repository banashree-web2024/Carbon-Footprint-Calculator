import sqlite3

conn = sqlite3.connect("users.db")   # <-- correct DB for your app
cur = conn.cursor()

# Add full_name
try:
    cur.execute("ALTER TABLE users ADD COLUMN full_name TEXT;")
    print("Added: full_name")
except Exception as e:
    print("full_name already exists or error:", e)

# Add email
try:
    cur.execute("ALTER TABLE users ADD COLUMN email TEXT;")
    print("Added: email")
except Exception as e:
    print("email already exists or error:", e)

conn.commit()
conn.close()

print("Fix completed!")

