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
            
            <div id="checkout-step-1">
                <h2>Quase lá!</h2>
                <p>Para enviarmos o seu pedido, como podemos chamar você?</p>
                <input type="text" id="checkout-nome" placeholder="Seu Nome Completo" required>
                <button type="button" class="auth-submit-btn" onclick="irParaOpcoes()">Próximo ➡️</button>
                <button type="button" class="close-modal-btn" onclick="fecharModalCheckout()">Voltar ao cardápio</button>
            </div>
            
            <div id="checkout-step-2" style="display: none;">
                <h2>Como deseja finalizar?</h2>
                <p style="margin-bottom: 20px;">Total do Pedido: <strong id="valor-final-pix" style="color: #5A1E24; font-size: 1.2rem;">R$ 0,00</strong></p>
                
                <button type="button" class="auth-submit-btn" onclick="mostrarQrCode()" style="background: #5A1E24; margin-bottom: 12px;">Pagar via QR Code / Pix 📱</button>
                <button type="button" class="auth-submit-btn" onclick="confirmarEEnviar(event, 'whats')" style="background: #25d366;">Pedir direto no WhatsApp 🚀</button>
                
                <button type="button" class="close-modal-btn" onclick="voltarParaNome()">⬅️ Voltar</button>
            </div>

            <div id="checkout-step-3" style="display: none;">
                <h2>Pagamento via Pix</h2>
                <p style="margin-bottom: 10px;">Valor Total: <strong id="valor-final-pix-2" style="color: #5A1E24; font-size: 1.2rem;">R$ 0,00</strong></p>
                
                <div style="background: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px dashed #ccc; margin-bottom: 15px;">
                    <img src="qrcode.png" alt="QR Code Pix" style="width: 150px; height: 150px; border-radius: 8px; margin-bottom: 10px; object-fit: contain;">
                    <p style="font-size: 0.9rem; color: #555;">Abra o app do seu banco e escaneie o código acima.</p>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <p style="font-size: 0.9rem;">Ou use a nossa Chave Celular:</p>
                    <strong style="font-size: 1.1rem; color: #5A1E24; user-select: all;">5551991156047</strong>
                </div>

                <button type="button" class="auth-submit-btn" onclick="confirmarEEnviar(event, 'pix')" style="background: #25d366;">Enviar Comprovante no Whats 🚀</button>
                <button type="button" class="close-modal-btn" onclick="voltarParaOpcoes()">⬅️ Voltar</button>
            </div>

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
            <button class="nav-btn" onclick="alternarAba('feedbacks')">Feedbacks</button>
            <button class="nav-btn" onclick="alternarAba('sobre')">Sobre Nós</button>
        </div>
    </nav>

    <div class="global-delivery-alert">
        <span>📍 <strong>AVISO:</strong> Operamos exclusivamente via <strong>retirada agendada</strong>.</span>
    </div>

    <main class="content-wrapper">

        <section id="aba-home" class="tab-section active" data-emoji="🧑‍🍳" data-boas-vindas="Olá! Seja muito bem-vindo(a)! Fique à vontade para babar no nosso cardápio atualizado! 🍫✨">
            <div class="clean-hero">
                <h3>A Experiência Definitiva em Brownies</h3>
                <p class="hero-subtitle">Casquinha crocante, interior cremoso e ingredientes premium. A alta confeitaria pronta para o seu dia a dia.</p>
                <div class="divider"></div>
            </div>

            <div class="home-floating-grid">
                <article class="floating-box"><div class="box-icon">✨</div><h4>Variedade</h4><p>Temos desde o brownie clássico até caixas para presente.</p></article>
                <article class="floating-box"><div class="box-icon">🎉</div><h4>Para Você</h4><p>Doces feitos artesanalmente para adoçar qualquer momento do seu dia.</p></article>
                <article class="floating-box"><div class="box-icon">📍</div><h4>Retirada Local</h4><p>Suas delícias são retiradas diretamente em nossa cozinha com horário marcado.</p></article>
                <article class="floating-box"><div class="box-icon">📱</div><h4>Atendimento</h4><p><strong>WhatsApp:</strong> +55 51 9115-6047<br>Tire suas dúvidas conosco.</p></article>
            </div>
        </section>

        <section id="aba-produtos" class="tab-section" data-emoji="🤤" data-boas-vindas="O cardápio oficial! Escolha com o coração... e com a barriga! 🤎">
            <div class="section-heading">
                <h2>Nosso Cardápio</h2>
                <p>Todas as nossas delícias em um só lugar.</p>
            </div>

            <div class="shop-layout">
                <div class="menu-grid">
                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-tradicional"></div>
                        <div class="menu-item-info">
                            <h4>Brownie de chocolate simples</h4>
                            <div class="price-row"><span class="price-value">R$ 7,00</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Brownie simples', 7.00)">+ Carrinho</button></div>
                        </div>
                    </article>

                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-recheado"></div>
                        <div class="menu-item-info">
                            <h4>Brownie de chocolate recheado</h4>
                            <div class="price-row"><span class="price-value">R$ 9,00</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Brownie recheado', 9.00)">+ Carrinho</button></div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <h4>Brownie CHOCOGOL</h4>
                            <div class="price-row"><span class="price-value">R$ 8,00</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Brownie CHOCOGOL', 8.00)">+ Carrinho</button></div>
                        </div>
                    </article>

                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-tradicional"></div>
                        <div class="menu-item-info">
                            <h4>O duo predileto</h4>
                            <div class="price-row"><span class="price-value">R$ 13,00</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('O duo predileto', 13.00)">+ Carrinho</button></div>
                        </div>
                    </article>

                    <article class="menu-item-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image img-caixa"></div>
                        <div class="menu-item-info">
                            <h4>Quarteto Brownie</h4>
                            <div class="price-row"><span class="price-value">R$ 25,50</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Quarteto Brownie', 25.50)">+ Carrinho</button></div>
                        </div>
                    </article>

                    <article class="menu-item-card cup-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image cup-brownie-img"></div>
                        <div class="menu-item-info">
                            <h4>CHOCOGOL(2un)</h4>
                            <div class="price-row"><span class="price-value">R$ 15,00</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('CHOCOGOL(2un)', 15.00)">+ Carrinho</button></div>
                        </div>
                    </article>

                    <article class="menu-item-card love-card" onmouseenter="mascoteAnimaHover()" onmouseleave="mascoteResetaHover()">
                        <div class="menu-item-image love-brownie-img"></div>
                        <div class="menu-item-info">
                            <h4>Dolce amor</h4>
                            <div class="price-row"><span class="price-value">R$ 16,00</span><button class="add-to-cart-btn" onclick="adicionarAoCarrinho('Dolce amor', 16.00)">+ Carrinho</button></div>
                        </div>
                    </article>
                </div>

                <aside class="cart-sidebar">
                    <h3>🛒 Seu Carrinho</h3>
                    <div id="cart-items-container-1"><p class="empty-cart-text">O carrinho está vazio.</p></div>
                    <div class="cart-total-row"><span>Total:</span><strong class="cart-total-display">R$ 0,00</strong></div>
                    <button class="checkout-btn" onclick="iniciarCheckout()">🛒 Fechar Pedido</button>
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
                        <textarea id="feed-mensagem" placeholder="Conta pra gente como foi sua experiência..." rows="4" required></textarea>
                        <button type="submit" class="auth-submit-btn">Enviar Feedback 🚀</button>
                    </form>
                </div>

                <div class="feedback-wall">
                    <h3>Mural de Clientes</h3>
                    <div id="lista-feedbacks">
                        <div class="feedback-card">
                            <div class="feed-stars">⭐⭐⭐⭐⭐</div>
                            <p class="feed-text">"Melhor brownie da cidade! O Quarteto Brownie é perfeito pra presentear."</p>
                            <span class="feed-author">- Maria Luiza S.</span>
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
                    <button class="about-tab-btn active" onclick="mudarSlideSobre(0, this)">1. Nossos Objetivos</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(1, this)">2. Nossa Excelência</button>
                    <button class="about-tab-btn" onclick="mudarSlideSobre(2, this)">3. O Mascote</button>
                </div>
                
                <div class="about-content-area">
                    <div class="about-slide active" id="slide-0">
                        <h3>🎯 Nossos Objetivos</h3>
                        <p style="text-align: justify;">A Dolce Brownie tem como principal objetivo oferecer brownies artesanais de alta qualidade, preparados com ingredientes selecionados, muito cuidado e dedicação em cada etapa da produção. A empresa busca proporcionar aos clientes uma experiência diferenciada através de produtos saborosos, criativos e feitos com carinho, capazes de transformar momentos simples do dia em ocasiões mais especiais e felizes.</p>
                        <p style="text-align: justify;">Além de prezar pela qualidade dos brownies, a Dolce Brownie também procura oferecer um atendimento acolhedor e de confiança, valorizando a satisfação dos clientes e buscando sempre atender às suas expectativas. A empresa pretende crescer no mercado de doces, conquistando reconhecimento pela excelência dos produtos, pela criatividade dos sabores e pelo compromisso em levar alegria e bem-estar através de cada brownie produzido.</p>
                    </div>

                    <div class="about-slide" id="slide-1">
                        <h3>✨ Nossa Excelência</h3>
                        <p style="text-align: justify;">A Dolce Brownie destaca-se pela excelência na produção artesanal de brownies recheados, unindo qualidade, sabor e sofisticação em cada detalhe. Nosso compromisso é oferecer produtos elaborados com ingredientes selecionados, proporcionando uma experiência única e marcante aos clientes.</p>
                        <p style="text-align: justify;">Além do cuidado com o preparo, valorizamos a apresentação e a identidade da marca, transmitindo carinho, dedicação e autenticidade em cada produto. Dessa forma, buscamos transformar momentos simples em experiências especiais e memoráveis.</p>
                    </div>

                    <div class="about-slide" id="slide-2">
                        <h3>🧑‍🍳 O Dono da Cozinha</h3>
                        <p>Você já deve ter notado nosso Chef flutuando no canto da tela! Ele representa a alma do nosso atendimento: descontraído e acolhedor.</p>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <div id="mascote-container">
        <div id="balao-fala">Olá! Seja muito bem-vindo(a)! Fique à vontade para babar no nosso cardápio atualizado! 🍫✨</div>
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
    --vinho-deep: #5A1E24; 
    --rosa-light: #FDF4F5; 
    --rosa-accent: #E58C93; 
    --marrom-texto: #3E161A; 
    --branco-card: #ffffff; 
    --borda-elegante: rgba(90, 30, 36, 0.08); 
    --font-heading: 'Playfair Display', serif; 
    --font-body: 'Inter', sans-serif; 
    --shadow-soft: 0 10px 30px rgba(90, 30, 36, 0.06); 
    --shadow-hover: 0 15px 40px rgba(90, 30, 36, 0.12); 
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-body); background-color: var(--rosa-light); color: var(--marrom-texto); overflow-x: hidden; }
h1, h2, h3, h4, h5 { font-family: var(--font-heading); color: var(--vinho-deep); }

/* MODAL DE CHECKOUT */
#checkout-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(90, 30, 36, 0.95); z-index: 10000; display: none; justify-content: center; align-items: center; backdrop-filter: blur(10px); }
.auth-modal { background: var(--branco-card); padding: 40px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.3); animation: slideInModal 0.3s ease; }
@keyframes slideInModal { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.auth-modal h2 { margin-bottom: 10px; font-size: 1.8rem; color: var(--vinho-deep); }
.auth-modal p { color: #666; margin-bottom: 25px; font-size: 0.9rem; line-height: 1.4; }
.auth-modal input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-family: var(--font-body); font-size: 1rem; outline: none; }
.auth-submit-btn { width: 100%; background: var(--vinho-deep); color: white; padding: 15px; border: none; border-radius: 10px; font-weight: bold; font-size: 1.05rem; cursor: pointer; transition: filter 0.3s; margin-bottom: 5px; }
.auth-submit-btn:hover { filter: brightness(0.9); }
.close-modal-btn { background: transparent; color: #888; border: none; margin-top: 10px; cursor: pointer; text-decoration: underline; font-size: 0.9rem; width: 100%; padding: 10px;}

.main-header { background-color: var(--vinho-deep); color: var(--rosa-light); text-align: center; padding: 40px 20px; }
.main-header h1 { font-size: 3rem; font-weight: 800; color: var(--rosa-light); margin-bottom: 5px; }
.minimal-slogan { font-style: italic; font-size: 1.1rem; opacity: 0.9; }

.navigation-bar { background-color: #4A171D; position: sticky; top: 0; z-index: 900; box-shadow: 0 4px 20px rgba(0,0,0,0.15); overflow-x: auto; white-space: nowrap;}
.nav-container { display: flex; justify-content: center; padding: 0 20px; }
.nav-btn { background: transparent; border: none; color: #f0c9cb; padding: 18px 25px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: color 0.3s ease; }
.nav-btn.active { color: #ffffff; border-bottom: 3px solid var(--rosa-accent); }

.global-delivery-alert { background-color: #8c2d36; color: #ffffff; text-align: center; padding: 10px 20px; font-size: 0.9rem; }

.content-wrapper { max-width: 1150px; margin: 40px auto; padding: 0 20px; }
.tab-section { display: none; animation: fadeInUp 0.5s ease; } .tab-section.active { display: block; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

.home-floating-grid { display: flex; flex-wrap: wrap; gap: 30px; justify-content: center; margin-top: 30px;}
.floating-box { background: var(--branco-card); border-radius: 20px; padding: 30px; width: calc(50% - 15px); text-align: center; box-shadow: var(--shadow-soft); }
.box-icon { font-size: 2.5rem; margin-bottom: 15px; }

.shop-layout { display: grid; grid-template-columns: 1fr 340px; gap: 40px; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 25px; }
.menu-item-card { background: var(--branco-card); border-radius: 20px; overflow: hidden; box-shadow: var(--shadow-soft); display: flex; flex-direction: column; border: 1px solid var(--borda-elegante); transition: transform 0.3s ease; }
.menu-item-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-hover); }
.menu-item-image { height: 160px; background-size: cover; background-position: center; }

.img-tradicional { background-image: url('https://images.unsplash.com/photo-1564355808539-22fda35bed7e?auto=format&fit=crop&w=600&q=80'); }
.img-recheado { background-image: url('https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=600&q=80'); }
.cup-brownie-img { background-image: url('https://images.unsplash.com/photo-1518622358385-8ea7d0794bf6?auto=format&fit=crop&w=600&q=80'); }
.love-brownie-img { background-image: url('https://images.unsplash.com/photo-1518192546895-11f898e4e941?auto=format&fit=crop&w=600&q=80'); }
.img-caixa { background-image: url('https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&w=600&q=80'); }
.love-card { border-color: rgba(230, 57, 70, 0.2); background: #fffaff; }
.cup-card { border-color: rgba(255, 183, 3, 0.2); background: #fffff2; }

.menu-item-info { padding: 20px; position: relative; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
.price-row { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--borda-elegante); padding-top: 15px; margin-top: auto; }
.price-value { font-size: 1.2rem; font-weight: 700; color: var(--vinho-deep); }
.add-to-cart-btn { background-color: var(--vinho-deep); color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-size: 0.85rem; font-weight: 600; }

.cart-sidebar { background: var(--branco-card); border-radius: 20px; padding: 25px; position: sticky; top: 90px; box-shadow: var(--shadow-soft); height: fit-content; }
.cart-item-row { display: flex; flex-direction: column; margin-bottom: 12px; border-bottom: 1px dashed #ccc; padding-bottom: 12px; }
.cart-item-info { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.95rem; }
.cart-controls { display: flex; align-items: center; gap: 8px; }
.cart-controls button { width: 25px; height: 25px; border-radius: 5px; border: none; background: #eee; cursor: pointer; font-weight: bold; }
.cart-controls .remove-btn { background: #ffcccc; color: #cc0000; margin-left: auto; width: auto; padding: 0 8px; font-size: 0.8rem; }
.checkout-btn { background-color: #25d366; color: white; border: none; padding: 15px; width: 100%; border-radius: 12px; font-weight: 600; margin-top: 15px; cursor: pointer; }

.feedback-container { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px; }
.feedback-form-box { background: var(--branco-card); padding: 30px; border-radius: 20px; box-shadow: var(--shadow-soft); }
.feedback-form-box input, .feedback-form-box select, .feedback-form-box textarea { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-family: var(--font-body); }
.feedback-wall { display: flex; flex-direction: column; gap: 15px; }
.feedback-card { background: var(--branco-card); padding: 20px; border-radius: 15px; box-shadow: var(--shadow-soft); border-left: 4px solid var(--rosa-accent); }

.about-complex-container { display: flex; background: var(--branco-card); border-radius: 20px; overflow: hidden; box-shadow: var(--shadow-soft); min-height: 380px; margin-top: 20px;}
.about-sidebar { width: 260px; background: var(--vinho-deep); display: flex; flex-direction: column; }
.about-tab-btn { background: transparent; color: rgba(255,255,255,0.7); border: none; padding: 18px 20px; text-align: left; font-size: 1rem; font-family: var(--font-heading); cursor: pointer; border-left: 4px solid transparent; border-bottom: 1px solid rgba(255,255,255,0.05); }
.about-tab-btn.active { color: white; border-left-color: var(--rosa-accent); background: rgba(0,0,0,0.2); }
.about-content-area { flex-grow: 1; padding: 30px 40px; }
.about-slide { display: none; animation: fadeIn 0.5s ease; } .about-slide.active { display: block; }
.about-slide h3 { font-size: 1.6rem; margin-bottom: 15px; } .about-slide p { line-height: 1.6; color: #555; font-size: 1rem; margin-bottom: 15px; }

#mascote-container { position: fixed; bottom: 20px; left: 30px; display: flex; flex-direction: column-reverse; align-items: flex-start; z-index: 1000; pointer-events: none; }
#mascote-container * { pointer-events: auto; }
#balao-fala { background-color: var(--vinho-deep); color: white; padding: 15px; border-radius: 16px; margin-bottom: 10px; font-size: 0.9rem; box-shadow: 0 10px 20px rgba(0,0,0,0.2); max-width: 250px; }
#mascote-emoji { font-size: 4rem; text-shadow: 0 5px 15px rgba(0,0,0,0.2); cursor: pointer; animation: flutuarEmoji 3s ease-in-out infinite; }
@keyframes flutuarEmoji { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
.emoji-animado-hover { animation: puloEmoji 0.3s infinite alternate !important; }
@keyframes puloEmoji { from { transform: translateY(0) scale(1); } to { transform: translateY(-15px) scale(1.1); } }

#toast-container { position: fixed; top: 20px; right: 20px; z-index: 9999; }
.toast { background: white; border-left: 5px solid #25d366; padding: 15px 20px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); animation: slideIn 0.3s ease forwards; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

@media (max-width: 768px) {
    .shop-layout { grid-template-columns: 1fr; }
    .cart-sidebar { position: static; margin-top: 20px; }
    .home-floating-grid { flex-direction: column; }
    .floating-box { width: 100%; }
    .about-complex-container { flex-direction: column; }
    .about-sidebar { width: 100%; flex-direction: row; overflow-x: auto; white-space: nowrap; padding: 10px; }
    .about-tab-btn { padding: 10px 15px; border-left: none; border-bottom: 3px solid transparent; text-align: center; }
    .about-tab-btn.active { border-left-color: transparent; border-bottom-color: var(--rosa-accent); }
    .about-content-area { padding: 20px; }
    .main-header h1 { font-size: 2.2rem; }
    .feedback-container { grid-template-columns: 1fr; }
    #mascote-container { left: 10px; bottom: 10px; }
    #mascote-emoji { font-size: 3rem; }
    #balao-fala { font-size: 0.8rem; padding: 10px; max-width: 200px; }
}
"""

js_content = """
let emojiAtualDefault = "🧑‍🍳";
const numeroWhats = "5551991156047"; 
let nomeCliente = "";
let valorTotalAtual = 0;

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
    const t = document.createElement('div'); 
    t.className = 'toast'; 
    t.innerHTML = `✅ ${msg}`;
    container.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

function mascoteAnimaHover() {
    document.getElementById('mascote-emoji').innerText = "😋";
    document.getElementById('mascote-emoji').classList.add('emoji-animado-hover');
    document.getElementById('balao-fala').innerHTML = "Nossa, essa escolha vale muito a pena! 🌟";
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
    novoCard.innerHTML = `<div class="feed-stars">${estrelas}</div><p class="feed-text">"${mensagem}"</p><span class="feed-author">- ${nome}</span>`;
    
    mural.insertBefore(novoCard, mural.firstChild);
    document.getElementById('feed-nota').value = ""; 
    document.getElementById('feed-mensagem').value = "";
    showToast("Feedback enviado!");
}

let carrinho = {};

function adicionarAoCarrinho(nome, preco, silent = false) {
    if(carrinho[nome]) carrinho[nome].qtd++; 
    else carrinho[nome] = { preco: preco, qtd: 1 };
    atualizarCarrinho();
    if(!silent) showToast(`Adicionado: ${nome}`);
}

function diminuirDoCarrinho(nome) {
    if(carrinho[nome]) {
        carrinho[nome].qtd--;
        if(carrinho[nome].qtd <= 0) delete carrinho[nome];
        atualizarCarrinho();
    }
}

function removerDoCarrinho(nome) {
    if(carrinho[nome]) { delete carrinho[nome]; atualizarCarrinho(); showToast(`Removido: ${nome}`); }
}

function atualizarCarrinho() {
    const container = document.getElementById('cart-items-container-1');
    const totaisDisplays = document.querySelectorAll('.cart-total-display');
    valorTotalAtual = 0;
    
    if(Object.keys(carrinho).length === 0) { 
        if(container) container.innerHTML = "<p class='empty-cart-text'>O carrinho está vazio.</p>";
        totaisDisplays.forEach(td => td.innerText = "R$ 0,00");
        return; 
    }
    
    let htmlCarrinho = "";
    for(let item in carrinho) {
        let sub = carrinho[item].preco * carrinho[item].qtd; 
        valorTotalAtual += sub;
        htmlCarrinho += `
        <div class="cart-item-row">
            <div class="cart-item-info"><strong>${item}</strong><span>R$ ${sub.toFixed(2)}</span></div>
            <div class="cart-controls">
                <button onclick="diminuirDoCarrinho('${item}')">-</button>
                <span>${carrinho[item].qtd}</span>
                <button onclick="adicionarAoCarrinho('${item}', ${carrinho[item].preco}, true)">+</button>
                <button class="remove-btn" onclick="removerDoCarrinho('${item}')">🗑️ Remover</button>
            </div>
        </div>`;
    }
    if(container) container.innerHTML = htmlCarrinho;
    totaisDisplays.forEach(td => td.innerText = `R$ ${valorTotalAtual.toFixed(2)}`);
}

function iniciarCheckout() {
    if(Object.keys(carrinho).length === 0) return alert("Seu carrinho está vazio!");
    document.getElementById('checkout-step-1').style.display = 'block';
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-3').style.display = 'none';
    document.getElementById('checkout-overlay').style.display = 'flex';
}

function fecharModalCheckout() { document.getElementById('checkout-overlay').style.display = 'none'; }

function irParaOpcoes() {
    const inputNome = document.getElementById('checkout-nome');
    if(!inputNome.value) { alert("Por favor, preencha o seu nome."); return; }
    nomeCliente = inputNome.value;
    document.getElementById('valor-final-pix').innerText = `R$ ${valorTotalAtual.toFixed(2)}`;
    document.getElementById('checkout-step-1').style.display = 'none';
    document.getElementById('checkout-step-2').style.display = 'block';
}

function voltarParaNome() {
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-1').style.display = 'block';
}

function mostrarQrCode() {
    document.getElementById('valor-final-pix-2').innerText = `R$ ${valorTotalAtual.toFixed(2)}`;
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-3').style.display = 'block';
}

function voltarParaOpcoes() {
    document.getElementById('checkout-step-3').style.display = 'none';
    document.getElementById('checkout-step-2').style.display = 'block';
}

function confirmarEEnviar(e, tipo) {
    e.preventDefault(); 
    fecharModalCheckout(); 
    
    let txt = `*Novo Pedido | Dolce Brownie*\\n*Cliente:* ${nomeCliente}\\n\\n`;
    for(let item in carrinho) {
        let sub = carrinho[item].preco * carrinho[item].qtd;
        txt += `• ${carrinho[item].qtd}x ${item} (R$ ${sub.toFixed(2)})\\n`;
    }
    txt += `\\n*Valor Total:* R$ ${valorTotalAtual.toFixed(2)}\\n`;
    
    if(tipo === 'pix') {
        txt += `*Pagamento:* Pix / QR Code\\n\\nOlá! Estou enviando o comprovante do Pix em seguida e gostaria de agendar a retirada!`;
    } else {
        txt += `*Pagamento:* A combinar no Whats\\n\\nOlá! Gostaria de finalizar meu pedido e agendar a retirada!`;
    }
    
    window.open(`https://api.whatsapp.com/send?phone=${numeroWhats}&text=${encodeURIComponent(txt)}`);
}
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
with open("style.css", "w", encoding="utf-8") as f:
    f.write(css_content)
with open("script.js", "w", encoding="utf-8") as f:
    f.write(js_content)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

Timer(1.5, open_browser).start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("-> Portal Dolce Brownie atualizado com QR Code e Chave Celular!")
    httpd.serve_forever()
