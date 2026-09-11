import mysql.connector
from config import DB_CONFIG

def inserir_aluno(nome, cpf, data_nascimento, telefone, email, data_matricula):
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        sql = """
            INSERT INTO alunos (nome, cpf, data_nascimento, telefone, email, data_matricula)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nome, cpf, data_nascimento, telefone, email, data_matricula)
        cursor.execute(sql, valores)
        conexao.commit()
        return {"sucesso": True, "id": cursor.lastrowid}
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            return {"sucesso": False, "erro": "CPF já cadastrado"}
        return {"sucesso": False, "erro": str(erro)}
    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()

def listar_alunos():
    conexao = None
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        cursor = conexao.cursor(dictionary=True)
        sql = "SELECT * FROM alunos"
        cursor.execute(sql)
        alunos = cursor.fetchall()
        return {"sucesso": True, "alunos": alunos}
    except mysql.connector.Error as erro:
        return {"sucesso": False, "erro": str(erro)}
    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()
