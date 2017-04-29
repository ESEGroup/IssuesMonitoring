import sqlite3

class DB:
    def __init__(self, name):
        self.name = name

    def connect(self):
        conn = sqlite3.connect(self.name)
        return conn

    def execute(self, query, arguments=tuple(), return_id=False):
        pk = None
        _tries = 2
        while(_tries > 0):
            try:
                conn = self.connect()
                cursor = conn.cursor()
                cursor.execute(query, arguments)

                if return_id:
                    cursor.execute("SELECT last_insert_rowid();")
                    pk = cursor.fetchone()[0]

                conn.commit()
                conn.close()
                _tries = 0
            except sqlite3.Error:
                _tries -= 1
                if _tries == 0:
                    raise

        return pk

    def executemany(self, query, list_of_arguments=[tuple()]):
        _tries = 2
        while(_tries > 0):
            try:
                conn = self.connect()
                cursor = conn.cursor()
                cursor.executemany(query, list_of_arguments)
                conn.commit()
                conn.close()
                _tries = 0
            except sqlite3.Error:
                _tries -= 1
                if _tries == 0:
                    raise

    def fetchone(self, query, arguments=tuple()):
        _tries = 2
        while(_tries > 0):
            try:
                conn = self.connect()
                cursor = conn.cursor()
                cursor.execute(query, arguments)
                data = cursor.fetchone()
                conn.close()
                _tries = 0
            except sqlite3.Error:
                _tries -= 1
                if _tries == 0:
                    raise
        return data

    def fetchall(self, query, arguments=tuple()):
        _tries = 2
        while(_tries > 0):
            try:
                conn = self.connect()
                cursor = conn.cursor()
                cursor.execute(query, arguments)
                data = cursor.fetchall()
                conn.close()
                _tries = 0
            except sqlite3.Error:
                _tries -= 1
                if _tries == 0:
                    raise
        return data
