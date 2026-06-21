from flask import Blueprint, request, jsonify, session
from app.respositories.crud_atendimento import *

bp_atendimento = Blueprint("bp_atendimento", __name__, url_prefix="/api/atendimentos")


# =====================
# LISTAR
# =====================
@bp_atendimento.route("", methods=["GET"])
def listar():

    dados = consultar_atendimentos()

    return jsonify({
        "success": True,
        "atendimentos": dados
    })


# =====================
# CRIAR (PACIENTE)
# =====================
@bp_atendimento.route("", methods=["POST"])
def criar():

    if "paciente_id" not in session:
        return jsonify({"success": False}), 401

    data = request.get_json()

    criar_atendimento(
        paciente_id=session["paciente_id"],
        medico_id=None,
        idade=data["idade"],
        sintomas=str(data["sintomas"]),
        intensidade=data["intensidade"],
        observacoes=data['observacao'],
        prioridade="urgente" if data["intensidade"] >= 8 else "moderado" if data["intensidade"] >= 5 else "leve",
        status="pendente"
    )

    return jsonify({"success": True})


# =====================
# CONCLUIR (MEDICO)
# =====================
@bp_atendimento.route("/<int:id>", methods=["PUT"])
def concluir(id):

    if "medico_id" not in session:
        return jsonify({"success": False}), 401

    data = request.get_json()

    atualizar_status_atendimento(id, "concluido")

    return jsonify({"success": True})
