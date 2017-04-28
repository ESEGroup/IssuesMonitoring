import sqlite3

class DB:
    def __init__(self, name):
        self.name = name

    def connect(self):
        conn = sqlite3.connect(self.name)
        return conn

    def execute(self, query, arguments=tuple()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, arguments)
        conn.commit()
        conn.close()

    def executemany(self, query, list_of_arguments=[tuple()]):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany(query, list_of_arguments)
        conn.commit()
        conn.close()

    def fetchone(self, query, arguments=tuple()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, arguments)
        data = cursor.fetchone()
        conn.close()
        return data

    def fetchall(self, query, arguments=tuple()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, arguments)
        data = cursor.fetchall()
        conn.close()
        return data

    def get_pk(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT last_insert_rowid();")
        data = cursor.fetchone()
        conn.close()
        return data[0]
