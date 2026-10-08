#!/bin/sh
# One command for the before/after builds (README "Structure mode and before/after"):
#   1. build/before/  today's category tree (assets -> ../../docs/assets symlink)
#   2. docs/          the hand-designed tree from data/structure.yaml (+ data/restructure-map.json,
#                     data/structure-metrics.json, docs/assets/images-manifest.json)
#   3. download images/posters listed in docs/assets/images-manifest.json into docs/assets/ (skipped when
#      nothing is missing apart from the assets data/download-report.json records as unreachable;
#      FORCE_DOWNLOAD=1 to always run). The downloader records the type of extension-less external images in
#      data/external-asset-types.json and the converter names those files by it, so when that file changed
#      both trees are converted again and the downloader runs once more to rename its ".img" placeholders.
#   4. link check of both trees
# Usage: scripts/build_all.sh [structure.yaml]   (default data/structure.yaml)
set -eu
cd "$(dirname "$0")/.."
PY=.venv/bin/python
STRUCTURE="${1:-data/structure.yaml}"
TYPES=data/external-asset-types.json

[ -x "$PY" ] || { echo "missing .venv (see notes/converter-notes.md)"; exit 1; }
"$PY" -c 'import yaml, bs4, markdownify' 2>/dev/null || .venv/bin/pip install -q beautifulsoup4 markdownify pyyaml

# validate first so a broken structure file fails before anything is rebuilt
"$PY" -I scripts/convert.py --structure "$STRUCTURE" --check-structure

convert_both() {
    "$PY" -I scripts/convert.py --out build/before
    "$PY" -I scripts/convert.py --structure "$STRUCTURE"   # writes docs/assets/images-manifest.json
}
# content of the types file (key order/whitespace ignored), to detect whether the downloader learned new types
types_sum() {
    "$PY" -I -c 'import json, pathlib, sys; p = pathlib.Path(sys.argv[1])
print(json.dumps(json.loads(p.read_text()), sort_keys=True) if p.exists() else "none")' "$TYPES" | cksum
}

convert_both

# number of image/poster files in the manifest that are neither on disk nor known to be unreachable
missing=$("$PY" -I -c '
import json, pathlib
m = pathlib.Path("docs/assets/images-manifest.json")
r = pathlib.Path("data/download-report.json")
failed = {x["path"] for x in json.loads(r.read_text()) if x["status"] == "failed"} if r.exists() else set()
print(sum(1 for e in json.loads(m.read_text()) if e["kind"] != "video"
          and not pathlib.Path(e["local_path"]).exists() and e["local_path"] not in failed))
')
# videos (~1.3 GB) are never fetched here; <video src> points at wordpress.org (convert.py --video-src remote)
if [ "${FORCE_DOWNLOAD:-0}" = 1 ] || [ "$missing" != 0 ]; then
    echo "assets: downloading ($missing missing image/poster files)"
    before_types=$(types_sum)
    # individual unreachable files are recorded in data/download-report.json and do not fail the step;
    # anything else (missing manifest, crash) stops the build
    python3 -I scripts/download_assets.py --kinds image,poster
    if [ "$(types_sum)" != "$before_types" ]; then
        echo "assets: $TYPES changed; converting both trees again for the new file extensions"
        convert_both
        python3 -I scripts/download_assets.py --kinds image,poster
    fi
else
    echo "assets: all present (known-unreachable ones excepted, notes/missing-assets.md); skipping download"
fi

echo "== link check: build/before"; "$PY" -I scripts/check_links.py --docs build/before
echo "== link check: docs";         "$PY" -I scripts/check_links.py
