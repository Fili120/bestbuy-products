import json
import re
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup

def _parse_ld_json(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """Extract the most relevant product JSON-LD block."""
    candidates = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.text.strip())
        except Exception:
            continue
        # Sometimes wrapped in a list
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") in ("Product", "AggregateOffer"):
                    candidates.append(item)
        elif isinstance(data, dict) and data.get("@type") in ("Product", "AggregateOffer"):
            candidates.append(data)
        elif isinstance(data, dict) and data.get("@graph"):
            for item in data.get("@graph", []):
                if isinstance(item, dict) and item.get("@type") == "Product":
                    candidates.append(item)

    # Prefer Product type
    for c in candidates:
        if c.get("@type") == "Product":
            return c
    return candidates[0] if candidates else None

def _text(soup: BeautifulSoup, selector: str) -> Optional[str]:
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else None

def parse_product_from_html(html: str, url: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse raw product details from a BestBuy PDP HTML.
    Attempts JSON-LD first; falls back to DOM extraction heuristics.
    """
    soup = BeautifulSoup(html, "lxml")
    data: Dict[str, Any] = {"url": url} if url else {}

    ld = _parse_ld_json(soup)
    if ld:
        data.update(ld)

    # Fallback / enrichments
    name = data.get("name") or _text(soup, "h1, h1.sku-title, div.sku-title h1")
    if name:
        data["name"] = name

    # Extract SKU from URL or page
    if "sku" not in data or not data.get("sku"):
        # URL pattern ... .p?skuId=6452968
        if url:
            m = re.search(r"skuId=(\d+)", url)
            if m:
                data["sku"] = m.group(1)
        if "sku" not in data:
            # try DOM
            sku_dom = _text(soup, '[data-sku-id], .sku.product-data, .sku-value')
            if sku_dom:
                m = re.search(r"(\d{6,})", sku_dom)
                if m:
                    data["sku"] = m.group(1)

    # Primary image
    if not data.get("image"):
        img = soup.select_one('img.primary-image, img#main-image, img[src*="bbystatic.com"]')
        if img and img.get("src"):
            data["image"] = img["src"]

    # Gallery images
    images = set()
    for img in soup.select("img[src]"):
        src = img["src"]
        if "bbystatic.com" in src:
            images.add(src)
    if images:
        existing = data.get("image")
        if existing:
            images.add(existing)
        data["images"] = list(images)

    # Ratings
    if not data.get("aggregateRating"):
        rating_value = _text(soup, '[itemprop="ratingValue"], .c-reviews-v4 .average-rating')
        review_count = _text(soup, '[itemprop="reviewCount"], .c-reviews-v4 .count')
        if rating_value or review_count:
            data["aggregateRating"] = {
                "ratingValue": rating_value,
                "reviewCount": review_count,
            }

    # Offers (fallback if LD missing)
    if not data.get("offers"):
        price_text = _text(soup, ".priceView-hero-price span, .priceView-customer-price span, [itemprop='price']")
        orig_text = _text(soup, ".pricing-price__regular-price, .priceView-hero-price__regular-price")
        offers = {
            "priceCurrency": "USD",
            "seller": {"name": "Best Buy"},
        }
        if price_text:
            # keep numeric with dot
            m = re.search(r"([0-9]+\.[0-9]{2})", price_text.replace(",", ""))
            if m:
                offers["lowPrice"] = m.group(1)
                offers["highPrice"] = m.group(1)
        if orig_text:
            m = re.search(r"([0-9]+\.[0-9]{2})", orig_text.replace(",", ""))
            if m:
                offers.setdefault("offers", [])
                offers["offers"].append(
                    {"priceCurrency": "USD", "price": m.group(1), "itemCondition": "NewCondition", "description": "Original"}
                )
        if offers.keys() - {"priceCurrency", "seller"}:
            data["offers"] = offers

    # Description
    if not data.get("description"):
        desc = _text(soup, "meta[name='description']") or _text(soup, "div.shop-product-description")
        if not desc and (meta := soup.find("meta", {"name": "description"})):
            desc = meta.get("content")
        if desc:
            data["description"] = desc

    return data