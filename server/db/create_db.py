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
            lab_id INTEGER REFERENCES Lab(lab_id),
            temp FLOAT NOT NULL,
            umid FLOAT NOT NULL,
            lum BOOLEAN NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Equip(
            equip_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER NOT NULL REFERENCES Lab(lab_id),
            temp_min FLOAT NOT NULL,
            temp_max FLOAT NOT NULL,
            end_mac CHAR(17) NOT NULL);
    """)

    cursor.execute("""
    CREATE TABLE Arduino(
            arduino_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER NOT NULL REFERENCES Lab(lab_id),
            equip_id INTEGER NOT NULL REFERENCES Equip(equip_id),
            end_mac_arduino CHAR(17) NOT NULL);
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
            user_id CHAR(4) NOT NULL PRIMARY KEY,
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
            lab_id INTEGER REFERENCES Lab(lab_id),
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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    work()
