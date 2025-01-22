import sqlite3

connection = sqlite3.connect('product.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER)
''')

for i in range(1, 4):
    cursor.execute(
        'INSERT INTO Product (title,description, price)'
            'VALUES (?, ?, ?)',
        (f'Продукт{i}', f'Описание{i}', i * 100, ))

cursor.execute("SELECT * FROM Product WHERE price > 1")
productes = cursor.fetchall()
for product in productes:
    id, title, description, price = product
    print(f'Продукт: {title} | '
          f'Описание: {description} | '
          f'Цена: {price}')

connection.commit()
connection.close()