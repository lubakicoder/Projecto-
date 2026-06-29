import sqlite3
from ..models.db import conectar

def get_conn():
    conn = conectar()
    conn.row_factory = sqlite3.Row  
    return conn

def criar_admin(username, password_hash):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO admin (nome, senha) VALUES (?,?)',(username, password_hash))
        conn.commit()
        return cursor.lastrowid

def consultar_admin_por_username(username):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT *  FROM admin WHERE nome =?', (username,))
        row = cursor.fetchone()
        return dict(row) if row else None 

def listar_admins_db():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM admin')
        rows = cursor.fetchall()
        return [dict(row) for row in rows] 

def deletar_admin(admin_id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM admin WHERE id = ?',
            (admin_id,)
        )
        conn.commit()
