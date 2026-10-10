from flask import Flask, render_template

app = Flask(__name__)

from routes.aluno_routes import aluno_bp
app.register_blueprint(aluno_bp)

from routes.plano_routes import plano_bp
app.register_blueprint(plano_bp)

@app.route('/')
def index():
    return render_template('alunos.html')

@app.route('/gestao-planos')
def pagina_planos():
    return render_template('planos.html')

if __name__ == '__main__':
    app.run(debug=False)
