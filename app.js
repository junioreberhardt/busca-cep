let enderecos = [];

// Função para remover acentos e deixar em minúsculo
const normalizar = (texto) =>
    texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

async function carregarDados() {
    try {
        const res = await fetch('dados.csv');
        const csv = await res.text();

        // Processa o CSV e já deixa uma versão "limpa" preparada para busca rápida
        enderecos = csv.split('\n').slice(1).map(linha => {
            const col = linha.split(',');
            if (col.length < 5) return null;

            const ruaOriginal = col[0].trim();
            const cepOriginal = col[4].trim();

            return {
                rua: ruaOriginal,
                bairro: col[1].trim(),
                cidade: col[2].trim(),
                uf: col[3].trim(),
                cep: cepOriginal,
                // Chaves de busca:
                ruaBusca: normalizar(ruaOriginal),
                cepBusca: cepOriginal.replace(/\D/g, '')
            };
        }).filter(Boolean);
    } catch (e) { console.error("Erro ao carregar dados:", e); }
}

const input = document.getElementById('busca');
const lista = document.getElementById('lista');
const painel = document.getElementById('resultado-final');

input.addEventListener('input', () => {
    const termoInput = input.value.trim();
    const termoLimpo = normalizar(termoInput);
    const termoNumerico = termoInput.replace(/\D/g, '');

    lista.innerHTML = '';
    painel.style.display = 'none';

    // Começa a busca após 3 caracteres (ou 3 números)
    if (termoInput.length < 3) {
        lista.style.display = 'none';
        return;
    }

    const filtrados = enderecos.filter(e =>
        e.ruaBusca.includes(termoLimpo) ||
        (termoNumerico !== '' && e.cepBusca.includes(termoNumerico))
    );

    lista.style.display = 'block';

    if (filtrados.length > 0) {
        // MOSTRA RESULTADOS ENCONTRADOS
        filtrados.slice(0, 10).forEach(res => {
            const item = document.createElement('div');
            item.className = 'opcao';
            item.innerHTML = `<strong>${res.cep}</strong> - ${res.rua} - ${res.bairro}`;
            item.onclick = () => {
                exibirDados(res);
                lista.style.display = 'none';
                input.value = '';
            };
            lista.appendChild(item);
        });
    } else {
        // MENSAGEM DE NÃO ENCONTRADO
        const aviso = document.createElement('div');
        aviso.className = 'opcao-vazia';

        // Se o usuário digitou mais números que letras, assumimos que busca um CEP
        const ehBuscaCep = termoNumerico.length >= termoLimpo.replace(/\d/g, '').length;

        if (ehBuscaCep) {
            aviso.innerHTML = `
                <p><strong>CEP não encontrado na base de dados</strong></p>
                <p style="font-size: 0.85em; color: #666;">
                    Verifique o CEP ou use o CEP da área rural: <b style="color: #2563eb;">89337-899</b>
                </p>
            `;
        } else {
            aviso.innerHTML = `
                <p><strong>Rua sem CEP cadastrado</strong></p>
                <p style="font-size: 0.85em; color: #666;">
                    Use o CEP da área rural: <b style="color: #2563eb;">89337-899</b>
                </p>
            `;
        }
        lista.appendChild(aviso);
    }
});

function exibirDados(dados) {
    painel.style.display = 'block';

    // Lógica para separar o primeiro nome (Rua, Avenida, etc) do resto
    const partes = dados.rua.split(' '); // Divide o logradouro por espaços
    const tipoLogradouro = partes[0]; // Pega a primeira palavra (Rua, Av, etc)
    const nomeLogradouro = partes.slice(1).join(' '); // Pega todo o resto

    // Preenche o HTML separadamente
    document.getElementById('res-titulo').textContent = tipoLogradouro + ":";
    document.getElementById('res-rua').textContent = nomeLogradouro;

    document.getElementById('res-bairro').textContent = dados.bairro;
    document.getElementById('res-cep').textContent = dados.cep;
    document.getElementById('res-cidade').textContent = `${dados.cidade} / ${dados.uf}`;
}

carregarDados();
