"""Write title/frontmatter edge-case fixtures next to kitchen-sink.md and add all fixtures to
the served manifest under a `spike-fixtures` parent.

Usage: python3 -I make_fixtures.py <fixtures-dir> <served-dir>
"""
import json
import pathlib
import shutil
import sys

fx = pathlib.Path(sys.argv[1])
served = pathlib.Path(sys.argv[2])

files = {
    "no-frontmatter.md": "# Title from H1 without frontmatter\n\nBody paragraph.\n",
    "no-h1.md": "---\ntitle: x\n---\n\nNo H1 here, body starts with a paragraph.\n\n## An H2\n\nText.\n",
    "h1-not-first.md": "---\ntitle: x\n---\n\nIntro paragraph before the H1.\n\n# Late H1\n\nText.\n",
    "hash-no-space.md": "---\ntitle: x\n---\n\n#Title without space\n\nText.\n",
    "fm-dashes.md": "---\ntitle: x\nnote: \"a value with --- inside it\"\n---\n\n# Title after tricky frontmatter\n\nText.\n",
    "bom.md": "﻿---\ntitle: x\n---\n\n# Title in BOM file\n\nText.\n",
    "crlf.md": "---\r\ntitle: x\r\n---\r\n\r\n# Title in CRLF file\r\n\r\nPara one\r\nwraps here.\r\n\r\n- a\r\n- b\r\n",
    "sibling-page.md": "---\ntitle: x\n---\n\n# Sibling page\n\n## Section\n\nText.\n",
    "README.md": "---\ntitle: x\nsection: true\n---\n\n# Spike fixtures\n\nIndex page for fixtures.\n",
    "setext.md": "---\ntitle: x\n---\n\nSetext title\n============\n\nText.\n",
    "h1-with-html.md": "---\ntitle: x\n---\n\n# Title with <em>html</em> &amp; entity\n\nText.\n",
    "block-only.md": "---\ntitle: x\n---\n\n# Block-markup page\n\nA normal markdown paragraph.\n\nAnother markdown paragraph\nwith a soft wrap.\n\n<!-- wp:paragraph -->\n<p>Block paragraph.</p>\n<!-- /wp:paragraph -->\n",
}
for name, content in files.items():
    (fx / name).write_bytes(content.encode("utf-8"))

dest = served / "spike-fixtures"
if dest.exists():
    shutil.rmtree(dest)
shutil.copytree(fx, dest)

mpath = served / "manifest.json"
m = json.loads(mpath.read_text())
m = {k: v for k, v in m.items() if not k.startswith("spike-fixtures")}
m["spike-fixtures"] = {
    "title": "Manifest title: Spike fixtures", "slug": "spike-fixtures",
    "markdown_source": "spike-fixtures/README.md", "parent": None, "order": 99,
}
for i, f in enumerate(sorted(p.name for p in fx.glob("*.md") if p.name != "README.md"), 1):
    slug = f[:-3]
    m["spike-fixtures/" + slug] = {
        "title": "Manifest title: " + slug, "slug": slug,
        "markdown_source": "spike-fixtures/" + f, "parent": "spike-fixtures", "order": i,
    }
mpath.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
print(len(m), "manifest entries")
