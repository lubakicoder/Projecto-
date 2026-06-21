from app.respositories.crud_paciente import consultar_pacientes, criar_paciente, consultar_paciente_por_id
from flask import session

class PacienteServiceError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code     

def login_paciente_service(bi, nome):
    if not bi or not nome:
        raise PacienteServiceError('BI e nome obrigatórios', 400)
                                           
    paciente = consultar_paciente_por_id(bi)
    if not paciente:                        
        criar_paciente(bi, nome)
        paciente = consultar_paciente_por_id(bi)
    
    session['paciente_id'] = paciente['id']
    session['paciente_nome'] = paciente['nome']
    session['paciente_bi'] = paciente['bi']
    
    return {'id': paciente['id'], 'nome': paciente['nome'], 'bi': paciente['bi']}

def listar_pacientes_service():
    pacientes = consultar_pacientes()
    return pacientes

def logout_paciente_service():
    session.pop('paciente_id', None)
    session.pop('paciente_nome', None)
    session.pop('paciente_bi', None)
