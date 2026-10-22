// Seleção interativa dos cards de terreno
function selecionarTerreno(element, valor) {
    document.querySelectorAll('.terrain-card').forEach(card => card.classList.remove('active'));
    element.classList.add('active');
    document.getElementById('terrain_mod').value = valor;
}

// Renderiza a divisão na grade no estilo HOI4
function renderizarDesignerHOI4(composicao) {
    const supportContainer = document.getElementById('support-slots');
    const combatContainer = document.getElementById('combat-slots');

    supportContainer.innerHTML = '';
    combatContainer.innerHTML = '';

    const suporte = [];
    const combate = [];

    const obterIcone = (nome) => {
        const lower = nome.toLowerCase();
        if (lower.includes('engenharia')) return '🛠️';
        if (lower.includes('antiaérea') || lower.includes('aa')) return '🎯';
        if (lower.includes('artilharia')) return '💥';
        if (lower.includes('infantaria')) return '🪖';
        if (lower.includes('tanque') || lower.includes('blindado')) return '🚜';
        if (lower.includes('recon') || lower.includes('reconhecimento')) return '🔭';
        return '🎖️';
    };

    // Separa entre suporte (companhias) e combate (batalhões)
    composicao.forEach(item => {
        if (item.toLowerCase().includes('companhia')) {
            suporte.push(item);
        } else {
            const match = item.match(/^(\d+)x\s*(.*)$/);
            if (match) {
                const qtd = parseInt(match[1]);
                const nome = match[2];
                for (let i = 0; i < qtd; i++) {
                    combate.push(nome);
                }
            } else {
                combate.push(item);
            }
        }
    });

    // Renderiza Coluna de Suporte (Até 5 slots)
    for (let i = 0; i < 5; i++) {
        const slot = document.createElement('div');
        if (suporte[i]) {
            slot.className = 'designer-slot active';
            slot.innerHTML = `<span class="slot-icon">${obterIcone(suporte[i])}</span><span class="slot-text">${suporte[i].replace('Companhia de ', '')}</span>`;
        } else {
            slot.className = 'designer-slot empty';
            slot.innerHTML = '+';
        }
        supportContainer.appendChild(slot);
    }

    // Renderiza Grade de Combate (25 slots: 5 colunas x 5 linhas)
    for (let i = 0; i < 25; i++) {
        const slot = document.createElement('div');
        if (combate[i]) {
            slot.className = 'designer-slot active';
            slot.innerHTML = `<span class="slot-icon">${obterIcone(combate[i])}</span><span class="slot-text">${combate[i].replace('Batalhões de ', '').replace('Batalhão de ', '')}</span>`;
        } else {
            slot.className = 'designer-slot empty';
            slot.innerHTML = '+';
        }
        combatContainer.appendChild(slot);
    }
}

document.getElementById('optimizer-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // 1. Coleta os valores da interface
    const terrain_mod = parseFloat(document.getElementById('terrain_mod').value);
    const fort_level = parseInt(document.getElementById('fort_level').value);
    const combat_width = parseInt(document.getElementById('combat_width').value);
    const cas_support = document.getElementById('cas_support').checked ? 1 : 0;

    const requestData = {
        terrain_mod: terrain_mod,
        fort_level: fort_level,
        combat_width: combat_width,
        cas_support: cas_support
    };

    // 2. Manipulação de UI
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    // 3. MOCK de testes (Simula resposta do algoritmo Python)
    setTimeout(() => {
        const mockResponse = {
            composição: [
                "15x Batalhões de Infantaria",
                "3x Batalhões de Artilharia",
                "1x Companhia de Engenharia",
                "1x Companhia de Artilharia Antiaérea"
            ],
            status: {
                organizacao: 48.5,
                soft_attack: 285.0,
                breakthrough: 45.0,
                defense: 380.0
            }
        };
        atualizarInterface(mockResponse);
    }, 1200);
});

function atualizarInterface(dados) {
    document.getElementById('loading').classList.add('hidden');
    
    // Renderiza visual no formato HOI4 Designer
    renderizarDesignerHOI4(dados.composição);

    // Atualiza estatísticas do painel
    const status = dados.status;
    document.getElementById('stat-org').textContent = status.organizacao.toFixed(1);
    document.getElementById('stat-soft').textContent = status.soft_attack.toFixed(1);
    document.getElementById('stat-break').textContent = status.breakthrough.toFixed(1);
    document.getElementById('stat-def').textContent = status.defense.toFixed(1);
    
    document.getElementById('results').classList.remove('hidden');
}