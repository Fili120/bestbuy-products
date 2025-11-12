from extractors.schema_normalizer import normalize_product

def test_normalize_product_shapes_fields():
    raw = {
        "name": "Acme Phone X",
        "url": "https://www.bestbuy.com/site/acme-phone-x/1234567.p?skuId=1234567",
        "description": "Great device",
        "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/1234/1234567_sd.jpg",
        "sku": "1234567",
        "brand": {"name": "Acme"},
        "aggregateRating": {"ratingValue": "4.6", "reviewCount": "321"},
        "offers": {
            "priceCurrency": "USD",
            "lowPrice": "199.99",
            "highPrice": "299.99",
            "offers": [
                {"priceCurrency": "USD", "price": "299.99", "itemCondition": "NewCondition", "description": "New"},
                {"priceCurrency": "USD", "price": "219.99", "itemCondition": "UsedCondition", "description": "Open-Box Excellent"}
            ]
        },
        "images": ["a.jpg", "b.jpg"]
    }
    doc = normalize_product(raw)
    assert doc["name"] == "Acme Phone X"
    assert doc["sku"] == "1234567"
    assert doc["brand"]["name"] == "Acme"
    assert doc["offers"]["offercount"] == 2
    assert doc["offers"]["lowPrice"] == "219.99"
    assert "images" in doc and len(doc["images"]) == 2