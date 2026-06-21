import sqlite3
from ..models.db import conectar

def consultar_atendimentos():
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            a.id,
            p.nome AS paciente,
            p.bi,
            a.idade,
            a.sintomas,
            a.intensidade,
            a.observacoes,
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
            item["obs"] = item["observacoes"] or ""
            item["diag"] = item["diagnostico"] or ""

            if item["sintomas"]:
                item["sintomas"] = item["sintomas"].split(",")
            else:
                item["sintomas"] = []

            atendimentos.append(item)

        return atendimentos

def criar_atendimento(
    paciente_id,
    medico_id,
    idade,
    sintomas,
    intensidade,
    observacoes,
    prioridade,
    status
):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO atendimento (
            paciente_id,
            medico_id,
            idade,
            sintomas,
            intensidade,
            observacoes,
            prioridade,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paciente_id,
            medico_id,
            idade,
            sintomas,
            intensidade,
            observacoes,
            prioridade,
            status
        ))

        conn.commit()

        return cursor.lastrowid

def atualizar_diagnostico(
    atendimento_id,
    diagnostico
):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE atendimento
        SET diagnostico = ?,
            status = 'concluido'
        WHERE id = ?
        """, (
            diagnostico,
            atendimento_id
        ))

        conn.commit()

def excluir_atendimento(atendimento_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM atendimento WHERE id = ?', (atendimento_id,))
        conn.commit()
