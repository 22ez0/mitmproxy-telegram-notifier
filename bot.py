#!/usr/bin/env python3
"""
Bot Telegram - MITMProxy Notifier
Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
"""
import os
import telebot
import requests
from urllib.parse import urlparse, quote
from shared_storage import storage

TELEGRAM_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

def get_domain():
    """Detecta automaticamente o dominio baseado no ambiente (Replit, Render, local)"""
    if os.environ.get("RENDER"):
        render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
        if render_url:
            return render_url.replace("https://", "").replace("http://", "")
    
    replit_domain = os.environ.get("REPLIT_DEV_DOMAIN") or os.environ.get("REPLIT_DOMAINS")
    if replit_domain:
        return replit_domain
    
    return "localhost:5000"

DOMAIN = get_domain()

def shorten_url(long_url: str, original_url: str, url_id: str) -> str:
    """Encurta URL usando is.gd com nome personalizado"""
    try:
        parsed = urlparse(original_url)
        domain_name = parsed.netloc.replace('www.', '').split('.')[0]
        custom_slug = f"{domain_name}_{url_id}"
        
        response = requests.get(
            f"https://is.gd/create.php?format=simple&url={quote(long_url)}&shorturl={custom_slug}",
            timeout=5
        )
        
        if response.status_code == 200 and not response.text.startswith('Error'):
            short_url = response.text.strip()
            print(f"[Bot] URL encurtada: {long_url} -> {short_url}")
            return short_url
        else:
            response_fallback = requests.get(
                f"https://is.gd/create.php?format=simple&url={quote(long_url)}",
                timeout=5
            )
            if response_fallback.status_code == 200:
                return response_fallback.text.strip()
            return long_url
    except Exception as e:
        print(f"[Bot] Erro no encurtador: {e}")
        return long_url

if not TELEGRAM_BOT_TOKEN or ":" not in TELEGRAM_BOT_TOKEN:
    print("ERRO: TG_BOT_TOKEN nao configurado corretamente")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """Bem-vindo ao MITMProxy Telegram Notifier!

Este bot gera links especiais que capturam headers de qualquer site.

Comandos disponiveis:
/intercept URL - Gera link de interceptacao
/help - Ajuda e instrucoes
/status - Verificar status do sistema
/criadores - Informacoes sobre os criadores

Exemplo de uso:
/intercept https://www.example.com/login

O bot vai gerar um link que funciona em qualquer navegador (Chrome, Safari, Firefox, etc)!"""
    
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """Como usar o Interceptor de Headers:

1. Envie o comando com a URL que deseja interceptar:
   /intercept https://www.example.com/login

2. O bot vai gerar um link especial de interceptacao

3. Copie o link e abra em QUALQUER navegador:
   - Chrome
   - Safari
   - Firefox
   - Edge
   - Browser do Telegram

4. Quando voce clicar no link, o bot vai:
   - Capturar todos os headers da requisicao
   - Enviar para voce em formato Python pronto para usar
   - Redirecionar para o site original

Os headers sao enviados neste formato:
url = 'https://...'
headers = {
    'accept': '...',
    'user-agent': '...',
}

Para mais informacoes, use /criadores"""
    
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['status'])
def send_status(message):
    chat_id = os.environ.get("TG_CHAT_ID", "")
    
    status_text = f"""Status do Sistema:

Bot: Ativo
Chat ID configurado: {'Sim' if chat_id else 'Nao'}
Token: Valido

O sistema esta pronto para receber notificacoes."""
    
    bot.reply_to(message, status_text)

@bot.message_handler(commands=['criadores'])
def send_creators(message):
    creators_text = """Criadores do Bot:

Telegram: @vgsswon
Grupo oficial: https://t.me/+RriqgodAtpY4NTgx

Entre no grupo para suporte e atualizacoes!"""
    
    bot.reply_to(message, creators_text)

@bot.message_handler(commands=['intercept'])
def intercept_command(message):
    text = message.text.replace('/intercept', '').strip()
    
    if not text:
        bot.reply_to(message, "Uso: /intercept URL\n\nExemplo:\n/intercept https://www.example.com/login")
        return
    
    try:
        parsed = urlparse(text)
        if parsed.scheme in ('http', 'https') and parsed.netloc:
            url_id = storage.store(text)
            intercept_link = f"https://{DOMAIN}/i/{url_id}"
            short_link = shorten_url(intercept_link, text, url_id)
            
            response = f"""✅ Link gerado!

🎯 Clique aqui:
{short_link}

📌 URL alvo: {text}

💡 Ao clicar, os headers serao capturados e enviados automaticamente em formato Python."""
            
            bot.reply_to(message, response, disable_web_page_preview=False)
        else:
            bot.reply_to(message, "❌ URL invalida. Envie uma URL completa comecando com http:// ou https://\n\nExemplo:\n/intercept https://www.example.com/login")
    except Exception as e:
        print(f"[Bot] Erro ao processar comando intercept: {e}")
        bot.reply_to(message, "❌ Erro ao processar URL. Use /help para ver exemplos.")

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.reply_to(message, "Comando nao reconhecido.\n\nUse /intercept URL para gerar um link de interceptacao.\n\nExemplo:\n/intercept https://www.example.com/login")

def main():
    print("[Bot] Iniciando bot Telegram...")
    print("[Bot] Bot pronto e aguardando comandos")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
