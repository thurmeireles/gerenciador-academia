from flask import Flask, render_template

app = Flask(__name__)

from routes.aluno_routes import aluno_bp
app.register_blueprint(aluno_bp)

@app.route('/')
def index():
    return render_template('alunos.html')

if __name__ == '__main__':
    app.run(debug=False)
