
let emojiAtualDefault = "🧑‍🍳";
const numeroWhats = "555191156047"; 

// --- SISTEMA DE AUTENTICAÇÃO ---
let isLoginMode = false;
let currentUser = null;

window.onload = function() {
    const userSaved = localStorage.getItem('dolceUser');
    if(userSaved) {
        currentUser = JSON.parse(userSaved);
        liberarAcesso();
    }
};

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    document.getElementById('auth-title').innerText = isLoginMode ? "Fazer Login" : "Criar Conta";
    document.getElementById('auth-subtitle').innerText = isLoginMode ? "Bem-vindo de volta!" : "Para acessar nossas delícias, crie sua conta.";
    document.getElementById('auth-nome').style.display = isLoginMode ? "none" : "block";
    if(isLoginMode) document.getElementById('auth-nome').removeAttribute("required");
    else document.getElementById('auth-nome').setAttribute("required", "true");
    
    document.querySelector('.auth-submit-btn').innerText = isLoginMode ? "Entrar" : "Cadastrar e Entrar";
    document.querySelector('.auth-switch').innerHTML = isLoginMode ? "Não tem conta? <span onclick='toggleAuthMode()'>Cadastre-se</span>" : "Já tem conta? <span onclick='toggleAuthMode()'>Faça Login</span>";
}

function handleAuth(e) {
    e.preventDefault();
    const email = document.getElementById('auth-email').value;
    const nome = isLoginMode ? email.split('@')[0] : document.getElementById('auth-nome').value; 
    
    currentUser = { nome: nome, email: email };
    localStorage.setItem('dolceUser', JSON.stringify(currentUser));
    liberarAcesso();
}

function liberarAcesso() {
    document.getElementById('auth-overlay').style.opacity = "0";
    setTimeout(() => { document.getElementById('auth-overlay').style.display = "none"; }, 500);
    document.getElementById('user-greeting').innerText = `Olá, ${currentUser.nome}!`;
    document.getElementById('user-greeting').style.display = "block";
    document.getElementById('balao-fala').innerHTML = `Que bom ter você aqui, ${currentUser.nome}! Lembre-se que a retirada é agendada! 🍫✨`;
    
    // Preenche o nome no form de feedback
    const feedNome = document.getElementById('feed-nome');
    if(feedNome) feedNome.value = currentUser.nome;
}

function fazerLogout() {
    localStorage.removeItem('dolceUser');
    location.reload();
}

// --- NAVEGAÇÃO E MASCOTE ---
function alternarAba(nomeAba) {
    document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    
    const abaAlvo = document.getElementById('aba-' + nomeAba);
    abaAlvo.classList.add('active');
    event.currentTarget.classList.add('active');
    
    emojiAtualDefault = abaAlvo.getAttribute('data-emoji');
    document.getElementById('mascote-emoji').innerText = emojiAtualDefault;
    document.getElementById('balao-fala').innerHTML = abaAlvo.getAttribute('data-boas-vindas');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function mudarSlideSobre(index, btn) {
    document.querySelectorAll('.about-tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.about-slide').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('slide-' + index).classList.add('active');
}

function showToast(msg) {
    const container = document.getElementById('toast-container');
    const t = document.createElement('div'); t.className = 'toast'; t.innerHTML = `✅ ${msg}`;
    container.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

function mascoteAnimaHover() {
    document.getElementById('mascote-emoji').innerText = "😋";
    document.getElementById('mascote-emoji').classList.add('emoji-animado-hover');
    document.getElementById('balao-fala').innerHTML = "Nossa, essa escolha vale muito a pena! 🌟";
}

function mascoteZoeira(msg, emoji) {
    document.getElementById('mascote-emoji').innerText = emoji;
    document.getElementById('mascote-emoji').classList.add('emoji-animado-hover');
    document.getElementById('balao-fala').innerHTML = msg;
}

function mascoteResetaHover() {
    document.getElementById('mascote-emoji').innerText = emojiAtualDefault;
    document.getElementById('mascote-emoji').classList.remove('emoji-animado-hover');
    document.getElementById('balao-fala').innerHTML = document.querySelector('.tab-section.active').getAttribute('data-boas-vindas');
}

// --- SISTEMA DE FEEDBACKS ---
function enviarFeedback(e) {
    e.preventDefault();
    const nome = document.getElementById('feed-nome').value;
    const nota = document.getElementById('feed-nota').value;
    const mensagem = document.getElementById('feed-mensagem').value;
    
    let estrelas = "";
    for(let i=0; i<nota; i++) estrelas += "⭐";

    const mural = document.getElementById('lista-feedbacks');
    const novoCard = document.createElement('div');
    novoCard.className = 'feedback-card';
    novoCard.innerHTML = `
        <div class="feed-stars">${estrelas}</div>
        <p class="feed-text">"${mensagem}"</p>
        <span class="feed-author">- ${nome}</span>
    `;
    
    // Adiciona o novo comentário no topo
    mural.insertBefore(novoCard, mural.firstChild);
    
    // Limpa os campos (mantém o nome)
    document.getElementById('feed-nota').value = "";
    document.getElementById('feed-mensagem').value = "";
    
    showToast("Feedback enviado com sucesso! Muito obrigado! ❤️");
    
    // Reação do Mascote
    const el = document.getElementById('mascote-emoji');
    el.innerText = "🥰";
    el.classList.add('emoji-explodindo');
    document.getElementById('balao-fala').innerHTML = "Que amor! Ler isso aquece nosso coração! 💖";
    setTimeout(() => {
        el.classList.remove('emoji-explodindo');
        mascoteResetaHover();
    }, 3500);
}


// --- CARRINHO AVANÇADO ---
let carrinho = {};

function adicionarAoCarrinho(nome, preco, silent = false) {
    if(carrinho[nome]) carrinho[nome].qtd++; else carrinho[nome] = { preco: preco, qtd: 1 };
    atualizarCarrinho();
    if(!silent) {
        showToast(`Adicionado: ${nome}`);
        const el = document.getElementById('mascote-emoji');
        el.innerText = "🤩"; el.classList.add('emoji-explodindo');
        document.getElementById('balao-fala').innerHTML = "Adicionado ao carrinho! Toma que é de graça (mentira)! 🛒🎈";
        setTimeout(() => { el.classList.remove('emoji-explodindo'); mascoteResetaHover(); }, 1800);
    }
}

function diminuirDoCarrinho(nome) {
    if(carrinho[nome]) {
        carrinho[nome].qtd--;
        if(carrinho[nome].qtd <= 0) delete carrinho[nome];
        atualizarCarrinho();
    }
}

function removerDoCarrinho(nome) {
    if(carrinho[nome]) {
        delete carrinho[nome];
        atualizarCarrinho();
        showToast(`Removido: ${nome}`);
    }
}

function atualizarCarrinho() {
    const containers = [
        document.getElementById('cart-items-container-1'), 
        document.getElementById('cart-items-container-2'),
        document.getElementById('cart-items-container-3')
    ];
    const totaisDisplays = document.querySelectorAll('.cart-total-display');
    
    if(Object.keys(carrinho).length === 0) { 
        containers.forEach(c => { if(c) c.innerHTML = "<p class='empty-cart-text'>O carrinho está vazio.</p>"; });
        totaisDisplays.forEach(td => td.innerText = "R$ 0,00");
        return; 
    }
    
    let htmlCarrinho = ""; 
    let total = 0;
    
    for(let item in carrinho) {
        let sub = carrinho[item].preco * carrinho[item].qtd; total += sub;
        htmlCarrinho += `
        <div class="cart-item-row">
            <div class="cart-item-info">
                <strong>${item}</strong>
                <span>R$ ${sub.toFixed(2)}</span>
            </div>
            <div class="cart-controls">
                <button onclick="diminuirDoCarrinho('${item}')">-</button>
                <span>${carrinho[item].qtd}</span>
                <button onclick="adicionarAoCarrinho('${item}', ${carrinho[item].preco}, true)">+</button>
                <button class="remove-btn" onclick="removerDoCarrinho('${item}')">🗑️ Remover</button>
            </div>
        </div>`;
    }
    
    containers.forEach(c => { if(c) c.innerHTML = htmlCarrinho; });
    totaisDisplays.forEach(td => td.innerText = `R$ ${total.toFixed(2)}`);
}

function finalizarPedidoWhatsApp() {
    if(Object.keys(carrinho).length === 0) return alert("Seu carrinho está vazio!");
    let txt = `*Novo Pedido | Dolce Brownie*\n*Cliente:* ${currentUser ? currentUser.nome : 'Não identificado'}\n\n`;
    let total = 0;
    for(let item in carrinho) {
        let sub = carrinho[item].preco * carrinho[item].qtd; total += sub;
        txt += `• ${carrinho[item].qtd}x ${item} (R$ ${sub.toFixed(2)})\n`;
    }
    txt += `\n*Valor Total:* R$ ${total.toFixed(2)}\n\nOlá! Gostaria de confirmar este pedido e agendar a retirada!`;
    window.open(`https://api.whatsapp.com/send?phone=${numeroWhats}&text=${encodeURIComponent(txt)}`);
}
