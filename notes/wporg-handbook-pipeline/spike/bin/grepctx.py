"""Print regex matches with context from stored post_content in a dump.

Usage: python3 -I grepctx.py <dump.jsonl> <regex> [max] [ctx-chars] [key-filter-substring]
"""
import json
import re
import sys

dump, rx = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 5
ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 200
filt = sys.argv[5] if len(sys.argv) > 5 else ""
n = 0
for line in open(dump):
    r = json.loads(line)
    key = r["permalink"].split("/documentation/")[1].rstrip("/")
    if filt not in key:
        continue
    for m in re.finditer(rx, r.get("post_content", "")):
        s = r["post_content"][max(0, m.start() - ctx): m.end() + ctx]
        print(f"=== {key} @{m.start()}\n{s}\n")
        n += 1
        if n >= mx:
            sys.exit()
