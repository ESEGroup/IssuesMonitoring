"""
Created on Wed Apr 26 11:36:42 2017

@author: Bruno Dias
"""

import sqlite3

conn = sqlite3.connect('Issues.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

print("Tables: ")
print(cursor.fetchall())

print("\nTable Zona_de_Conforto_Lab")
meta = cursor.execute("PRAGMA table_info('Zona_de_Conforto_Lab')")
for r in meta:
    print(r)

print("\nTable Lab")
meta = cursor.execute("PRAGMA table_info('Lab')")
for r in meta:
    print(r)

print("\nTable Log_Lab")
meta = cursor.execute("PRAGMA table_info('Log_Lab')")
for r in meta:
    print(r)

print("\nTable Equip")
meta = cursor.execute("PRAGMA table_info('Equip')")
for r in meta:
    print(r)

print("\nTable Log_Equip")
meta = cursor.execute("PRAGMA table_info('Log_Equip')")
for r in meta:
    print(r)

print("\nTable User_Lab")
meta = cursor.execute("PRAGMA table_info('User_Lab')")
for r in meta:
    print(r)

print("\nTable Presenca")
meta = cursor.execute("PRAGMA table_info('Presenca')")
for r in meta:
    print(r)

print("\nTable Log_Presenca")
meta = cursor.execute("PRAGMA table_info('Log_Presenca')")
for r in meta:
    print(r)

print("\nTable User_Sys")
meta = cursor.execute("PRAGMA table_info('User_Sys')")
for r in meta:
    print(r)
