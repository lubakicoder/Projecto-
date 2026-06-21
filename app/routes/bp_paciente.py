from flask import Blueprint, request, jsonify

from app.services.paciente_service import (
    login_paciente_service,
    logout_paciente_service
)

bp_paciente = Blueprint(
    'bp_paciente',
    __name__,
    url_prefix='/api/auth/paciente'
)


@bp_paciente.route('/login', methods=['POST'])
def login():

    dados = request.get_json()

    bi = dados.get('bi')
    nome = dados.get('nome')

    try:

        paciente = login_paciente_service(
            bi,
            nome
        )

        return jsonify({
            'success': True,
            'paciente': paciente
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@bp_paciente.route('/logout', methods=['POST'])
def logout():

    logout_paciente_service()

    return jsonify({
        'success': True
    })
