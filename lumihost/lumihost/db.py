"""
Main data storage file
"""

import sqlite3 as sql
from time import time


class BasicDB:
    """Base DB class"""

    def __init__(self, name):
        self.conn = sql.connect(f"{name}.db")
        self.cur = self.conn.cursor()
        self.make()
        self.conn.commit()

    def make(self):
        """Make sure that we have the needed sqlite file (Must be overwriten)"""
        pass


class UsersDB(BasicDB):
    def __init__(self):
        super().__init__("users")

    def make(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
           id INT PRIMARY KEY,
           balance INT,
           subscription INT,
           invited INT,
           userbot TEXT);
        """)

    def make_sure_valid(self, user_id):
        """Make sure that user is in this db"""
        self.cur.execute(
            """INSERT INTO users (id, balance, subscription, invited, userbot) SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT * FROM users WHERE id = ?);""",
            (user_id, 0, 0, 0, "", user_id,)
        )
        self.conn.commit()

    def get_user(self, user_id):
        """Returns a user db list, see `make` to know the order"""
        return self.cur.execute("""SELECT * FROM users WHERE id = ?""", (user_id,)).fetchone()

    def get_subscriptions_days_left(self, user_id):
        """Returns the amount of days of the subscription the user has right now"""
        return (self.get_user(user_id)[2] - int(time())) // 86400


class CryptoPaysDB(BasicDB):
    def __init__(self):
        super().__init__("cryptopays")

    def make(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cryptopays(
           id INT PRIMARY KEY,
           user_id INT);
        """)

    def create_payment(self, payment_id, userid):
        """Insert a payment in this db"""
        self.cur.execute(
            """INSERT INTO cryptopays (id, user_id) SELECT ?, ?;""",
            (payment_id, userid,)
        )
        self.conn.commit()

    def remove_payment(self, payment_id):
        """Delete a payment from this db"""
        self.cur.execute(
            """DELETE FROM cryptopays WHERE id = ?;""",
            (payment_id,)
        )
        self.conn.commit()


users_db = UsersDB()
crypto_db = CryptoPaysDB()
