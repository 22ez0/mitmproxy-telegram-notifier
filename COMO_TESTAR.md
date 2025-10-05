# Como Testar Todas as Funcionalidades

## Métodos de Teste Disponíveis

### 1. Teste Automático Completo (Recomendado)

```bash
python test_completo.py
```

Este script testa automaticamente:
- Configuração de secrets
- Conexão com o proxy
- Filtragem por palavras-chave
- Diferentes métodos HTTP (GET, POST, PUT, DELETE)
- Captura de headers customizados

---

### 2. Teste Simples com Cliente Python

```bash
python test_client.py
```

Envia requisições de teste através do proxy.

---

### 3. Teste Manual com cURL

#### Testar requisição que SERÁ capturada:

```bash
# GET com palavra-chave "login"
curl -x http://localhost:8080 http://httpbin.org/login

# POST com palavra-chave "auth"
curl -x http://localhost:8080 -X POST http://httpbin.org/auth/token

# Com headers customizados
curl -x http://localhost:8080 \
  -H "Authorization: Bearer test-123" \
  -H "X-Custom: MyValue" \
  http://httpbin.org/signin
```

#### Testar requisição que será IGNORADA:

```bash
# Sem palavra-chave
curl -x http://localhost:8080 http://httpbin.org/api/data

# Método não monitorado (PUT)
curl -x http://localhost:8080 -X PUT http://httpbin.org/login
```

---

### 4. Teste com Navegador

1. **Configure o proxy no navegador:**
   - Host: `localhost`
   - Porta: `8080`

2. **Acesse URLs de teste:**
   - `http://httpbin.org/get` (não captura)
   - `http://httpbin.org/login` (captura!)
   - `http://example.com/auth` (captura!)
   - `http://site.com/signin` (captura!)

---

## Verificar Resultados

### Opção 1: Logs do MITMProxy

Veja o console do workflow "MITMProxy" no Replit. Procure por:

```
[HeaderCapture] matched flow <id> -> notifying bot
```

### Opção 2: Telegram

Verifique as mensagens no chat do bot. Você deve receber:
- JSON com headers capturados
- Flow ID
- Método HTTP
- URL completa

---

## Critérios de Captura

### URLs que SERÃO capturadas:

- Contém `login` no caminho
- Contém `auth` no caminho  
- Contém `signin` no caminho
- Métodos: **GET** ou **POST** apenas

### URLs que serão IGNORADAS:

- Sem palavras-chave
- Métodos: PUT, DELETE, PATCH, etc.

---

## Solução de Problemas

### Erro: "chat not found"

1. **Obtenha o Chat ID correto:**
   - Abra o Telegram
   - Converse com [@userinfobot](https://t.me/userinfobot)
   - Copie o número do Chat ID

2. **Inicie conversa com o bot:**
   - Procure seu bot no Telegram (nome que você deu ao criar)
   - Envie `/start`
   - Aguarde resposta

3. **Atualize o secret:**
   - No Replit, vá em "Secrets"
   - Edite `TG_CHAT_ID` com o ID correto
   - Reinicie o workflow

### Proxy não responde

1. Verifique se o workflow "MITMProxy" está rodando
2. Confirme a porta 8080 está disponível
3. Reinicie o workflow se necessário

---

## Checklist de Testes

- [ ] Secrets configurados (TG_BOT_TOKEN, TG_CHAT_ID)
- [ ] Workflow MITMProxy rodando
- [ ] Teste com URL contendo "login" → deve capturar
- [ ] Teste com URL contendo "auth" → deve capturar
- [ ] Teste com URL contendo "signin" → deve capturar
- [ ] Teste com URL normal → não deve capturar
- [ ] Teste com método GET → deve capturar
- [ ] Teste com método POST → deve capturar
- [ ] Teste com método PUT → não deve capturar
- [ ] Notificação recebida no Telegram
- [ ] Headers corretos na notificação

---

## Exemplo de Notificação Esperada

```json
{
  "flow_id": "abc123...",
  "method": "GET",
  "url": "http://example.com/login",
  "headers": {
    "Host": "example.com",
    "User-Agent": "Mozilla/5.0...",
    "Accept": "*/*",
    ...
  },
  "note": "capturado apenas headers; body omitido por segurança"
}
```
