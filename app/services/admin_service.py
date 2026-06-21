from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.respositories.crud_admin import criar_admin, consultar_admin_por_username, listar_admins_db
           

def login_admin_service(username, password):
    if not username or not password:
        raise Exception("Usuário e senha obrigatórios")

    admin = consultar_admin_por_username(username)
    if not admin:
        raise Exception("Usuário não encontrado")

    if not check_password_hash(admin['senha'], password):
        raise Exception("Senha incorreta")

    session['admin_id'] = admin['id']
    session['admin_user'] = admin['nome']

    return {
        "id": admin['id'],
        "nome": admin['nome']
    }


def criar_admin_service(username, password):
    if not username or not password:
        raise Exception("Usuário e senha obrigatórios")

    if consultar_admin_por_username(username):
        raise Exception("Usuário já existe")

    hash_pass = generate_password_hash(password)
    admin_id = criar_admin(username, hash_pass)

    return {
        "id": admin_id,
        "nome": username
    }


def logout_admin_service():
    session.pop('admin_id', None)
    session.pop('admin_user', None)


def listar_admins_service():
    return listar_admins_db()
