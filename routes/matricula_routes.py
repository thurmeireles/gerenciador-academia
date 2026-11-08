from flask import Blueprint, request, jsonify
from models.matricula import matricular_aluno, listar_matriculas

matricula_bp = Blueprint('matricula_bp', __name__)

STATUS_POR_TIPO = {
    "invalido": 400,
    "nao_encontrado": 404,
    "conflito": 409,
    "erro": 500
}

@matricula_bp.route('/matriculas', methods=['POST'])
def cadastrar_matricula():
    dados = request.get_json()

    campos_obrigatorios = ['aluno_id', 'plano_id', 'data_inicio']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    resultado = matricular_aluno(
        aluno_id=dados.get('aluno_id'),
        plano_id=dados.get('plano_id'),
        data_inicio=dados.get('data_inicio')
    )

    if resultado['sucesso']:
        return jsonify({
            "mensagem": "Matrícula realizada com sucesso",
            "id": resultado['id'],
            "data_fim": resultado['data_fim']
        }), 201

    status = STATUS_POR_TIPO.get(resultado['tipo'], 500)
    return jsonify({"erro": resultado['erro']}), status

@matricula_bp.route('/matriculas', methods=['GET'])
def obter_matriculas():
    resultado = listar_matriculas()

    if resultado['sucesso']:
        return jsonify(resultado['matriculas']), 200
    else:
        return jsonify({"erro": resultado['erro']}), 500