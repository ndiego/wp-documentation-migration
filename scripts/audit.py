#!/usr/bin/env python3
"""Content audit of raw/ HelpHub data. Writes notes/audit-stats.json and prints a summary.

Usage: .venv/bin/python -I scripts/audit.py
"""
import json, re, collections, pathlib, urllib.parse
from bs4 import BeautifulSoup, Comment

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

def load(n):
    return json.loads((RAW / f"{n}.json").read_text())

datasets = {"article": load("articles"), "version": load("versions"), "page": load("pages")}
media = load("media")

class Tally:
    def __init__(self):
        self.count = collections.Counter()      # total occurrences
        self.docs = collections.defaultdict(set)  # key -> set of slugs
    def add(self, key, slug, n=1):
        if n:
            self.count[key] += n
            self.docs[key].add(slug)
    def dump(self, top=None):
        out = {}
        for k, c in self.count.most_common(top):
            out[k] = {"occurrences": c, "docs": len(self.docs[k]), "examples": sorted(self.docs[k])[:4]}
        return out

stats = {}
for dsname, items in datasets.items():
    T = collections.defaultdict(Tally)
    img_urls = collections.Counter()
    img_hosts = collections.Counter()
    link_hosts = collections.Counter()
    link_kinds = Tally()
    article_targets = collections.Counter()
    for it in items:
        slug = it["slug"]
        html = it["content"]["rendered"]
        soup = BeautifulSoup(html, "html.parser")
        # tags
        for tag in soup.find_all(True):
            T["tags"].add(tag.name, slug)
            for c in tag.get("class", []) or []:
                if c.startswith("wp-block") or c.startswith("is-") or c.startswith("has-") or c.startswith("wp-") or c.startswith("align") or c.startswith("size-"):
                    T["classes"].add(c, slug)
                else:
                    T["other_classes"].add(c, slug)
            if tag.get("style"):
                T["inline_style_tags"].add(tag.name, slug)
                for decl in tag["style"].split(";"):
                    if ":" in decl:
                        T["inline_style_props"].add(decl.split(":")[0].strip().lower(), slug)
            if tag.get("dir") or tag.get("lang"):
                T["dir_lang"].add(f'{tag.name} dir={tag.get("dir")} lang={tag.get("lang")}', slug)
            if tag.get("id"):
                T["ids"].add("has id attr", slug)
        for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
            T["comments"].add(c.strip()[:40], slug)
        # headings
        for h in range(1, 7):
            T["headings"].add(f"h{h}", slug, len(soup.find_all(f"h{h}")))
        # nesting depth of lists
        for lst in soup.find_all(["ul", "ol"]):
            depth = len(lst.find_parents(["ul", "ol"]))
            if depth:
                T["nested_lists"].add(f"list nested depth {depth}", slug)
        # tables
        for tb in soup.find_all("table"):
            T["tables"].add("table", slug)
            if tb.find(attrs={"rowspan": True}) or tb.find(attrs={"colspan": True}):
                T["tables"].add("table with rowspan/colspan", slug)
            if not tb.find("thead") and not tb.find("th"):
                T["tables"].add("table without header row", slug)
            for cell in tb.find_all(["td", "th"]):
                if cell.find(["ul", "ol", "p", "br", "img", "pre", "table"]):
                    T["tables"].add("table with block content in cells (list/br/img/p)", slug)
                    break
            if tb.find_parent("table"):
                T["tables"].add("nested table", slug)
        # iframes / embeds
        for f in soup.find_all("iframe"):
            src = f.get("src", "")
            host = urllib.parse.urlparse(src).netloc
            T["iframes"].add(host or "(none)", slug)
        for fig in soup.find_all("figure"):
            cls = fig.get("class", [])
            for c in cls:
                if c.startswith("is-provider-") or c.startswith("wp-block-embed-"):
                    T["embeds"].add(c, slug)
        for v in soup.find_all("video"):
            T["embeds"].add("<video> tag", slug)
            src = v.get("src") or (v.find("source") or {}).get("src") if v.find("source") else v.get("src")
        for v in soup.find_all(class_=re.compile("videopress|jetpack-videopress")):
            T["embeds"].add("videopress-class element", slug)
        # shortcodes
        text = soup.get_text(" ")
        for m in re.finditer(r"\[(/?[a-z_][a-z0-9_-]*)(\s[^\]]*)?\]", text):
            name = m.group(1)
            T["shortcodes"].add(f"[{name}]", slug)
        # callouts
        for p in soup.find_all(class_="has-background"):
            T["callouts"].add(f"{p.name}.has-background", slug)
            bg = [c for c in p.get("class", []) if c.endswith("-background-color")]
            for b in bg:
                T["callout_colors"].add(b, slug)
            if p.get("style"):
                T["callout_colors"].add("inline style background", slug)
        for el in soup.find_all(class_=re.compile(r"(callout|alert|notice|warning|tip|info)", re.I)):
            T["callouts"].add("class~" + ",".join(c for c in el.get("class") if re.search("callout|alert|notice|warning|tip|info", c, re.I)), slug)
        # first word "Note:" paragraphs
        for p in soup.find_all("p"):
            t = p.get_text(" ", strip=True)
            m = re.match(r"^(Note|Tip|Warning|Important|Caution|Alert)\s*:", t, re.I)
            if m:
                T["callouts"].add(f"paragraph starting '{m.group(1).title()}:'", slug)
        # images
        for img in soup.find_all("img"):
            src = img.get("src", "")
            img_urls[src] += 1
            u = urllib.parse.urlparse(src)
            img_hosts[u.netloc] += 1
            ext = pathlib.PurePosixPath(u.path).suffix.lower()
            T["images"].add("img", slug)
            T["image_ext"].add(ext or "(none)", slug)
            if img.get("srcset"):
                T["images"].add("img with srcset", slug)
            if img.find_parent("a"):
                T["images"].add("img inside <a>", slug)
            if not img.get("alt"):
                T["images"].add("img with empty/missing alt", slug)
            if "/documentation/files/" in src:
                T["images"].add("img under /documentation/files/", slug)
            elif "wordpress.org/support/files/" in src:
                T["images"].add("img under legacy /support/files/", slug)
            if img.find_parent("table"):
                T["images"].add("img inside table", slug)
            if img.find_parent(["li"]):
                T["images"].add("img inside list item", slug)
            if not img.find_parent("figure"):
                T["images"].add("img not inside figure (inline)", slug)
        for fig in soup.find_all("figure"):
            if fig.find("figcaption"):
                T["figures"].add("figure with figcaption: " + (fig.get("class") or ["(noclass)"])[0], slug)
        # links
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            u = urllib.parse.urlparse(href)
            if href.startswith("#"):
                link_kinds.add("same-page anchor (#...)", slug); continue
            if u.scheme in ("mailto", "tel"):
                link_kinds.add(u.scheme, slug); continue
            if not u.netloc:
                link_kinds.add("relative URL (no host)", slug); continue
            host = u.netloc.lower()
            link_hosts[host] += 1
            path = u.path
            if host in ("wordpress.org", "www.wordpress.org"):
                if path.startswith("/documentation/article/"):
                    link_kinds.add("wordpress.org/documentation/article/*", slug)
                    parts = [p for p in path.split("/") if p]
                    if len(parts) >= 3:
                        article_targets[parts[2]] += 1
                    if u.fragment:
                        link_kinds.add("documentation/article/* with #fragment", slug)
                elif path.startswith("/documentation/category/"):
                    link_kinds.add("wordpress.org/documentation/category/*", slug)
                elif path.startswith("/documentation/wordpress-version/"):
                    link_kinds.add("wordpress.org/documentation/wordpress-version/*", slug)
                elif path.startswith("/documentation/files/"):
                    link_kinds.add("wordpress.org/documentation/files/* (link to file)", slug)
                elif path.startswith("/documentation"):
                    link_kinds.add("wordpress.org/documentation/ (other)", slug)
                elif path.startswith("/support/article/"):
                    link_kinds.add("LEGACY wordpress.org/support/article/*", slug)
                elif path.startswith("/support/forum") or path.startswith("/support/topic") or path == "/support/" or path.startswith("/support/welcome"):
                    link_kinds.add("wordpress.org/support (forums)", slug)
                elif path.startswith("/support/"):
                    link_kinds.add("wordpress.org/support/* (other)", slug)
                elif path.startswith("/plugins"):
                    link_kinds.add("wordpress.org/plugins", slug)
                elif path.startswith("/themes"):
                    link_kinds.add("wordpress.org/themes", slug)
                elif path.startswith("/news"):
                    link_kinds.add("wordpress.org/news", slug)
                else:
                    link_kinds.add("wordpress.org (other)", slug)
            elif host == "codex.wordpress.org":
                link_kinds.add("codex.wordpress.org (legacy)", slug)
            elif host.endswith(".wordpress.org"):
                link_kinds.add(host, slug)
            else:
                link_kinds.add("external", slug)
    stats[dsname] = {
        "items": len(items),
        **{k: v.dump() for k, v in T.items()},
        "link_kinds": link_kinds.dump(),
        "link_hosts": dict(link_hosts.most_common()),
        "img_total": sum(img_urls.values()),
        "img_unique": len(img_urls),
        "img_hosts": dict(img_hosts.most_common()),
        "article_link_targets_top": dict(article_targets.most_common(15)),
        "article_link_targets_distinct": len(article_targets),
        "_article_targets": list(article_targets),
        "_img_urls": list(img_urls),
    }

# dead article links
art_slugs = {a["slug"] for a in datasets["article"]}
for ds in stats:
    tg = stats[ds].pop("_article_targets")
    stats[ds]["article_link_targets_unresolved"] = sorted(t for t in tg if t not in art_slugs)

# media usage
all_imgs = set()
for ds in stats:
    all_imgs |= set(stats[ds].pop("_img_urls"))
all_html = "\n".join(it["content"]["rendered"] for items in datasets.values() for it in items)
def base_no_size(u):
    return re.sub(r"-\d+x\d+(?=\.[a-z0-9]+$)", "", u.split("?")[0], flags=re.I)
img_bases = {base_no_size(u) for u in all_imgs}
referenced = 0; ref_by_any_url = 0; attached = 0
featured_ids = {it.get("featured_media") for items in datasets.values() for it in items if it.get("featured_media")}
mime = collections.Counter()
for m in media:
    mime[m.get("mime_type")] += 1
    src = m["source_url"]
    if base_no_size(src) in img_bases or src in all_imgs:
        referenced += 1
    # also any reference anywhere (links, video src, etc.)
    fname = src.rsplit("/", 1)[-1]
    stem = re.sub(r"\.[a-z0-9]+$", "", fname, flags=re.I)
    if src in all_html or (stem and src.rsplit("/", 1)[0] + "/" + stem in all_html):
        ref_by_any_url += 1
    elif m["id"] in featured_ids:
        ref_by_any_url += 1
    if m.get("post"):
        attached += 1
stats["media"] = {
    "total": len(media),
    "mime_types": dict(mime.most_common()),
    "referenced_as_img_src_incl_sized_variants": referenced,
    "referenced_anywhere_in_html_or_featured": ref_by_any_url,
    "attached_to_a_post": attached,
    "unique_img_urls_all_content": len(all_imgs),
    "unique_img_files_after_stripping_size_suffix": len(img_bases),
    "featured_media_ids": len(featured_ids),
}
media_bases = {base_no_size(m["source_url"]) for m in media}
stats["media"]["content_imgs_not_in_media_library"] = len([b for b in img_bases if b not in media_bases])
stats["media"]["content_imgs_not_in_media_library_examples"] = sorted(b for b in img_bases if b not in media_bases)[:10]

(ROOT / "notes" / "audit-stats.json").write_text(json.dumps(stats, indent=1))
print("wrote notes/audit-stats.json")
