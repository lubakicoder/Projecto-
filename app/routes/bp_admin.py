from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from app.respositories.crud_admin import (
    consultar_admin_por_username,
    listar_admins_db
)
from app.respositories.crud_medico import listar_medicos
from app.respositories.crud_paciente import consultar_pacientes
from app.respositories.crud_atendimento import consultar_atendimentos
from app.services.admin_service import (
    criar_admin_service,
    listar_admins_service
)


bp_admin = Blueprint(
    'bp_admin',
    __name__,
    url_prefix='/api/auth/admin'
)

def admin_logado():
    return 'admin_id' in session


@bp_admin.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    admin = consultar_admin_por_username(username)
    if not admin:
        return jsonify({
            "success": False,
            "message": "Admin não encontrado"
        }), 404
    if not check_password_hash(admin["senha"], password):
        return jsonify({
            "success": False,
            "message": "Senha inválida"
        }), 401
    session["admin_id"] = admin["id"]
    session["admin_user"] = admin["nome"]
    return jsonify({
        "success": True,
        "admin": {
            "id": admin["id"],
            "nome": admin["nome"]
        }
    })


@bp_admin.route('/me', methods=['GET'])
def me():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autenticado'
        }), 401

    return jsonify({
        'success': True,
        'admin': {
            'id': session.get('admin_id'),
            'nome': session.get('admin_user')
        }
    })

@bp_admin.route('/list', methods=['GET'])
def list_admins():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    admins = listar_admins_service()

    return jsonify({
        'success': True,
        'admins': admins
    })


@bp_admin.route('/create', methods=['POST'])
def create_admin():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    dados = request.get_json()

    username = dados.get('username')
    password = dados.get('password')
    try:
        admin = criar_admin_service(
            username,
            password
        )
        return jsonify({
            'success': True,
            'admin': admin
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@bp_admin.route('/stats', methods=['GET'])
def stats():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    admins = listar_admins_db()
    medicos = listar_medicos()
    pacientes = consultar_pacientes()
    atendimentos = consultar_atendimentos()

    return jsonify({
        'success': True,
        'admins': len(admins),
        'medicos': len(medicos),
        'pacientes': len(pacientes),
        'atendimentos': len(atendimentos)
    })



@bp_admin.route('/dashboard-metrics', methods=['GET'])
def dashboard_metrics():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401
    atendimentos = consultar_atendimentos()
    pendentes = len([
        a for a in atendimentos
        if a['status'] == 'pendente'
    ])

    concluidos = len([
        a for a in atendimentos
        if a['status'] == 'concluido'
    ])

    urgentes = len([
        a for a in atendimentos
        if a['prioridade'] == 'urgente'
    ])

    moderados = len([
        a for a in atendimentos
        if a['prioridade'] == 'moderado'
    ])

    leves = len([
        a for a in atendimentos
        if a['prioridade'] == 'leve'
    ])

    return jsonify({
        'success': True,
        'pendentes': pendentes,
        'concluidos': concluidos,
        'urgentes': urgentes,
        'moderados': moderados,
        'leves': leves
    })



@bp_admin.route('/medicos', methods=['GET'])
def medicos():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    dados = listar_medicos()

    return jsonify({
        'success': True,
        'medicos': dados
    })


@bp_admin.route('/pacientes', methods=['GET'])
def pacientes():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    dados = consultar_pacientes()

    return jsonify({
        'success': True,
        'pacientes': dados
    })



@bp_admin.route('/atendimentos', methods=['GET'])
def atendimentos():

    if not admin_logado():
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    dados = consultar_atendimentos()

    return jsonify({
        'success': True,
        'atendimentos': dados
    })


