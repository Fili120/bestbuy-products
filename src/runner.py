import argparse
import json
import logging
import os
import sys
import time
from typing import Dict, Iterable, Optional

from crawler.fetch import HttpClient
from crawler.paginator import BestBuyPaginator
from extractors.product_parser import parse_product_from_html
from extractors.schema_normalizer import normalize_product
from outputs.writer_jsonl import JsonlWriter
from outputs.dataset_adapter import ensure_parent_dir

LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"

def load_settings(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_proxies(path: Optional[str]) -> Optional[Dict[str, str]]:
    if not path:
        return None
    if not os.path.exists(path):
        logging.warning("Proxies file '%s' not found. Continuing without proxies.", path)
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # requests expects {"http": "...", "https": "..."}
    if isinstance(data, dict):
        return data
    if isinstance(data, list) and data:
        # pick first proxy as default
        proxy = data[0]
        return {"http": proxy, "https": proxy}
    return None

def iter_product_urls(paginator: BestBuyPaginator, max_products: int) -> Iterable[str]:
    count = 0
    for url in paginator.iter_product_urls():
        yield url
        count += 1
        if max_products and count >= max_products:
            break

def main():
    parser = argparse.ArgumentParser(
        description="BestBuy category scraper → normalized JSONL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--settings",
        "-s",
        required=True,
        help="Path to settings JSON (see src/config/settings.example.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output JSONL path (overrides settings.outputPath if provided)",
    )
    parser.add_argument("--max", type=int, default=None, help="Max products to scrape")
    parser.add_argument("--delay", type=float, default=None, help="Delay between requests (seconds)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logs")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format=LOG_FORMAT)

    settings = load_settings(args.settings)
    category_url = settings.get("categoryUrl")
    if not category_url:
        logging.error("categoryUrl missing in settings.")
        sys.exit(2)

    output_path = args.output or settings.get("outputPath", "data/out/bestbuy_products.jsonl")