import sqlite3
from ..models.db import conectar
from werkzeug.security import generate_password_hash

def criar_paciente(nome, bi, data_nascimento, telefone, email, senha):

    with conectar() as conn:
        cursor = conn.cursor()
        senha_hash = generate_password_hash(senha)
        cursor.execute("""
        INSERT INTO paciente(
            nome,
            bi,
            data_nascimento,
            telefone,
            email,
            senha
        )
        VALUES(?,?,?,?,?,?)
        """, (
            nome,
            bi,
            data_nascimento,
            telefone,
            email,
            senha_hash
        ))
        conn.commit()
        return cursor.lastrowid

def consultar_paciente_por_bi(bi):

    with conectar() as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM paciente
        WHERE bi=?
        """, (bi,))

        paciente = cursor.fetchone()

        return dict(paciente) if paciente else None

def consultar_paciente_por_id(id):

    with conectar() as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM paciente
        WHERE id=?
        """, (id,))

        paciente = cursor.fetchone()

        return dict(paciente) if paciente else None


def consultar_paciente_por_email(email):
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM paciente WHERE email=?",
            (email,)
        )
        paciente = cursor.fetchone()
        return dict(paciente) if paciente else None

def consultar_pacientes():
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                id,
                nome,
                bi,
                nascimento,
                telefone,
                email
            FROM paciente
            ORDER BY id DESC
        """)
        pacientes = cursor.fetchall()
        return [dict(p) for p in pacientes]
