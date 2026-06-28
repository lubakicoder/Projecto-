from app.respositories.crud_paciente import consultar_pacientes, criar_paciente, consultar_paciente_por_email, consultar_paciente_por_bi
from flask import session
from werkzeug.security import check_password_hash


class PacienteServiceError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


def cadastrar_paciente_service(
    nome,
    bi,
    data_nascimento,
    telefone,
    email,
    senha
):

    if not all([
        nome,
        bi,
        data_nascimento,
        telefone,
        email,
        senha
    ]):
        raise Exception("Todos os campos são obrigatórios")

    if consultar_paciente_por_bi(bi):
        raise Exception("BI já cadastrado")

    if consultar_paciente_por_email(email):
        raise Exception("Email já cadastrado")

    paciente_id = criar_paciente(
        nome,
        bi,
        data_nascimento,
        telefone,
        email,
        senha
    )

    return {
        "id": paciente_id,
        "nome": nome,
        "bi": bi
    }


def login_paciente_service(email, senha):
    if not email or not senha:
        raise PacienteServiceError("Email e senha obrigatórios", 400)
    email = email.strip().lower()
    paciente = consultar_paciente_por_email(email)

    if not paciente:
        raise PacienteServiceError("Paciente não encontrado", 404)

    if not paciente.get("senha"):
        raise PacienteServiceError("Conta sem senha cadastrada", 400)

    if not check_password_hash(paciente["senha"], senha):
        raise PacienteServiceError("Senha incorreta", 401)

    session["paciente_id"] = paciente["id"]
    session["paciente_nome"] = paciente["nome"]
    session["paciente_bi"] = paciente["bi"]

    return {
        "id": paciente["id"],
        "nome": paciente["nome"],
        "bi": paciente["bi"],
        "email": paciente["email"]
    }


def listar_pacientes_service():
    pacientes = consultar_pacientes()
    return pacientes

def logout_paciente_service():
    session.pop('paciente_id', None)
    session.pop('paciente_nome', None)
    session.pop('paciente_bi', None)

