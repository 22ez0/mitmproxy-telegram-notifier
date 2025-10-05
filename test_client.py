#!/usr/bin/env python3
"""
Cliente de teste para MITMProxy
Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
"""
import requests
import time
from typing import Dict

PROXY_URL = "http://localhost:8080"

proxies: Dict[str, str] = {
    'http': PROXY_URL,
    'https': PROXY_URL,
}

test_urls = [
    "http://httpbin.org/get",
    "http://httpbin.org/login",
    "http://httpbin.org/auth/bearer",
    "http://httpbin.org/signin",
    "http://httpbin.org/user/authenticate",
]

def test_proxy():
    print("Cliente de Teste do MITMProxy")
    print("=" * 50)
    print(f"Proxy configurado: {PROXY_URL}")
    print("=" * 50)
    print()
    
    for i, url in enumerate(test_urls, 1):
        print(f"[{i}/{len(test_urls)}] Testando: {url}")
        
        try:
            response = requests.get(
                url, 
                proxies=proxies,
                timeout=10,
                verify=False
            )
            
            status = "[OK]" if response.status_code == 200 else "[AVISO]"
            print(f"  {status} Status: {response.status_code}")
            
            if "login" in url or "auth" in url or "signin" in url:
                print(f"  [TELEGRAM] Deve enviar notificacao ao Telegram!")
            else:
                print(f"  [SKIP] Nao deve enviar notificacao (sem palavra-chave)")
                
        except requests.exceptions.ProxyError:
            print(f"  [ERRO] Erro: Proxy nao esta rodando em {PROXY_URL}")
            print(f"  [DICA] Certifique-se de que o workflow MITMProxy esta ativo")
            break
        except Exception as e:
            print(f"  [ERRO] Erro: {e}")
        
        print()
        time.sleep(1)
    
    print("=" * 50)
    print("[OK] Teste concluido!")
    print("[TELEGRAM] Verifique seu Telegram para as notificacoes")
    print()

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_proxy()
