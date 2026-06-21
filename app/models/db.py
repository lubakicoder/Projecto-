import sqlite3


def conectar():
    conn = sqlite3.connect('database.db')
    return conn

def tbl_paciente():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paciente(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bi INTEGER NOT NULL,
                nome TEXT NOT NULL
            )
        ''')
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
        idade INTEGER NOT NULL,
        sintomas TEXT NOT NULL,
        intensidade INTEGER NOT NULL,
        observacoes TEXT,
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
