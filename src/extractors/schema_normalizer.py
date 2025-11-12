from typing import Any, Dict, List, Optional

def _as_float(val) -> Optional[float]:
    try:
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            return float(val.replace(",", "").strip())
    except Exception:
        return None
    return None

def _norm_brand(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        name = obj.get("name") or obj.get("brand")
        return {"name": name} if name else {}
    if isinstance(obj, str):
        return {"name": obj}
    return {}

def _norm_aggregate_rating(obj: Any) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        return {}
    rating = obj.get("ratingValue") or obj.get("ratingvalue") or obj.get("rating")
    count = obj.get("reviewCount") or obj.get("ratingCount") or obj.get("reviewcount")
    return {"ratingValue": str(rating) if rating is not None else None, "reviewCount": str(count) if count is not None else None}

def _norm_offers(obj: Any) -> Dict[str, Any]:
    """
    Normalize offers to:
    {
      priceCurrency,
      seller: { name },
      lowPrice, highPrice, offercount,
      offers: [ { priceCurrency, price, availability, itemCondition, description, offers?: [] } ]
    }
    """
    if not obj:
        return {}
    result: Dict[str, Any] = {"priceCurrency": "USD", "seller": {"name": "Best Buy"}}
    if isinstance(obj, dict):
        result["priceCurrency"] = obj.get("priceCurrency") or obj.get("pricecurrency") or result["priceCurrency"]
        seller = obj.get("seller")
        if seller:
            if isinstance(seller, dict):
                result["seller"] = {"name": seller.get("name")}
            elif isinstance(seller, str):
                result["seller"] = {"name": seller}
        low = _as_float(obj.get("lowPrice") or obj.get("lowprice") or obj.get("price"))
        high = _as_float(obj.get("highPrice") or obj.get("highprice") or obj.get("price"))
        if low is not None:
            result["lowPrice"] = f"{low:.2f}"
        if high is not None:
            result["highPrice"] = f"{high:.2f}"
        items: List[Dict[str, Any]] = []
        raw_items = obj.get("offers") or obj.get("items") or []
        if isinstance(raw_items, dict):
            raw_items = [raw_items]
        for it in raw_items:
            if not isinstance(it, dict):
                continue
            item = {
                "priceCurrency": it.get("priceCurrency") or result["priceCurrency"],
                "price": f"{_as_float(it.get('price')):.2f}" if _as_float(it.get("price")) is not None else None,
                "availability": it.get("availability") or it.get("availabilityStatus"),
                "itemCondition": it.get("itemCondition"),
                "description": it.get("description") or it.get("name"),
            }
            nested = it.get("offers")
            if nested and isinstance(nested, list):
                # Nested carrier/plan breakdowns
                item["offers"] = []
                for n in nested:
                    if not isinstance(n, dict):
                        continue
                    item["offers"].append(
                        {
                            "priceCurrency": n.get("priceCurrency") or result["priceCurrency"],
                            "price": f"{_as_float(n.get('price')):.2f}" if _as_float(n.get("price")) is not None else None,
                            "itemCondition": n.get("itemCondition"),
                            "description": n.get("description") or n.get("name"),
                        }
                    )
            items.append(item)
        if items:
            result["offers"] = items
            result["offercount"] = len(items)
            # tighten bounds if possible
            prices = [_as_float(i.get("price")) for i in items if _as_float(i.get("price")) is not None]
            if prices:
                result["lowPrice"] = f"{min(prices):.2f}"
                result["highPrice"] = f"{max(prices):.2f}"
        return result
    # If it's a list, treat as multiple offers
    if isinstance(obj, list):
        collated = {"priceCurrency": "USD", "seller": {"name": "Best Buy"}, "offers": []}
        prices = []
        for it in obj:
            if isinstance(it, dict):
                price = _as_float(it.get("price"))
                if price is not None:
                    prices.append(price)
                collated["offers"].append(
                    {
                        "priceCurrency": it.get("priceCurrency") or "USD",
                        "price": f"{price:.2f}" if price is not None else None,
                        "availability": it.get("availability"),
                        "itemCondition": it.get("itemCondition"),
                        "description": it.get("description") or it.get("name"),
                    }
                )
        if prices:
            collated["lowPrice"] = f"{min(prices):.2f}"
            collated["highPrice"] = f"{max(prices):.2f}"
            collated["offercount"] = len(prices)
        return collated
    return {}

def normalize_product(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map a raw product dict (from parser) into the target schema.
    """
    if not isinstance(raw, dict):
        return {}

    brand = _norm_brand(raw.get("brand"))
    aggregate = _norm_aggregate_rating(raw.get("aggregateRating"))
    offers = _norm_offers(raw.get("offers"))

    # Prefer explicit fields if present; else try common alternatives.
    name = raw.get("name")
    url = raw.get("url")
    description = raw.get("description")
    image = raw.get("image")
    images = raw.get("images") if isinstance(raw.get("images"), list) else None
    sku = raw.get("sku") or raw.get("skuId")
    gtin13 = raw.get("gtin13") or raw.get("gtin") or raw.get("gtin_13")
    model = raw.get("model") or raw.get("modelNumber")
    color = raw.get("color")

    # Final normalized document
    doc: Dict[str, Any] = {
        "name": name,
        "image": image,
        "url": url,
        "description": description,
        "sku": str(sku) if sku is not None else None,
        "gtin13": str(gtin13) if gtin13 is not None else None,
        "model": str(model) if model is not None else None,
        "color": color,
        "brand": brand if brand else None,
        "aggregateRating": aggregate if aggregate else None,
        "offers": offers if offers else None,
        "images": images or ([image] if image else None),
    }

    # Remove empty keys to keep output clean
    return {k: v for k, v in doc.items() if v not in (None, "", [], {})}