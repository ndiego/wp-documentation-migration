"""Diff two `wp spike dump --content` files by post ID.

Usage: python3 -I diffdump.py <before.jsonl> <after.jsonl>
"""
import json
import sys

a = {r["ID"]: r for r in map(json.loads, open(sys.argv[1]))}
b = {r["ID"]: r for r in map(json.loads, open(sys.argv[2]))}
print("posts before", len(a), "after", len(b))
print("new IDs:", [(i, b[i]["post_name"], b[i]["post_title"], b[i]["post_parent"]) for i in b if i not in a])
print("gone IDs:", [(i, a[i]["post_name"]) for i in a if i not in b])
changed = {}
for i in a:
    if i not in b:
        continue
    d = [f for f in a[i] if a[i][f] != b[i].get(f)]
    if d:
        changed[i] = d
print("changed posts:", len(changed))
for i, fields in changed.items():
    print(f"  {i} {a[i]['post_name']}: {fields}")
    for f in fields:
        if f != "post_content":
            print(f"      {f}: {a[i][f]!r} -> {b[i][f]!r}")
