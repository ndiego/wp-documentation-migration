#!/usr/bin/env python3
"""Convert the production Theme Handbook export (fetch_prod.py) to Markdown + manifest.json
for the wporg-markdown importer.

Reuses this repo's HelpHub converter (scripts/convert.py: BeautifulSoup pre-pass + markdownify
subclass) and replaces only the HelpHub-specific parts:

  - links:     kept absolute (the AAH/SCF convention); root-relative URLs made absolute
  - images:    kept as the production /files/ URLs (no asset migration in this spike)
  - callouts:  wp-block-wporg-notice -> [info] / [tip] / [alert] / [warning] shortcodes, the form
               AAH and WPCS use and which DevHub renders as the same wporg/notice markup
  - headings:  DevHub's wporg/table-of-contents rule: explicit id, else sanitize_title(text),
               de-duplicated -2, -3. Only where production has an explicit id that differs from
               the generated one is a PHP Markdown Extra "{#id}" emitted
  - embeds:    WordPress post embeds and <video> become a bare URL / <video> tag
  - <tt>:      treated as <code>
  - fixes:     <p> around block elements unwrapped; links inside inline code kept; <br> moved
               out of inline code; empty headings dropped
  - literal shortcodes ([audio], [gallery], ...) are left as written: the importer subclass
               escapes every registered shortcode except the callouts (Jetpack decodes &#91;)

Outputs, under --out:
  md/<path>.md      one file per page; pages with children are <path>/index.md
  md/manifest.json  keyed by URL path below /themes/, parent = parent's full path
  convert-report.json  per-page counts and warnings

Usage: .venv/bin/python -I convert_theme.py --pages DATA/pages.json --out OUT [--only ID,ID]
"""
import argparse
import collections
import html
import importlib.util
import json
import pathlib
import re
import sys

from bs4 import NavigableString

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = "https://developer.wordpress.org/themes/"
HOST = "https://developer.wordpress.org"
# Theme-handbook post type: the landing page (slug theme-handbook) is keyed "index".
LANDING_SLUG = "theme-handbook"

spec = importlib.util.spec_from_file_location("hh_convert", REPO / "scripts" / "convert.py")
hh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hh)

hh.CALLOUT_STYLE = "shortcode"  # keeps "Note:" labels as text (strip_label remove=False)
NOTICE_SHORTCODE = {"info": "info", "tip": "tip", "alert": "alert", "warning": "warning"}


# ---------------------------------------------------------------------------
# Site / context stand-ins
# ---------------------------------------------------------------------------
class Site:
    def __init__(self, referenced_frags):
        self.referenced_frags = referenced_frags
        self.videopress = {}
        self.manifest = collections.defaultdict(dict)

    def asset(self, url, slug, kind=None, extra=None):
        return url, url, []

    def normalise_url(self, url):
        return url


class Ctx(hh.Ctx):
    def rel(self, path):
        return str(path)


# ---------------------------------------------------------------------------
# Patched pre-pass steps
# ---------------------------------------------------------------------------
def rewrite_href(href, ctx):
    href = html.unescape(href.strip())
    if href.startswith("/") and not href.startswith("//"):
        href = HOST + href
        ctx.counts["relative_url_made_absolute"] += 1
    if href.startswith(BASE) or href.startswith(BASE.replace("https:", "http:")):
        ctx.counts["internal_links"] += 1
    return href


def handle_images(soup, ctx):
    for img in list(soup.find_all("img")):
        src = img.get("src", "")
        if not src:
            img.decompose()
            continue
        if src.startswith("/"):
            src = HOST + src
        width = None
        if img.get("width") and img.find_parent(class_="is-resized"):
            try:
                width = int(img["width"])
            except ValueError:
                width = None
        alt = img.get("alt", "")
        img.attrs = {"src": src, "alt": alt}
        if width and width <= 240:
            img["width"] = str(width)
            ctx.counts["small_images_kept_as_html"] += 1
        ctx.counts["images"] += 1
        if not alt.strip():
            ctx.counts["images_missing_alt"] += 1


_orig_videos = hh.handle_videos_and_embeds


def handle_videos_and_embeds(soup, ctx):
    # WordPress post embeds: <figure class="wp-block-embed is-type-wp-embed"> with a blockquote
    # link plus an iframe. The canonical post URL is the blockquote link, not the /embed/ iframe.
    for fig in list(soup.select("figure.wp-block-embed")):
        if not fig.parent:
            continue
        bq = fig.find("blockquote", class_="wp-embedded-content")
        a = bq.find("a", href=True) if bq else None
        wrapper = fig.find(class_="wp-block-embed__wrapper")
        url = a["href"] if a else None
        if not url and wrapper and re.match(r"^\s*https?://\S+\s*$", wrapper.get_text()):
            url = wrapper.get_text().strip()
        if not url:
            iframe = fig.find("iframe")
            url = iframe.get("src", "").split("#")[0].replace("/embed/", "/") if iframe else None
        if url:
            fig.replace_with(hh.embed_block(soup, "embed", url, hh.caption_text(fig)))
            ctx.counts["embeds"] += 1
        else:
            fig.decompose()
            ctx.warn("embed without URL removed")
    for video in list(soup.find_all("video")):
        if not video.parent:
            continue
        src = video.get("src") or (video.find("source") or {}).get("src", "") if video.find("source") else video.get("src", "")
        container = video.find_parent(class_="wp-video") or video.find_parent("figure") or video
        if not src:
            container.decompose()
            ctx.warn("video without src removed")
            continue
        src = re.sub(r"[?&]_=\d+$", "", html.unescape(src))
        container.replace_with(hh.raw_block(soup, f'<video controls preload="metadata" src="{html.escape(src)}"></video>'))
        ctx.counts["videos"] += 1
    _orig_videos(soup, ctx)


def emit_callout(soup, el, inner_nodes, kind, ctx, style=None):
    tag = soup.new_tag("mdcallout")
    tag["data-alert"] = NOTICE_SHORTCODE.get(kind, "info")
    for n in list(inner_nodes):
        tag.append(n.extract())
    el.replace_with(tag)


def handle_headings(soup, ctx):
    """DevHub TOC rule (wporg-mu-plugins blocks/table-of-contents get_id_for_item): explicit id,
    else sanitize_title(text), de-duplicated -2, -3; and no ids at all when the page has fewer
    than two headings with text. Emit "{#id}" wherever the rendered id would otherwise differ."""
    used = set()
    ctx.heading_ids = set()
    heads = []
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        if h.name == "h1":
            h.name = "h2"
            ctx.counts["h1_demoted_to_h2"] += 1
        for t in h.find_all(["strong", "b", "em", "i", "span", "mark"]):
            t.unwrap()
        if not html.unescape(re.sub(r"<[^>]*>", "", h.decode_contents())).strip():
            h.decompose()  # empty heading: renders as a stray "##"
            ctx.counts["empty_headings_removed"] += 1
            continue
        heads.append(h)
    toc_assigns_ids = len(heads) >= 2
    for h in heads:
        generated = hh.sanitize_title(h.decode_contents())
        explicit = h.get("id")
        final = hh.unique_id(explicit or generated, used)
        ctx.heading_ids.add(final)
        if explicit and (explicit != generated or not toc_assigns_ids):
            mark = soup.new_tag("mdinline")
            mark["data-md"] = " {#%s}" % explicit
            h.append(mark)
            ctx.counts["explicit_heading_ids"] += 1


def tt_to_code(soup):
    for t in soup.find_all("tt"):
        t.name = "code"


_orig_fix_inline = hh.fix_inline_structure


BLOCK_IN_P = ["pre", "figure", "div", "table", "ul", "ol", "blockquote", "h2", "h3", "h4"]


def split_partial_code_links(soup, ctx):
    """<code><a href>fn()</a> - </code> -> <a href><code>fn()</code></a><code> - </code>,
    so the link survives (the HelpHub fixer only handles code that is entirely one link)."""
    for code in list(soup.find_all("code")):
        if code.find_parent("pre") or not code.find("a", href=True):
            continue
        links = code.find_all("a", href=True)
        if len(links) == 1 and links[0].get_text() == code.get_text():
            continue  # handled by the original fixer
        parts = []
        for child in list(code.contents):
            if getattr(child, "name", None) == "a" and child.get("href"):
                a = soup.new_tag("a", href=child["href"])
                c = soup.new_tag("code")
                c.string = child.get_text()
                a.append(c)
                parts.append(a)
            else:
                t = child.get_text() if hasattr(child, "get_text") else str(child)
                if t.strip():
                    lead = t[: len(t) - len(t.lstrip())]
                    trail = t[len(t.rstrip()):]
                    if lead:
                        parts.append(NavigableString(lead))
                    c = soup.new_tag("code")
                    c.string = t.strip()
                    parts.append(c)
                    if trail:
                        parts.append(NavigableString(trail))
                elif t:
                    parts.append(NavigableString(t))
        for part in parts:
            code.insert_before(part)
        code.decompose()
        ctx.counts["partial_code_links_split"] += 1


def fix_inline_structure(soup, ctx):
    tt_to_code(soup)
    # <p><pre>..</pre></p> (7 pages): the <p> converter would escape "*" / "-" inside the fence.
    for p in list(soup.find_all("p")):
        if p.find(BLOCK_IN_P, recursive=False):
            p.unwrap()
            ctx.counts["block_in_p_unwrapped"] += 1
    split_partial_code_links(soup, ctx)
    # <code>flex-width<br></code>: a <br> inside inline code is printed literally after import
    for code in soup.find_all("code"):
        if code.find_parent("pre"):
            continue
        for br in code.find_all("br"):
            code.insert_after(br.extract())
            ctx.counts["br_moved_out_of_code"] += 1
    _orig_fix_inline(soup, ctx)


hh.rewrite_href = rewrite_href
hh.handle_images = handle_images
hh.handle_videos_and_embeds = handle_videos_and_embeds
hh.emit_callout = emit_callout
hh.handle_headings = handle_headings
hh.fix_inline_structure = fix_inline_structure
# The notice class decides the kind; a leading "Note:" in the text must not recolour it.
hh.strip_label = lambda el, remove=True: None


class ThemeConverter(hh.HelpHubConverter):
    def convert_mdcallout(self, el, text, parent_tags):
        kind = el.get("data-alert", "info")
        return f"\n\n[{kind}]\n{text.strip()}\n[/{kind}]\n\n"


hh.CONVERTER = ThemeConverter()


# ---------------------------------------------------------------------------
# Tree, manifest, files
# ---------------------------------------------------------------------------
def page_path(p):
    link = p["link"]
    assert link.startswith(BASE), link
    return link[len(BASE):].strip("/")


def build_tree(pages):
    byid = {p["id"]: p for p in pages}
    paths = {p["id"]: page_path(p) for p in pages}
    has_children = {p["parent"] for p in pages if p["parent"]}
    stubs = {}
    for p in pages:
        if p["parent"] and p["parent"] not in byid:
            # Parent is not public (draft/private): the URL path still contains it.
            ppath = paths[p["id"]].rsplit("/", 1)[0]
            stubs[p["parent"]] = ppath
    return byid, paths, has_children, stubs


def md_file_for(path, has_kids):
    if path == "":
        return "index.md"
    return f"{path}/index.md" if has_kids else f"{path}.md"


def tree_order(pages, byid, stubs):
    kids = collections.defaultdict(list)
    for p in pages:
        kids[p["parent"]].append(p)
    for sid in stubs:
        kids[0].append({"id": sid, "menu_order": 10**6, "title": "", "_stub": True})
    out = []

    def walk(pid):
        for c in sorted(kids.get(pid, []), key=lambda c: (c["menu_order"], html.unescape(c["title"]).lower())):
            out.append(c)
            walk(c["id"])
    walk(0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    pages = json.loads(pathlib.Path(a.pages).read_text())
    only = {int(x) for x in a.only.split(",") if x}
    out = pathlib.Path(a.out)
    mdroot = out / "md"
    mdroot.mkdir(parents=True, exist_ok=True)

    frags = set()
    for p in pages:
        frags |= set(re.findall(r'href="[^"#]*#([^"]+)"', p["content"]))
    site = Site(frags)
    byid, paths, has_children, stubs = build_tree(pages)

    manifest, report = {}, {}
    for p in tree_order(pages, byid, stubs):
        pid = p["id"]
        if p.get("_stub"):
            path = stubs[pid]
            slug = path.rsplit("/", 1)[-1]
            f = f"{path}/index.md"
            title = slug.replace("-", " ").title()
            manifest[path] = {"title": title, "slug": slug, "markdown_source": f, "parent": None,
                              "order": 0, "status": "private", "stub_for_nonpublic_parent": pid}
            (mdroot / f).parent.mkdir(parents=True, exist_ok=True)
            (mdroot / f).write_text(f"# {title}\n\nPlaceholder for non-public production parent {pid}.\n")
            continue
        path = paths[pid]
        f = md_file_for(path, pid in has_children)
        key = path or "index"
        slug = LANDING_SLUG if path == "" else p["slug"]
        if p["parent"] in byid:
            parent = paths[p["parent"]]
        elif p["parent"] in stubs:
            parent = stubs[p["parent"]]
        else:
            parent = None
        title = html.unescape(p["title"])
        manifest[key] = {"title": title, "slug": slug, "markdown_source": f, "parent": parent,
                         "order": p["menu_order"]}
        if only and pid not in only:
            continue
        ctx = Ctx(site, p["slug"], mdroot / f)
        body = hh.html_to_md(p["content"], ctx)
        (mdroot / f).parent.mkdir(parents=True, exist_ok=True)
        (mdroot / f).write_text(f"# {title}\n\n{body}")
        report[pid] = {"path": path, "file": f, "counts": dict(ctx.counts), "warnings": ctx.warnings,
                       "notes": ctx.info}
    (mdroot / "manifest.json").write_text(json.dumps(manifest, indent="\t", ensure_ascii=False) + "\n")
    (out / "convert-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    tot = collections.Counter()
    for r in report.values():
        tot.update(r["counts"])
    print(f"{len(report)} pages converted, {len(manifest)} manifest entries ({len(stubs)} stub parents)")
    print(dict(tot))
    print(sum(1 for r in report.values() if r["warnings"]), "pages with warnings")


if __name__ == "__main__":
    sys.exit(main())
