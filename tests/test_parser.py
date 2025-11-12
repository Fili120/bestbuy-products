import json
from extractors.product_parser import parse_product_from_html

HTML = """
<html>
  <head>
    <title>Test Product</title>
    <meta name="description" content="Great device">
    <script type="application/ld+json">
    {
      "@context": "http://schema.org/",
      "@type": "Product",
      "name": "Acme Phone X",
      "sku": "1234567",
      "brand": {"@type": "Brand", "name": "Acme"},
      "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "321"},
      "offers": {
        "@type": "AggregateOffer",
        "priceCurrency": "USD",
        "lowPrice": "199.99",
        "highPrice": "299.99",
        "offers": [
          {"priceCurrency": "USD", "price": "299.99", "itemCondition": "NewCondition", "description": "New"},
          {"priceCurrency": "USD", "price": "219.99", "itemCondition": "UsedCondition", "description": "Open-Box Excellent"}
        ]
      }
    }
    </script>
  </head>
  <body>
    <img src="https://pisces.bbystatic.com/image2/BestBuy_US/images/products/1234/1234567_sd.jpg" />
    <div class="sku-title"><h1>Acme Phone X</h1></div>
  </body>
</html>
"""

def test_parse_product_from_html_basic():
    data = parse_product_from_html(HTML, url="https://www.bestbuy.com/site/acme-phone-x/1234567.p?skuId=1234567")
    assert data["name"] == "Acme Phone X"
    assert data["sku"] == "1234567"
    assert data["aggregateRating"]["ratingValue"] == "4.6"
    assert data["offers"]["lowPrice"] == "199.99"
    assert "image" in data or "images" in data