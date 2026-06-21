from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from app.respositories.crud_admin import listar_admins_db
from app.respositories.crud_medico import listar_medicos
from app.respositories.crud_paciente import consultar_pacientes
from app.respositories.crud_atendimento import consultar_atendimentos

from app.services.admin_service import (
    login_admin_service,
    criar_admin_service,
    logout_admin_service,
    listar_admins_service
)

bp_admin = Blueprint(
    'bp_admin',
    __name__,
    url_prefix='/api/auth/admin'
)


# ==================================
# VERIFICAR SESSÃO
# ==================================

def admin_logado():
    return 'admin_id' in session


# ==================================
# LOGIN
# ==================================

@bp_admin.route('/login', methods=['POST'])
def login():

    dados = request.get_json()

    username = dados.get('username')
    password = dados.get('password')

    try:

        admin = login_admin_service(
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
        }), 401


# ==================================
# VERIFICAR USUÁRIO LOGADO
# ==================================

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


# ==================================
# LOGOUT
# ==================================

@bp_admin.route('/logout', methods=['POST'])
def logout():

    logout_admin_service()

    return jsonify({
        'success': True
    })


# ==================================
# LISTAR ADMINS
# ==================================

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


# ==================================
# CRIAR ADMIN
# ==================================

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


# ==================================
# ESTATÍSTICAS GERAIS
# ==================================

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


# ==================================
# MÉTRICAS DO DASHBOARD
# ==================================

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


# ==================================
# LISTAR MÉDICOS
# ==================================

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


# ==================================
# LISTAR PACIENTES
# ==================================

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


# ==================================
# LISTAR ATENDIMENTOS
# ==================================

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
