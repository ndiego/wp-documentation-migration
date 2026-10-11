"""Check same-page anchor links (#frag) against ids present in stored HTML, and estimate how many
would resolve if the theme auto-added GitHub-style heading ids (lowercase, strip punctuation,
spaces->dashes) vs WordPress sanitize_title-style ids.

Usage: python3 -I anchors.py <dump-with-content.jsonl>
"""
import html as H
import json
import re
import sys
import unicodedata


def gh_slug(text):
    t = H.unescape(re.sub(r"<[^>]+>", "", text)).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def wp_slug(text):
    t = H.unescape(re.sub(r"<[^>]+>", "", text)).strip().lower()
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9 _-]", "", t)
    t = re.sub(r"[\s_]+", "-", t)
    return re.sub(r"-+", "-", t).strip("-")


tot = ok_explicit = ok_gh = ok_wp = 0
miss = []
for line in open(sys.argv[1]):
    r = json.loads(line)
    c = r["post_content"]
    ids = set(re.findall(r'\s(?:id|name)="([^"]+)"', c))
    heads = re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", c, re.S)
    gh = {gh_slug(h) for h in heads}
    wp = {wp_slug(h) for h in heads}
    for frag in re.findall(r'href="#([^"]+)"', c):
        tot += 1
        if frag in ids:
            ok_explicit += 1
        elif frag in gh:
            ok_gh += 1
        else:
            miss.append((r["post_name"], frag))
        if frag in ids or frag in wp:
            ok_wp += 1
print(f"same-page #anchor links: {tot}")
print(f"  resolve to an explicit id/name in stored HTML: {ok_explicit}")
print(f"  resolve only if theme adds GitHub-style heading ids: {ok_gh}")
print(f"  resolve with explicit ids + sanitize_title-style heading ids: {ok_wp}")
print(f"  resolve to nothing either way: {len(miss)}  e.g. {miss[:8]}")
