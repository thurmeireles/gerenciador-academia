# Sistema de Gerenciamento de Academia

Projeto acadêmico com front-end (HTML/CSS/JavaScript), back-end (Python/Flask) e banco de dados (MySQL).

Board do projeto: https://github.com/users/thurmeireles/projects/1/views/1

## Funcionalidades

1. **Cadastro de Alunos**
2. **Gestão de Planos**
3. **Controle de Matrículas**: matricula um aluno em um plano, calcula a data de término e permite uma única matrícula ativa por aluno
4. **Controle de Pagamentos**: registra o pagamento de uma matrícula, com o valor do plano

## Como executar

1. Crie o ambiente virtual e instale as dependências:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. No MySQL, execute o arquivo `banco.sql` para criar o banco e as tabelas.
3. Copie `config.py.example` para `config.py` e preencha com seu usuário e senha do MySQL.
4. Rode `python app.py` e acesse http://127.0.0.1:5000

## Estrutura

- `models/`: acesso ao banco de dados
- `routes/`: rotas da API (Flask Blueprints)
- `templates/` e `static/`: telas (HTML, CSS e JavaScript)