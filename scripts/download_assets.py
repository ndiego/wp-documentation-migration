#!/usr/bin/env python3
"""Download every asset listed in docs/assets/images-manifest.json to its local_path.

Usage: python3 -I scripts/download_assets.py [--workers 6] [--kinds image,poster,video]
Skips files that already exist with a non-zero size. Writes data/download-report.json.

Extension-less external images (lh3.googleusercontent.com/...): the converter picks the local file
extension from data/external-asset-types.json, which this script maintains (Content-Type of each
download, or magic bytes of a file already on disk). Workflow: download -> convert -> download again;
the second run renames files that were saved under a placeholder ".img" name to the new local_path
and deletes ".img" files no longer referenced by the manifest.
"""
import json, sys, time, pathlib, argparse, urllib.request, urllib.error, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "docs" / "assets" / "images-manifest.json"
REPORT = ROOT / "data" / "download-report.json"
TYPES = ROOT / "data" / "external-asset-types.json"
ASSETS = ROOT / "docs" / "assets"
MAGIC = [(b"\x89PNG\r\n\x1a\n", "image/png"), (b"\xff\xd8\xff", "image/jpeg"), (b"GIF87a", "image/gif"),
         (b"GIF89a", "image/gif"), (b"BM", "image/bmp")]


def sniff(path):
    head = path.read_bytes()[:64]
    for sig, mime in MAGIC:
        if head.startswith(sig):
            return mime
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    if head[4:12] in (b"ftypavif", b"ftypavis"):
        return "image/avif"
    if head.lstrip().startswith((b"<svg", b"<?xml")):
        return "image/svg+xml"
    return None


def needs_type(item):
    """Assets whose URL has no file extension (their local name depends on the detected type)."""
    path = urllib.parse.urlsplit(item["source_url"]).path
    return item.get("kind") in ("image", "poster") and not pathlib.PurePosixPath(path).suffix
UA = "Mozilla/5.0 (compatible; wp-docs-migration/0.1; +nick.diego@a8c.com)"

def fetch(item, types):
    dest = ROOT / item["local_path"]
    placeholder = dest.with_suffix(".img")
    if not (dest.exists() and dest.stat().st_size > 0) and dest != placeholder and placeholder.exists() \
            and placeholder.stat().st_size > 0:
        placeholder.rename(dest)  # downloaded earlier under the ".img" name; the converter now knows the type
        return {"url": item["source_url"], "path": item["local_path"], "status": "renamed",
                "from": str(placeholder.relative_to(ROOT))}
    if dest.exists() and dest.stat().st_size > 0:
        if needs_type(item) and item["source_url"] not in types:
            mime = sniff(dest)
            if mime:
                types[item["source_url"]] = {"mime": mime, "via": "magic bytes"}
        return {"url": item["source_url"], "path": item["local_path"], "status": "exists"}
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = item["source_url"]
    if not url.startswith(("http://", "https://")) or url.startswith(("http://source.mp4", "http://video-source.mp4")):
        return {"url": url, "path": item["local_path"], "status": "failed", "error": "not a real URL"}
    # Percent-encode non-ASCII characters in the path (e.g. "Profile-‹-Your-Website-—-WordPress.png").
    parts = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(parts.path, safe="/%")))
    headers = {"User-Agent": UA, "Referer": "https://wordpress.org/documentation/"}
    req = urllib.request.Request(url, headers=headers)
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                while chunk := r.read(1 << 16):
                    f.write(chunk)
            if needs_type(item):
                mime = sniff(dest) or (ctype if ctype.startswith("image/") else None)
                if mime:
                    types[item["source_url"]] = {"mime": mime, "via": "magic bytes" if sniff(dest) else "content-type"}
            return {"url": item["source_url"], "path": item["local_path"], "status": "ok", "bytes": dest.stat().st_size}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (403, 404, 410):
                break
        except Exception as e:  # noqa
            last = str(e)
        time.sleep(2 ** attempt)
    if dest.exists():
        dest.unlink()
    return {"url": item["source_url"], "path": item["local_path"], "status": "failed", "error": last}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--kinds", default="image,poster,video")
    a = ap.parse_args()
    kinds = set(a.kinds.split(","))
    items = [i for i in json.loads(MANIFEST.read_text()) if i.get("kind") in kinds]
    print(f"{len(items)} assets to fetch", file=sys.stderr)
    types = json.loads(TYPES.read_text()) if TYPES.exists() else {}
    results = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(fetch, i, types) for i in items]
        for n, fut in enumerate(as_completed(futs), 1):
            r = fut.result(); results.append(r)
            if n % 100 == 0 or r["status"] == "failed":
                print(f"[{n}/{len(items)}] {r['status']} {r['url'] if r['status']=='failed' else ''}", file=sys.stderr)
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(results, indent=1))
    TYPES.write_text(json.dumps(dict(sorted(types.items())), indent=1) + "\n")
    # placeholder ".img" files that no manifest entry points at any more
    wanted = {(ROOT / i["local_path"]).resolve() for i in json.loads(MANIFEST.read_text())}
    orphans = [p for p in ASSETS.rglob("*.img") if p.resolve() not in wanted]
    for p in orphans:
        p.unlink()
    pending = sum(1 for i in items if needs_type(i) and i["source_url"] in types
                  and i["local_path"].endswith(".img"))
    print(f"external types cached: {len(types)}; orphaned .img removed: {len(orphans)}"
          + (f"; {pending} entries still named .img although their type is known: re-run convert.py, "
             "then this script" if pending else ""), file=sys.stderr)
    from collections import Counter
    c = Counter(r["status"] for r in results)
    total = sum(r.get("bytes", 0) for r in results)
    print(f"done: {dict(c)}; downloaded {total/1e6:.1f} MB; report at {REPORT}", file=sys.stderr)
