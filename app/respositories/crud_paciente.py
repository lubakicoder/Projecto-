import sqlite3
from ..models.db import conectar

def _get_conn():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    return conn

def consultar_pacientes():
    with _get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, bi, nome FROM paciente')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def consultar_paciente_por_id(bi):
    with _get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM paciente
            WHERE bi = ?
            ''',
            (bi,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
def criar_paciente(bi, nome):
    with _get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO paciente (bi, nome) VALUES (?, ?)', (bi, nome))
        conn.commit()
        return cursor.lastrowid
