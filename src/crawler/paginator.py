import logging
import re
from typing import Generator, Iterable, List, Optional
from urllib.parse import urljoin, urlencode, urlparse, ParseResult, parse_qs, urlunparse

from bs4 import BeautifulSoup

from .fetch import HttpClient

BESTBUY_DOMAIN = "www.bestbuy.com"

def _with_query(url: str, params: dict) -> str:
    pr: ParseResult = urlparse(url)
    q = parse_qs(pr.query)
    for k, v in params.items():
        q[str(k)] = [str(v)]
    new_query = urlencode({k: v[0] if isinstance(v, list) else v for k, v in q.items()})
    return urlunparse(pr._replace(query=new_query))

class BestBuyPaginator:
    """
    Iterate product detail URLs from a BestBuy category/listing page.

    It detects product card anchors and follows page= N query parameter.
    """

    def __init__(self, client: HttpClient, category_url: str, country: str = "US"):
        self.client = client
        self.category_url = category_url
        self.country = country

    def _extract_product_urls(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "lxml")
        urls: List[str] = []

        # Typical card selector for BestBuy listings: a[data-sku-id], or anchors with class "sku-header"
        for a in soup.select('a.sku-header, a[data-sku-id], div.sku-title a, a[href*=".p?skuId="]'):
            href = a.get("href")
            if not href:
                continue
            # Normalize to absolute URL
            abs_url = urljoin(base_url, href)
            # Heuristic: PDP links contain "/site/" and end with ".p?skuId=<digits>"
            if re.search(r"/site/.*\.p\?skuId=\d+", abs_url):
                urls.append(abs_url)

        # Fallback: detect LD+JSON listing items if present
        if not urls:
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    import json
                    data = json.loads(script.text.strip())
                    if isinstance(data, dict) and data.get("@type") in ("ItemList", "CollectionPage"):
                        for item in data.get("itemListElement", []):
                            url = (item.get("url") if isinstance(item, dict) else item.get("item", {}).get("url"))
                            if url:
                                urls.append(urljoin(base_url, url))
                except Exception:
                    continue

        # De-duplicate while preserving order
        seen = set()
        deduped = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                deduped.append(u)
        return deduped

    def _next_page_url(self, url: str, page: int) -> Optional[str]:
        if "page=" in url:
            return _with_query(url, {"page": page})
        # If no 'page' query parameter, add it
        return _with_query(url, {"page": page})

    def iter_product_urls(self) -> Generator[str, None, None]:
        page = 1
        while True:
            page_url = self._next_page_url(self.category_url, page)
            logging.debug("Fetching list page %d: %s", page, page_url)
            resp = self.client.get(page_url)
            html = resp.text

            urls = self._extract_product_urls(html, base_url=page_url)
            if not urls:
                if page > 1:
                    logging.info("No more product URLs at page %d. Stopping.", page)
                else:
                    logging.warning("No products found on the first page. Check category URL.")
                break

            for u in urls:
                yield u

            # Stop if there is no obvious pagination control
            soup = BeautifulSoup(html, "lxml")
            pager = soup.select_one('nav.pagination, div.pagination, a[aria-label="Next Page"]')
            if not pager:
                # Heuristic: Stop after first page if pager missing
                break

            page += 1