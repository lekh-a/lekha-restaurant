import sqlite3

connection = sqlite3.connect('restaurant.db') 
cursor = connection.cursor()


# USERS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT,
    visits INTEGER DEFAULT 0,
    wallet REAL DEFAULT 1000
)
''')

# ---------- Menu Item table ------------------
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS menu_items (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE,
#     price REAL,
#     category TEXT
# )
# ''')

# ----------Orders table ---------------
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS orders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     customer_id INTEGER,
#     total REAL,
#     discount REAL,
#     final_total REAL,
#     order_date TEXT,
#     FOREIGN KEY(customer_id) REFERENCES users(id)
# )
# ''')

connection.commit()
connection.close()
print("✅ Database created successfully!")
