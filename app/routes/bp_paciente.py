from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.services.paciente_service import login_paciente_service, PacienteServiceError
from app.respositories.crud_paciente import (
    consultar_paciente_por_email,
    criar_paciente
)

bp_paciente = Blueprint(
    "bp_paciente",
    __name__,
    url_prefix="/api/auth/paciente"
)

@bp_paciente.route("/register", methods=["POST"])
def register_paciente():
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        bi = dados.get("bi")
        data_nascimento = dados.get("data_nascimento")
        telefone = dados.get("telefone")
        email = dados.get("email")
        senha = dados.get("senha")
        if not all([nome, bi, email, senha]):
            return jsonify({
                "success": False,
                "message": "Campos obrigatórios em falta"
            }), 400

        if consultar_paciente_por_email(email):
            return jsonify({
                "success": False,
                "message": "Email já cadastrado"
            }), 400

        paciente_id = criar_paciente(
            nome=nome,
            bi=bi,
            data_nascimento=data_nascimento,
            telefone=telefone,
            email=email,
            senha=senha
        )

        return jsonify({
            "success": True,
            "paciente": {
                "id": paciente_id,
                "nome": nome,
                "bi": bi,
                "email": email,
                "nascimento": data_nascimento
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@bp_paciente.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    try:
        paciente = login_paciente_service(dados.get("email"), dados.get("senha"))
        return jsonify({
            "success": True,
            "paciente": paciente
        })
    except PacienteServiceError as e:
        return jsonify({
            "success": False,
            "message": e.message
        }), e.code
