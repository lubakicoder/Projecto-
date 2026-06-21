from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from app.respositories.crud_admin import consultar_admin_por_username
from app.respositories.crud_medico import consultar_medico_por_crm
from app.respositories.crud_paciente import consultar_paciente_por_id

bp_auth = Blueprint("bp_auth", __name__, url_prefix="/api/auth")


# =====================
# ADMIN LOGIN
# =====================
@bp_auth.route("/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json()

    user = data.get("username")
    password = data.get("password")

    admin = consultar_admin_por_username(user)

    if not admin:
        return jsonify({"success": False, "message": "Admin não encontrado"}), 404

    if not check_password_hash(admin["senha"], password):
        return jsonify({"success": False, "message": "Senha inválida"}), 401

    session["admin_id"] = admin["id"]
    session["admin_user"] = admin["nome"]

    return jsonify({
        "success": True,
        "user": {
            "id": admin["id"],
            "nome": admin["nome"],
            "role": "admin"
        }
    })


# =====================
# MEDICO LOGIN
# =====================
@bp_auth.route("/medico/login", methods=["POST"])
def medico_login():

    data = request.get_json()

    crm = data.get("crm")
    senha = data.get("senha")

    medico = consultar_medico_por_crm(crm)

    if not medico:
        return jsonify({"success": False, "message": "CRM não encontrado"}), 404

    if not check_password_hash(medico["senha"], senha):
        return jsonify({"success": False, "message": "Senha inválida"}), 401

    session["medico_id"] = medico["id"]
    session["medico_nome"] = medico["nome"]
    session["medico_crm"] = medico["crm"]

    return jsonify({
        "success": True,
        "user": {
            "id": medico["id"],
            "nome": medico["nome"],
            "crm": medico["crm"],
            "especialidade": medico["especialidade"],
            "role": "medico"
        }
    })


# =====================
# PACIENTE LOGIN
# =====================
@bp_auth.route("/paciente/login", methods=["POST"])
def paciente_login():

    data = request.get_json()

    bi = data.get("cpf")
    nome = data.get("nome")

    paciente = consultar_paciente_por_id(bi)

    if not paciente:
        return jsonify({"success": False, "message": "Paciente não encontrado"}), 404

    session["paciente_id"] = paciente["id"]
    session["paciente_nome"] = paciente["nome"]
    session["paciente_bi"] = paciente["bi"]

    return jsonify({
        "success": True,
        "user": {
            "id": paciente["id"],
            "nome": paciente["nome"],
            "cpf": paciente["bi"],
            "role": "paciente"
        }
    })


# =====================
# LOGOUT
# =====================
@bp_auth.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({"success": True})
