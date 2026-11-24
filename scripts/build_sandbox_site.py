"""Build the static sandbox shop for Lab 3.4.

Writes plain HTML + CSS into ./sandbox_site/ (served by nginx in the `scrape` profile):
  index.html            landing page
  page-1.html..page-5   listing pages, 12 products each (60 total), with prev/next links
  product/<slug>.html   one detail page per product (the target of each product link)
  new-in.html, sale.html  collection pages linked from the header (they repeat products from the listing)
  img/*.svg             simple line drawings used as product images
  robots.txt            allows everything except /admin/, asks for a 1-second crawl delay
  admin/index.html      staff-only page the scraper must refuse
  style.css             shared stylesheet

The fixed seed means the site is identical every time it is rebuilt.
Run from the repo root:  python scripts/build_sandbox_site.py
"""
import random
import shutil
from html import escape
from pathlib import Path

SEED = 42
PAGES = 5
PER_PAGE = 12
SHOP = "NOIRE"
OUT = Path("sandbox_site")

CATEGORIES = {
    "Outerwear": (["Track Jacket", "Bomber", "Shell Jacket", "Puffer Vest", "Coach Jacket"], (2499, 6999)),
    "Tops": (["Boxy Tee", "Longsleeve", "Mesh Top", "Hoodie", "Knit Polo"], (899, 2899)),
    "Bottoms": (["Cargo Pants", "Track Pants", "Wide Denim", "Nylon Shorts", "Pleated Trousers"], (1499, 3999)),
    "Accessories": (["Shield Sunglasses", "Signet Ring", "Leather Gloves", "Chain Necklace", "Bucket Hat"], (499, 2499)),
}
ADJECTIVES = ["Onyx", "Static", "Mono", "Ghost", "Carbon", "Eclipse", "Raw", "Shadow", "Neon", "Ash", "Night", "Steel"]

SVG_HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" fill="none" stroke="#f4f4f2" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
ICONS = {
    "jacket": '<path d="M70 40 L100 52 L130 40 L165 62 L152 100 L138 94 L138 165 L62 165 L62 94 L48 100 L35 62 Z"/><path d="M100 52 L100 165"/><path d="M85 46 L100 70 L115 46"/>',
    "vest": '<path d="M72 40 L100 60 L128 40 L140 70 L140 165 L60 165 L60 70 Z"/><path d="M100 60 L100 165"/><path d="M60 95 H140 M60 125 H140"/>',
    "tee": '<path d="M75 40 Q100 58 125 40 L165 62 L150 95 L135 88 L135 165 L65 165 L65 88 L50 95 L35 62 Z"/>',
    "hoodie": '<path d="M78 46 Q100 20 122 46 L165 66 L152 102 L138 95 L138 165 L62 165 L62 95 L48 102 L35 66 Z"/><path d="M80 46 Q100 74 120 46"/><path d="M78 130 H122 V150 H78 Z"/>',
    "pants": '<path d="M65 35 H135 L145 165 H108 L100 80 L92 165 H55 Z"/><path d="M65 50 H135"/>',
    "shorts": '<path d="M60 60 H140 L148 135 H108 L100 95 L92 135 H52 Z"/><path d="M60 74 H140"/>',
    "sunglasses": '<path d="M30 92 H170"/><path d="M40 92 Q40 125 70 125 Q92 125 92 98 L92 92"/><path d="M108 92 L108 98 Q108 125 130 125 Q160 125 160 92"/>',
    "ring": '<circle cx="100" cy="115" r="42"/><path d="M82 72 L100 52 L118 72 Z"/>',
    "gloves": '<path d="M70 165 V100 L58 70 Q55 62 63 60 L78 90 V45 Q78 37 86 37 Q94 37 94 45 V85 V38 Q94 30 102 30 Q110 30 110 38 V85 V44 Q110 36 118 36 Q126 36 126 44 V92 V60 Q126 52 134 52 Q142 52 142 60 V120 Q142 150 125 165 Z"/>',
    "chain": '<ellipse cx="100" cy="60" rx="18" ry="12"/><ellipse cx="100" cy="88" rx="12" ry="18"/><ellipse cx="100" cy="116" rx="18" ry="12"/><ellipse cx="100" cy="144" rx="12" ry="18"/>',
    "hat": '<path d="M65 110 Q65 55 100 55 Q135 55 135 110"/><path d="M40 112 Q100 140 160 112 L148 104 Q100 124 52 104 Z"/>',
}
ICON_FOR = {
    "Track Jacket": "jacket", "Bomber": "jacket", "Shell Jacket": "jacket", "Coach Jacket": "jacket", "Puffer Vest": "vest",
    "Boxy Tee": "tee", "Longsleeve": "tee", "Mesh Top": "tee", "Knit Polo": "tee", "Hoodie": "hoodie",
    "Cargo Pants": "pants", "Track Pants": "pants", "Wide Denim": "pants", "Pleated Trousers": "pants", "Nylon Shorts": "shorts",
    "Shield Sunglasses": "sunglasses", "Signet Ring": "ring", "Leather Gloves": "gloves", "Chain Necklace": "chain", "Bucket Hat": "hat",
}

DETAIL_TEMPLATES = {
    "Outerwear": [
        "{a_adj} layer cut for city nights. Relaxed through the body with dropped shoulders and a two-way zip.",
        "Built to be seen: a structured shell with contrast stitching and deep side pockets.",
        "Lightweight but weatherproof, with a stand collar and elastic cuffs that keep the wind out.",
    ],
    "Tops": [
        "A heavyweight piece with a boxy fit and a slightly cropped hem. Gets softer with every wash.",
        "Clean lines, no logos. {a_adj} staple that goes under a jacket or on its own.",
        "Garment-dyed for a lived-in tone, with a ribbed collar that holds its shape.",
    ],
    "Bottoms": [
        "Wide through the leg with a high rise and a clean drape. Pairs with everything in the drop.",
        "Utility pockets, adjustable hems and a tapered finish. Made for long days on foot.",
        "A relaxed, {adj_l}-toned fit with an elastic waist and drawcord, dressed up or down.",
    ],
    "Accessories": [
        "The finishing piece. Minimal, sharp and made to be worn every day.",
        "A small detail with a loud presence. Polished finish, built to last.",
        "Designed in monochrome to sit with the rest of the collection.",
    ],
}
MATERIALS = {
    "Outerwear": ["100% recycled nylon", "Cotton twill, nylon lining", "Water-repellent polyester"],
    "Tops": ["100% cotton jersey, 260 gsm", "Cotton-modal blend", "Open-knit mesh"],
    "Bottoms": ["Cotton ripstop", "14 oz rigid denim", "Nylon with a matte finish"],
    "Accessories": ["Stainless steel", "Full-grain leather", "Polycarbonate frame, UV400 lenses", "Cotton canvas"],
}
SIZES = {"Outerwear": ["S", "M", "L", "XL"], "Tops": ["XS", "S", "M", "L", "XL"], "Bottoms": ["28", "30", "32", "34", "36"],
         "Accessories": ["One size"]}
COLORS = ["Black", "Off-white", "Charcoal", "Ash grey", "Black / white"]


def add_details(products, rng):
    """Detail-page content, from its own random stream so listing prices and ratings don't change."""
    for p in products:
        adj = p["name"].split()[0]
        p["description"] = rng.choice(DETAIL_TEMPLATES[p["category"]]).format(adj_l=adj.lower(), a_adj=("An " if adj[0] in "AEIOU" else "A ") + adj.lower())
        p["material"] = rng.choice(MATERIALS[p["category"]])
        p["color"] = rng.choice(COLORS)
        sizes = SIZES[p["category"]]
        p["sizes_out"] = [] if len(sizes) == 1 else rng.sample(sizes, k=rng.choice([0, 0, 1, 2]))
        p["sizes"] = sizes
        p["stock"] = rng.choice(["In stock"] * 8 + ["Low stock"] * 2 + ["Sold out"])


def peso(amount):
    return f"₱{amount:,.2f}"


def make_products(rng):
    products, seen = [], set()
    while len(products) < PAGES * PER_PAGE:
        category = rng.choice(list(CATEGORIES))
        items, (low, high) = CATEGORIES[category]
        item = rng.choice(items)
        name = f"{rng.choice(ADJECTIVES)} {item}"
        if name in seen:
            continue
        seen.add(name)
        price = rng.randrange(low, high, 100) + 0.0
        on_sale = rng.random() < 0.15
        has_reviews = rng.random() > 0.1
        products.append({
            "id": f"NR-{len(products) + 1:03d}",
            "name": name,
            "slug": name.lower().replace(" ", "-"),
            "category": category,
            "image": f"img/{ICON_FOR[item]}.svg",
            "price": round(price * 0.7, 2) if on_sale else price,
            "old_price": price if on_sale else None,
            "rating": round(rng.uniform(3.2, 5.0), 1) if has_reviews else None,
            "reviews": rng.randint(3, 480) if has_reviews else 0,
            "tone": rng.randint(18, 70),
        })
    return products


def layout(title, body, depth=0):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} | {SHOP}</title>
  <link rel="stylesheet" href="{up}style.css">
</head>
<body>
  <header class="site-header">
    <a class="wordmark" href="{up}index.html">{SHOP}</a>
    <nav><a href="{up}page-1.html">Shop all</a><a href="{up}new-in.html">New in</a><a href="{up}sale.html">Sale</a></nav>
  </header>
  <main>
{body}
  </main>
  <footer class="site-footer">{SHOP} is a practice shop for scraping exercises. Not a real store.</footer>
</body>
</html>
"""


def card(p):
    old = f'<span class="price-old">{peso(p["old_price"])}</span>' if p["old_price"] else ""
    badge = '<span class="badge">Sale</span>' if p["old_price"] else ""
    if p["rating"] is None:
        rating = '<p class="rating no-reviews">No reviews yet</p>'
    else:
        rating = (f'<p class="rating" data-rating="{p["rating"]}">★ {p["rating"]} '
                  f'<span class="review-count">({p["reviews"]})</span></p>')
    return f"""      <article class="product" data-product-id="{p['id']}">
        <a class="product-link" href="product/{p['slug']}.html">
          <div class="product-image" style="--tone: {p['tone']}%">{badge}<img src="{p['image']}" alt="{escape(p['name'])}"></div>
          <h2 class="product-name">{escape(p['name'])}</h2>
        </a>
        <p class="product-category">{escape(p['category'])}</p>
        <p class="price-line"><span class="price">{peso(p['price'])}</span>{old}</p>
        {rating}
      </article>"""


def listing_page(number, items):
    prev_link = f'<a class="prev" href="page-{number - 1}.html">← Previous</a>' if number > 1 else '<span></span>'
    next_link = f'<a class="next" rel="next" href="page-{number + 1}.html">Next →</a>' if number < PAGES else '<span></span>'
    cards = "\n".join(card(p) for p in items)
    body = f"""    <section class="listing-head">
      <h1>Shop all</h1>
      <p>Page {number} of {PAGES}</p>
    </section>
    <section class="product-grid">
{cards}
    </section>
    <nav class="pagination">{prev_link}<span class="page-number">{number} / {PAGES}</span>{next_link}</nav>"""
    return layout(f"Shop all, page {number}", body)


def collection_page(title, intro, items):
    cards = "\n".join(card(p) for p in items)
    body = f"""    <section class="listing-head">
      <h1>{escape(title)}</h1>
      <p>{escape(intro)}</p>
    </section>
    <section class="product-grid">
{cards}
    </section>
    <nav class="pagination"><span></span><a class="button-inline" href="page-1.html">Shop all →</a><span></span></nav>"""
    return layout(title, body)


def product_page(p):
    old = f'<span class="price-old">{peso(p["old_price"])}</span>' if p["old_price"] else ""
    sizes = "".join(
        f'<li class="size{" out" if size in p["sizes_out"] else ""}">{size}</li>' for size in p["sizes"]
    )
    rating = (f'<p class="rating" data-rating="{p["rating"]}">★ {p["rating"]} <span class="review-count">({p["reviews"]} reviews)</span></p>'
              if p["rating"] is not None else '<p class="rating no-reviews">No reviews yet</p>')
    stock_class = p["stock"].lower().replace(" ", "-")
    body = f"""    <p class="breadcrumb"><a href="../page-1.html">Shop all</a> / {escape(p['category'])}</p>
    <section class="product-detail">
      <div class="product-image large" style="--tone: {p['tone']}%"><img src="../{p['image']}" alt="{escape(p['name'])}"></div>
      <div class="product-info">
        <p class="product-category">{escape(p['category'])}</p>
        <h1 class="product-name">{escape(p['name'])}</h1>
        <p class="price-line"><span class="price">{peso(p['price'])}</span>{old}</p>
        {rating}
        <p class="stock {stock_class}">{p['stock']}</p>
        <p class="description">{escape(p['description'])}</p>
        <h3>Size</h3>
        <ul class="sizes">{sizes}</ul>
        <dl class="specs">
          <dt>Color</dt><dd class="color">{escape(p['color'])}</dd>
          <dt>Material</dt><dd class="material">{escape(p['material'])}</dd>
          <dt>SKU</dt><dd class="sku">{p['id']}</dd>
        </dl>
        <a class="button" href="../page-1.html">Back to shop</a>
      </div>
    </section>"""
    return layout(p["name"], body, depth=1)


INDEX_BODY = f"""    <section class="hero">
      <h1>Wear it<br>loud.</h1>
      <p>Monochrome streetwear and accessories. 60 pieces, 5 pages.</p>
      <a class="button" href="page-1.html">Shop all</a>
    </section>"""

ADMIN_BODY = """    <section class="listing-head">
      <h1>Staff only</h1>
      <p>Inventory and order admin. Crawlers are not allowed here (see robots.txt).</p>
    </section>"""

ROBOTS = """# robots.txt for the NOIRE practice shop
User-agent: *
Disallow: /admin/
Crawl-delay: 1
"""

CSS = """:root {
  --ink: #0b0b0b;
  --paper: #f4f4f2;
  --mid: #8a8a86;
  --line: #d9d9d5;
  --font: "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--font); }
a { color: inherit; text-decoration: none; }
main { max-width: 1200px; margin: 0 auto; padding: 0 24px 64px; }

.site-header { position: sticky; top: 0; z-index: 2; display: flex; align-items: center; justify-content: space-between;
  padding: 18px 32px; background: var(--ink); color: var(--paper); }
.wordmark { font-size: 28px; font-weight: 800; letter-spacing: -1.5px; transform: scaleY(1.15); }
.site-header nav a { margin-left: 28px; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; opacity: .85; }
.site-header nav a:hover { opacity: 1; }

.hero { min-height: 70vh; display: flex; flex-direction: column; justify-content: center; padding: 48px 0;
  background: linear-gradient(135deg, var(--ink) 0 55%, #2a2a2a 55% 100%); color: var(--paper);
  margin: 0 -24px; padding-left: 48px; }
.hero h1 { font-size: clamp(56px, 10vw, 128px); line-height: .92; letter-spacing: -4px; margin: 0 0 24px; }
.hero p { color: #bdbdb8; max-width: 420px; }

.listing-head { display: flex; align-items: baseline; justify-content: space-between; padding: 40px 0 20px;
  border-bottom: 2px solid var(--ink); margin-bottom: 28px; }
.listing-head h1 { font-size: 44px; letter-spacing: -2px; margin: 0; text-transform: uppercase; }
.listing-head p { color: var(--mid); margin: 0; }

.product-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px 20px; }
@media (max-width: 900px) { .product-grid { grid-template-columns: repeat(2, 1fr); } }
.product-image { position: relative; aspect-ratio: 3 / 4; display: flex; align-items: flex-end; padding: 12px;
  background: linear-gradient(160deg, hsl(0 0% calc(var(--tone) + 20%)), hsl(0 0% var(--tone)));
  color: rgba(255,255,255,.7); font-size: 11px; text-transform: uppercase; letter-spacing: 2px;
  transition: filter .2s; }
.product:hover .product-image { filter: contrast(1.25); }
.product-image img { position: absolute; inset: 14% 12%; width: 76%; height: 72%; object-fit: contain; }
.pagination .button-inline { border: 2px solid var(--ink); padding: 10px 18px; font-weight: 700; }
.product-image.large { aspect-ratio: 4 / 5; }
.badge { position: absolute; top: 12px; left: 12px; background: var(--paper); color: var(--ink); padding: 4px 8px;
  font-weight: 700; letter-spacing: 1px; }
.product-name { font-size: 15px; font-weight: 700; margin: 12px 0 2px; text-transform: uppercase; letter-spacing: .3px; }
.product-category { font-size: 12px; color: var(--mid); margin: 0 0 6px; text-transform: uppercase; letter-spacing: 1px; }
.price-line { margin: 0 0 4px; font-size: 15px; }
.price { font-weight: 700; }
.price-old { margin-left: 8px; color: var(--mid); text-decoration: line-through; font-size: 13px; }
.rating { margin: 0; font-size: 13px; }
.review-count, .no-reviews { color: var(--mid); }

.pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 48px; padding-top: 20px;
  border-top: 1px solid var(--line); text-transform: uppercase; font-size: 13px; letter-spacing: 1.5px; }
.pagination a { border: 2px solid var(--ink); padding: 10px 18px; font-weight: 700; }
.pagination a:hover, .button:hover { background: var(--ink); color: var(--paper); }
.button { display: inline-block; margin-top: 16px; border: 2px solid currentColor; padding: 12px 22px;
  text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; font-size: 13px; }
.hero .button:hover { background: var(--paper); color: var(--ink); }

.product-detail { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; padding-top: 40px; }
.product-detail h1 { font-size: 40px; letter-spacing: -1.5px; margin: 4px 0 12px; }
.breadcrumb { margin: 28px 0 0; font-size: 12px; color: var(--mid); text-transform: uppercase; letter-spacing: 1px; }
.product-info h3 { font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; margin: 24px 0 8px; }
.description { line-height: 1.6; max-width: 46ch; margin: 18px 0 0; }
.stock { display: inline-block; margin: 12px 0 0; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.stock.low-stock { color: #a15c00; }
.stock.sold-out { color: var(--mid); text-decoration: line-through; }
.sizes { list-style: none; display: flex; flex-wrap: wrap; gap: 8px; padding: 0; margin: 0; }
.size { min-width: 44px; text-align: center; padding: 8px 10px; border: 1.5px solid var(--ink); font-size: 13px; font-weight: 700; }
.size.out { color: var(--mid); border-color: var(--line); text-decoration: line-through; }
.specs { display: grid; grid-template-columns: 90px 1fr; gap: 6px 12px; margin: 24px 0 0; font-size: 13px; }
.specs dt { color: var(--mid); text-transform: uppercase; letter-spacing: 1px; font-size: 11px; padding-top: 2px; }
.specs dd { margin: 0; }
.site-footer { padding: 24px 32px; font-size: 12px; color: var(--mid); border-top: 1px solid var(--line); }
"""


def main():
    rng = random.Random(SEED)
    products = make_products(rng)
    add_details(products, random.Random(SEED + 1))
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "product").mkdir(parents=True)
    (OUT / "admin").mkdir()
    (OUT / "img").mkdir()
    for icon, shape in ICONS.items():
        (OUT / "img" / f"{icon}.svg").write_text(f"{SVG_HEAD}{shape}</svg>", encoding="utf-8")

    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (OUT / "index.html").write_text(layout("Home", INDEX_BODY), encoding="utf-8")
    (OUT / "admin" / "index.html").write_text(layout("Admin", ADMIN_BODY, depth=1), encoding="utf-8")
    for number in range(1, PAGES + 1):
        items = products[(number - 1) * PER_PAGE: number * PER_PAGE]
        (OUT / f"page-{number}.html").write_text(listing_page(number, items), encoding="utf-8")
    newest = products[-12:][::-1]
    sale = [p for p in products if p["old_price"] is not None]
    (OUT / "new-in.html").write_text(collection_page("New in", "The 12 latest drops.", newest), encoding="utf-8")
    (OUT / "sale.html").write_text(collection_page("Sale", f"{len(sale)} pieces at 30% off.", sale), encoding="utf-8")
    for p in products:
        (OUT / "product" / f"{p['slug']}.html").write_text(product_page(p), encoding="utf-8")

    on_sale = sum(p["old_price"] is not None for p in products)
    no_reviews = sum(p["rating"] is None for p in products)
    print(f"Built {len(products)} products on {PAGES} pages in {OUT}/ ({on_sale} on sale, {no_reviews} without reviews)")


if __name__ == "__main__":
    main()
