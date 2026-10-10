import mysql.connector
from config import DB_CONFIG

def inserir_plano(nome, duracao_meses, valor, descricao=None):
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor()

        sql = """
            INSERT INTO planos (nome, duracao_meses, valor, descricao)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, duracao_meses, valor, descricao)

        cursor.execute(sql, valores)
        conexao.commit()

        return {"sucesso": True, "id": cursor.lastrowid}

    except mysql.connector.Error as erro:
        return {"sucesso": False, "erro": str(erro)}

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()

def listar_planos():
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM planos"
        cursor.execute(sql)
        planos = cursor.fetchall()

        return {"sucesso": True, "planos": planos}

    except mysql.connectior.Error as erro:
        return {"sucesso": False, "erro": str(erro)}

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()