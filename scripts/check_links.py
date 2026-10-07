#!/usr/bin/env python3
"""Check docs/ output: every relative link/image resolves to a file in docs/ or to an asset listed in
docs/assets/images-manifest.json; every #fragment exists in the target, using the ids the live
wporg/table-of-contents would generate after import (sanitize_title of heading text, -2/-3 de-dupe)
plus explicit <a id> anchors. Also validates importer constraints (H1 first, frontmatter safe for
the importer's  #^---(.+)---#Us  regex, no extra H1s) and docs/manifest.json consistency.
Usage: .venv/bin/python -I scripts/check_links.py"""
import collections, importlib.util, json, os, pathlib, re
from urllib.parse import unquote as urllib_unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("convert", ROOT / "scripts" / "convert.py")
conv = importlib.util.module_from_spec(spec); spec.loader.exec_module(conv)
DOCS = ROOT / "docs"
assets = {e["local_path"] for e in json.loads((DOCS / "assets/images-manifest.json").read_text())}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|(?:href|src|poster)=\"([^\"]+)\"")


def body_of(path):
    txt = path.read_text()
    m = re.match(r"^---(.+?)---", txt, flags=re.S)  # same as the importer (ungreedy)
    return txt[m.end():].strip() if m else txt.strip()


def anchors(path, cache={}):
    if path not in cache:
        body = re.sub(r"```.*?```", "", body_of(path), flags=re.S)
        ids = set(re.findall(r'<a id="([^"]+)"', body))
        used = set()
        for h in re.findall(r"(?m)^#{1,6} (.+)$", body)[1:]:  # skip the H1 title (not part of post content)
            h = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", h)
            h = h.replace("\\", "")
            h = re.sub(r"[`*]", "", h)
            ids.add(conv.unique_id(conv.sanitize_title(h), used))
        cache[path] = ids
    return cache[path]


problems = collections.defaultdict(list)
ok = 0
for md in sorted(DOCS.glob("**/*.md")):
    rel_md = md.relative_to(ROOT).as_posix()
    txt = md.read_text()
    fm = re.match(r"^---(.+?)---", txt, flags=re.S)
    if fm and not re.match(r"^---\n.*\n---\n", txt[:fm.end() + 1], flags=re.S):
        problems["frontmatter cut short by importer regex"].append(rel_md)
    body = body_of(md)
    if not re.match(r"^#\s(.+)", body):
        problems["body does not start with '# Title'"].append(rel_md)
    nobody = re.sub(r"```.*?```", "", body, flags=re.S)
    nobody = re.sub(r"(`+)[^`].*?\1", "", nobody)
    if len(re.findall(r"(?m)^# ", nobody)) > 1:
        problems["more than one H1"].append(rel_md)
    if "<iframe" in nobody:
        problems["iframe (stripped by kses)"].append(rel_md)
    for m in LINK.finditer(nobody):
        url = next(g for g in m.groups() if g).strip("<>")
        if re.match(r"^[a-z]+:|^//", url):
            continue
        path, _, frag = url.partition("#")
        target = (md.parent / urllib_unquote(path)).resolve() if path else md
        if path and not target.exists():
            if os.path.relpath(target, ROOT) in assets:
                ok += 1
                continue
            problems["broken relative link"].append(f"{rel_md} -> {url}")
            continue
        ok += 1
        if frag and target.suffix == ".md" and frag not in anchors(target):
            problems["fragment not found in target"].append(f"{rel_md} -> {url}")

# importer manifest: every source exists, parents exist, slugs are sanitized and match the key
manifest = json.loads((DOCS / "manifest.json").read_text())
for key, doc in manifest.items():
    if not (DOCS / doc["markdown_source"]).exists():
        problems["manifest source missing"].append(key)
    if doc["parent"] and doc["parent"] not in manifest:
        problems["manifest parent missing"].append(key)
    if key.rsplit("/", 1)[-1] != doc["slug"] or conv.sanitize_title(doc["slug"]) != doc["slug"]:
        problems["manifest slug mismatch / unsanitized"].append(key)
slugs = collections.Counter(d["slug"] for d in manifest.values())
for s, n in slugs.items():
    if n > 1:
        problems["duplicate slug in manifest (importer slug_only fallback can mis-match)"].append(s)
md_files = {p.relative_to(DOCS).as_posix() for p in DOCS.glob("**/*.md")}
listed = {d["markdown_source"] for d in manifest.values()}
for f in sorted(md_files - listed - {"README.md"}):
    problems["file not in manifest"].append(f)

report = {k: v for k, v in problems.items()}
(ROOT / "data/link-check.json").write_text(json.dumps(report, indent=1))
print(f"relative links/images ok: {ok}")
for k, v in problems.items():
    print(f"{len(v):5d}  {k}")
    for x in v[:5]:
        print("         ", x)
