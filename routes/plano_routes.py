from flask import Blueprint, request, jsonify
from models.plano import inserir_plano, listar_planos

plano_bp = Blueprint('plano_bp', __name__)

@plano_bp.route('/planos', methods=['POST'])
def cadastrar_plano():
    dados = request.get_json()

    campos_obrigatorios = ['nome', 'duracao_meses', 'valor']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    resultado = inserir_plano(
        nome=dados.get('nome'),
        duracao_meses=dados.get('duracao_meses'),
        valor=dados.get('valor'),
        descricao=dados.get('descricao')
    )

    if resultado['sucesso']:
        return jsonify({"mensagem": "Plano cadastrado com sucesso", "id": resultado['id']}), 201
    else:
        return jsonify({"erro": resultado['erro']}), 400

@plano_bp.route('/planos', methods=['GET'])
def obter_planos():
    resultado = listar_planos()

    if resultado['sucesso']:
        return jsonify(resultado['planos']), 200
    else:
        return jsonify({"erro": resultado['erro']}), 500