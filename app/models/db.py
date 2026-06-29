import os
import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "sistema.db")

def conectar():
    return sqlite3.connect(DB)

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Cria todas tabelas + admin padrão se banco for novo"""
    db = conectar() 
    cur = db.cursor()
    
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS paciente(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        bi TEXT NOT NULL UNIQUE,
        data_nascimento TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS medico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crm TEXT NOT NULL UNIQUE,
        nome TEXT NOT NULL,
        especialidade TEXT NOT NULL,
        senha TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    );

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
        FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
        FOREIGN KEY (medico_id) REFERENCES medico(id) ON DELETE SET NULL
    );
    """)

    # Cria admin padrão só 1 vez
    cur.execute("SELECT 1 FROM admin WHERE nome = ?", ('admin',))
    if cur.fetchone() is None:
        pwd_hash = generate_password_hash('admin123') # TROCA DEPOIS
        cur.execute("INSERT INTO admin (nome, senha) VALUES (?, ?)", ('admin', pwd_hash))
        print(">>> Admin criado: admin / admin123 <<<")

    db.commit()

def init_app(app):
    """Chama no __init__.py"""
    app.teardown_appcontext(close_db)
    with app.app_context():
        os.makedirs(app.config['INSTANCE_PATH'], exist_ok=True)
        init_db()
