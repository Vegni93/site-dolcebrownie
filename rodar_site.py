import os
import http.server
import socketserver
import webbrowser
from threading import Timer

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dolce Brownie | Confeitaria Premium</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,800;1,600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div id="toast-container"></div>

    <div id="checkout-overlay" style="display: none;">
        <div class="auth-modal">
            <h2 id="auth-title">Quase lá!</h2>
            <p id="auth-subtitle">Para enviarmos o seu pedido, como podemos chamar você?</p>
            
            <form id="checkout-form" onsubmit="confirmarNomeEEnviar(event)">
                <input type="text" id="checkout-nome" placeholder="Seu Nome Completo" required>
                <button type="submit" class="auth-submit-btn">Ir para o WhatsApp 🚀</button>
                <button type="button" class="close-modal-btn" onclick="fecharModalCheckout()">Voltar ao cardápio</button>
            </form>
        </div>
    </div>

    <header class="main-header">
        <div class="header-container">
            <h1>Dolce brownie</h1>
            <h2>CONFEITARIA ARTESANAL</h2>
            <p class="minimal-slogan">"Detalhes que Encantam"</p>
        </div>
    </header>

    <nav class="navigation-bar">
        <div class="nav-container">
            <button class="nav-btn active" onclick="alternarAba('home')">Início</button>
            <button class="nav-btn" onclick="alternarAba('produtos')">Cardápio</button>
            <button class="nav-btn" onclick="alternarAba('promocoes')">Promoções & Festas</button>
            <button class="nav-btn" onclick="alternarAba('eventos')">Edições Especiais</button>
            <button class="nav-btn" onclick="alternarAba('feedbacks')">Feedbacks</button>
            <button class="nav-btn" onclick="alternarAba('sobre')">Sobre Nós</button>
        </div>
    </nav>

    <div class="global-delivery-alert">
        <span>📍 <strong>AVISO:</strong> Operamos exclusivamente via <strong>retirada agendada</strong>.</span>
    </div>

    <main class="content-wrapper">

        <section id="aba-home" class="tab-section active" data-emoji="🧑‍🍳" data-boas-vindas="Olá! Seja muito bem-vindo(a)! Fique à vontade para babar no nosso cardápio! 🍫✨">
            <div class="clean-hero">
                <h3>A Experiência Definitiva em Brownies</h3>
                <p class="hero-subtitle">Casquinha crocante, interior cremoso e ingredientes premium. A alta confeitaria pronta para o seu dia a dia ou para sua festa.</p>
                <div class="divider"></div>
            </div>

            <div class="home-floating-grid">
                <article class="floating-box"><div class="box-icon">✨</div><h4>Nossa Essência</h4><p>Ingredientes selecionados para o verdadeiro sabor do chocolate.</p></article>
                <article class="floating-box"><div class="box-icon">🎉</div><h4>Para Festas</h4><p>Combos especiais de até 50 unidades para casamentos e aniversários.</p></article>
                <article class="floating-box"><div class="box-icon">📍</div><h4>Retirada Local</h4><p>Suas delícias são retiradas diretamente em nossa cozinha.</p></article>
                <article class="floating-box"><div class="box-icon">📱</div><h4>Atendimento</h4><p><strong>WhatsApp:</strong> +55 51 9115-6047<br>Atendimento humanizado.</p></article>
            </div>
        </section>

        <section id="aba-produtos" class="tab-section" data-emoji="🤤" data-boas-vindas="As opções avulsas e combos pequenos estão aqui. Leve mais e pague menos! 🤎">
            <div class="section-heading">
                <h2>Cardápio Padrão</h2>
                <p>Nossas receitas clássicas para adoçar o seu dia. Mais unidades = Mais economia.</p>
            </div>

            <div class="shop-layout">
                <div class="menu-grid">
                    
                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-tradicional"></div>
                        <div class="menu-item-info">
                            <span class="product-tag">Linha Tradicional</span>
                            <h4>Clássico (1 Unidade)</h4>
                            <div class="price-row">
                                <span class="price-value">R$ 7,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Clássico (1 un)', 7.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-tradicional"></div>
                        <div class="menu-item-info">
                            <span class="product-tag">Linha Tradicional</span>
                            <h4>Dueto Clássico (2 Unidades)</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 0,50!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 13,50</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Dueto Clássico (2 un)', 13.50)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-tradicional"></div>
                        <div class="menu-item-info">
                            <span class="product-tag">Linha Tradicional</span>
                            <h4>Trio Clássico (3 Unidades)</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 1,50!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 19,50</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Trio Clássico (3 un)', 19.50)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card premium-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-recheado"></div>
                        <div class="menu-item-info">
                            <span class="product-tag gold-tag">Linha Recheada</span>
                            <h4>Premium Recheado (1 Unidade)</h4>
                            <div class="price-row">
                                <span class="price-value">R$ 9,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Premium Recheado (1 un)', 9.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card premium-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-recheado"></div>
                        <div class="menu-item-info">
                            <span class="product-tag gold-tag">Linha Recheada</span>
                            <h4>Dueto Recheado (2 Unidades)</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 1,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 17,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Dueto Recheado (2 un)', 17.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card premium-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-recheado"></div>
                        <div class="menu-item-info">
                            <span class="product-tag gold-tag">Linha Recheada</span>
                            <h4>Trio Recheado (3 Unidades)</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 2,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 25,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Trio Recheado (3 un)', 25.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                </div>

                <aside class="cart-sidebar">
                    <h3>🛒 Seu Carrinho</h3>
                    <div id="cart-items-container-1"><p class="empty-cart-text">O carrinho está vazio.</p></div>
                    <div class="cart-total-row"><span>Total:</span><strong class="cart-total-display">R$ 0,00</strong></div>
                    <button class="checkout-btn" onclick="finalizarPedidoWhatsApp()">🛒 Fechar Pedido</button>
                </aside>
            </div>
        </section>

        <section id="aba-promocoes" class="tab-section" data-emoji="🤑" data-boas-vindas="Opa! Aqui é onde você economiza de verdade! Leve mais, pague menos! 📉💰">
            <div class="section-heading">
                <h2>Promoções & Combos para Festas</h2>
            </div>
            <div class="shop-layout">
                <div class="menu-grid">
                    
                    <article class="promo-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header">Linha Tradicional</div>
                        <div class="promo-body">
                            <h4>Box Família (5 un)</h4>
                            <div class="economia-badge">Economize R$ 4,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 31,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Box Família Tradicional (5 un)', 31.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header">Linha Tradicional</div>
                        <div class="promo-body">
                            <h4>Box Galera (10 un)</h4>
                            <div class="economia-badge">Economize R$ 10,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 60,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Box Galera Tradicional (10 un)', 60.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header">Linha Tradicional</div>
                        <div class="promo-body">
                            <h4>Box Eventos (20 un)</h4>
                            <div class="economia-badge">Economize R$ 25,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 115,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Box Eventos Tradicional (20 un)', 115.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card premium-promo-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header mega-header">👑 FESTA (TRADICIONAL)</div>
                        <div class="promo-body">
                            <h4>Mega Box Festa (50 un)</h4>
                            <div class="economia-badge pulse-badge">Economize R$ 85,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 265,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Mega Box Festa Tradicional (50 un)', 265.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card recheado-border" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header recheado-header">Linha Recheada</div>
                        <div class="promo-body">
                            <h4>Box Família Recheado (5 un)</h4>
                            <div class="economia-badge">Economize R$ 5,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 40,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Box Família Recheado (5 un)', 40.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card recheado-border" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header recheado-header">Linha Recheada</div>
                        <div class="promo-body">
                            <h4>Box Galera Recheado (10 un)</h4>
                            <div class="economia-badge">Economize R$ 15,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 75,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Box Galera Recheado (10 un)', 75.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card recheado-border" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header recheado-header">Linha Recheada</div>
                        <div class="promo-body">
                            <h4>Box Eventos Recheado (20 un)</h4>
                            <div class="economia-badge">Economize R$ 40,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 140,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Box Eventos Recheado (20 un)', 140.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="promo-card premium-promo-card recheado-border" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="promo-header mega-header recheado-header">👑 FESTA (RECHEADO)</div>
                        <div class="promo-body">
                            <h4>Mega Box Festa Recheado (50 un)</h4>
                            <div class="economia-badge pulse-badge">Economize R$ 120,00!</div>
                            <div class="price-row">
                                <div class="price-col"><span class="price-value">R$ 330,00</span></div>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Mega Box Festa Recheado (50 un)', 330.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                </div>

                <aside class="cart-sidebar">
                    <h3>🛒 Seu Carrinho</h3>
                    <div id="cart-items-container-2"><p class="empty-cart-text">O carrinho está vazio.</p></div>
                    <div class="cart-total-row"><span>Total:</span><strong class="cart-total-display">R$ 0,00</strong></div>
                    <button class="checkout-btn" onclick="finalizarPedidoWhatsApp()">🛒 Fechar Pedido</button>
                </aside>
            </div>
        </section>

        <section id="aba-eventos" class="tab-section" data-emoji="🎉" data-boas-vindas="As edições mais pedidas voltaram! Passe o mouse neles pra ver o que eu acho... 👀🔥">
            <div class="section-heading"><h2>Edições Especiais: Namorados & Copa</h2></div>
            <div class="shop-layout">
                <div class="menu-grid">
                    
                    <article class="menu-item-card love-card" onmouseenter="mascoteZoeira('Comprando um só pro Dia dos Namorados? O amor próprio é tudo... ou só tá encalhado mesmo! 🤣💔', '🕵️‍♂️')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image love-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag love-tag">Namorados (1 un)</span>
                            <h4>Amor Individual</h4>
                            <div class="price-row">
                                <span class="price-value">R$ 8,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Namorados Individual (1un)', 8.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card love-card" onmouseenter="mascoteZoeira('Dueto? Aí sim! Vai dividir o brownie e quem sabe mais alguma coisa hoje à noite... 😏🍷', '😏')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image love-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag love-tag">Namorados (2 un)</span>
                            <h4>Dueto Apaixonado</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 1,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 15,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Namorados Dueto (2un)', 15.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card love-card" onmouseenter="mascoteZoeira('Cinco brownies? Ih... fez besteira e tá tentando comprar o perdão, né? Boa sorte! 🤣💐', '😬')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image love-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag love-tag">Namorados (5 un)</span>
                            <h4>Bouquet de Brownies</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 4,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 36,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Namorados Bouquet (5un)', 36.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card love-card" onmouseenter="mascoteZoeira('Dez brownies românticos? Ou você vai pedir em casamento, ou tem dois(duas) namorados(as)! 👀💍', '😳')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image love-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag love-tag">Namorados (10 un)</span>
                            <h4>Caixa Romântica</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 12,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 68,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Namorados Caixa (10un)', 68.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card love-card" onmouseenter="mascoteZoeira('20 brownies pros namorados?! Isso não é um encontro, é uma suruba romântica! 🔥🌚', '🔥')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image love-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag love-tag">Namorados (20 un)</span>
                            <h4>Festa dos Apaixonados</h4>
                            <div class="economia-badge badge-pequeno pulse-badge">Economize R$ 30,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 130,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Namorados Festa (20un)', 130.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteZoeira('Um só pra curar o trauma do 7x1! Come logo antes que a Alemanha faça outro gol! 🇧🇷😭', '😭')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag cup-tag">Copa (1 un)</span>
                            <h4>Chocogol Canarinho</h4>
                            <div class="price-row">
                                <span class="price-value">R$ 8,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Copa Canarinho (1un)', 8.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteZoeira('Dois brownies pra dividir no intervalo... se o juiz não roubar da gente de novo! 🤬📺', '🤬')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag cup-tag">Copa (2 un)</span>
                            <h4>Dueto Torcida</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 1,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 15,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Copa Dueto (2un)', 15.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteZoeira('Goleada de brownie pra compensar aquele nosso centroavante perna de pau que não faz gol! ⚽🤦‍♂️', '🤦‍♂️')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag cup-tag">Copa (5 un)</span>
                            <h4>Combo Goleada</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 4,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 36,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Copa Goleada (5un)', 36.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteZoeira('10 brownies pra comer de ansiedade esperando o VAR analisar o impedimento! Haja coração! 💔📺', '😰')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag cup-tag">Copa (10 un)</span>
                            <h4>Caixa Artilheiro</h4>
                            <div class="economia-badge badge-pequeno">Economize R$ 12,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 68,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Copa Artilheiro (10un)', 68.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteZoeira('20 brownies da Copa?! Amigo, se o Hexa não vier com essa oferenda, eu mudo de país! 🏆🇧🇷', '🛐')" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <span class="product-tag cup-tag">Copa (20 un)</span>
                            <h4>Festa do Hexa</h4>
                            <div class="economia-badge badge-pequeno pulse-badge">Economize R$ 30,00!</div>
                            <div class="price-row">
                                <span class="price-value">R$ 130,00</span>
                                <button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Copa Hexa (20un)', 130.00)">+ Carrinho</button>
                            </div>
                        </div>
                    </article>

                </div>

                <aside class="cart-sidebar">
                    <h3>🛒 Seu Carrinho</h3>
                    <div id="cart-items-container-3"><p class="empty-cart-text">O carrinho está vazio.</p></div>
                    <div class="cart-total-row"><span>Total:</span><strong class="cart-total-display">R$ 0,00</strong></div>
                    <button class="checkout-btn" onclick="finalizarPedidoWhatsApp()">🛒 Fechar Pedido</button>
                </aside>
            </div>
        </section>

        <section id="aba-feedbacks" class="tab-section" data-emoji="💌" data-boas-vindas="Sua opinião é o ingrediente secreto da nossa receita! Conta pra gente o que achou! ✨">
            <div class="section-heading">
                <h2>Avaliações e Feedbacks</h2>
                <p>Nos ajude a melhorar ou deixe um recadinho carinhoso para a nossa equipe!</p>
            </div>
            
            <div class="feedback-container">
                <div class="feedback-form-box">
                    <h3>Deixe sua avaliação</h3>
                    <form id="feedback-form" onsubmit="enviarFeedback(event)">
                        <input type="text" id="feed-nome" placeholder="Seu Nome" required>
                        <select id="feed-nota" required>
                            <option value="" disabled selected>Que nota você dá?</option>
                            <option value="5">⭐⭐⭐⭐⭐ - Perfeito, derrete na boca!</option>
                            <option value="4">⭐⭐⭐⭐ - Muito Bom, recomendo</option>
                            <option value="3">⭐⭐⭐ - Bom, mas pode melhorar</option>
                            <option value="2">⭐⭐ - Não gostei muito</option>
                            <option value="1">⭐ - Decepcionante</option>
                        </select>
                        <textarea id="feed-mensagem" placeholder="Conta pra gente como foi sua experiência..." rows="5" required></textarea>
                        <button type="submit" class="auth-submit-btn">Enviar Feedback 🚀</button>
                    </form>
                </div>

                <div class="feedback-wall">
                    <h3>Mural de Clientes</h3>
                    <div id="lista-feedbacks">
                        <div class="feedback-card">
                            <div class="feed-stars">⭐⭐⭐⭐⭐</div>
                            <p class="feed-text">"Melhor brownie da cidade! O recheado de doce de leite é surreal. Atendimento super rápido pelo WhatsApp também."</p>
                            <span class="feed-author">- Maria Luiza S.</span>
                        </div>
                        <div class="feedback-card">
                            <div class="feed-stars">⭐⭐⭐⭐⭐</div>
                            <p class="feed-text">"Comprei a caixa de namorados e minha esposa amou. Salvou a minha pele haha! Muito capricho na embalagem."</p>
                            <span class="feed-author">- João Pedro</span>
                        </div>
                        <div class="feedback-card">
                            <div class="feed-stars">⭐⭐⭐⭐</div>
                            <p class="feed-text">"O brownie é ótimo, mas cheguei um pouco atrasada para retirar e quase me perdi. Tirando isso, a comida é perfeita."</p>
                            <span class="feed-author">- Fernanda Alves</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="aba-sobre" class="tab-section" data-emoji="📖" data-boas-vindas="Vem conhecer a nossa jornada, nossos produtos e os nossos segredos! 📖✨">
            <div class="section-heading">
                <h2>A Nossa História</h2>
                <p>Muito mais do que uma confeitaria, somos criadores de memórias.</p>
            </div>
            
            <div class="about-complex-container">
                <div class="about-sidebar">
                    <button class="about-tab-btn active" onclick="mudarSlideSobre(0, this)">1. Nossa Origem</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(1, this)">2. Nossos Objetivos</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(2, this)">3. A Excelência</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(3, this)">4. O Cardápio</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(4, this)">5. O Mascote</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(5, this)">6. Como Comprar</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(6, this)">7. Gratidão</button>
                </div>
                
                <div class="about-content-area">
                    <div class="about-slide active" id="slide-0">
                        <h3>🌱 De onde viemos</h3>
                        <p><strong>Quem Somos:</strong> A Dolce Brownie é uma confeitaria artesanal focada inteiramente em criar a experiência definitiva em chocolates e doces premium.</p>
                        <p><strong>Como a empresa surgiu:</strong> A Dolce Brownie nasceu na cozinha de casa, quando cinco amigos começaram a testar receitas em busca do brownie perfeito. Depois de várias tentativas, encontramos a combinação ideal: casquinha crocante por fora e interior macio por dentro. O que começou como uma forma de presentear amigos logo virou nossa paixão e deu origem à marca, criada para levar sabor e carinho em cada brownie.</p>
                    </div>

                    <div class="about-slide" id="slide-1">
                        <h3>🎯 Nossos Objetivos</h3>
                        <p>A Dolce Brownie tem como principal objetivo oferecer brownies artesanais de alta qualidade, preparados com ingredientes selecionados, muito cuidado e dedicação em cada etapa da produção.</p>
                        <p>A empresa busca proporcionar aos clientes uma experiência diferenciada através de produtos saborosos, criativos e feitos com carinho, capazes de transformar momentos simples do dia em ocasiões mais especiais e felizes.</p>
                        <p>Além de prezar pela qualidade dos brownies, a Dolce Brownie também procura oferecer um atendimento acolhedor e de confiança, valorizando a satisfação dos clientes e buscando sempre atender às suas expectativas.</p>
                    </div>

                    <div class="about-slide" id="slide-2">
                        <h3>✨ A Excelência nos Recheados</h3>
                        <p>A Dolce Brownie destaca-se pela excelência na produção artesanal de brownies recheados, unindo qualidade, sabor e sofisticação em cada detalhe. Nosso compromisso é oferecer produtos elaborados com ingredientes selecionados, proporcionando uma experiência única e marcante aos clientes.</p>
                        <p>Além do cuidado com o preparo, valorizamos a apresentação e a identidade da marca, transmitindo carinho, dedicação e autenticidade em cada produto. Dessa forma, buscamos transformar momentos simples em experiências especiais e memoráveis.</p>
                    </div>

                    <div class="about-slide" id="slide-3">
                        <h3>🍫 O Que Sai do Nosso Forno</h3>
                        <p><strong>O que vendemos & Explicação dos produtos:</strong> Somos especialistas em brownies! Vendemos nossa <em>Linha Tradicional</em> (o clássico atemporal) e a <em>Linha Recheada</em> (com coberturas e recheios intensos). Nossos formatos vão desde porções individuais até Mega Boxes com 50 unidades, ideais para festas. E claro, lançamos linhas temáticas sazonais como as amadas coleções de Dia dos Namorados e Copa.</p>
                        <p><strong>Diferenciais da Empresa:</strong> Não utilizamos atalhos. Nosso maior diferencial é a pureza dos ingredientes: usamos cacau nobre e manteiga de verdade, sem uso de conservantes artificiais. O assamento é milimetricamente calculado para manter a textura perfeita, e todos os doces são entregues frescos.</p>
                    </div>

                    <div class="about-slide" id="slide-4">
                        <h3>🧑‍🍳 O Dono da Cozinha</h3>
                        <p><strong>Quem é ele?</strong> Você já deve ter notado nosso Chef tagarela (o emoji 🧑‍🍳) flutuando no canto da tela enquanto você escolhe seus doces!</p>
                        <p><strong>O Significado:</strong> Ele representa a alma da nossa equipe e do nosso atendimento. Ele é descontraído, acolhedor e fala a verdade de forma leve (ele adora zoar seus pedidos no carrinho!). O mascote existe para lembrar que, por trás deste site, existem seres humanos dedicados e felizes fazendo a comida que vai chegar até você.</p>
                    </div>

                    <div class="about-slide" id="slide-5">
                        <h3>💳 Atendimento e Pagamentos</h3>
                        <p><strong>Plataformas de Atendimento:</strong> Todo o nosso contato para finalização de orçamentos, pedidos especiais e acompanhamento das encomendas é centralizado via <strong>WhatsApp</strong>. Essa foi a forma que encontramos para garantir um atendimento rápido, humano e sem burocracias.</p>
                        <p><strong>Formas de Pagamento:</strong> Buscamos máxima facilidade para você. Aceitamos:<br>
                        • <strong>Pix</strong> (nossa modalidade preferida pela agilidade).<br>
                        • <strong>Cartões de Crédito e Débito</strong>.<br>
                        • <strong>Dinheiro em espécie</strong> (pago diretamente no momento da retirada).</p>
                    </div>

                    <div class="about-slide" id="slide-6">
                        <h3>💖 Muito Obrigado!</h3>
                        <p>Construir a Dolce Brownie exigiu centenas de testes, noites em claro e fornalhas cheias. Mas tudo isso ganha sentido quando vemos o seu sorriso na hora da retirada e as mensagens maravilhosas que recebemos pós-festa.</p>
                        <p><strong>Encerramento:</strong> Agradecemos do fundo do coração por apoiar o nosso trabalho artesanal. Cada caixa que sai daqui é um pedaço do nosso sonho. Volte sempre, a nossa cozinha estará sempre de portas abertas (e fornos aquecidos) para você!</p>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <div id="mascote-container">
        <div id="balao-fala">Olá! Seja muito bem-vindo(a)! Fique à vontade para babar no nosso cardápio! 🍫✨</div>
        <div id="mascote-wrapper">
            <div id="mascote-emoji">🧑‍🍳</div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
"""

css_content = """
:root {
    --vinho-deep: #5A1E24; --rosa-light: #FDF4F5; --rosa-accent: #E58C93; --marrom-texto: #3E161A; --branco-card: #ffffff;
    --borda-elegante: rgba(90, 30, 36, 0.08); --font-heading: 'Playfair Display', serif; --font-body: 'Inter', sans-serif;
    --shadow-soft: 0 10px 30px rgba(90, 30, 36, 0.06); --shadow-hover: 0 15px 40px rgba(90, 30, 36, 0.12);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-body); background-color: var(--rosa-light); color: var(--marrom-texto); overflow-x: hidden; }
h1, h2, h3, h4, h5 { font-family: var(--font-heading); color: var(--vinho-deep); }

/* --- MODAL CHECKOUT OBRIGATÓRIO NO FINAL --- */
#checkout-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(90, 30, 36, 0.95); z-index: 10000; display: none; justify-content: center; align-items: center; backdrop-filter: blur(10px); }
.auth-modal { background: var(--branco-card); padding: 40px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.3); animation: slideInModal 0.3s ease; }
@keyframes slideInModal { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.auth-modal h2 { margin-bottom: 10px; font-size: 2rem; }
.auth-modal p { color: #666; margin-bottom: 25px; font-size: 0.9rem; line-height: 1.4; }
.auth-modal input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-family: var(--font-body); font-size: 1rem; outline: none; transition: border 0.3s; }
.auth-modal input:focus { border-color: var(--vinho-deep); }
.auth-submit-btn { width: 100%; background: var(--vinho-deep); color: white; padding: 15px; border: none; border-radius: 10px; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: background 0.3s; }
.auth-submit-btn:hover { background: #4A171D; }
.close-modal-btn { background: transparent; color: #888; border: none; margin-top: 15px; cursor: pointer; font-family: var(--font-body); text-decoration: underline; font-size: 0.9rem; }
.close-modal-btn:hover { color: var(--vinho-deep); }

.main-header { background-color: var(--vinho-deep); color: var(--rosa-light); text-align: center; padding: 50px 20px; }
.main-header h1 { font-size: 3.5rem; font-weight: 800; color: var(--rosa-light); margin-bottom: 5px; }
.navigation-bar { background-color: #4A171D; position: sticky; top: 0; z-index: 900; box-shadow: 0 4px 20px rgba(0,0,0,0.15); overflow-x: auto; white-space: nowrap;}
.nav-container { display: flex; justify-content: center; padding: 0 20px; }
.nav-btn { background: transparent; border: none; color: #f0c9cb; padding: 18px 25px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: color 0.3s ease; }
.nav-btn.active { color: #ffffff; border-bottom: 3px solid var(--rosa-accent); }
.global-delivery-alert { background-color: #8c2d36; color: #ffffff; text-align: center; padding: 12px 20px; font-size: 0.9rem; font-weight: 500; }
.content-wrapper { max-width: 1150px; margin: 50px auto; padding: 0 20px; }
.tab-section { display: none; animation: fadeInUp 0.5s ease; } .tab-section.active { display: block; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

/* Grid Layout */
.home-floating-grid { display: flex; flex-wrap: wrap; gap: 30px; justify-content: center; }
.floating-box { background: var(--branco-card); border-radius: 20px; padding: 35px 30px; width: calc(50% - 15px); text-align: center; box-shadow: var(--shadow-soft); }
.shop-layout { display: grid; grid-template-columns: 1fr 340px; gap: 40px; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 30px; }
.menu-item-card, .promo-card { background: var(--branco-card); border-radius: 20px; overflow: hidden; box-shadow: var(--shadow-soft); display: flex; flex-direction: column; border: 1px solid var(--borda-elegante); transition: transform 0.3s ease; }
.menu-item-card:hover, .promo-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-hover); }

/* Imagens */
.menu-item-image { height: 180px; background-size: cover; background-position: center; }
.img-tradicional { background-image: url('https://images.unsplash.com/photo-1564355808539-22fda35bed7e?auto=format&fit=crop&w=600&q=80'); }
.img-recheado { background-image: url('https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=600&q=80'); }
.love-brownie-img { background-image: url('https://images.unsplash.com/photo-1518192546895-11f898e4e941?auto=format&fit=crop&w=600&q=80'); }
.cup-brownie-img { background-image: url('https://images.unsplash.com/photo-1518622358385-8ea7d0794bf6?auto=format&fit=crop&w=600&q=80'); }

.love-card { border-color: rgba(230, 57, 70, 0.2); background: #fffaff; }
.cup-card { border-color: rgba(255, 183, 3, 0.2); background: #fffff2; }
.menu-item-info { padding: 25px; position: relative; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
.product-tag { position: absolute; top: -14px; left: 25px; background: var(--vinho-deep); color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
.gold-tag { background: #b08d57; } 
.love-tag { background: #e63946; } 
.cup-tag { background: #ffb703; color: #000; font-weight: 700; }
.price-row { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--borda-elegante); padding-top: 15px; margin-top: auto; }
.price-value { font-size: 1.25rem; font-weight: 700; color: var(--vinho-deep); }
.add-to-cart-btn { background-color: var(--vinho-deep); color: white; border: none; padding: 10px 18px; border-radius: 25px; cursor: pointer; font-size: 0.85rem; font-weight: 600; }

.promo-header { background: var(--vinho-deep); color: white; padding: 12px; text-align: center; font-weight: 600; font-size: 0.9rem; }
.mega-header { background: #1a1a1a; }
.recheado-header { background: #b08d57; }
.recheado-border { border-color: #b08d57; }
.promo-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; }

/* Badges de Economia */
.economia-badge { background: #25d366; color: white; display: inline-block; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: bold; margin: 8px 0; width: fit-content; }
.badge-pequeno { font-size: 0.75rem; padding: 3px 8px; margin: 5px 0 10px 0; background: #20b558; } 
.pulse-badge { animation: pulse 2s infinite; background: #e63946; }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }

/* Carrinho */
.cart-sidebar { background: var(--branco-card); border-radius: 20px; padding: 30px; position: sticky; top: 100px; box-shadow: var(--shadow-soft); height: fit-content; }
.cart-item-row { display: flex; flex-direction: column; margin-bottom: 15px; border-bottom: 1px dashed rgba(0,0,0,0.1); padding-bottom: 15px; }
.cart-item-info { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.95rem; }
.cart-item-info strong { color: var(--vinho-deep); }
.cart-controls { display: flex; align-items: center; gap: 10px; }
.cart-controls button { width: 28px; height: 28px; border-radius: 5px; border: none; background: #eee; cursor: pointer; font-weight: bold; color: #333; transition: background 0.2s; }
.cart-controls button:hover { background: #ddd; }
.cart-controls .remove-btn { background: #ffcccc; color: #cc0000; margin-left: auto; width: auto; padding: 0 10px; font-size: 0.8rem; }
.cart-controls .remove-btn:hover { background: #ff9999; }
.cart-total-row { display: flex; justify-content: space-between; margin-top: 20px; font-size: 1.1rem; }
.checkout-btn { background-color: #25d366; color: white; border: none; padding: 16px; width: 100%; border-radius: 12px; font-weight: 600; margin-top: 20px; cursor: pointer; transition: background 0.3s; }
.checkout-btn:hover { background-color: #1ebc5a; }

/* FEEDBACKS */
.feedback-container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px; }
.feedback-form-box { background: var(--branco-card); padding: 40px; border-radius: 20px; box-shadow: var(--shadow-soft); border: 1px solid var(--borda-elegante); }
.feedback-form-box h3 { margin-bottom: 20px; font-size: 1.5rem; color: var(--vinho-deep); }
.feedback-form-box input, .feedback-form-box select, .feedback-form-box textarea { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-family: var(--font-body); font-size: 1rem; outline: none; transition: border 0.3s; resize: vertical; }
.feedback-form-box input:focus, .feedback-form-box select:focus, .feedback-form-box textarea:focus { border-color: var(--vinho-deep); }
.feedback-wall { display: flex; flex-direction: column; gap: 20px; padding: 10px; }
.feedback-wall h3 { font-size: 1.5rem; margin-bottom: 10px; color: var(--vinho-deep); }
.feedback-card { background: var(--branco-card); padding: 25px; border-radius: 15px; box-shadow: var(--shadow-soft); border-left: 4px solid var(--rosa-accent); animation: fadeIn 0.5s ease; }
.feed-stars { font-size: 1.2rem; margin-bottom: 10px; }
.feed-text { font-style: italic; color: #555; margin-bottom: 15px; line-height: 1.6; }
.feed-author { font-weight: bold; color: var(--vinho-deep); font-size: 0.9rem; }

/* REGRAS RESPONSIVAS PARA CELULAR */
@media (max-width: 768px) {
    .shop-layout { grid-template-columns: 1fr; }
    .cart-sidebar { position: static; margin-top: 20px; }
    .home-floating-grid { flex-direction: column; }
    .floating-box { width: 100%; }
    .about-complex-container { flex-direction: column; }
    .about-sidebar { width: 100%; flex-direction: row; overflow-x: auto; white-space: nowrap; padding: 10px; }
    .about-tab-btn { padding: 12px 15px; border-left: none; border-bottom: 3px solid transparent; text-align: center; }
    .about-tab-btn.active { border-left-color: transparent; border-bottom-color: var(--rosa-accent); }
    .about-content-area { padding: 25px 20px; }
    .main-header h1 { font-size: 2.5rem; }
    .main-header { padding: 30px 20px; }
    .feedback-container { grid-template-columns: 1fr; }
    #mascote-container { left: 10px; bottom: 10px; }
    #mascote-emoji { font-size: 3.5rem; }
    #balao-fala { font-size: 0.8rem; padding: 10px 15px; max-width: 220px; }
}

/* Sobre Nós Complexo */
.about-complex-container { display: flex; background: var(--branco-card); border-radius: 20px; overflow: hidden; box-shadow: var(--shadow-soft); min-height: 420px; margin-top: 30px;}
.about-sidebar { width: 280px; background: var(--vinho-deep); display: flex; flex-direction: column; }
.about-tab-btn { background: transparent; color: rgba(255,255,255,0.7); border: none; padding: 18px 20px; text-align: left; font-size: 1rem; font-family: var(--font-heading); cursor: pointer; transition: all 0.3s; border-left: 4px solid transparent; border-bottom: 1px solid rgba(255,255,255,0.05); }
.about-tab-btn:hover { background: rgba(0,0,0,0.1); color: white; }
.about-tab-btn.active { color: white; border-left-color: var(--rosa-accent); background: rgba(0,0,0,0.2); }
.about-content-area { flex-grow: 1; padding: 40px 50px; position: relative; }
.about-slide { display: none; animation: fadeIn 0.5s ease; }
.about-slide.active { display: block; }
.about-slide h3 { font-size: 1.8rem; margin-bottom: 20px; }
.about-slide p { line-height: 1.8; color: #555; font-size: 1.05rem; margin-bottom: 15px; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* Widget Emoji Animado */
#mascote-container { position: fixed; bottom: 30px; left: 40px; display: flex; flex-direction: column-reverse; align-items: flex-start; z-index: 1000; pointer-events: none; }
#mascote-container * { pointer-events: auto; }
#balao-fala { background-color: var(--vinho-deep); color: white; padding: 16px 20px; border-radius: 16px; margin-bottom: 15px; font-size: 0.9rem; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-width: 280px; transition: all 0.3s ease; }
#mascote-emoji { font-size: 4.5rem; text-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: transform 0.2s ease; cursor: pointer; animation: flutuarEmoji 3s ease-in-out infinite; }
@keyframes flutuarEmoji { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
.emoji-animado-hover { animation: puloEmoji 0.3s infinite alternate !important; }
@keyframes puloEmoji { from { transform: translateY(0) scale(1); } to { transform: translateY(-15px) scale(1.1); } }
.emoji-explodindo { animation: explosaoEmoji 0.6s ease-out !important; }
@keyframes explosaoEmoji { 0% { transform: scale(1); } 50% { transform: scale(1.8) rotate(15deg); } 100% { transform: scale(1) rotate(0); } }
#toast-container { position: fixed; top: 20px; right: 20px; z-index: 9999; }
.toast { background: white; border-left: 5px solid #25d366; padding: 15px 25px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); animation: slideIn 0.3s ease forwards; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
"""

js_content = """
let emojiAtualDefault = "🧑‍🍳";
const numeroWhats = "555191156047"; 

let nomeCliente = "";

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
    
    mural.insertBefore(novoCard, mural.firstChild);
    
    document.getElementById('feed-nota').value = "";
    document.getElementById('feed-mensagem').value = "";
    
    showToast("Feedback enviado com sucesso! Muito obrigado! ❤️");
    
    const el = document.getElementById('mascote-emoji');
    el.innerText = "🥰";
    el.classList.add('emoji-explodindo');
    document.getElementById('balao-fala').innerHTML = "Que amor! Ler isso aquece nosso coração! 💖";
    setTimeout(() => {
        el.classList.remove('emoji-explodindo');
        mascoteResetaHover();
    }, 3500);
}

// --- CARRINHO ---
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

function fecharModalCheckout() {
    document.getElementById('checkout-overlay').style.display = 'none';
}

function confirmarNomeEEnviar(e) {
    e.preventDefault();
    nomeCliente = document.getElementById('checkout-nome').value;
    fecharModalCheckout();
    enviarParaOWhatsApp();
}

function finalizarPedidoWhatsApp() {
    if(Object.keys(carrinho).length === 0) return alert("Seu carrinho está vazio!");
    
    if(!nomeCliente) {
        document.getElementById('checkout-overlay').style.display = 'flex';
        return;
    }
    
    enviarParaOWhatsApp();
}

function enviarParaOWhatsApp() {
    let txt = `*Novo Pedido | Dolce Brownie*\\n*Cliente:* ${nomeCliente}\\n\\n`;
    let total = 0;
    for(let item in carrinho) {
        let sub = carrinho[item].preco * carrinho[item].qtd; total += sub;
        txt += `• ${carrinho[item].qtd}x ${item} (R$ ${sub.toFixed(2)})\\n`;
    }
    txt += `\\n*Valor Total:* R$ ${total.toFixed(2)}\\n\\nOlá! Gostaria de confirmar este pedido e agendar a retirada!`;
    window.open(`https://api.whatsapp.com/send?phone=${numeroWhats}&text=${encodeURIComponent(txt)}`);
}
"""

with open("index.html", "w", encoding="utf-8") as f: f.write(html_content)
with open("style.css", "w", encoding="utf-8") as f: f.write(css_content)
with open("script.js", "w", encoding="utf-8") as f: f.write(js_content)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
def open_browser(): webbrowser.open(f"http://localhost:{PORT}")
Timer(1.5, open_browser).start()
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("-> Portal atualizado: Agora 100% responsivo para celulares!")
    httpd.serve_forever()