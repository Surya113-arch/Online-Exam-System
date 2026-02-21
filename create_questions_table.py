import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS questions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
question TEXT,
option1 TEXT,
option2 TEXT,
option3 TEXT,
answer TEXT
)
''')

conn.commit()
conn.close()

print("Questions table created!")