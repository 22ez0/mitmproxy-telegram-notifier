import threading
import time
import uuid
import json
import os
from typing import Dict, Optional
from filelock import FileLock

STORAGE_FILE = "/tmp/url_storage.json"
LOCK_FILE = "/tmp/url_storage.lock"

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
        return url_id
    
    def get(self, url_id: str) -> Optional[str]:
        with self.lock:
            storage = self._load_storage()
            if url_id in storage:
                data = storage[url_id]
                if time.time() - data['timestamp'] < self.ttl_seconds:
                    return data['url']
                else:
                    del storage[url_id]
                    self._save_storage(storage)
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
