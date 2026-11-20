from flask import Flask, render_template

app = Flask(__name__)

from routes.aluno_routes import aluno_bp
app.register_blueprint(aluno_bp)

from routes.plano_routes import plano_bp
app.register_blueprint(plano_bp)

from routes.matricula_routes import matricula_bp
app.register_blueprint(matricula_bp)

from routes.pagamento_routes import pagamento_bp
app.register_blueprint(pagamento_bp)

@app.route('/')
def index():
    return render_template('alunos.html')

@app.route('/gestao-planos')
def pagina_planos():
    return render_template('planos.html')

@app.route('/gestao-matriculas')
def pagina_matriculas():
    return render_template('matriculas.html')

@app.route('/gestao-pagamentos')
def pagina_pagamentos():
    return render_template('pagamentos.html')

if __name__ == '__main__':
    app.run(debug=False)
