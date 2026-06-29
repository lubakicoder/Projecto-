from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from werkzeug.security import check_password_hash, generate_password_hash
from app.respositories import crud_medico
from app.respositories.crud_paciente import consultar_pacientes
from app.respositories.crud_atendimento import consultar_atendimentos


bp_medico = Blueprint(
    'bp_medico',
    __name__,
    url_prefix='/api/auth/medico'
)


@bp_medico.route("/login", methods=["POST"])
def login_medico():
    dados = request.get_json()
    crm = dados.get("crm")
    senha = dados.get("senha")
    medico = crud_medico.consultar_medico_por_crm(crm)
    if not medico:
        return jsonify({"success": False, "message": "CRM inválido"}), 401

    if not check_password_hash(medico["senha"], senha):
        return jsonify({"success": False, "message": "Senha inválida"}), 401
    session["medico_id"] = medico["id"]
    session["medico_nome"] = medico["nome"]
    session["medico_crm"] = medico["crm"]
    return jsonify({
        "success": True,
        "medico": {
            "nome": medico["nome"],
            "crm": medico["crm"],
            "especialidade": medico["especialidade"]
        }
    })

@bp_medico.route("/register", methods=["POST"])
def register_medico():
    dados = request.get_json()
    crm = dados.get("crm")
    nome = dados.get("nome")
    espec = dados.get("espec")
    senha = dados.get("senha")
    if not crm or not nome or not senha:
        return jsonify({
            "success": False,
            "message": "Campos obrigatórios"
        }), 400
    medico = crud_medico.consultar_medico_por_crm(crm)
    if medico:
        return jsonify({
            "success": False,
            "message": "Médico já existe"
        }), 400
    senha_hash = generate_password_hash(senha)
    crud_medico.criar_medico(
        crm=crm,
        nome=nome,
        especialidade=espec,
        senha=senha_hash
    )
    return jsonify({
        "success": True,
        "message": "Médico criado"
    })
