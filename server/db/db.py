import sqlite3

class DB:
    def __init__(self, name):
        self.name = name

    def connect(self):
        conn = sqlite3.connect(self.name)
        return conn
