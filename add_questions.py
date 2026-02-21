import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

questions = [
("Python is?", "Programming Language", "Animal", "Car", "Food", "Programming Language"),

("HTML stands for?", "Hyper Text Markup Language", "High Text Machine Language", "Hyper Tool Multi Language", "None", "Hyper Text Markup Language"),

("Which symbol used for comment in Python?", "#", "//", "/* */", "<!-- -->", "#")
]

cursor.executemany("INSERT INTO questions(question, option1, option2, option3, option4, answer) VALUES(?,?,?,?,?,?)", questions)

conn.commit()
conn.close()

print("Questions inserted!")