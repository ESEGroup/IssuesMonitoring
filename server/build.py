import sqlite3
from subprocess import Popen
from .issues_monitoring.models import AdministradorSistema
from .db.create_db import work as create_db

Popen(["virtualenv",
       "-p",
       "python3",
       ".env"])
Popen(["source",
       ".env/bin/activate"])
Popen(["pip",
       "install",
       "-r",
       "requirements.txt"])
Popen(["cp",
       "config.py.example",
       "config.py"])

try:
    create_db()
except sqlite3.Error:
    pass

print("Crie um usuário administrador")
print("Usuário:")
usuario = input()
print("Senha:")
senha = input()
print("E-mail:")
email = input()
print("Nome:")
nome = input()

administrador = AdministradorSistema(usuario,
                                     senha,
                                     email,
                                     nome)
administrador.cadastrar()
print("Administrador criado")

print("Por favor altere as informações no arquivo `config.py`")
