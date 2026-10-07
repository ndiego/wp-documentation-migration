#!/usr/bin/env python3
"""Pull all content from wordpress.org/documentation REST API into raw/ as JSON.

Usage: python3 -I scripts/fetch_raw.py [--media]
"""
import json, sys, time, urllib.request, urllib.parse, pathlib

BASE = "https://wordpress.org/documentation/wp-json/wp/v2"
UA = "Mozilla/5.0 (compatible; wp-docs-migration/0.1; +nick.diego@a8c.com)"
RAW = pathlib.Path(__file__).resolve().parent.parent / "raw"
RAW.mkdir(exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r), dict(r.headers)
        except Exception as e:  # noqa
            wait = 2 ** attempt
            print(f"  retry {attempt+1} after error {e}; sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise SystemExit(f"failed: {url}")

def paginate(endpoint, params):
    items = []
    page = 1
    while True:
        q = dict(params, per_page=100, page=page)
        url = f"{BASE}/{endpoint}?{urllib.parse.urlencode(q)}"
        data, headers = get(url)
        items.extend(data)
        total_pages = int(headers.get("X-WP-TotalPages", "1"))
        print(f"{endpoint}: page {page}/{total_pages} ({len(items)} items)", file=sys.stderr)
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)
    return items

def dump(name, data):
    p = RAW / f"{name}.json"
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"wrote {p} ({len(data)} items)", file=sys.stderr)

if __name__ == "__main__":
    dump("categories", paginate("category", {}))
    dump("pages", paginate("pages", {"context": "view"}))
    dump("articles", paginate("articles", {"_embed": "wp:term,wp:featuredmedia"}))
    dump("versions", paginate("wordpress-versions", {"_embed": "wp:term"}))
    if "--media" in sys.argv:
        dump("media", paginate("media", {"_fields": "id,date,slug,source_url,alt_text,caption,title,media_type,mime_type,media_details,post,link"}))
