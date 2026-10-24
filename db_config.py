import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "",
    "database": "db_sistem_pakar",
    "charset":  "utf8mb4",
    "use_pure": True,   # FIX: Hindari crash 0xC0000005 di Windows (C extension mysql-connector 9.x)
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None

def test_connection():
    conn = get_connection()
    if conn:
        ver = conn.server_info
        conn.close()
        return True, f"Terhubung ke MySQL Server v{ver}"
    return False, "Gagal terhubung ke database."

def fetch_all(query, params=None):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Error as e:
        print(f"[QUERY ERROR] {e}")
        return []
    finally:
        conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    if not conn:
        return -1
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[EXEC ERROR] {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()
