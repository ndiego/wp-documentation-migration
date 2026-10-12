#!/bin/bash
# Fetch the locally imported version of every production page (same URL path on localhost:8888).
# usage: fetch_local.sh <data-dir>     (reads <data-dir>/pages.json from fetch_prod.py)
# writes <data-dir>/local-html/<id>.html and <data-dir>/local-status.tsv (id, status, final URL)
D=$1
mkdir -p "$D/local-html"
: > "$D/local-status.tsv"
python3 -I -c '
import json, sys
for p in json.load(open(sys.argv[1])):
    print(p["id"], p["link"])
' "$D/pages.json" | while read -r id url; do
  l="${url/https:\/\/developer.wordpress.org/http://localhost:8888}"
  curl -s -L -o "$D/local-html/$id.html" -w "$id\t%{http_code}\t%{url_effective}\n" "$l" >> "$D/local-status.tsv"
done
echo "fetched $(wc -l < "$D/local-status.tsv") pages; non-200: $(awk -F'\t' '$2!=200' "$D/local-status.tsv" | wc -l)"
