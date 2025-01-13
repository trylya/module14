import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
    )
''')

for i in range(1, 11):
    cursor.execute(
        'INSERT INTO Users (username, email, age, balance) '
            'VALUES (?, ?, ?, ?)',
        (f'User{i}', f'example{i}@gmail.com', i * 10, 1000))

for i in range(1, 11):
    if i % 2:  # каждая 2-я запись начиная с 1-й
        cursor.execute(
            'UPDATE Users SET balance = 500 WHERE id = ?',
            (i,))

for i in range(1, 11):
    if i % 3 == 1:  # каждая 3-я запись начиная с 1-й
        cursor.execute(
            'DELETE FROM Users WHERE id = ?',
            (i,))

cursor.execute("SELECT * FROM Users WHERE age <> 60")
users = cursor.fetchall()
for user in users:
    id, username, email, age, balance = user
    print(f'Имя: {username} | '
          f'Почта: {email} | '
          f'Возраст: {age} | '
          f'Баланс: {balance}')

connection.commit()
connection.close()