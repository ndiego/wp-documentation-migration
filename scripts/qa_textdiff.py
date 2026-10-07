#!/usr/bin/env python3
"""Text-fidelity check: compare visible words of the WordPress HTML against the words of the
Markdown output rendered back to HTML (markdown-it, GFM-like). Prints the lowest scoring
articles and writes data/qa-textdiff.json.

Usage: .venv/bin/python -I scripts/qa_textdiff.py [--rendered DIR] [SLUG ...]   (with slugs: show diffs)
  --rendered DIR  compare against HTML produced by the real Jetpack WPCom_GHF_Markdown_Parser
                  (DIR mirrors docs/ with .html files, see notes/converter-notes.md) instead of markdown-it
"""
import difflib, json, pathlib, re, sys
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).resolve().parent.parent
md = MarkdownIt("gfm-like", {"linkify": False})
RENDERED = None
if len(sys.argv) > 2 and sys.argv[1] == "--rendered":
    RENDERED = pathlib.Path(sys.argv[2])
    del sys.argv[1:3]
arts = {a["slug"]: a for a in json.loads((ROOT / "raw/articles.json").read_text())}
report = json.loads((ROOT / "data/convert-report.json").read_text())["articles"]


def words_html(h):
    s = BeautifulSoup(h, "html.parser")
    for t in s.find_all(["script", "style", "button", "svg"]):
        t.decompose()
    return re.findall(r"[\w'’]+", s.get_text(" "))


def rendered_html(path):
    rel = path.relative_to(ROOT / "docs").with_suffix(".html")
    h = (RENDERED / rel).read_text()
    h = re.sub(r"^<!-- TITLE: .*? -->\n", "", h)
    return re.sub(r"<!-- [^>]*? -->\s*<p>https?://\S+</p>", "", h)


def words_md(path):
    if RENDERED:
        return words_html(rendered_html(path))
    text = path.read_text().split("\n---\n", 1)[1]
    text = re.sub(r"^> \[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]$", "", text, flags=re.M)
    text = re.sub(r"^\s*# .*\n", "", text, count=1)  # H1 title (not part of WP content)
    text = re.sub(r"<!-- [^>]*? -->\n\nhttps?://\S+", "", text)  # video/embed placeholders
    text = re.sub(r"\[Video: ([^\]]*)\]\([^)]*\)( \(VideoPress\))?", r"\1", text)
    return words_html(md.render(text))


def struct(h):
    s = BeautifulSoup(h, "html.parser")
    for t in s.select("figure.wp-block-video, figure.wp-block-embed, figure.wp-block-jetpack-videopress, video, iframe, script"):
        t.decompose()
    return {
        "headings": len(s.find_all(re.compile(r"^h[2-6]$"))),
        "list_items": len(s.find_all("li")),
        "images": len(s.find_all("img")),
        "links": len([a for a in s.find_all("a", href=True) if a.get_text(strip=True) and not a.find("img")]),
        "code_blocks": len(s.find_all("pre")),
        "table_rows": len(s.find_all("tr")),
    }


def md_html(path):
    if RENDERED:
        return rendered_html(path)
    text = path.read_text().split("\n---\n", 1)[1]
    text = re.sub(r"^\s*# .*\n", "", text, count=1)
    text = re.sub(r"<!-- [^>]*? -->\n\nhttps?://\S+", "", text)
    return md.render(text)


struct_mismatch = {}
results = {}
targets = sys.argv[1:] or list(arts)
for slug in targets:
    a, b = words_html(arts[slug]["content"]["rendered"]), words_md(ROOT / report[slug]["path"])
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    results[slug] = round(sm.ratio(), 4)
    sh, sm2 = struct(arts[slug]["content"]["rendered"]), struct(md_html(ROOT / report[slug]["path"]))
    diff = {k: (sh[k], sm2[k]) for k in sh if sh[k] != sm2[k]}
    if diff:
        struct_mismatch[slug] = diff
        if sys.argv[1:]:
            print(f"  structure (html, md): {diff}")
    if sys.argv[1:]:
        print(f"== {slug}: ratio {sm.ratio():.4f}  html words {len(a)}  md words {len(b)}")
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != "equal":
                print(f"  {op:8s} html: {' '.join(a[i1:i2])[:150]!r}\n           md:   {' '.join(b[j1:j2])[:150]!r}")
if not sys.argv[1:]:
    vals = sorted(results.items(), key=lambda kv: kv[1])
    (ROOT / ("data/qa-textdiff-jetpack.json" if RENDERED else "data/qa-textdiff.json")).write_text(json.dumps(dict(vals), indent=1))
    import statistics
    print(f"articles: {len(vals)}  median ratio {statistics.median(results.values()):.4f}  "
          f">=0.99: {sum(v >= 0.99 for v in results.values())}  <0.95: {sum(v < 0.95 for v in results.values())}")
    for s, v in vals[:15]:
        print(f"  {v:.4f}  {s}")
    import collections
    kinds = collections.Counter(k for d in struct_mismatch.values() for k in d)
    print(f"structural mismatches (html vs md-rendered counts): {len(struct_mismatch)} articles; by kind: {dict(kinds)}")
    for s, d in list(struct_mismatch.items())[:40]:
        print(f"  {s}: {d}")
    (ROOT / ("data/qa-structure-jetpack.json" if RENDERED else "data/qa-structure.json")).write_text(json.dumps(struct_mismatch, indent=1))
