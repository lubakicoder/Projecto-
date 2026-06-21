import sqlite3
from ..models.db import conectar


def listar_medicos():
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT id,
                   crm,
                   nome,
                   especialidade
            FROM medico
            '''
        )
        return [dict(row) for row in cursor.fetchall()]

def consultar_medico_por_crm(crm):
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM medico
            WHERE crm = ?
            ''',
            (crm,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

def criar_medico(crm, nome, especialidade, senha):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO medico (crm, nome, especialidade, senha) VALUES (?, ?, ?, ?)', (crm, nome, especialidade, senha))
        conn.commit()

