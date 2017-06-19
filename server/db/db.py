import sqlite3
import os.path

class DB:
    def __init__(self, name):
        self.name = name
        # self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def connect(self):
        conn = sqlite3.connect(self.name)
        # db_path = os.path.join(self.base_dir, "Issues.db")
        # conn = sqlite3.connect(db_path)
        return conn

    def __execute(self, function, query, arguments, return_id, fetch):
        conn = self.connect()
        cursor = conn.cursor()

        sqlite3.Cursor.__dict__[function](cursor, query, arguments)
        conn.commit()

        if fetch is not None:
            data = sqlite3.Cursor.__dict__[fetch](cursor)
        elif return_id:
            cursor.execute("SELECT last_insert_rowid();")
            data = cursor.fetchone()[0]
        else:
            data = None

        conn.close()
        return data

    def __retry(self, function, query, arguments, return_id=None, fetch=None):
        _tries = 2
        while(_tries > 0):
            try:
                pk = DB.__execute(self,
                                  function,
                                  query,
                                  arguments,
                                  return_id,
                                  fetch)
                _tries = 0
            except sqlite3.Error:
                _tries -= 1
                if _tries == 0:
                    raise

        return pk

    def execute(self, query, arguments=tuple(), return_id=False):
        return DB.__retry(self, "execute", query, arguments, return_id)

    def executemany(self, query, list_of_arguments=[tuple()]):
        DB.__retry(self, "executemany", query, list_of_arguments)

    def fetchone(self, query, arguments=tuple()):
        return DB.__retry(self,
                          "execute",
                          query,
                          arguments,
                          fetch="fetchone")

    def fetchall(self, query, arguments=tuple()):
        return DB.__retry(self,
                          "execute",
                          query,
                          arguments,
                          fetch="fetchall")
