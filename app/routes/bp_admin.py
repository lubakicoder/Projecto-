from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from app.respositories.crud_admin import consultar_admin_por_username
from app.services.admin_service import criar_admin_service



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


