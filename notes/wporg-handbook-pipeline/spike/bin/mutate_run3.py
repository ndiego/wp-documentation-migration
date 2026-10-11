"""Run-3 mutations on the served copy (never the project). Each one isolates a single behaviour.

Usage: python3 -I mutate_run3.py <served-dir>
"""
import json
import pathlib
import sys

s = pathlib.Path(sys.argv[1])
mp = s / "manifest.json"
m = json.loads(mp.read_text())

def edit(rel, old, new):
    p = s / rel
    t = p.read_text(encoding="utf-8")
    assert old in t, (rel, old)
    p.write_text(t.replace(old, new, 1), encoding="utf-8")

# A. Body edit only.
edit("overview/where-to-start/wordpress-glossary.md", "\n## ", "\nSPIKE: a paragraph added in run 3.\n\n## ")
# B. Title change via the H1 in the file.
edit("overview/where-to-start/where-to-find-wordpress-help.md", "# Where to find WordPress help", "# Where to find WordPress help (H1 changed)")
# C. Title change via manifest only (file unchanged, file has an H1).
m["overview/where-to-start/introduction-to-blogging"]["title"] = "Introduction to Blogging (manifest title changed)"
# D. Title change via manifest only, file has NO H1 and is unchanged.
m["spike-fixtures/no-h1"]["title"] = "Manifest title: no-h1 CHANGED"
# E. Remove an entry from the manifest.
del m["overview/where-to-start/wordpress-semantics"]
# F. Slug change (same file, new key + slug).
e = m.pop("overview/about-wordpress/supported-versions")
e["slug"] = "supported-wordpress-versions"
m["overview/about-wordpress/supported-wordpress-versions"] = e
# G. Move: same slug, new parent (key changes).
e = m.pop("overview/faq/faq-troubleshooting")
e["parent"] = "overview/where-to-start"
m["overview/where-to-start/faq-troubleshooting"] = e
# H. Order change only, and order -> 0.
m["overview/where-to-start/get-started-with-wordpress"]["order"] = 42
m["overview/where-to-start/first-steps-with-wordpress-block-editor"]["order"] = 0
# I. markdown_source change only (point a page at a different file).
m["spike-fixtures/sibling-page"]["markdown_source"] = "spike-fixtures/no-frontmatter.md"
# J. Add an `index` entry (handbook landing-page convention).
m["index"] = {"title": "Documentation", "slug": "index", "markdown_source": "README.md", "parent": None, "order": 0}
# K. Brand-new page whose parent is ALSO new and listed AFTER it (tests recursive parent creation).
(s / "spike-fixtures" / "new-child.md").write_text("# New child\n\nChild created before its parent.\n")
(s / "spike-fixtures" / "new-parent.md").write_text("# New parent\n\nParent listed after child.\n")
m["spike-fixtures/new-parent/new-child"] = {"title": "New child", "slug": "new-child", "markdown_source": "spike-fixtures/new-child.md", "parent": "spike-fixtures/new-parent", "order": 1}
m["spike-fixtures/new-parent"] = {"title": "New parent", "slug": "new-parent", "markdown_source": "spike-fixtures/new-parent.md", "parent": "spike-fixtures", "order": 50}

mp.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
print("manifest entries:", len(m))
