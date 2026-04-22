import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(users);")
columns = cur.fetchall()

print("COLUMNS IN USERS TABLE:")
for col in columns:
    print(col)

conn.close()
