import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database/app.db")

def conectar():
    conn = sqlite3.connect(DB_PATH)
    return conn

def tbl_paciente():
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS paciente(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            bi TEXT NOT NULL UNIQUE,
            data_nascimento TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

def tbl_medico():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crm TEXT NOT NULL,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()

def tbl_admin():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()

def tbl_atendimento():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        medico_id INTEGER,
        sintomas TEXT NOT NULL,
        intensidade INTEGER NOT NULL,
        observacao TEXT,
        diagnostico TEXT,
        prioridade TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        data TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id)
        REFERENCES paciente(id)
        ON DELETE CASCADE,
        FOREIGN KEY (medico_id)
        REFERENCES medico(id)
        ON DELETE SET NULL
        )''')
        conn.commit()
