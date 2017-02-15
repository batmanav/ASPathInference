import sqlite3
import MySQLdb

class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()


class MyDatabaseManager:

    dbc = ("localhost","root","manav","gao")

    def __init__(self):
        self.db = MySQLdb.connect(*self.dbc)
        self.cursor = self.db.cursor()

    def query(self, arg):
        self.cursor.execute(arg)
        self.db.commit()
        return self.cursor

    def __del__(self):
        self.cursor.close()