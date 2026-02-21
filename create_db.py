import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
''')

conn.commit()
conn.close()

print("Database created successfully")