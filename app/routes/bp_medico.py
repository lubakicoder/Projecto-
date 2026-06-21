from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash

from app.respositories import crud_medico, crud_atendimento

bp_medico = Blueprint(
    'bp_medico',
    __name__,
    url_prefix='/api/auth/medico'
)


@bp_medico.route('/login', methods=['POST'])
def login():

    dados = request.get_json()

    crm = dados.get('crm')
    senha = dados.get('senha')

    medico = crud_medico.consultar_medico_por_crm(crm)

    if not medico:
        return jsonify({
            'success': False,
            'message': 'CRM inválido'
        }), 401

    if not check_password_hash(
        medico['senha'],
        senha
    ):
        return jsonify({
            'success': False,
            'message': 'Senha inválida'
        }), 401

    session['medico_id'] = medico['id']
    session['medico_nome'] = medico['nome']
    session['medico_crm'] = medico['crm']

    return jsonify({
        'success': True,
        'medico': {
            'id': medico['id'],
            'nome': medico['nome'],
            'crm': medico['crm'],
            'especialidade': medico['especialidade']
        }
    })


@bp_medico.route('/logout', methods=['POST'])
def logout():

    session.pop('medico_id', None)
    session.pop('medico_nome', None)
    session.pop('medico_crm', None)

    return jsonify({
        'success': True
    })
