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

    const select = document.getElementById('aluno_id');

    alunos.forEach(aluno => {
        const opcao = document.createElement('option');
        opcao.value = aluno.id;
        opcao.textContent = aluno.nome;
        select.appendChild(opcao);
    });
}

async function carregarPlanos() {
    const resposta = await fetch('/planos', { method: 'GET' });
    const planos = await resposta.json();

    const select = document.getElementById('plano_id');

    planos
        .filter(plano => plano.ativo)
        .forEach(plano => {
            const opcao = document.createElement('option');
            opcao.value = plano.id;
            opcao.textContent = `${plano.nome} (${plano.duracao_meses} ${plano.duracao_meses == 1 ? 'mês' : 'meses'})`;
            select.appendChild(opcao);
        });
}

async function carregarMatriculas() {
    const resposta = await fetch('/matriculas', { method: 'GET' });
    const matriculas = await resposta.json();

    const corpoTabela = document.getElementById('corpo-tabela-matriculas');
    corpoTabela.innerHTML = '';

    matriculas.forEach(matricula => {
        const linha = document.createElement('tr');
        linha.innerHTML = `
            <td>${matricula.id}</td>
            <td>${matricula.aluno}</td>
            <td>${matricula.plano}</td>
            <td>${formatarData(matricula.data_inicio)}</td>
            <td>${formatarData(matricula.data_fim)}</td>
        `;
        corpoTabela.appendChild(linha);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    carregarAlunos();
    carregarPlanos();
    carregarMatriculas();
});

document.getElementById('btn-cadastrar').addEventListener('click', async () => {
    const novaMatricula = {
        aluno_id: document.getElementById('aluno_id').value,
        plano_id: document.getElementById('plano_id').value,
        data_inicio: document.getElementById('data_inicio').value
    };

    const resposta = await fetch('/matriculas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(novaMatricula)
    });

    const resultado = await resposta.json();

    const mensagem = document.getElementById('mensagem-status');

    if (resposta.ok) {
        mensagem.textContent = `${resultado.mensagem}. Válida até ${formatarData(resultado.data_fim)}.`;
        mensagem.style.color = 'green';
        carregarMatriculas();

        document.getElementById('aluno_id').value = '';
        document.getElementById('plano_id').value = '';
        document.getElementById('data_inicio').value = '';
    } else {
        mensagem.textContent = resultado.erro;
        mensagem.style.color = 'red';
    }
});