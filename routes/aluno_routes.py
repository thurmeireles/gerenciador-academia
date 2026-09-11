from flask import Blueprint, request, jsonify
from models.aluno import inserir_aluno, listar_alunos

aluno_bp = Blueprint('aluno_bp', __name__)

@aluno_bp.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.get_json()
    campos_obrigatorios = ['nome', 'cpf', 'data_matricula']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
    resultado = inserir_aluno(
            nome=dados.get('nome'),
            cpf=dados.get('cpf'),
            data_nascimento=dados.get('data_nascimento'),
            telefone=dados.get('telefone'),
            email=dados.get('email'),
            data_matricula=dados.get('data_matricula')
        )
    if resultado['sucesso']:
        return jsonify({"mensagem": "Aluno cadastrado com sucesso", "id": resultado['id']}), 201
    else:
        if resultado['erro'] == 'CPF já cadastrado':
            return jsonify({"erro": resultado['erro']}), 409
        return jsonify({"erro": resultado['erro']}), 400

@aluno_bp.route('/alunos', methods=['GET'])
def obter_alunos():
    resultado = listar_alunos()

    if resultado['sucesso']:
        return jsonify(resultado['alunos']), 200
    else:
        return jsonify({"erro": resultado['erro']}), 500