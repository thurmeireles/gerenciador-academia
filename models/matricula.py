import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import DB_CONFIG


def matricular_aluno(aluno_id, plano_id, data_inicio):
    try:
        inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return {"sucesso": False, "tipo": "invalido", "erro": "Data de início inválida"}

    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True, buffered=True)

        cursor.execute("SELECT id FROM alunos WHERE id = %s", (aluno_id,))
        if cursor.fetchone() is None:
            return {"sucesso": False, "tipo": "nao_encontrado", "erro": "Aluno não encontrado"}

        cursor.execute("SELECT duracao_meses, ativo FROM planos WHERE id = %s", (plano_id,))
        plano = cursor.fetchone()
        if plano is None:
            return {"sucesso": False, "tipo": "nao_encontrado", "erro": "Plano não encontrado"}
        if not plano['ativo']:
            return {"sucesso": False, "tipo": "invalido", "erro": "Plano inativo"}

        cursor.execute(
            "SELECT id FROM matriculas WHERE aluno_id = %s AND data_fim >= CURDATE()",
            (aluno_id,)
        )
        if cursor.fetchone() is not None:
            return {"sucesso": False, "tipo": "conflito", "erro": "Aluno já possui matrícula ativa"}

        data_fim = inicio + relativedelta(months=plano['duracao_meses'])

        sql = """
            INSERT INTO matriculas (aluno_id, plano_id, data_inicio, data_fim)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (aluno_id, plano_id, inicio, data_fim))
        conexao.commit()

        return {"sucesso": True, "id": cursor.lastrowid, "data_fim": data_fim.isoformat()}

    except mysql.connector.Error as erro:
        return {"sucesso": False, "tipo": "erro", "erro": str(erro)}

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()


def listar_matriculas():
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT m.id, a.nome AS aluno, p.nome AS plano, m.data_inicio, m.data_fim
            FROM matriculas m
            JOIN alunos a ON m.aluno_id = a.id
            JOIN planos p ON m.plano_id = p.id
            ORDER BY m.id ASC
        """
        cursor.execute(sql)
        matriculas = cursor.fetchall()

        return {"sucesso": True, "matriculas": matriculas}

    except mysql.connector.Error as erro:
        return {"sucesso": False, "erro": str(erro)}

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()
    