import sqlite3




def initiate_db():
    connection = sqlite3.connect('product_14_5.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    ''')

    connection.commit()
    connection.close()

def check_db(id, title, description, price):
    connection = sqlite3.connect('product_14_5.db')
    cursor = connection.cursor()

    check_db = cursor.execute('SELECT * FROM Product WHERE title=?', (title,))

    if check_db.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Product (id, title, description, price) VALUES('{id}', '{title}', '{description}', '{price}')
''')
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('product_14_5.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Product WHERE id > ?', (0,))
    return cursor.fetchall()

    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect('product_14_5.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'{username}', f'{email}', age, 1000))

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('product_14_5.db')
    cursor = connection.cursor()

    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if check_user.fetchone() is None:
        return True
    else:
        return False

    connection.commit()
    connection.close()


initiate_db()


add_user('newuser', 'user@mail.ru', 30)