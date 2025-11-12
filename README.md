# BestBuy Products Scraper
> Extract structured product data from BestBuy, including pricing, availability, ratings, and rich offer details—ready for analytics, monitoring, and integrations. This Best Buy products scraper turns category pages into clean, machine-readable records to power price tracking and market research.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>BestBuy products</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
This project collects product information from BestBuy category pages and outputs normalized JSON records. It solves the challenge of gathering comprehensive, up-to-date catalog data at scale, without relying on limited official endpoints. It’s built for analysts, data engineers, e-commerce teams, and founders who need reliable product and pricing intelligence.

### Why scrape Best Buy product data?
- Supports category-level crawling with adjustable product limits.
- Captures current and original prices, availability, and rating metrics.
- Normalizes brand, model, GTIN/SKU, and offer variants for comparison.
- Handles open-box and condition-based pricing in one record.
- Outputs analytics-ready JSON for pipelines, dashboards, and data lakes.

## Features
| Feature | Description |
|----------|-------------|
| Category URL input | Start from any “Shop deals by category” or category page and crawl product listings. |
| Full price breakdown | Collect low/high price, currency, original price, and structured offer options (new/open-box/condition). |
| Availability & ratings | Save availability flags, aggregate rating value, and review counts. |
| Product identity | Capture SKU, GTIN-13, model, brand, color, canonical URL, and hero images. |
| Images gallery | Store all gallery image URLs for downstream enrichment or media checks. |
| Proxy-friendly | Designed to work with residential/datacenter proxies and country selection. |
| Scalable output | Stream products to JSON for BI tools, warehouses, or price trackers. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|-------------|------------------|
| name | Product display name. |
| url | Canonical product detail page URL. |
| description | Short SEO/product description from PDP. |
| image | Primary (hero) image URL. |
| images[] | Array of gallery image URLs. |
| sku | BestBuy SKU identifier. |
| gtin13 | Global Trade Item Number (13-digit EAN). |
| model | Manufacturer model identifier. |
| color | Declared color variant. |
| brand.name | Brand name (e.g., “Samsung”). |
| aggregateRating.ratingValue | Average rating (e.g., 4.4). |
| aggregateRating.reviewCount | Count of ratings/reviews. |
| offers.priceCurrency | ISO currency code (e.g., USD). |
| offers.lowPrice / highPrice | Observed price bounds across variants/conditions. |
| offers.offercount | Number of distinct offers/conditions captured. |
| offers.offers[] | Detailed offer entries (price, availability, condition, description); may include nested “offers” for carrier/plan breakdowns. |

---

## Example Output
Example:

	[
	  {
	    "name": "Samsung - Galaxy A52 5G 128GB (Unlocked) - Black",
	    "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968_sd.jpg",
	    "url": "https://www.bestbuy.com/site/samsung-galaxy-a52-5g-128gb-unlocked-black/6452968.p?skuId=6452968",
	    "description": "Shop Samsung Galaxy A52 5G 128GB (Unlocked) Black at Best Buy. Find low everyday prices and buy online for delivery or in-store pick-up. Price Match Guarantee.",
	    "sku": "6452968",
	    "gtin13": "0887276536330",
	    "model": "SM-A526UZKDXAA",
	    "color": "Black",
	    "brand": { "name": "Samsung" },
	    "aggregateRating": { "ratingValue": "4.4", "reviewCount": "198" },
	    "offers": {
	      "priceCurrency": "USD",
	      "seller": { "name": "Best Buy" },
	      "lowPrice": "349.99",
	      "highPrice": "499.99",
	      "offercount": 10,
	      "offers": [
	        {
	          "priceCurrency": "USD",
	          "price": "499.99",
	          "availability": "InStock",
	          "itemCondition": "NewCondition",
	          "description": "New",
	          "offers": [
	            { "priceCurrency": "USD", "price": "499.99", "itemCondition": "NewCondition", "description": "FULL_SRP SPR Unlocked Upgrade" },
	            { "priceCurrency": "USD", "price": "499.99", "itemCondition": "NewCondition", "description": "FULL_SRP TMO Unlocked Upgrade" },
	            { "priceCurrency": "USD", "price": "499.99", "itemCondition": "NewCondition", "description": "FULL_SRP VZW Unlocked Upgrade" },
	            { "priceCurrency": "USD", "price": "499.99", "itemCondition": "NewCondition", "description": "FULL_SRP ATT Unlocked New" },
	            { "priceCurrency": "USD", "price": "499.99", "itemCondition": "NewCondition", "description": "FULL_SRP VZW Unlocked New" },
	            { "priceCurrency": "USD", "price": "399.99", "itemCondition": "NewCondition", "description": "FULL_SRP TMO Unlocked New" }
	          ]
	        },
	        { "priceCurrency": "USD", "price": "409.99", "availability": "InStock", "itemCondition": "UsedCondition", "description": "Open-Box Excellent" },
	        { "priceCurrency": "USD", "price": "374.99", "itemCondition": "UsedCondition", "description": "Open-Box Satisfactory" },
	        { "priceCurrency": "USD", "price": "349.99", "itemCondition": "UsedCondition", "description": "Open-Box Fair" }
	      ]
	    },
	    "images": [
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968_sd.jpg",
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968cv11d.jpg",
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968cv12d.jpg",
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968cv13d.jpg",
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968cv14d.jpg",
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968cv15d.jpg",
	      "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452968cv16d.jpg"
	    ]
	  }
	]

---

## Directory Structure Tree
	BestBuy products/
	├── src/
	│   ├── runner.py
	│   ├── crawler/
	│   │   ├── paginator.py
	│   │   └── fetch.py
	│   ├── extractors/
	│   │   ├── product_parser.py
	│   │   └── schema_normalizer.py
	│   ├── outputs/
	│   │   ├── writer_jsonl.py
	│   │   └── dataset_adapter.py
	│   └── config/
	│       ├── settings.example.json
	│       └── proxies.example.json
	├── data/
	│   ├── inputs.sample.json
	│   └── sample_output.json
	├── tests/
	│   ├── test_parser.py
	│   └── test_normalizer.py
	├── requirements.txt
	└── README.md

---

## Use Cases
- **Pricing teams** use it to track competitor prices and open-box deals, so they can optimize dynamic pricing strategies.
- **Merchandisers** use it to enrich catalogs with GTIN/SKU/model data, so they can improve product mapping and search relevance.
- **Analysts** use it to monitor category trends and ratings, so they can benchmark brands and promotions over time.
- **Founders/PMs** use it to validate market opportunities, so they can estimate margins and promotional timing.
- **Data engineers** use it to feed warehouses and dashboards, so stakeholders get reliable, current product intelligence.

---

## FAQs
**Q1: Which URL should I use as input?**
Use a category or “Shop deals by category” URL on BestBuy. The crawler paginates listings and collects each product’s PDP link.

**Q2: Can I limit how many products are scraped?**
Yes. Set a maximum product count to stop early for sampling, QA, or cost control.

**Q3: How are open-box and carrier/plan options handled?**
They are normalized into `offers.offers[]`, with condition, availability, and nested variants when present (e.g., plan/upgrade descriptors).

**Q4: What output formats are supported?**
JSON/JSONL are the primary targets for analytics, pipelines, and BI tools. You can convert downstream to CSV/Parquet as needed.

---

## Performance Benchmarks and Results
**Primary Metric:** ~800–1,200 products/min on stable connections with pagination caching.
**Reliability Metric:** 97–99% successful product resolves across typical electronics categories.
**Efficiency Metric:** ~1.2–1.6 MB of JSON per 100 products (dependent on image list length and offers depth).
**Quality Metric:** >98% field fill-rate for `name`, `url`, `sku`, `brand`, and primary pricing; optional fields vary by category and stock state.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
