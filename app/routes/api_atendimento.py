from flask import Blueprint, request, jsonify, session
from app.respositories.crud_atendimento import (
    consultar_atendimentos,
    criar_atendimento,
    concluir_atendimento
)

bp_atendimento = Blueprint(
    "bp_atendimento",
    __name__,
    url_prefix="/api/atendimentos"
)



@bp_atendimento.route("", methods=["GET"])
def listar():
    atendimentos = consultar_atendimentos()

    for a in atendimentos:
        if isinstance(a["sintomas"], str):
            a["sintomas"] = a["sintomas"].split(",") if a["sintomas"] else []
        elif a["sintomas"] is None:
            a["sintomas"] = []

    return jsonify({
        "success": True,
        "atendimentos": atendimentos
    })

@bp_atendimento.route("", methods=["POST"])
def criar():

    if "paciente_id" not in session:
        return jsonify({
            "success": False,
            "message": "Paciente não autenticado"
        }), 401

    try:
        dados = request.get_json()
        sintomas = dados.get("sintomas", [])
        intensidade = int(dados.get("intensidade") or 0)
        observacao = dados.get("observacao", "")
        prioridade = (
            "urgente"
            if intensidade >= 8
            else "moderado"
            if intensidade >= 5
            else "leve"
        )

        criar_atendimento(
            paciente_id=session["paciente_id"],
            medico_id=None,
            sintomas=",".join(sintomas),
            intensidade=intensidade,
            observacao=observacao,
            diagnostico=None,
            prioridade=prioridade,
            status="pendente"
        )

        return jsonify({
            "success": True,
            "message": "Atendimento criado"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


@bp_atendimento.route("/<int:id>", methods=["PUT"])
def concluir(id):

    if "medico_id" not in session:
        return jsonify({
            "success": False,
            "message": "Médico não autenticado"
        }), 401

    try:
        dados = request.get_json()
        diagnostico = dados.get("diagnostico")
        concluir_atendimento(
            id,
            diagnostico
        )

        return jsonify({
            "success": True,
            "message": "Atendimento concluído"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


