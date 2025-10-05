# Deploy no Render - MITMProxy Telegram Notifier

## Passo a Passo

### 1. Criar conta no Render
- Acesse: https://render.com
- Crie conta gratuita (pode usar GitHub)

### 2. Fazer Deploy
1. No dashboard do Render, clique em "New +" → "Web Service"
2. Conecte este repositório Git
3. Configure:
   - **Name**: mitmproxy-interceptor
   - **Runtime**: Docker
   - **Plan**: Free
   
### 3. Configurar Variáveis de Ambiente
No painel do Render, vá em "Environment" e adicione:

- `TG_BOT_TOKEN` = seu token do bot (do @BotFather)
- `TG_CHAT_ID` = seu chat ID (do @userinfobot)

### 4. Deploy Automático
- Render vai fazer build e deploy automaticamente
- Aguarde ~5 minutos
- URL será: https://mitmproxy-interceptor.onrender.com

### 5. Atualizar Bot com Nova URL
Após deploy, edite `bot.py`:
```python
REPLIT_DOMAIN = "mitmproxy-interceptor.onrender.com"
```

### 6. Evitar Sleep (Importante!)

O app gratuito dorme após 15 min de inatividade. Configure um ping automático:

**Opção A: UptimeRobot (Recomendado)**
1. Acesse: https://uptimerobot.com (grátis)
2. Crie monitor:
   - Type: HTTP(s)
   - URL: https://mitmproxy-interceptor.onrender.com/ping
   - Interval: 5 minutos

**Opção B: cron-job.org**
1. Acesse: https://cron-job.org
2. Crie job:
   - URL: https://mitmproxy-interceptor.onrender.com/ping
   - Intervalo: */14 minutos (a cada 14 min)

## Como Usar

1. Envie `/intercept https://exemplo.com/login` para o bot
2. Clique no link gerado pelo Telegram
3. Headers serão capturados e enviados em formato Python

## Custos

- **100% Gratuito** no plano Free do Render
- Limitações: app dorme após inatividade (resolvido com ping)

## Troubleshooting

**App não responde?**
- Espere 30-60s (cold start após sleep)
- Verifique se o ping automático está configurado

**Links não funcionam?**
- Confirme que as variáveis TG_BOT_TOKEN e TG_CHAT_ID estão configuradas
- Verifique se o domínio no bot.py está correto

Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
