#!/usr/bin/env python3
"""Consolidate the per-area content reviews into one proposal.

Inputs:  data/content-proposal/*.json + *.md (one pair per review area), overrides.json, 00-preamble.md,
         data/core-linked-slugs.json
Outputs: data/content-proposal.json (all rows, overrides applied, core_linked flag),
         data/content-proposal-summary.json, data/content-proposal.md (preamble + areas, headings demoted)
Usage:   python3 -I scripts/build_content_proposal.py
"""
import json, re, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data" / "content-proposal"
AREAS = ["overview-and-using-wordpress", "editing-and-design", "classic-and-policies"]
core = json.load(open(ROOT / "data" / "core-linked-slugs.json"))["slugs"]
over = json.load(open(D / "overrides.json")); over.pop("_comment", None)

rows = []
for a in AREAS:
    for r in json.load(open(D / f"{a}.json")):
        r["area"] = a; rows.append(r)
# overrides
applied = []
kept = []
for r in rows:
    o = over.get(r["slug"])
    if o and o.get("drop"):
        applied.append((r["slug"], r["action"], "DROPPED", o["why"])); continue
    if o:
        applied.append((r["slug"], r["action"], o["action"], o["why"]))
        r["original_action"] = r["action"]; r["action"] = o["action"]; r["target"] = o["target"]; r["why"] = o["why"]
    r["core_linked"] = r["slug"] in core
    kept.append(r)
rows = kept
VALID = {"KEEP", "REWRITE", "MERGE", "SPLIT", "DELETE", "MOVE", "NEW"}
bad = [r for r in rows if r["action"] not in VALID]; assert not bad, bad
arts = {a["slug"] for a in json.load(open(ROOT / "raw" / "articles.json"))}
existing = [r for r in rows if r["action"] != "NEW"]
assert {r["slug"] for r in existing} >= arts, sorted(arts - {r["slug"] for r in existing})
assert len({r["slug"] for r in existing}) == len(existing), "duplicate slugs"

counts = collections.Counter(r["action"] for r in rows)
# pages after: KEEP + REWRITE + NEW + split results + merge targets that are not already a kept/rewritten/new page title
titles = {str(r["title"]).strip().lower() for r in rows if r["action"] in ("KEEP", "REWRITE", "NEW")}
targets = {str(r["target"]).split("(")[0].strip().lower() for r in rows if r["action"] == "MERGE" and r.get("target")}
extra_targets = sorted(t for t in targets if t and t not in titles and t not in arts)
splits = sum(len([x for x in str(r.get("target") or "").split(";") if x.strip()]) for r in rows if r["action"] == "SPLIT")
pages_after_from_rows = counts["KEEP"] + counts["REWRITE"] + counts["NEW"] + splits + len(extra_targets)
areas = json.load(open(D / "area-summaries.json")); areas.pop("_comment", None)
assert sum(a["now"] for a in areas.values()) == len(existing), (sum(a["now"] for a in areas.values()), len(existing))
pages_after = sum(a["proposed"] for a in areas.values())
core_non_keep = [(r["slug"], r["action"]) for r in rows if r.get("core_linked") and r["action"] not in ("KEEP", "REWRITE", "SPLIT")]
summary = {
    "pages_now": len(existing), "pages_after": pages_after, "counts": dict(counts),
    "core_linked_articles": sum(1 for s in core if s in arts),
    "core_linked_with_redirect": core_non_keep,
    "merge_targets_not_existing_pages": extra_targets, "overrides_applied": applied,
    "pages_after_definition": "sum of the per-area 'pages proposed' figures from each review's end-state list (data/content-proposal/area-summaries.json)",
    "pages_after_from_rows": pages_after_from_rows, "areas": areas,
}
(ROOT / "data" / "content-proposal.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
(ROOT / "data" / "content-proposal-summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))

def demote(md):
    md = re.sub(r"^# .*\n", "", md, count=1)           # drop the area H1 (we add our own H2)
    return re.sub(r"^(#{1,5}) ", lambda m: "#" * (len(m.group(1)) + 1) + " ", md, flags=re.M)
pre = (D / "00-preamble.md").read_text()
pre = pre.replace("{{pages_now}}", str(summary["pages_now"])).replace("{{pages_after}}", str(pages_after))
for k, v in counts.items(): pre = pre.replace("{{" + k + "}}", str(v))
pre = pre.replace("{{core_linked}}", str(summary["core_linked_articles"]))
ov = "\n".join(f"- `{s}`: {a} → {b}. {w}" for s, a, b, w in applied)
pre = pre.replace("{{overrides}}", ov)
parts = [pre]
H = {"overview-and-using-wordpress": "WordPress overview and Using WordPress", "editing-and-design": "Editing & design", "classic-and-policies": "Classic WordPress, and cross-cutting policies"}
for a in AREAS:
    parts.append(f"\n\n## {H[a]}\n\n" + demote((D / f"{a}.md").read_text()))
(ROOT / "data" / "content-proposal.md").write_text("\n".join(parts).rstrip() + "\n")
print(json.dumps({k: summary[k] for k in ("pages_now", "pages_after", "counts", "core_linked_articles")}, indent=1))
print("overrides:", len(applied), "| core-linked with redirect:", core_non_keep, "| merge targets that are new pages:", extra_targets)
