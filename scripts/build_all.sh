#!/bin/sh
# One command for the before/after builds (README "Structure mode and before/after"):
#   1. download images/posters into docs/assets/ (skipped when nothing is missing apart from the assets
#      data/download-report.json records as unreachable; FORCE_DOWNLOAD=1 to always run)
#   2. build/before/  today's category tree (assets -> ../../docs/assets symlink)
#   3. docs/          the hand-designed tree from data/structure.yaml (+ data/restructure-map.json,
#                     data/structure-metrics.json)
#   4. link check of both trees
# Usage: scripts/build_all.sh [structure.yaml]   (default data/structure.yaml)
set -eu
cd "$(dirname "$0")/.."
PY=.venv/bin/python
STRUCTURE="${1:-data/structure.yaml}"

[ -x "$PY" ] || { echo "missing .venv (see notes/converter-notes.md)"; exit 1; }
"$PY" -c 'import yaml, bs4, markdownify' 2>/dev/null || .venv/bin/pip install -q beautifulsoup4 markdownify pyyaml

# validate first so a broken structure file fails before anything is rebuilt
"$PY" -I scripts/convert.py --structure "$STRUCTURE" --check-structure

missing=$("$PY" -I -c '
import json, pathlib, sys
m = pathlib.Path("docs/assets/images-manifest.json")
if not m.exists():
    print("manifest"); sys.exit()
r = pathlib.Path("data/download-report.json")
failed = {x["path"] for x in json.loads(r.read_text()) if x["status"] == "failed"} if r.exists() else set()
print(sum(1 for e in json.loads(m.read_text()) if e["kind"] != "video"
          and not pathlib.Path(e["local_path"]).exists() and e["local_path"] not in failed))
')
# videos (~1.3 GB) are never fetched here; <video src> points at wordpress.org (convert.py --video-src remote)
if [ "${FORCE_DOWNLOAD:-0}" = 1 ] || [ "$missing" != 0 ]; then
    echo "assets: downloading ($missing missing image/poster files)"
    python3 -I scripts/download_assets.py --kinds image,poster || echo "download step reported failures; continuing"
else
    echo "assets: all present (known-unreachable ones excepted, notes/missing-assets.md); skipping download"
fi

"$PY" -I scripts/convert.py --out build/before
"$PY" -I scripts/convert.py --structure "$STRUCTURE"
echo "== link check: build/before"; "$PY" -I scripts/check_links.py --docs build/before
echo "== link check: docs";         "$PY" -I scripts/check_links.py
