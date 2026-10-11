"""Corpus-wide audit of stored post_content vs source Markdown.

Usage: python3 -I audit.py <served-dir> <manifest.json> <dump-with-content.jsonl>
"""
import json
import os
import re
import sys
from collections import Counter

served, mpath, dpath = sys.argv[1:4]
manifest = json.load(open(mpath))
rows = {r["permalink"].replace("http://localhost:8881/documentation/", "").rstrip("/"): r
        for r in map(json.loads, open(dpath))}

checks = {
    "href to *.md (dangling relative)": r'href="(?!https?:)[^"]*\.md(#[^"]*)?"',
    "href to README.md": r'href="[^"]*README\.md',
    "href relative ../": r'href="\.\./',
    "img src relative": r'<img[^>]+src="(?!https?:)',
    "img src ../assets": r'<img[^>]+src="(\.\./)+assets/',
    "<video": r"<video",
    "<video> without src attr": r"<video(?![^>]*\ssrc=)[^>]*>",
    "<iframe": r"<iframe",
    "<details": r"<details",
    "<script (tag kept)": r"<script",
    "[!NOTE]/[!TIP]... literal": r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]",
    "<blockquote": r"<blockquote",
    "HTML comment kept": r"<!--",
    "stray </p> (parser quirk)": r"</p>",
    "<p> tags (strip_paras off?)": r"<p>",
    "heading with id=": r"<h[1-6][^>]* id=",
    "<a id= / name= anchors": r'<a (id|name)=',
    "<kbd": r"<kbd",
    "<table": r"<table",
    "<pre><code": r"<pre><code",
    "lang class on code": r'<code class="language-',
    "bare URL alone on a line (oEmbed candidate)": r"(?m)^https?://\S+$",
    "<h1 in body": r"<h1",
    "shortcode-looking [word ...]": r"(?m)^\[[a-z_]+[ \]]",
    "unconverted markdown link [x](y)": r"\]\((?!#)[^)\s]+\)",
    "literal ** left over": r"\*\*",
}
counts = Counter()
pages = {k: [] for k in checks}
for key, r in rows.items():
    html = r.get("post_content", "")
    for name, rx in checks.items():
        n = len(re.findall(rx, html))
        if n:
            counts[name] += n
            pages[name].append(key)
for name in checks:
    print(f"{name:48s} {counts[name]:6d} occurrences in {len(pages[name]):4d} pages  e.g. {pages[name][:2]}")

# Source-vs-stored element counts for a few tags that kses may remove.
lost = Counter()
for key, e in manifest.items():
    src = open(os.path.join(served, e["markdown_source"]), encoding="utf-8").read()
    html = rows.get(key, {}).get("post_content", "")
    for tag in ["video", "iframe", "script", "details", "img", "kbd", "source", "audio", "div", "span"]:
        a = len(re.findall(rf"<{tag}\b", src))
        b = len(re.findall(rf"<{tag}\b", html))
        if a != b:
            lost[(tag, "source", a, "stored", b, key)] += 1
for k in sorted(lost):
    print("tag count change:", k[0], "src", k[2], "stored", k[4], k[5])
