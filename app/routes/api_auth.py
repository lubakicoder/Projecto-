from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from app.respositories.crud_admin import consultar_admin_por_username
from app.respositories.crud_medico import consultar_medico_por_crm
from app.respositories.crud_paciente import consultar_paciente_por_id

bp_auth = Blueprint("bp_auth", __name__, url_prefix="/api/auth")



@bp_auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})
