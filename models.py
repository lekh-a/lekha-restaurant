import sqlite3
import datetime

DB_NAME = "restaurant.db" # setting the db filename

# ------------------- User Class --------------------------
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    #------ inserting new user ---------------
    def save(self):
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (self.username, self.password, self.email)
        )
        connection.commit()
        connection.close()

    # -------- authenticate and increment the visits ------
    @staticmethod
    def get_user(username, password):
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            # --- Increase visits count-------
            cursor.execute("UPDATE users SET visits = visits + 1 WHERE id=?", (user[0],))
            connection.commit()

            # --------- Fetch updated user -----
            cursor.execute("SELECT * FROM users WHERE id=?", (user[0],))
            user = cursor.fetchone()

        connection.close()
        return user

    #---------- festching user deatils ----------
    @staticmethod
    def get_user_by_id(user_id):
        connection = sqlite3.connect("restaurant.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        connection.close()
        return user
    
    #---------- updating wallet ----------
    @staticmethod
    def update_wallet(user_id, new_balance):
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET wallet = ? WHERE id = ?", (new_balance, user_id))
        connection.commit()
        connection.close()

# ------------------- Menu Item Class --------------------------------
# class MenuItem:
#     def __init__(self, name, price, category):
#         self.name = name
#         self.price = price
#         self.category = category

#     def save(self):
#         connection = sqlite3.connect(DB_NAME)
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO menu_items (name, price, category) VALUES (?, ?, ?)",
#                        (self.name, self.price, self.category))
#         connection.commit()
#         connection.close()

#     @staticmethod
#     def get_all():
#         connection = sqlite3.connect(DB_NAME)
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM menu_items")
#         items = cursor.fetchall()
#         connection.close()
#         return items




