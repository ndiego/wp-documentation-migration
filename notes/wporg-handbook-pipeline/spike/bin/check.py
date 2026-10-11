"""Compare a `wp spike dump` JSONL against the manifest.

Usage: python3 -I check.py <manifest.json> <dump.jsonl> [<docs-root-for-h1-check>]
"""
import json
import os
import re
import sys

manifest = json.load(open(sys.argv[1]))
rows = [json.loads(l) for l in open(sys.argv[2]) if l.strip().startswith("{")]
docs = sys.argv[3] if len(sys.argv) > 3 else None
BASE = "http://localhost:8881/documentation/"

by_key = {}
for r in rows:
    key = r["permalink"].replace(BASE, "").rstrip("/")
    by_key[key] = r
by_id = {r["ID"]: r for r in rows}

print("posts:", len(rows), "manifest entries:", len(manifest))
missing = [k for k in manifest if k not in by_key]
extra = [k for k in by_key if k not in manifest]
print("manifest keys with no post at that permalink:", len(missing), missing[:10])
print("posts whose permalink is not a manifest key:", len(extra), extra[:10])

bad_parent, bad_order, title_diff, empty = [], [], [], []
for k, e in manifest.items():
    r = by_key.get(k)
    if not r:
        continue
    want_parent = by_key.get(e["parent"], {}).get("ID", 0) if e["parent"] else 0
    if r["post_parent"] != want_parent:
        bad_parent.append((k, r["post_parent"], want_parent))
    if r["menu_order"] != (e.get("order") or 0):
        bad_order.append((k, r["menu_order"], e.get("order")))
    if r["post_title"] != e["title"]:
        title_diff.append((k, e["title"], r["post_title"]))
    if r["len"] == 0:
        empty.append(k)
print("wrong post_parent:", len(bad_parent), bad_parent[:10])
print("menu_order != manifest order:", len(bad_order), bad_order[:10])
print("post_title != manifest title:", len(title_diff))
for t in title_diff[:25]:
    print("   ", t)
print("empty content:", len(empty), empty[:10])

if docs:
    # How do files start? (frontmatter? H1 on line 1?)
    starts = {}
    for k, e in manifest.items():
        txt = open(os.path.join(docs, e["markdown_source"]), encoding="utf-8").read()
        first = txt.lstrip().split("\n", 1)[0]
        kind = "frontmatter" if first.startswith("---") else ("h1" if re.match(r"#\s", first) else "other:" + first[:30])
        starts[kind] = starts.get(kind, 0) + 1
    print("file starts:", starts)
