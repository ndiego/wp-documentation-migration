#!/usr/bin/env python3
"""Resolve article slugs that are linked from content but are not in raw/articles.json.

Many links point at old slugs (e.g. /documentation/article/blocks/) or the legacy
/support/article/<slug>/ path; wordpress.org 301-redirects these. This script finds every
such slug and follows the redirect once, writing data/redirects.json:
  {"old-slug": {"slug": "new-slug" | null, "final_url": "...", "status": 200|404|...}}
Usage: python3 -I scripts/resolve_redirects.py
"""
import json, re, pathlib, time, urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OUT = ROOT / "data" / "redirects.json"
UA = "Mozilla/5.0 (compatible; wp-docs-migration/0.1)"
LINK_RE = re.compile(r'href="(?:https?://(?:www\.)?wordpress\.org)?/(?:documentation|support)/article/([^/"#?]+)', re.I)

articles = json.loads((RAW / "articles.json").read_text())
pages = json.loads((RAW / "pages.json").read_text())
known = {a["slug"] for a in articles}
wanted = set()
for it in articles + pages:
    for m in LINK_RE.finditer(it["content"]["rendered"]):
        s = urllib.parse.unquote(m.group(1)).lower()
        if s not in known:
            wanted.add(s)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
opener = urllib.request.build_opener(NoRedirect)

result = json.loads(OUT.read_text()) if OUT.exists() else {}
for slug in sorted(wanted):
    if slug in result:
        continue
    url = f"https://wordpress.org/documentation/article/{slug}/"
    target = None
    status = None
    for _ in range(4):  # follow up to 4 hops manually
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        try:
            status = opener.open(req, timeout=30).status
            break  # 200 at a URL we can't map
        except urllib.error.HTTPError as e:
            status = e.code
            if e.code in (301, 302, 307, 308) and e.headers.get("Location"):
                url = urllib.parse.urljoin(url, e.headers["Location"])
                m = re.search(r"/documentation/article/([^/#?]+)/?", url)
                if m and m.group(1) in known:
                    target = m.group(1)
                    break
                continue
            break
    result[slug] = {"slug": target, "final_url": url, "status": status}
    print(f"{slug} -> {target} ({url})")
    time.sleep(0.3)

OUT.write_text(json.dumps(result, indent=1, sort_keys=True))
print(f"wrote {OUT}: {sum(1 for v in result.values() if v['slug'])}/{len(result)} resolved")
