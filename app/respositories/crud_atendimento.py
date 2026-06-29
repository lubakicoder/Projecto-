import sqlite3
from ..models.db import conectar

def criar_atendimento(
    paciente_id,
    sintomas,
    intensidade,
    observacao,
    diagnostico=None,
    prioridade=None,
    status="pendente",
    medico_id=None
):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO atendimento (
            paciente_id,
            medico_id,
            sintomas,
            intensidade,
            observacao,
            diagnostico,
            prioridade,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paciente_id,
            medico_id,
            sintomas,
            intensidade,
            observacao,
            diagnostico,
            prioridade,
            status
        ))

        conn.commit()
        return cursor.lastrowid

def consultar_atendimentos():
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            a.id,
            p.nome AS paciente,
            p.bi,
            p.data_nascimento,
            a.sintomas,
            a.intensidade,
            a.observacao,
            a.diagnostico,
            a.prioridade,
            a.status,
            a.data
        FROM atendimento a
        INNER JOIN paciente p
            ON p.id = a.paciente_id
        ORDER BY a.id DESC
        """)
        atendimentos = []
        for row in cursor.fetchall():
            item = dict(row)
            item["cpf"] = item["bi"]
            item["obs"] = item["observacao"] or ""
            item["diag"] = item["diagnostico"] or ""
            item["sintomas"] = (
                item["sintomas"].split(",")
                if item["sintomas"]
                else []
            )
            atendimentos.append(item)
        return atendimentos

def atualizar_diagnostico_atendimento(id, diagnostico):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE atendimento
            SET diagnostico = ?
            WHERE id = ?
        """, (diagnostico, id))
        conn.commit()

def excluir_atendimento(atendimento_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM atendimento WHERE id = ?', (atendimento_id,))
        conn.commit()

def atualizar_status_atendimento(id, status):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE atendimento
            SET status = ?
            WHERE id = ?
        """, (status, id))
        conn.commit()

def concluir_atendimento(id, diagnostico):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE atendimento
        SET
            diagnostico = ?,
            status = 'concluido'
        WHERE id = ?
        """, (diagnostico, id))
        conn.commit()
