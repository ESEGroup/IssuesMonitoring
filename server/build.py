import sqlite3
from datetime import datetime
from getpass import getpass
from os import getcwd
from os.path import join, isfile
from subprocess import Popen, DEVNULL
from db.create_db import work as create_db

Popen(["virtualenv",
       "-p",
       "python3",
       ".env"],
       stderr=DEVNULL).wait()

Popen([".env/bin/pip",
       "install",
       "-r",
       "requirements.txt"]).wait()

if not isfile("config.py"):
    Popen(["cp",
           "config.py.example",
           "config.py"]).wait()

__file__ = join(".env", "bin", "activate_this.py")
with open(join(".env", "bin", "activate_this.py"), "r") as f:
    exec(f.read())

import bcrypt

if not isfile("db/Issues.db"):
    create_db()
    Popen(["mv",
           "Issues.db",
           "db/Issues.db"]).wait()

print("")
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

now = int(datetime.now().timestamp())

conn = sqlite3.connect(join(getcwd(),
                            "db",
                            "Issues.db"))
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO User_Sys
    (login, senha, email, nome, admin, data_aprov)
    VALUES (?, ?, ?, ?, ?);""", (usuario,
                                 senha,
                                 email,
                                 nome,
                                 True,
                                 now))
conn.commit()
conn.close()
print("Administrador criado")

print("Por favor altere as informações no arquivo `config.py`")
