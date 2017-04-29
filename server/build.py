import bcrypt
from getpass import getpass
from os import getcwd
from os.path import join
from subprocess import Popen, DEVNULL
from db.create_db import work as create_db

Popen(["virtualenv",
       "-p",
       "python3",
       ".env"],
       stderr=DEVNULL).wait()

with open(join(getcwd(), ".env/bin/activate_this.py"), "r") as f:
    exec(f.read())

Popen([".env/bin/pip",
       "install",
       "-r",
       "requirements.txt"]).wait()

Popen(["mv",
       "config.py.example",
       "config.py"]).wait()

import sqlite3

try:
    create_db()
    Popen(["cp",
           "Issues.db",
           "db/Issues.db"]).wait()
except sqlite3.Error:
    pass

print("Crie um usuário administrador")
print("Usuário:")
usuario = input()
print("Senha:")
senha = getpass("")
print("E-mail:")
email = input()
print("Nome:")
nome = input()

senha = bytes(senha, 'utf-8')
senha = bcrypt.hashpw(senha, bcrypt.gensalt()).decode('utf-8')

conn = sqlite3.connect(join(getcwd(),
                            "db",
                            "Issues.db"))
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO User_Sys
    (login, senha, email, nome, admin)
    VALUES (?, ?, ?, ?, ?);""", (usuario,
                                 senha,
                                 email,
                                 nome,
                                 True))
conn.commit()
conn.close()
print("Administrador criado")

print("Por favor altere as informações no arquivo `config.py`")
