from flask import Blueprint, request, jsonify, session


bp_auth = Blueprint("bp_auth", __name__, url_prefix="/api/auth")

@bp_auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})
