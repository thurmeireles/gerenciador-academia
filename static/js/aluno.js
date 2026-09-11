function formatarData(dataString) {
    const data = new Date(dataString);
    const dia = String(data.getUTCDate()).padStart(2, '0');
    const mes = String(data.getUTCMonth() + 1).padStart(2, '0');
    const ano = data.getUTCFullYear();
    return `${dia}/${mes}/${ano}`;
}

async function carregarAlunos() {
    const resposta = await fetch('/alunos', { method: 'GET' });

    const alunos = await resposta.json();

    const corpoTabela = document.getElementById('corpo-tabela-alunos');

    corpoTabela.innerHTML = '';

    alunos.forEach(aluno => {
        const linha = document.createElement('tr');
        linha.innerHTML = `
            <td>${aluno.id}</td>
            <td>${aluno.nome}</td>
            <td>${aluno.cpf}</td>
            <td>${formatarData(aluno.data_nascimento)}</td>
            <td>${aluno.telefone}</td>
            <td>${aluno.email}</td>
            <td>${formatarData(aluno.data_matricula)}</td>
        `;
        corpoTabela.appendChild(linha);
    });
}

document.addEventListener('DOMContentLoaded', carregarAlunos);

document.getElementById('btn-cadastrar').addEventListener('click', async () => {
    const novoAluno = {
        nome: document.getElementById('nome').value,
        cpf: document.getElementById('cpf').value,
        data_nascimento: document.getElementById('data_nascimento').value,
        telefone: document.getElementById('telefone').value,
        email: document.getElementById('email').value,
        data_matricula: document.getElementById('data_matricula').value
    };

    const resposta = await fetch('/alunos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(novoAluno)
    });

    const resultado = await resposta.json();

    const mensagem = document.getElementById('mensagem-status');

    if (resposta.ok) {
        mensagem.textContent = resultado.mensagem;
        mensagem.style.color = 'green';
        carregarAlunos();

        document.getElementById('nome').value = '';
        document.getElementById('cpf').value = '';
        document.getElementById('data_nascimento').value = '';
        document.getElementById('telefone').value = '';
        document.getElementById('email').value = '';
        document.getElementById('data_matricula').value = '';
    } else {
        mensagem.textContent = resultado.erro;
        mensagem.style.color = 'red';
    }
});