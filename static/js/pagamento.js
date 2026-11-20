const FORMAS = {
    dinheiro: 'Dinheiro',
    pix: 'Pix',
    cartao_debito: 'Cartão de débito',
    cartao_credito: 'Cartão de crédito'
};

function formatarData(dataString) {
    const data = new Date(dataString);
    const dia = String(data.getUTCDate()).padStart(2, '0');
    const mes = String(data.getUTCMonth() + 1).padStart(2, '0');
    const ano = data.getUTCFullYear();
    return `${dia}/${mes}/${ano}`;
}

function formatarValor(valor) {
    return `R$ ${parseFloat(valor).toFixed(2).replace('.', ',')}`;
}

async function carregarPendentes() {
    const resposta = await fetch('/pagamentos/pendentes', { method: 'GET' });
    const matriculas = await resposta.json();

    const select = document.getElementById('matricula_id');
    select.innerHTML = '<option value="">Selecione uma matrícula</option>';

    matriculas.forEach(matricula => {
        const opcao = document.createElement('option');
        opcao.value = matricula.id;
        opcao.textContent = `${matricula.aluno} - ${matricula.plano} (${formatarValor(matricula.valor)})`;
        select.appendChild(opcao);
    });
}

async function carregarPagamentos() {
    const resposta = await fetch('/pagamentos', { method: 'GET' });
    const pagamentos = await resposta.json();

    const corpoTabela = document.getElementById('corpo-tabela-pagamentos');
    corpoTabela.innerHTML = '';

    pagamentos.forEach(pagamento => {
        const linha = document.createElement('tr');
        linha.innerHTML = `
            <td>${pagamento.id}</td>
            <td>${pagamento.aluno}</td>
            <td>${pagamento.plano}</td>
            <td>${formatarValor(pagamento.valor)}</td>
            <td>${FORMAS[pagamento.forma_pagamento]}</td>
            <td>${formatarData(pagamento.data_pagamento)}</td>
        `;
        corpoTabela.appendChild(linha);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    carregarPendentes();
    carregarPagamentos();
});

document.getElementById('btn-cadastrar').addEventListener('click', async () => {
    const novoPagamento = {
        matricula_id: document.getElementById('matricula_id').value,
        forma_pagamento: document.getElementById('forma_pagamento').value,
        data_pagamento: document.getElementById('data_pagamento').value
    };

    const resposta = await fetch('/pagamentos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(novoPagamento)
    });

    const resultado = await resposta.json();

    const mensagem = document.getElementById('mensagem-status');

    if (resposta.ok) {
        mensagem.textContent = `${resultado.mensagem}: ${formatarValor(resultado.valor)}.`;
        mensagem.style.color = 'green';
        carregarPagamentos();
        carregarPendentes();

        document.getElementById('matricula_id').value = '';
        document.getElementById('forma_pagamento').value = '';
        document.getElementById('data_pagamento').value = '';
    } else {
        mensagem.textContent = resultado.erro;
        mensagem.style.color = 'red';
    }
});