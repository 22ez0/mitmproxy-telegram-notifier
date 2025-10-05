import threading
import time
import uuid
import json
import os
from typing import Dict, Optional
from filelock import FileLock

STORAGE_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(STORAGE_DIR, exist_ok=True)

STORAGE_FILE = os.path.join(STORAGE_DIR, "url_storage.json")
LOCK_FILE = os.path.join(STORAGE_DIR, "url_storage.lock")

class URLStorage:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl_seconds = ttl_seconds
        self.lock = FileLock(LOCK_FILE)
        if not os.path.exists(STORAGE_FILE):
            self._save_storage({})
    
    def _load_storage(self) -> Dict:
        try:
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_storage(self, data: Dict):
        with open(STORAGE_FILE, 'w') as f:
            json.dump(data, f)
    
    def generate_id(self) -> str:
        return uuid.uuid4().hex[:8]
    
    def store(self, url: str) -> str:
        url_id = self.generate_id()
        with self.lock:
            storage = self._load_storage()
            storage[url_id] = {
                'url': url,
                'timestamp': time.time()
            }
            self._save_storage(storage)
        print(f"[Storage] Armazenado: {url_id} -> {url}")
        print(f"[Storage] Arquivo: {STORAGE_FILE}")
        return url_id
    
    def get(self, url_id: str) -> Optional[str]:
        with self.lock:
            storage = self._load_storage()
            print(f"[Storage] Buscando ID: {url_id}")
            print(f"[Storage] IDs disponíveis: {list(storage.keys())}")
            print(f"[Storage] Arquivo: {STORAGE_FILE}")
            if url_id in storage:
                data = storage[url_id]
                if time.time() - data['timestamp'] < self.ttl_seconds:
                    print(f"[Storage] Encontrado: {data['url']}")
                    return data['url']
                else:
                    print(f"[Storage] Expirado!")
                    del storage[url_id]
                    self._save_storage(storage)
            else:
                print(f"[Storage] ID não encontrado!")
        return None
    
    def cleanup_expired(self):
        now = time.time()
        with self.lock:
            storage = self._load_storage()
            expired = [
                uid for uid, data in storage.items()
                if now - data['timestamp'] >= self.ttl_seconds
            ]
            for uid in expired:
                del storage[uid]
            if expired:
                self._save_storage(storage)

storage = URLStorage()
