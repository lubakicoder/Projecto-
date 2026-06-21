from flask import Flask  # type: ignore
from app.routes.bp_user import bp_user
from app.routes.bp_medico import bp_medico
from app.routes.bp_paciente import bp_paciente
from app.routes.bp_admin import bp_admin
from app.routes.api_atendimento import bp_atendimento
from app.routes.api_auth import bp_auth
from app.models.db import tbl_paciente, tbl_medico, tbl_admin, tbl_atendimento
from app.config import get_config



def criar_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_medico)
    app.register_blueprint(bp_paciente)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_atendimento)
    app.register_blueprint(bp_auth)
    tbl_paciente()
    tbl_medico()
    tbl_admin()
    tbl_atendimento()

    return app
