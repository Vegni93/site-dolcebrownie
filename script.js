let carrinho = [];
let nomeCliente = "";
let valorTotal = 0;

// ─── ABAS ───
function alternarAba(abaId, btn) {
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    document.getElementById('aba-' + abaId).classList.add('active');
    btn.classList.add('active');

    const balao = document.getElementById('fala-balao');
    const msgs = {
        produtos:   "Escolha com carinho! Cada mordida é mágica. 😋",
        feedbacks:  "Amo ver o carinho dos nossos clientes! 🥰",
        sobre:      "Nossa história tem cheiro de chocolate... 📖",
        home:       "Olá! Que tal um brownie dos deuses hoje? 😋"
    };
    balao.innerText = msgs[abaId] || msgs.home;
    mascoteReseta();

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── CARRINHO ───
function adicionarAoCarrinho(nome, preco) {
    carrinho.push({ nome, preco });
    atualizarCarrinho();
    showToast("Adicionado à sacola! 🍫");

    setMascote('feliz', "Excelente escolha! Esse é sensacional! 😍");

    setTimeout(() => {
        setMascote('padrao', "Escolha com carinho! Cada brownie é mágico. 😋");
    }, 2800);
}

function removerDoCarrinho(index) {
    carrinho.splice(index, 1);
    atualizarCarrinho();
}

function atualizarCarrinho() {
    const list   = document.getElementById('cart-list');
    const total  = document.getElementById('cart-total');
    const count  = document.getElementById('cart-count');
    valorTotal   = 0;

    if (carrinho.length === 0) {
        list.innerHTML = '<p class="empty-msg">Sua sacola está vazia...</p>';
        total.innerText = 'R$ 0,00';
        count.style.display = 'none';
        return;
    }

    count.style.display = 'flex';
    count.innerText = carrinho.length;

    list.innerHTML = carrinho.map((item, i) => {
        valorTotal += item.preco;
        return `<div class="cart-item">
            <span>${item.nome}</span>
            <strong>R$ ${item.preco.toFixed(2).replace('.', ',')}</strong>
            <button onclick="removerDoCarrinho(${i})" title="Remover">✕</button>
        </div>`;
    }).join('');

    total.innerText = `R$ ${valorTotal.toFixed(2).replace('.', ',')}`;
}

// ─── MASCOTE ───
// Nomes possíveis (o ã pode variar dependendo do sistema de arquivos)
const MASCOTE = {
    padrao:  ["mascote-padrão.png", "mascote-padrao.png", "mascote-padr%C3%A3o.png"],
    feliz:   ["mascote-feliz.png"],
    comendo: ["mascote-comendo.png"]
};

let mascoteCache = {}; // armazena qual nome funcionou para cada chave

function carregarMascote(chave, callback) {
    if (mascoteCache[chave]) { callback(mascoteCache[chave]); return; }
    const nomes = MASCOTE[chave];
    let i = 0;
    function tentar() {
        if (i >= nomes.length) { callback(null); return; }
        const img = new Image();
        img.onload  = () => { mascoteCache[chave] = nomes[i]; callback(nomes[i]); };
        img.onerror = () => { i++; tentar(); };
        img.src = nomes[i];
    }
    tentar();
}

function setMascote(chave, balaoTexto) {
    const img    = document.getElementById('mascote-render');
    const balao  = document.getElementById('fala-balao');
    const fallbk = document.getElementById('mascote-fallback');
    if (balaoTexto) balao.innerText = balaoTexto;
    carregarMascote(chave, (src) => {
        if (src) {
            img.style.display = 'block';
            fallbk.style.display = 'none';
            img.src = src;
        } else {
            img.style.display = 'none';
            fallbk.style.display = 'flex';
        }
    });
}

function mascoteFocaCard() {
    setMascote('comendo', "Hummm… Esse é de dar água na boca! 🤤");
}

function mascoteReseta() {
    setMascote('padrao', null);
}

// ─── TOAST ───
function showToast(msg) {
    const container = document.getElementById('toast-container');
    const t = document.createElement('div');
    t.className = 'toast-msg';
    t.innerText = msg;
    container.appendChild(t);
    setTimeout(() => {
        t.style.opacity = '0';
        t.style.transform = 'translateX(20px)';
        t.style.transition = 'all 0.3s ease';
        setTimeout(() => t.remove(), 300);
    }, 2800);
}

// ─── CHECKOUT ───
function iniciarCheckout() {
    if (carrinho.length === 0) {
        showToast("Adicione itens à sacola primeiro! 🛒");
        return;
    }
    // Reset steps
    document.getElementById('checkout-step-1').style.display = 'block';
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-3').style.display = 'none';
    document.getElementById('checkout-overlay').style.display = 'flex';
}

function irParaOpcoes() {
    nomeCliente = document.getElementById('checkout-nome').value.trim();
    if (!nomeCliente) { showToast("Por favor, informe seu nome! ✍️"); return; }
    document.getElementById('valor-final-display').innerText = `R$ ${valorTotal.toFixed(2).replace('.', ',')}`;
    document.getElementById('checkout-step-1').style.display = 'none';
    document.getElementById('checkout-step-2').style.display = 'block';
}

function voltarParaNome() {
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-1').style.display = 'block';
}

function mostrarQrCode() {
    document.getElementById('valor-final-pix-locked').innerText = `R$ ${valorTotal.toFixed(2).replace('.', ',')}`;
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-3').style.display = 'block';
}

function voltarParaOpcoes() {
    document.getElementById('checkout-step-3').style.display = 'none';
    document.getElementById('checkout-step-2').style.display = 'block';
}

function copiarPix() {
    const input = document.getElementById('pix-copia-cola');
    input.select();
    navigator.clipboard?.writeText(input.value).catch(() => document.execCommand('copy'));
    showToast("Chave Pix copiada! 📋");
}

function confirmarEEnviar(e, tipo) {
    const numero = "5551991156047";
    let msg = `*Novo Pedido — Dolce Brownie* 🍫\n\n`;
    msg += `*Cliente:* ${nomeCliente}\n\n`;
    msg += `*Itens:*\n`;
    carrinho.forEach(i => msg += `• ${i.nome} — R$ ${i.preco.toFixed(2).replace('.', ',')}\n`);
    msg += `\n*Total:* R$ ${valorTotal.toFixed(2).replace('.', ',')}\n`;
    msg += `*Pagamento:* ${tipo === 'pix' ? 'Pix efetuado ✅' : 'A combinar via WhatsApp 🤝'}`;

    window.open(`https://api.whatsapp.com/send?phone=${numero}&text=${encodeURIComponent(msg)}`, '_blank');
    fecharModalCheckout();
    carrinho = [];
    atualizarCarrinho();
    showToast("Pedido enviado com sucesso! 🎉");
}

function fecharModalCheckout() {
    document.getElementById('checkout-overlay').style.display = 'none';
}

// Fechar modal clicando fora
document.getElementById('checkout-overlay')?.addEventListener('click', function(e) {
    if (e.target === this) fecharModalCheckout();
});

// ─── FEEDBACKS ───
function enviarFeedback(e) {
    e.preventDefault();
    const nome  = document.getElementById('feed-nome').value;
    const nota  = document.getElementById('feed-nota').value;
    const msg   = document.getElementById('feed-msg').value;
    const mural = document.getElementById('lista-feedbacks');

    const card = document.createElement('div');
    card.className = 'feed-card';
    card.innerHTML = `
        <div class="stars">${'⭐'.repeat(nota)}</div>
        <p>"${msg}"</p>
        <span>— ${nome}</span>
    `;
    mural.prepend(card);

    document.getElementById('feed-nome').value = '';
    document.getElementById('feed-msg').value  = '';
    showToast("Obrigado pelo carinho! 🤎");
}

// ─── SOBRE ───
const sobreSlides = [
    { title: "O Início de um Sonho",   text: "A Dolce Brownie nasceu de uma verdadeira paixão pela confeitaria e pelo desejo de criar algo mais do que um simples doce. Nossa jornada começou em uma cozinha pequena, testando receitas incansavelmente até alcançarmos a textura perfeita." },
    { title: "Nossos Objetivos",        text: "A Dolce Brownie tem como principal objetivo oferecer brownies artesanais de alta qualidade, preparados com ingredientes selecionados, muito cuidado e dedicação em cada etapa da produção. Transformamos momentos simples em ocasiões especiais." },
    { title: "Nossa Excelência",        text: "A Dolce Brownie destaca-se pela excelência na produção artesanal de brownies recheados, unindo qualidade, sabor e sofisticação em cada detalhe — da receita à embalagem." },
    { title: "Ingredientes Premium",    text: "Acreditamos que o segredo de um doce inesquecível está na matéria-prima. Não abrimos mão de utilizar os melhores chocolates, cacau de altíssima qualidade e manteiga de verdade." },
    { title: "O Toque Artesanal",       text: "Fugimos da produção industrializada. Nossos brownies são feitos de forma 100% artesanal, em pequenos lotes. Isso nos permite controlar rigorosamente a qualidade de cada fornada." },
    { title: "Nossos Clientes",         text: "Vocês são o motivo pelo qual ligamos os nossos fornos todos os dias. Proporcionar um atendimento acolhedor, transparente e de confiança é tão importante quanto a qualidade dos doces." },
    { title: "O Mascote da Casa",       text: "Nosso carismático Brownie é a personificação do nosso cuidado e afeto. Ele interage com você enquanto explora nosso cardápio — vibrando com cada escolha!" }
];

function mudarSlideSobre(idx, btn) {
    document.querySelectorAll('.about-nav button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const content = document.getElementById('about-content');
    content.style.opacity = '0';
    content.style.transform = 'translateY(10px)';

    setTimeout(() => {
        content.innerHTML = `<div class="slide active"><h3>${sobreSlides[idx].title}</h3><p>${sobreSlides[idx].text}</p></div>`;
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
        content.style.transition = 'all 0.4s ease';
    }, 220);
}

// ─── INIT ───
document.addEventListener('DOMContentLoaded', () => {
    setMascote('padrao', null);
});