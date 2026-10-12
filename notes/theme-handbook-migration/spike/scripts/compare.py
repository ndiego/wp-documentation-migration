#!/usr/bin/env python3
"""Compare rendered production pages with the locally imported ones.

Inputs : <data>/pages.json, <data>/prod-html/<id>.html (fetch_prod.py --html)
         <data>/local-html/<id>.html  (same URL path on http://localhost:8888)
         <data>/local-status.tsv      id<TAB>http status<TAB>final url  (optional)
Output : <data>/fidelity.json  per-page diffs + totals; summary on stdout

Compared per page: HTTP status, title (h1), breadcrumbs, chapter list (order, links, labels),
previous/next links, headings (level, text, id), and inside the post content: images, code
blocks (+ languages), links (count and normalised targets), notices by kind, tables, embeds,
and a text similarity ratio.

Usage: .venv/bin/python -I compare.py <data-dir>
"""
import collections
import difflib
import json
import pathlib
import re
import sys

from bs4 import BeautifulSoup

PROD = "https://developer.wordpress.org"
LOCAL = "http://localhost:8888"


def norm_url(u):
    if not u:
        return u
    u = u.replace(LOCAL, PROD).replace("http://developer.wordpress.org", PROD)
    if u.startswith("/") and not u.startswith("//"):
        u = PROD + u
    u = re.sub(r"[?&]ssl=1$", "", u)
    if u.startswith(PROD) and "#" not in u and not re.search(r"\.[a-z0-9]{2,4}$", u):
        u = u.rstrip("/") + "/"
    return u


def text(el):
    return " ".join(el.get_text(" ", strip=True).split()) if el else ""


def extract(path):
    soup = BeautifulSoup(path.read_text(errors="replace"), "html.parser")
    d = {}
    h1 = soup.find("h1", class_="wp-block-post-title")
    d["title"] = text(h1)
    bc = soup.find(class_="wporg-site-breadcrumbs__wrapper")
    d["breadcrumbs"] = [text(a) for a in bc.find_all(["a", "span"]) if text(a)] if bc else []
    cl = soup.find("aside", class_="wp-block-wporg-chapter-list")
    d["chapters"] = [(norm_url(a.get("href")), text(a)) for a in cl.find_all("a")] if cl else []
    nav = {}
    for k in ("previous", "next"):
        el = soup.find(class_=f"post-navigation-link-{k}")
        a = el.find("a") if el else None
        nav[k] = (norm_url(a.get("href")), text(el.find(class_="post-navigation-link__title"))) if a else None
    d["nav"] = nav
    c = soup.find(class_="wp-block-post-content")
    if not c:
        d["missing_content"] = True
        return d
    d["headings"] = [(h.name, text(h), h.get("id")) for h in c.find_all(re.compile(r"^h[2-4]$"))]
    d["images"] = len(c.find_all("img"))
    pres = c.find_all("pre")
    d["code_blocks"] = len(pres)
    langs = []
    for p in pres:
        code = p.find("code")
        cls = " ".join((code.get("class") if code else None) or p.get("class") or [])
        m = re.search(r"language-([a-z0-9]+)", cls)
        langs.append(m.group(1) if m else "")
    d["code_langs"] = langs
    links = [a for a in c.find_all("a", href=True)
             if not (a.parent and re.match(r"^h[1-6]$", a.parent.name) and a["href"].startswith("#"))]
    d["links"] = sorted(norm_url(a["href"]) for a in links)
    notices = collections.Counter()
    for n in c.find_all(class_="wp-block-wporg-notice"):
        kind = next((x[3:-7] for x in n.get("class", []) if x.startswith("is-") and x.endswith("-notice")), "?")
        notices[kind] += 1
    for n in c.find_all(class_="callout"):
        kind = next((x[8:] for x in n.get("class", []) if x.startswith("callout-")), "?")
        notices[kind] += 1
    d["notices"] = dict(notices)
    d["tables"] = len(c.find_all("table"))
    d["embeds"] = len(c.find_all("iframe")) + len(c.find_all(class_="wp-embedded-content"))
    d["videos"] = len(c.find_all("video"))
    d["text"] = text(c)
    return d


def main():
    data = pathlib.Path(sys.argv[1])
    pages = json.loads((data / "pages.json").read_text())
    status = {}
    st = data / "local-status.tsv"
    if st.exists():
        for line in st.read_text().splitlines():
            i, code, final = (line.split("\t") + ["", ""])[:3]
            status[int(i)] = (code, final)
    out, totals = {}, collections.Counter()
    examples = collections.defaultdict(list)
    for p in pages:
        pid = p["id"]
        pr = extract(data / "prod-html" / f"{pid}.html")
        lo = extract(data / "local-html" / f"{pid}.html")
        diff = {}
        if pid in status and (status[pid][0] != "200" or norm_url(status[pid][1]) != norm_url(p["link"])):
            diff["url"] = status[pid]
        for k in ("title", "breadcrumbs", "chapters", "nav"):
            if pr.get(k) != lo.get(k):
                diff[k] = {"prod": pr.get(k), "local": lo.get(k)}
        if lo.get("missing_content") or pr.get("missing_content"):
            if lo.get("missing_content") != pr.get("missing_content"):
                diff["missing_content"] = {"prod": bool(pr.get("missing_content")), "local": bool(lo.get("missing_content"))}
        else:
            if pr["headings"] != lo["headings"]:
                ph, lh = pr["headings"], lo["headings"]
                diff["headings"] = {
                    "count": (len(ph), len(lh)),
                    "text_or_level": [(a, b) for a, b in zip(ph, lh) if a[:2] != b[:2]][:5],
                    "id_only": [(a[2], b[2]) for a, b in zip(ph, lh) if a[:2] == b[:2] and a[2] != b[2]][:5],
                }
            for k in ("images", "code_blocks", "tables", "embeds", "videos"):
                if pr[k] != lo[k]:
                    diff[k] = (pr[k], lo[k])
            if pr["code_langs"] != lo["code_langs"]:
                diff["code_langs"] = [(a, b) for a, b in zip(pr["code_langs"], lo["code_langs"]) if a != b][:5]
            if pr["notices"] != lo["notices"]:
                diff["notices"] = (pr["notices"], lo["notices"])
            if pr["links"] != lo["links"]:
                pc, lc = collections.Counter(pr["links"]), collections.Counter(lo["links"])
                diff["links"] = {"count": (len(pr["links"]), len(lo["links"])),
                                 "only_prod": sorted((pc - lc).elements())[:6],
                                 "only_local": sorted((lc - pc).elements())[:6]}
            ratio = difflib.SequenceMatcher(None, pr["text"], lo["text"], autojunk=False).ratio() \
                if len(pr["text"]) < 60000 else difflib.SequenceMatcher(None, pr["text"], lo["text"]).ratio()
            if ratio < 0.999:
                diff["text_ratio"] = round(ratio, 4)
            totals["prod_headings"] += len(pr["headings"])
            totals["local_headings"] += len(lo["headings"])
            for k in ("images", "code_blocks", "tables", "embeds", "videos"):
                totals[f"prod_{k}"] += pr[k]
                totals[f"local_{k}"] += lo[k]
            totals["prod_links"] += len(pr["links"])
            totals["local_links"] += len(lo["links"])
            totals["prod_notices"] += sum(pr["notices"].values())
            totals["local_notices"] += sum(lo["notices"].values())
        for k in diff:
            totals[f"pages_diff_{k}"] += 1
            if len(examples[k]) < 4:
                examples[k].append(p["link"].replace(PROD, ""))
        out[pid] = {"link": p["link"], "diff": diff}
    totals["pages"] = len(pages)
    totals["pages_identical"] = sum(1 for v in out.values() if not v["diff"])
    (data / "fidelity.json").write_text(json.dumps({"totals": totals, "examples": examples, "pages": out},
                                                   indent=1, ensure_ascii=False, default=list))
    for k, v in sorted(totals.items()):
        print(f"{k:32} {v}")
    for k, v in examples.items():
        print(f"e.g. {k}: {v}")


if __name__ == "__main__":
    main()
