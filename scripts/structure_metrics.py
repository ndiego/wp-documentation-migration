#!/usr/bin/env python3
"""Before/after metrics for a restructure (category layout vs. data/structure.yaml layout).

Imported by scripts/convert.py when --structure is given; it writes data/structure-metrics.json.
Inputs are plain dicts (convert.layout_summary()) plus the converted Markdown bodies, so this module has
no dependency on the converter internals:

  before / after   {"kind", "top": [{key, title}], "folders": [{key, title, parent, depth, top, articles,
                    index_slug, hand_written}], "articles": {slug: {title, folder, top, depth, path}}}
  bodies_before    {slug: Markdown body as the category layout has it (nav-link paragraphs kept)}
  bodies_after     {slug: Markdown body as written in the structure layout (nav links removed if configured)}
  link_paths       {slug: path (relative to the output root) the bodies were written for}; used to resolve
                   relative .md links back to slugs. Both body variants come from the same run, so they share it.

Definitions (also written into the JSON under "definitions"):
  depth                 number of folders above an article (docs/a/b/x.md -> 2; a section index README -> its folder depth)
  folders               sections, i.e. folders with a README.md (the repository root is not counted)
  articles_per_folder   direct articles per folder, index article excluded; every folder counted (also pure containers)
  ordering              share of folders with >= 2 articles whose order is not alphabetical by title
                        (case-insensitive); label "curated" when that share is >= 0.5, else "alphabetical"
  orphan_articles       articles with no inbound relative link from any other article
  manual_breadcrumb_paragraphs  articles whose first body paragraph is only a link
  folders_with_index_page       folders whose README is hand-written (structure title+intro or an index article).
                        Category READMEs generated from the category name/description count as 0.
  articles_moved        articles whose folder path changed
  misfiled_fixed        articles whose after top-level section differs from the before top-level category that
                        supplies most of that after section's articles (its "successor"). A plain "top-level
                        slug changed" count would be meaningless when the top level is renamed.
  boilerplate_sentence_share  per top-level section: share of sentences with >= 6 words that appear verbatim
                        in >= 3 different articles (counted over all articles of the same tree)
"""
import collections
import posixpath
import re
import statistics
import urllib.parse

MIN_WORDS = 6
MIN_ARTICLES = 3
LINK_RE = re.compile(r"\]\(([^)\s]+)\)|href=\"([^\"]+)\"")


# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------
def first_paragraph_is_nav_link(body):
    for block in re.split(r"\n\s*\n", body.strip()):
        b = block.strip()
        if not b or re.fullmatch(r'<a id="[^"]*"></a>', b) or b.startswith("<!--"):
            continue
        return bool(re.fullmatch(r"\[[^\]]+\]\([^)\s]+\)", b))
    return False


def link_targets(bodies, link_paths):
    """{slug: set(target slugs)} from relative .md links (README.md of an index section -> its article)."""
    by_path = {p: s for s, p in link_paths.items()}
    out = {}
    for slug, body in bodies.items():
        here = posixpath.dirname(link_paths[slug])
        text = re.sub(r"```.*?```", "", body, flags=re.S)
        targets = set()
        for m in LINK_RE.finditer(text):
            url = (m.group(1) or m.group(2)).strip("<>")
            if re.match(r"^[a-z][a-z0-9+.-]*:|^//|^#", url, re.I):
                continue
            path = urllib.parse.unquote(url.split("#", 1)[0])
            if not path.endswith(".md"):
                continue
            t = by_path.get(posixpath.normpath(posixpath.join(here, path)))
            if t and t != slug:
                targets.add(t)
        out[slug] = targets
    return out


def plain_text(md):
    t = re.sub(r"```.*?```", " ", md, flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"(?m)^\s*(#{1,6}|>\s*\[![A-Z]+\]|>|[-*+]|\d+\.)\s+", "", t)
    t = re.sub(r"[*`|]|\\(?=\S)", "", t)
    return t


def sentences(md):
    out = []
    for block in re.split(r"\n", plain_text(md)):
        for s in re.split(r"(?<=[.!?])\s+", block):
            s = " ".join(s.split())
            if len(s.split()) >= MIN_WORDS:
                out.append(s)
    return out


# ---------------------------------------------------------------------------
# Per-tree metrics
# ---------------------------------------------------------------------------
def is_alphabetical(titles):
    keys = [t.lower() for t in titles]
    return keys == sorted(keys)


def tree_metrics(tree, bodies, inbound):
    arts = tree["articles"]
    folders = tree["folders"]
    title = {s: a["title"] for s, a in arts.items()}
    depths = [a["depth"] for a in arts.values()]
    per_folder = [len(f["articles"]) for f in folders]
    ordered = [f for f in folders if len(f["articles"]) >= 2]
    non_alpha = [f["key"] for f in ordered if not is_alphabetical([title[s] for s in f["articles"]])]
    share = len(non_alpha) / len(ordered) if ordered else 0.0
    # boilerplate sentences, frequency over this tree's bodies
    sent_by_art = {s: set(sentences(b)) for s, b in bodies.items()}
    freq = collections.Counter(x for ss in sent_by_art.values() for x in ss)
    boiler = {}
    for top in tree["top"]:
        members = [s for s, a in arts.items() if a["top"] == top["key"]]
        total = sum(len(sentences(bodies[s])) for s in members if s in bodies)
        hits = sum(1 for s in members if s in bodies for x in sentences(bodies[s]) if freq[x] >= MIN_ARTICLES)
        boiler[top["key"]] = {"title": top["title"], "articles": len(members), "sentences": total,
                              "boilerplate_sentences": hits, "share": round(hits / total, 4) if total else 0.0}
    return {
        "articles": len(arts),
        "folders": len(folders),
        "max_depth": max(depths) if depths else 0,
        "mean_depth": round(statistics.mean(depths), 3) if depths else 0,
        "folders_with_index_page": sum(1 for f in folders if f["hand_written"]),
        "articles_per_folder": {"min": min(per_folder), "median": statistics.median(per_folder), "max": max(per_folder)}
        if per_folder else {"min": 0, "median": 0, "max": 0},
        "ordering": {"label": "curated" if share >= 0.5 else "alphabetical", "non_alphabetical_share": round(share, 4),
                     "folders_considered": len(ordered), "non_alphabetical_folders": non_alpha},
        "orphan_articles": sum(1 for s in arts if not inbound.get(s)),
        "manual_breadcrumb_paragraphs": sum(1 for s in arts if s in bodies and first_paragraph_is_nav_link(bodies[s])),
        "sections_using_article_as_index": sum(1 for f in folders if f["index_slug"]),
        "boilerplate_sentence_share": boiler,
    }


def compute(before, after, bodies_before, bodies_after, link_paths, structure_file=None):
    def inbound(bodies):
        inc = collections.defaultdict(set)
        for src, targets in link_targets(bodies, link_paths).items():
            for t in targets:
                inc[t].add(src)
        return inc

    b = tree_metrics(before, bodies_before, inbound(bodies_before))
    a = tree_metrics(after, bodies_after, inbound(bodies_after))
    b["folders_with_index_page_note"] = ("0 by definition: the category README.md files are generated from the category "
                                         "name/description and the live landing pages are theme-generated")
    ba, aa = before["articles"], after["articles"]
    a["articles_moved"] = sum(1 for s in aa if s in ba and aa[s]["folder"] != ba[s]["folder"])
    # renames alone move every file; this counts only articles whose containing folder title changed
    ftitle = lambda tree: {f["key"]: f["title"].lower() for f in tree["folders"]}
    bt, at = ftitle(before), ftitle(after)
    a["articles_moved_by_folder_title"] = sum(1 for s in aa if s in ba and at[aa[s]["folder"]] != bt[ba[s]["folder"]])
    # successor mapping: each after top-level section -> the before top-level category most of its articles came from
    successor = {}
    for top in after["top"]:
        c = collections.Counter(ba[s]["top"] for s, x in aa.items() if x["top"] == top["key"] and s in ba)
        successor[top["key"]] = c.most_common(1)[0][0] if c else None
    a["misfiled_fixed"] = sum(1 for s, x in aa.items() if s in ba and ba[s]["top"] != successor.get(x["top"]))
    a["top_level_successor"] = successor
    return {
        "structure_file": structure_file,
        "definitions": {k: v for k, v in DEFINITIONS.items()},
        "before": b,
        "after": a,
    }


DEFINITIONS = {
    "depth": "folders above the article (docs/a/b/x.md = 2); a section index README counts as its folder's depth",
    "folders": "sections (folders with a README.md); the repository root is not counted",
    "articles_per_folder": "direct articles per folder, index article excluded, all folders counted",
    "ordering": "share of folders with >= 2 articles not in case-insensitive alphabetical title order; 'curated' if >= 0.5",
    "orphan_articles": "articles with no inbound relative link from another article (computed from the converted Markdown)",
    "manual_breadcrumb_paragraphs": "articles whose first body paragraph is only a link (e.g. 'Go back to the list of Blocks')",
    "folders_with_index_page": "folders with a hand-written README (structure title+intro, or an index article); generated category READMEs = 0",
    "articles_moved": "articles whose folder path changed (renaming a top-level folder moves everything below it)",
    "articles_moved_by_folder_title": "articles whose containing folder's title (case-insensitive) changed",
    "misfiled_fixed": "articles whose after top-level section is not the successor of their before top-level category "
                      "(successor = the before top-level category supplying most of that after section's articles)",
    "boilerplate_sentence_share": f"per top-level section: share of sentences with >= {MIN_WORDS} words appearing verbatim "
                                  f"in >= {MIN_ARTICLES} articles of the same tree",
}


def print_summary(m):
    keys = ["articles", "folders", "max_depth", "mean_depth", "folders_with_index_page", "orphan_articles",
            "manual_breadcrumb_paragraphs", "sections_using_article_as_index"]
    print(f"{'metric':32s} {'before':>10s} {'after':>10s}")
    for k in keys:
        print(f"{k:32s} {m['before'][k]!s:>10s} {m['after'][k]!s:>10s}")
    for k in ("ordering",):
        print(f"{k:32s} {m['before'][k]['label']:>10s} {m['after'][k]['label']:>10s}")
    apf = lambda d: f"{d['min']}/{d['median']}/{d['max']}"
    print(f"{'articles_per_folder min/med/max':32s} {apf(m['before']['articles_per_folder']):>10s} "
          f"{apf(m['after']['articles_per_folder']):>10s}")
    print(f"{'articles_moved':32s} {'':>10s} {m['after']['articles_moved']!s:>10s}")
    print(f"{'articles_moved_by_folder_title':32s} {'':>10s} {m['after']['articles_moved_by_folder_title']!s:>10s}")
    print(f"{'misfiled_fixed':32s} {'':>10s} {m['after']['misfiled_fixed']!s:>10s}")
