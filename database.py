# database.py
import sqlite3

def conectar_db(db_path="inventario.db"):
    conn = sqlite3.connect(db_path)
    return conn