import sqlite3

connection = sqlite3.connect('product.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')
    connection.commit()



def get_all_products():
    cursor.execute('SELECT * FROM Product')
    return cursor.fetchall()


if __name__ == '__main__':
    initiate_db()
    connection.close()