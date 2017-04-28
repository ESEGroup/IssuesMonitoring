import sqlite3

class DB:
    def __init__(self, name):
        self.name = name

    def connect(self):
        conn = sqlite3.connect(self.name)
        return conn

    def execute(self, query, arguments=tuple(), return_id=False):
        pk = None

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, arguments)

        if return_id:
            cursor.execute("SELECT last_insert_rowid();")
            pk = cursor.fetchone()[0]

        conn.commit()
        conn.close()
        return pk

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
