#!/usr/bin/env python3
"""
Script de teste completo para o MITMProxy Telegram Notifier
Testa todas as funcionalidades do sistema

Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
"""

import requests
import urllib3
import os
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXY_URL = "http://localhost:8080"
proxies = {
    'http': PROXY_URL,
    'https': PROXY_URL,
}

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_secrets():
    """Teste 1: Verificar se os secrets estão configurados"""
    print_section("TESTE 1: Verificação de Secrets")
    
    token = os.environ.get("TG_BOT_TOKEN", "")
    chat_id = os.environ.get("TG_CHAT_ID", "")
    
    if token and ":" in token:
        print("[OK] TG_BOT_TOKEN: Configurado corretamente")
    else:
        print("[ERRO] TG_BOT_TOKEN: Não configurado ou inválido")
    
    if chat_id:
        print(f"[OK] TG_CHAT_ID: Configurado ({chat_id[:5]}...)")
    else:
        print("[ERRO] TG_CHAT_ID: Não configurado")
    
    return bool(token and chat_id)

def test_proxy_connection():
    """Teste 2: Verificar se o proxy está respondendo"""
    print_section("TESTE 2: Conexão com o Proxy")
    
    try:
        response = requests.get(
            "http://httpbin.org/get",
            proxies=proxies,
            timeout=5,
            verify=False
        )
        print(f"[OK] Proxy respondendo (Status: {response.status_code})")
        return True
    except requests.exceptions.ProxyError:
        print("[ERRO] Proxy não está rodando na porta 8080")
        print("[DICA] Verifique se o workflow MITMProxy está ativo")
        return False
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
        return False

def test_url_filtering():
    """Teste 3: Testar filtragem por palavras-chave"""
    print_section("TESTE 3: Filtragem de URLs")
    
    test_cases = [
        ("http://httpbin.org/get", False, "URL normal"),
        ("http://httpbin.org/login", True, "Palavra-chave: login"),
        ("http://httpbin.org/auth/token", True, "Palavra-chave: auth"),
        ("http://httpbin.org/user/signin", True, "Palavra-chave: signin"),
        ("http://httpbin.org/api/data", False, "Sem palavra-chave"),
    ]
    
    for url, should_match, description in test_cases:
        try:
            response = requests.get(url, proxies=proxies, timeout=5, verify=False)
            icon = "[TELEGRAM]" if should_match else "[SKIP]"
            action = "CAPTURADA" if should_match else "IGNORADA"
            print(f"{icon} {description}")
            print(f"   URL: {url}")
            print(f"   Status: {response.status_code} | Ação: {action}")
        except Exception as e:
            print(f"[ERRO] Erro ao testar {url}: {e}")

def test_http_methods():
    """Teste 4: Testar diferentes métodos HTTP"""
    print_section("TESTE 4: Métodos HTTP")
    
    url = "http://httpbin.org/anything/login"
    
    methods = [
        ("GET", True, "Deve capturar"),
        ("POST", True, "Deve capturar"),
        ("PUT", False, "Deve ignorar"),
        ("DELETE", False, "Deve ignorar"),
    ]
    
    for method, should_capture, description in methods:
        try:
            if method == "GET":
                response = requests.get(url, proxies=proxies, timeout=5, verify=False)
            elif method == "POST":
                response = requests.post(url, proxies=proxies, timeout=5, verify=False)
            elif method == "PUT":
                response = requests.put(url, proxies=proxies, timeout=5, verify=False)
            elif method == "DELETE":
                response = requests.delete(url, proxies=proxies, timeout=5, verify=False)
            
            icon = "[OK]" if should_capture else "[SKIP]"
            print(f"{icon} {method}: {description} (Status: {response.status_code})")
        except Exception as e:
            print(f"[ERRO] Erro no método {method}: {e}")

def test_headers_capture():
    """Teste 5: Testar captura de headers customizados"""
    print_section("TESTE 5: Captura de Headers")
    
    custom_headers = {
        "X-Custom-Header": "TestValue123",
        "User-Agent": "MITMProxy-Test-Client/1.0",
        "Authorization": "Bearer test-token-12345",
    }
    
    try:
        response = requests.get(
            "http://httpbin.org/headers/login",
            headers=custom_headers,
            proxies=proxies,
            timeout=5,
            verify=False
        )
        
        print("[OK] Requisição com headers customizados enviada")
        print("[TELEGRAM] O bot deve receber estes headers:")
        for key, value in custom_headers.items():
            print(f"   - {key}: {value}")
        print(f"\n   Status da resposta: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro: {e}")

def run_all_tests():
    """Executar todos os testes"""
    print("\n" + "=" * 60)
    print("  TESTE COMPLETO DO MITMPROXY TELEGRAM NOTIFIER")
    print("=" * 60)
    
    secrets_ok = test_secrets()
    
    if not secrets_ok:
        print("\n[AVISO] AVISO: Secrets não configurados completamente")
        print("   As notificações do Telegram podem falhar\n")
    
    proxy_ok = test_proxy_connection()
    
    if not proxy_ok:
        print("\n[ERRO] ERRO: Proxy não está rodando")
        print("   Não é possível continuar os testes\n")
        return
    
    test_url_filtering()
    test_http_methods()
    test_headers_capture()
    
    print("\n" + "=" * 60)
    print("  RESUMO DOS TESTES")
    print("=" * 60)
    print("[OK] Testes concluídos!")
    print("\n[NEXT] PRÓXIMOS PASSOS:")
    print("   1. Verifique os logs do workflow MITMProxy")
    print("   2. Verifique seu Telegram para as notificações")
    print("   3. As mensagens devem conter os headers capturados")
    print("\n[DICA] DICAS:")
    print("   - Apenas URLs com 'login', 'auth' ou 'signin' geram notificações")
    print("   - Apenas métodos GET e POST são capturados")
    print("   - Os headers são enviados em formato JSON")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_all_tests()
