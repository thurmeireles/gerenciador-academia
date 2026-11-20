import mysql.connector
from datetime import datetime
from config import DB_CONFIG

FORMAS_VALIDAS = ('dinheiro', 'pix', 'cartao_debito', 'cartao_credito')


def registrar_pagamento(matricula_id, forma_pagamento, data_pagamento):
    if forma_pagamento not in FORMAS_VALIDAS:
        return {"sucesso": False, "tipo": "invalido", "erro": "Forma de pagamento inválida"}

    try:
        data = datetime.strptime(data_pagamento, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return {"sucesso": False, "tipo": "invalido", "erro": "Data de pagamento inválida"}

    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True, buffered=True)

        cursor.execute(
            """
            SELECT p.valor
            FROM matriculas m
            JOIN planos p ON m.plano_id = p.id
            WHERE m.id = %s
            """,
            (matricula_id,)
        )
        matricula = cursor.fetchone()
        if matricula is None:
            return {"sucesso": False, "tipo": "nao_encontrado", "erro": "Matrícula não encontrada"}

        cursor.execute("SELECT id FROM pagamentos WHERE matricula_id = %s", (matricula_id,))
        if cursor.fetchone() is not None:
            return {"sucesso": False, "tipo": "conflito", "erro": "Matrícula já possui pagamento registrado"}

        sql = """
            INSERT INTO pagamentos (matricula_id, valor, forma_pagamento, data_pagamento)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (matricula_id, matricula['valor'], forma_pagamento, data))
        conexao.commit()

        return {"sucesso": True, "id": cursor.lastrowid, "valor": str(matricula['valor'])}

    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            return {"sucesso": False, "tipo": "conflito", "erro": "Matrícula já possui pagamento registrado"}
        return {"sucesso": False, "tipo": "erro", "erro": str(erro)}

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()


def listar_pagamentos():
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT pg.id, a.nome AS aluno, pl.nome AS plano,
                   pg.valor, pg.forma_pagamento, pg.data_pagamento
            FROM pagamentos pg
            JOIN matriculas m ON pg.matricula_id = m.id
            JOIN alunos a ON m.aluno_id = a.id
            JOIN planos pl ON m.plano_id = pl.id
            ORDER BY pg.id ASC
        """
        cursor.execute(sql)
        pagamentos = cursor.fetchall()

        return {"sucesso": True, "pagamentos": pagamentos}

    except mysql.connector.Error as erro:
        return {"sucesso": False, "erro": str(erro)}

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()


def listar_matriculas_pendentes():
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT m.id, a.nome AS aluno, pl.nome AS plano, pl.valor,
                   m.data_inicio, m.data_fim
            FROM matriculas m
            LEFT JOIN pagamentos pg ON pg.matricula_id = m.id
            JOIN alunos a ON m.aluno_id = a.id
            JOIN planos pl ON m.plano_id = pl.id
            WHERE pg.id IS NULL
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