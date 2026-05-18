"""
╔══════════════════════════════════════════╗
║        Dolce Brownie — Servidor Local    ║
║        python rodar_site.py              ║
╚══════════════════════════════════════════╝

Serve os arquivos estáticos do site (index.html, style.css,
script.js e imagens) e abre o navegador automaticamente.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import signal
from threading import Timer
from datetime import datetime

# ─── Configurações ────────────────────────────────────────────
PORT       = 8000
HOST       = "localhost"
DIRETORIO  = os.path.dirname(os.path.abspath(__file__))

ARQUIVOS_NECESSARIOS = ["index.html", "style.css", "script.js"]

# ─── Cores ANSI ───────────────────────────────────────────────
class Cor:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    VINHO  = "\033[38;5;124m"
    OURO   = "\033[38;5;136m"
    VERDE  = "\033[38;5;71m"
    CINZA  = "\033[38;5;244m"
    BRANCO = "\033[97m"
    ERRO   = "\033[38;5;196m"

def banner():
    v, o, b, r = Cor.VINHO, Cor.OURO, Cor.BOLD, Cor.RESET
    print(f"""
{v}{'─' * 46}{r}
{v}  🍫  {b}{o}Dolce Brownie{r}{v}  •  Servidor Local{r}
{v}{'─' * 46}{r}
""")

def log(nivel, msg):
    hora  = datetime.now().strftime("%H:%M:%S")
    icons = {"OK": f"{Cor.VERDE}✓{Cor.RESET}", "INFO": f"{Cor.OURO}•{Cor.RESET}", "ERRO": f"{Cor.ERRO}✗{Cor.RESET}"}
    icone = icons.get(nivel, "•")
    print(f"  {Cor.CINZA}{hora}{Cor.RESET}  {icone}  {msg}")

# ─── Handler customizado ──────────────────────────────────────
class SilentHandler(http.server.SimpleHTTPRequestHandler):
    """Suprime os logs de acesso padrão (muito verbosos) e exibe só o essencial."""

    def log_message(self, format, *args):
        codigo  = args[1] if len(args) > 1 else "???"
        recurso = args[0].split()[1] if args else "?"

        # Mostra apenas erros (4xx / 5xx)
        if isinstance(codigo, str) and not codigo.startswith(("2", "3")):
            log("ERRO", f"{Cor.ERRO}{codigo}{Cor.RESET}  {recurso}")

    def log_error(self, format, *args):
        log("ERRO", format % args)

# ─── Verificações ─────────────────────────────────────────────
def verificar_arquivos():
    os.chdir(DIRETORIO)
    faltando = [f for f in ARQUIVOS_NECESSARIOS if not os.path.isfile(f)]
    if faltando:
        log("ERRO", f"Arquivo(s) não encontrado(s): {Cor.ERRO}{', '.join(faltando)}{Cor.RESET}")
        log("INFO", f"Certifique-se de que o script está na mesma pasta que o site.")
        sys.exit(1)

    for f in ARQUIVOS_NECESSARIOS:
        tamanho = os.path.getsize(f)
        log("OK", f"{Cor.BRANCO}{f}{Cor.RESET}  {Cor.CINZA}({tamanho:,} bytes){Cor.RESET}")

def porta_disponivel(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) != 0

# ─── Encerramento gracioso ────────────────────────────────────
def ao_encerrar(sig, frame):
    print(f"\n\n  {Cor.OURO}Servidor encerrado. Até a próxima! 🍫{Cor.RESET}\n")
    sys.exit(0)

signal.signal(signal.SIGINT,  ao_encerrar)
signal.signal(signal.SIGTERM, ao_encerrar)

# ─── Main ─────────────────────────────────────────────────────
def main():
    banner()

    # Verifica arquivos
    print(f"  {Cor.OURO}Verificando arquivos...{Cor.RESET}\n")
    verificar_arquivos()

    # Verifica porta
    port = PORT
    if not porta_disponivel(port):
        log("INFO", f"Porta {port} ocupada — tentando {port + 1}...")
        port += 1
        if not porta_disponivel(port):
            log("ERRO", f"Portas {PORT} e {port} estão ocupadas. Encerre outro servidor e tente novamente.")
            sys.exit(1)

    url = f"http://{HOST}:{port}"

    print(f"""
  {Cor.VERDE}✓  Servidor iniciado com sucesso!{Cor.RESET}

  {Cor.OURO}🌐  Acesse:{Cor.RESET}  {Cor.BOLD}{url}{Cor.RESET}
  {Cor.CINZA}    Pasta:   {DIRETORIO}{Cor.RESET}

  {Cor.CINZA}Pressione Ctrl+C para encerrar.{Cor.RESET}
{'─' * 46}
""")

    # Abre o navegador após 1.2s
    Timer(1.2, lambda: webbrowser.open(url)).start()

    # Inicia o servidor
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, port), SilentHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    main()