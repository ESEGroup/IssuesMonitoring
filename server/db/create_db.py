"""
@author Bruno Dias

"""

import sqlite3

def work():
    conn = sqlite3.connect('Issues.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys")

    cursor.execute("""
    CREATE TABLE Zona_de_Conforto_Lab(
            zona_conforto_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            temp_min FLOAT NOT NULL,
            temp_max FLOAT NOT NULL,
            umid_min FLOAT NOT NULL,
            umid_max FLOAT NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Lab(
            lab_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            zona_conforto_id INTEGER NOT NULL REFERENCES Zona_de_Conforto_Lab(zona_conforto_id),
            nome CHAR(255) NOT NULL,
            endereco CHAR(255) NOT NULL,
            intervalo_parser INTEGER NOT NULL,
            intervalo_arduino INTEGER NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Log_Lab(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL,
            lab_id INTEGER NOT NULL REFERENCES Lab(lab_id),
            temp FLOAT NOT NULL,
            umid FLOAT NOT NULL,
            lum BOOLEAN NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Equip(
            equip_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome CHAR(255) NOT NULL,
            descricao CHAR(255) NOT NULL,
            lab_id INTEGER NOT NULL REFERENCES Lab(lab_id),
            temp_min FLOAT NOT NULL,
            temp_max FLOAT NOT NULL,
            end_mac CHAR(17) NOT NULL,
            parent_id INTEGER);
    """)

    cursor.execute("""
    CREATE TABLE Log_Equip(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL,
            equip_id INTEGER NOT NULL REFERENCES Equip(equip_id),
            temp FLOAT NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE User_Lab(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id CHAR(4) NOT NULL,
            nome CHAR(255) NOT NULL,
            email CHAR(255) NOT NULL,
            data_aprov INTEGER);
    """)

    cursor.execute("""
    CREATE TABLE Presenca(
            presenca_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id CHAR(4) NOT NULL REFERENCES User_Labs(user_id),
            lab_id INTEGER NOT NULL REFERENCES Lab(lab_id),
            presente BOOLEAN NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Log_Presenca(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL,
            user_id CHAR(4) NOT NULL REFERENCES User_Labs(user_id),
            lab_id INTEGER NOT NULL REFERENCES Lab(lab_id),
            evento CHAR(3) NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE User_Sys(
            user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            login CHAR(255) NOT NULL,
            senha CHAR(60) NOT NULL,
            email CHAR(255) NOT NULL,
            nome CHAR(255) NOT NULL,
            data_aprov INTEGER,
            admin BOOLEAN NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Log_Parser(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Log_MyDenox(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL,
            evento CHAR(255) NOT NULL,
            slug CHAR(255) NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Sistema(
            ultima_analise INTEGER NOT NULL,
            intervalo_parser INTEGER NOT NULL);
    """)

    cursor.execute("""
    INSERT INTO Sistema
    (ultima_analise, intervalo_parser)
    VALUES (0, 3);
    """)

    cursor.execute("""
    CREATE TABLE Anomalias(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            slug CHAR(255) UNIQUE NOT NULL,
            tipo_anomalia CHAR(255) NOT NULL,
            descricao_anomalia CHAR(255) NOT NULL);
    """)

    cursor.executemany("""
    INSERT INTO Anomalias
    (id, slug, tipo_anomalia, descricao_anomalia)
    VALUES (?, ?, ?, ?);""",
    [(1, "temp-min", "Temperatura Abaixo", "Temperatura {}ºC do laboratório abaixo do mínimo da Zona de Conforto ({}ºC)"),
     (2, "temp-max", "Temperatura Acima", "Temperatura {}ºC do laboratório acima do máximo da Zona de Conforto ({}ºC)"),
     (3, "umid-min", "Umidade Abaixo", "Umidade {}% do laboratório abaixo do mínimo da Zona de Conforto {}%"),
     (4, "umid-max", "Umidade Acima", "Umidade {}% do laboratório acima do máximo da Zona de Conforto {}%"),
     (5, "temp-equip-min", "Temperatura de Equipamento Abaixo", "Temperatura {}ºC do Equipamento {} abaixo do mínimo da Zona de Conforto ({}ºC)"),
     (6, "temp-equip-max", "Temperatura de Equipamento Acima", "Temperatura {}ºC do Equipamento {} acima do máximo da Zona de Conforto ({}ºC)"),
     (7, "luz", "Luz acesa sem pessoas presentes", "Luz do laboratório está acesa sem usuários presentes"),
     (8, "imap", "Falha na conexão com servidor de e-mail", "Falha na comunicação com o servidor IMAP para ler os e-mails de registro de presença no laboratório")]) 

    cursor.execute("""
    CREATE TABLE Log_Anomalias(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL,
            lab_id INTEGER REFERENCES Lab(lab_id),
            equip_id INTEGER,
            slug_anomalia CHAR(255) NOT NULL REFERENCES Anomalias(slug),
            valor INTEGER,
            valor_limite INTEGER,
            resolvido BOOLEAN NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Log_Acoes(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data INTEGER NOT NULL,
            id_log_anomalia INTEGER NOT NULL REFERENCES Log_Anomalias(id),
            descricao_acao CHAR(255) NOT NULL,
            autor INTEGER NOT NULL REFERENCES User_Sys(user_id));
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    work()
