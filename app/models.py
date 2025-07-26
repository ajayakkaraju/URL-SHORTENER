
import threading
import time

class URLStore:
    def __init__(self):
        self.lock = threading.RLock()
        self.url_map = {}  # short_code -> {url, created_at, clicks}

    def add_url(self, short_code, url):
        with self.lock:
            self.url_map[short_code] = {
                'url': url,
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'clicks': 0
            }

    def get_url(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code]['clicks'] += 1
                return True
            return False

    def get_stats(self, short_code):
        with self.lock:
            entry = self.url_map.get(short_code)
            if entry:
                return {
                    'url': entry['url'],
                    'clicks': entry['clicks'],
                    'created_at': entry['created_at']
                }
            return None

store = URLStore()