import sqlite3
data = sqlite3.connect('testdata.db')
cursor = data.cursor()
pid = 'p700'
cursor.execute("SELECT mp.name, mp.birthYear \
                FROM moviePeople mp, casts c \
                WHERE mp.pid = c.pid AND c.pid = :pid", {"pid": pid})
nameyear = cursor.fetchone()
name, year = nameyear[0], nameyear[1]
print("The cast member you chose is:\n\tName:", name, "\n\tBirthyear:", year)