"""Run-4 mutations on the served copy.

Usage: python3 -I mutate_run4.py <served-dir>
"""
import json
import pathlib
import sys

s = pathlib.Path(sys.argv[1])
mp = s / "manifest.json"
m = json.loads(mp.read_text())

# L. Delete the Markdown file of the entry removed from the manifest in run 3 (orphan post).
(s / "overview/where-to-start/wordpress-semantics.md").unlink()
# M. Change the body of the no-H1 file: does the (run-3) manifest title now apply?
p = s / "spike-fixtures/no-h1.md"
p.write_text(p.read_text() + "\nBody edited in run 4.\n")
# N. Duplicate slug in a different section: does it hijack the existing post with that slug?
(s / "spike-fixtures" / "dup-glossary.md").write_text("# Duplicate-slug page\n\nI share a slug with the glossary.\n")
m["spike-fixtures/wordpress-glossary"] = {"title": "Dup", "slug": "wordpress-glossary", "markdown_source": "spike-fixtures/dup-glossary.md", "parent": "spike-fixtures", "order": 60}
# O. Another child-before-parent pair, to observe post_parent right after the manifest stage.
(s / "spike-fixtures" / "c2.md").write_text("# C2\n\nchild\n")
(s / "spike-fixtures" / "p2.md").write_text("# P2\n\nparent\n")
m["spike-fixtures/p2/c2"] = {"title": "C2", "slug": "c2", "markdown_source": "spike-fixtures/c2.md", "parent": "spike-fixtures/p2", "order": 1}
m["spike-fixtures/p2"] = {"title": "P2", "slug": "p2", "markdown_source": "spike-fixtures/p2.md", "parent": "spike-fixtures", "order": 70}
# P. Slug that is not already sanitized (uppercase) -> create_post_from_manifest_doc refuses it.
(s / "spike-fixtures" / "Bad_Slug.md").write_text("# Bad slug\n\nx\n")
m["spike-fixtures/Bad_Slug"] = {"title": "Bad", "slug": "Bad_Slug", "markdown_source": "spike-fixtures/Bad_Slug.md", "parent": "spike-fixtures", "order": 80}

mp.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
print("manifest entries:", len(m))
