import os
import mysql.connector
from mysql.connector import Error

def get_config():
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "admin123"),
        "password": os.environ.get("DB_PASS", "admin123"),
        "database": os.environ.get("DB_NAME", "estoque"),
        "port": int(os.environ.get("DB_PORT", 3306))
    }

def conectar():
    cfg = get_config()
    try:
        conn = mysql.connector.connect(
            host = cfg["host"],
            user = cfg["user"],
            password = cfg["password"],
            database = cfg["database"],
            port = cfg["port"],
        )

        if conn.is_connected():
            return conn
        
    except Error as e:
        print("Erro conctando ao MySQL: ", e)
        raise