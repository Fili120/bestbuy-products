import logging
import random
import time
from typing import Dict, Optional

import requests

class HttpClient:
    def __init__(self, default_headers: Optional[Dict[str, str]] = None, proxies: Optional[Dict[str, str]] = None, timeout: int = 30):
        self.session = requests.Session()
        self.default_headers = default_headers or {}
        self.session.headers.update(self.default_headers)
        self.proxies = proxies
        self.timeout = timeout

    def get(self, url: str, headers: Optional[Dict[str, str]] = None, retries: int = 3, backoff: float = 0.8) -> requests.Response:
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                h = self.default_headers.copy()
                if headers:
                    h.update(headers)
                resp = self.session.get(url, headers=h, proxies=self.proxies, timeout=self.timeout, allow_redirects=True)
                if resp.status_code >= 500:
                    raise requests.HTTPError(f"Server error {resp.status_code}")
                if resp.status_code in (403, 429):
                    # Backoff for anti-bot triggers
                    logging.warning("Received %s for %s. Backing off.", resp.status_code, url)
                    time.sleep(backoff * attempt + random.uniform(0, 0.5))
                else:
                    return resp
            except Exception as e:
                last_exc = e
                logging.warning("GET attempt %d failed for %s: %s", attempt, url, e)
                time.sleep(backoff * attempt + random.uniform(0, 0.5))
        # Final try: return last response if available, else raise
        if isinstance(last_exc, requests.HTTPError):
            raise last_exc
        raise RuntimeError(f"Failed to fetch {url}: {last_exc}")