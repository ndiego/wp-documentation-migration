#!/usr/bin/env python3
"""Export the production Theme Handbook (post type theme-handbook) from the REST API.

Writes <data>/pages.json (id, slug, title, parent, menu_order, link, modified, content) and,
with --html, the rendered front-end page of every entry to <data>/prod-html/<id>.html
(the TOC ids, chapter list and prev/next links only exist in the front-end HTML).

Usage: python3 -I fetch_prod.py <data-dir> [--html]
"""
import json
import pathlib
import sys
import time
import urllib.request

API = "https://developer.wordpress.org/wp-json/wp/v2/theme-handbook"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
FIELDS = "id,slug,title,parent,menu_order,link,modified,content"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), dict(r.headers)


def main():
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    pages, page = [], 1
    while True:
        body, headers = get(f"{API}?per_page=100&page={page}&_fields={FIELDS}")
        pages += json.loads(body)
        if page >= int(headers.get("X-WP-TotalPages") or headers.get("x-wp-totalpages") or 1):
            break
        page += 1
    rows = [dict(id=p["id"], slug=p["slug"], title=p["title"]["rendered"], parent=p["parent"],
                 menu_order=p["menu_order"], link=p["link"], modified=p["modified"],
                 content=p["content"]["rendered"]) for p in pages]
    (out / "pages.json").write_text(json.dumps(rows, indent=1))
    print(f"{len(rows)} pages -> {out / 'pages.json'}")
    if "--html" in sys.argv:
        d = out / "prod-html"
        d.mkdir(exist_ok=True)
        for p in rows:
            f = d / f"{p['id']}.html"
            if f.exists() and f.stat().st_size:
                continue
            f.write_bytes(get(p["link"])[0])
            time.sleep(0.3)
        print(f"front-end HTML -> {d}")


if __name__ == "__main__":
    main()
