from flask import Blueprint, request, jsonify
from models.pagamento import registrar_pagamento, listar_pagamentos, listar_matriculas_pendentes

pagamento_bp = Blueprint('pagamento_bp', __name__)

STATUS_POR_TIPO = {
    "invalido": 400,
    "nao_encontrado": 404,
    "conflito": 409,
    "erro": 500
}

@pagamento_bp.route('/pagamentos', methods=['POST'])
def cadastrar_pagamento():
    dados = request.get_json()

    campos_obrigatorios = ['matricula_id', 'forma_pagamento', 'data_pagamento']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    resultado = registrar_pagamento(
        matricula_id=dados.get('matricula_id'),
        forma_pagamento=dados.get('forma_pagamento'),
        data_pagamento=dados.get('data_pagamento')
    )

    if resultado['sucesso']:
        return jsonify({
            "mensagem": "Pagamento registrado com sucesso",
            "id": resultado['id'],
            "valor": resultado['valor']
        }), 201

    status = STATUS_POR_TIPO.get(resultado['tipo'], 500)
    return jsonify({"erro": resultado['erro']}), status


@pagamento_bp.route('/pagamentos', methods=['GET'])
def obter_pagamentos():
    resultado = listar_pagamentos()

    if resultado['sucesso']:
        return jsonify(resultado['pagamentos']), 200
    else:
        return jsonify({"erro": resultado['erro']}), 500


@pagamento_bp.route('/pagamentos/pendentes', methods=['GET'])
def obter_matriculas_pendentes():
    resultado = listar_matriculas_pendentes()

    if resultado['sucesso']:
        return jsonify(resultado['matriculas']), 200
    else:
        return jsonify({"erro": resultado['erro']}), 500