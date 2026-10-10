async function carregarPlanos() {
    const resposta = await fetch('/planos', { method: 'GET' });

    const planos = await resposta.json();

    const corpoTabela = document.getElementById('corpo-tabela-planos');

    corpoTabela.innerHTML = '';

    planos.forEach(plano => {
        const linha = document.createElement('tr');
        linha.innerHTML = `
            <td>${plano.id}</td>
            <td>${plano.nome}</td>
            <td>${plano.duracao_meses} ${plano.duracao_meses == 1 ? 'mês' : 'meses'}</td>
            <td>R$ ${parseFloat(plano.valor).toFixed(2).replace('.', ',')}</td>
            <td>${plano.descricao ?? '-'}</td>
            <td>${plano.ativo ? 'Ativo' : 'Inativo'}</td>
        `;
        corpoTabela.appendChild(linha);
    });
}

document.addEventListener('DOMContentLoaded', carregarPlanos);

document.getElementById('btn-cadastrar').addEventListener('click', async () => {
    const novoPlano = {
        nome: document.getElementById('nome').value,
        duracao_meses: document.getElementById('duracao_meses').value,
        valor: document.getElementById('valor').value,
        descricao: document.getElementById('descricao').value
    };

    const resposta = await fetch('/planos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(novoPlano)
    });

    const resultado = await resposta.json();

    const mensagem = document.getElementById('mensagem-status');

    if (resposta.ok) {
        mensagem.textContent = resultado.mensagem;
        mensagem.style.color = 'green';
        carregarPlanos();

        document.getElementById('nome').value = '';
        document.getElementById('duracao_meses').value = '';
        document.getElementById('valor').value = '';
        document.getElementById('descricao').value = '';
    } else {
        mensagem.textContent = resultado.erro;
        mensagem.style.color = 'red';
    }
});