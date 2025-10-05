# MITMProxy Telegram Notifier

Addon para mitmproxy que captura headers HTTP de requisições específicas e envia notificações via Telegram.

## Descrição

Este projeto monitora o tráfego HTTP(S) através do mitmproxy e envia notificações automáticas via Telegram quando detecta requisições que correspondem a padrões configuráveis (por padrão: "login", "/auth", "/signin").

### Características

- Monitora requisições GET e POST
- Filtra por palavras-chave configuráveis na URL
- Captura apenas headers (sem corpo da requisição por segurança)
- Envio assíncrono para Telegram via bot
- Suporte para mensagens grandes (chunking automático)
- Tratamento de erros robusto

## Instalação

### Pré-requisitos

- Python 3.11 ou superior
- Token de bot do Telegram (obtenha via [@BotFather](https://t.me/BotFather))
- Chat ID do Telegram (obtenha via [@userinfobot](https://t.me/userinfobot))

### Configuração

1. Configure as variáveis de ambiente:

```bash
export TG_BOT_TOKEN="seu_token_aqui"
export TG_CHAT_ID="seu_chat_id_aqui"
```

Ou crie um arquivo `.env` (não commitado):

```
TG_BOT_TOKEN=seu_token_aqui
TG_CHAT_ID=seu_chat_id_aqui
```

## Uso

### Executar o mitmproxy com o addon:

```bash
mitmproxy -s header_capture.py
```

Ou use mitmdump para modo não-interativo:

```bash
mitmdump -s header_capture.py
```

### Configurar o cliente

Configure seu navegador ou aplicação para usar o proxy:

- Host: `localhost`
- Porta: `8080` (padrão do mitmproxy)

### Instalar certificado HTTPS

Para interceptar tráfego HTTPS, instale o certificado do mitmproxy:

1. Inicie o mitmproxy
2. Acesse [http://mitm.it](http://mitm.it) através do proxy
3. Baixe e instale o certificado para seu sistema operacional

## Personalização

### Modificar palavras-chave de filtro

Edite a variável `MATCH_KEYWORDS` em `header_capture.py`:

```python
MATCH_KEYWORDS = ["login", "/auth", "/signin", "sua_palavra_chave"]
```

### Ajustar tamanho de chunk para mensagens

Edite a variável `CHUNK_SIZE` em `header_capture.py`:

```python
CHUNK_SIZE = 3800  # caracteres por mensagem
```

## Segurança

**IMPORTANTE**: 

- Use apenas em redes e serviços com autorização explícita
- O addon captura apenas headers, não corpos de requisição
- Nunca commit tokens ou credenciais no código
- Mantenha suas variáveis de ambiente seguras

## Estrutura do Projeto

```
.
├── header_capture.py    # Addon principal do mitmproxy
├── pyproject.toml       # Configuração do projeto Python
├── README.md           # Este arquivo
└── .gitignore          # Arquivos ignorados pelo git
```

## Desenvolvimento

### Dependências

- `mitmproxy` - Proxy HTTP(S) interativo
- `pyTelegramBotAPI` - Interface para Telegram Bot API

### Logs

O addon gera logs informativos sobre as requisições capturadas:

```
[HeaderCapture] matched flow <id> -> notifying bot
```

## Licença

Este projeto é fornecido como está, sem garantias. Use por sua conta e risco.
