#!/usr/bin/env python3
"""Convert HelpHub (wordpress.org/documentation) REST API dumps to Markdown for the
wporg-markdown Importer (the Block Editor handbook pipeline; see notes/reference/wporg-markdown/).

Approach: BeautifulSoup pre-pass that normalises WordPress block markup (callouts,
figures, videos, embeds, galleries, complex tables, links, image URLs, heading anchors),
followed by a markdownify subclass that emits Markdown that both GitHub (CommonMark/GFM)
and Jetpack's WPCom_GHF_Markdown_Parser (PHP Markdown Extra based) render the same way.

Importer constraints honoured (class-importer.php):
  - frontmatter is stripped with  #^---(.+)---#Us  -> frontmatter must not contain "---"
  - title = first line  "# Title"  (regex /^#\s(.+)/ on the trimmed body) -> exactly one H1, first
  - Markdown inside raw HTML blocks is NOT parsed -> callouts/details are emitted as pure HTML
  - output passes wp_filter_post_kses -> no <iframe>; videos become bare oEmbed URLs, <video> kept
  - PHP Markdown needs 4-space indentation for nested list content; no backslash hard breaks

Inputs : raw/articles.json, raw/pages.json, raw/categories.json, raw/media.json,
         data/redirects.json (optional, from scripts/resolve_redirects.py)
Outputs: docs/<top-cat>/<sub-cat>/<slug>.md      one per article
         docs/<cat>[/<sub>]/README.md            folder index pages (category name + description)
         docs/site-health.md, docs/update-php.md static pages
         docs/manifest.json                      wporg-markdown importer manifest
         docs/assets/images-manifest.json        source URL -> local path (for the download step)
         data/convert-report.json                per-file warnings summary

Usage:   .venv/bin/python -I scripts/convert.py [--only SLUG ...] [--callout-style gutenberg|gfm-alert]
             [--out DIR] [--structure data/structure.yaml [--check-structure]]

Layouts: without --structure the tree follows the HelpHub categories (unchanged behaviour). With
--structure the same articles are laid out by the YAML file (sections -> folders, ordered articles,
optional `index` article as a folder's README.md) and data/restructure-map.json +
data/structure-metrics.json (scripts/structure_metrics.py) are written. See README "Structure mode".
"""
import argparse
import collections
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import sys
import urllib.parse

import yaml
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from markdownify import MarkdownConverter, BACKSLASH, ATX

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
DOCS = ROOT / "docs"
CONTENT = DOCS  # article tree root
ASSETS = DOCS / "assets"
# Where the asset files really live (scripts/download_assets.py target). images-manifest.json always records
# local_path under here, even when --out writes the Markdown elsewhere (that tree gets an assets symlink).
CANON_DOCS = DOCS
CANON_ASSETS = CANON_DOCS / "assets"

# Callout output style, switchable for comparison:
#   "gutenberg": <div class="callout callout-info"><p>..</p></div>  (Block Editor handbook convention, no importer change needed)
#   "gfm-alert": > [!NOTE]                                         (renders on GitHub; needs an importer filter on wordpress.org)
CALLOUT_STYLE = "gfm-alert"
# Where self-hosted <video src> points:
#   "remote": the original https://wordpress.org/documentation/files/... URL (videos are ~1.3 GB and are
#             NOT committed to GitHub; docs/assets/videos/ is gitignored). Posters stay local.
#   "local":  ../../assets/videos/... (needs scripts/download_assets.py to have fetched them)
VIDEO_SRC = "remote"
DATA = ROOT / "data"

DOCS_HOSTS = {"wordpress.org", "www.wordpress.org"}
PHOTON_RE = re.compile(r"^i[0-3]\.wp\.com$")
SIZE_SUFFIX_RE = re.compile(r"-\d+x\d+(?=\.[A-Za-z0-9]+$)")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}
MIME_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp",
            "image/svg+xml": ".svg", "image/bmp": ".bmp", "image/avif": ".avif"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".m4v", ".ogv"}
LABEL_RE = re.compile(r"^\s*(note|tip|warning|important|caution|alert)\s*:?\s*", re.I)
# Callout kinds use the Gutenberg handbook vocabulary: info | tip | warning | alert
KIND_FOR_LABEL = {"note": "info", "tip": "tip", "warning": "warning", "caution": "warning",
                  "important": "alert", "alert": "alert"}
KIND_FOR_NOTICE_CLASS = {"is-info-notice": "info", "is-tip-notice": "tip", "is-warning-notice": "warning",
                         "is-alert-notice": "alert", "is-success-notice": "tip",
                         "callout-info": "info", "callout-tip": "tip", "callout-warning": "warning",
                         "callout-alert": "alert"}
GFM_ALERT_FOR_KIND = {"info": "NOTE", "tip": "TIP", "warning": "WARNING", "alert": "CAUTION"}
# Background colours that mean "callout box" (everything else, e.g. colour swatches in the
# default-theme articles, is treated as plain content and the background is dropped).
CALLOUT_BG_INFO = {"#e5f5fa", "#e5f4fa", "#eaf3f9", "#e7eff4", "#e9ebee", "#f3f7fa", "#eeeeee", "#d3d3d3"}
CALLOUT_BG_CLASSES = {"has-very-light-gray-background-color": "info", "has-pale-cyan-blue-background-color": "info",
                      "has-light-grey-1-background-color": "info", "has-light-grey-2-background-color": "info",
                      "has-deep-blueberry-background-color": "info", "has-lemon-3-background-color": "warning",
                      "has-pomegrade-3-background-color": "alert"}
RESERVED_IDS = {"main", "masthead", "menu-header", "page", "primary", "secondary", "secondary-content",
                "site-navigation", "wordpress-org", "wp-toolbar", "wpadminbar", "wporg-footer", "wporg-header"}
KNOWN_SHORTCODES = re.compile(r"\[(audio|caption|embed|gallery|playlist|video|wp_caption)\b[^\]]*\]")
KEEP_ATTRS = {"href", "src", "alt", "title", "colspan", "rowspan", "data-md", "data-alert",
              "data-lang", "open", "start", "reversed", "width", "controls", "poster", "preload"}


def load(name):
    return json.loads((RAW / f"{name}.json").read_text())


def posix_rel(target: pathlib.Path, from_file: pathlib.Path) -> str:
    return pathlib.PurePosixPath(os.path.relpath(target, from_file.parent)).as_posix()


def sanitize_title(text: str) -> str:
    """Port of WordPress sanitize_title() / sanitize_title_with_dashes($title, '', 'save').

    The live HelpHub TOC (wporg/table-of-contents) uses this on the heading text to build
    anchor ids, so existing #anchor links depend on matching it exactly."""
    import unicodedata
    t = re.sub(r"<[^>]*>", "", text)                       # strip_tags
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))  # remove_accents
    t = t.replace("ß", "ss").replace("æ", "ae").replace("Æ", "AE").replace("ø", "o").replace("Ø", "O")
    t = t.lower()
    t = re.sub(r"(\u00a0|&nbsp;|&#160;|\u2013|\u2014|&ndash;|&#8211;|&mdash;|&#8212;)", "-", t)
    t = t.replace("/", "-")
    t = re.sub("[\u00a1\u00bf\u00ab\u00bb\u2039\u203a\u2018\u2019\u201c\u201d\u201a\u201b\u201e\u201f"
               "\u2022\u00a9\u00ae\u00b0\u2026\u2122\u00b4\u02dd\u0301\u0300\u0302\u0303\u0308]", "", t)
    t = re.sub(r"&#(8216|8217|8220|8221|8230|8482|169|174|176|171|187|161|191|8226);", "", t)
    t = t.replace("\u00d7", "x")
    t = re.sub(r"&.+?;", "", t)
    t = t.replace(".", "-")
    # non-ASCII letters that survive remove_accents are percent-encoded by WP (utf8_uri_encode)
    t = "".join(c if ord(c) < 128 else urllib.parse.quote(c).lower() for c in t)
    t = re.sub(r"[^%a-z0-9 _-]", "", t)
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"-+", "-", t)
    return t.strip("-")


def unique_id(base, used):
    """wporg/table-of-contents de-duplication: reserved ids and repeats get -2, -3, ..."""
    cand, n = base, 2
    while cand in used or cand in RESERVED_IDS:
        cand = f"{base}-{n}"
        n += 1
    used.add(cand)
    return cand


# ---------------------------------------------------------------------------
# Site model: categories, paths, media, redirects
# ---------------------------------------------------------------------------
class Site:
    def __init__(self):
        self.articles = load("articles")
        self.pages = load("pages")
        self.cats = {c["id"]: c for c in load("categories")}
        self.cat_by_slug = {c["slug"]: c for c in self.cats.values()}
        media = load("media")
        self.media_urls = {m["source_url"] for m in media}
        self.media_mime = {m["source_url"]: m.get("mime_type") for m in media if m.get("mime_type")}
        tp = DATA / "external-asset-types.json"  # written by scripts/download_assets.py
        self.asset_types = json.loads(tp.read_text()) if tp.exists() else {}
        self.media_by_base = {SIZE_SUFFIX_RE.sub("", m["source_url"]): m for m in media}
        self.videopress = {}
        for m in media:
            vp = (m.get("media_details") or {}).get("videopress")
            if vp and vp.get("guid"):
                self.videopress[vp["guid"]] = m
        rp = DATA / "redirects.json"
        self.redirects = json.loads(rp.read_text()) if rp.exists() else {}
        self.manifest = {}  # source url -> entry
        self.art_by_slug = {a["slug"]: a for a in self.articles}
        # every #fragment used in any href, so ids on non-heading elements can be kept when targeted
        self.referenced_frags = set()
        for it in self.articles + self.pages:
            for m in re.finditer(r'href="[^"#]*#([^"]+)"', it["content"]["rendered"]):
                self.referenced_frags.add(html.unescape(urllib.parse.unquote(m.group(1))))
            for m in re.finditer(r'<a [^>]*href="([A-Za-z][A-Za-z0-9_-]*)"', it["content"]["rendered"]):
                self.referenced_frags.add(m.group(1))  # bare "anchor" hrefs, see rewrite_href()
        # category layout (today's tree). In structure mode path_for_slug is replaced by the structure's
        # paths; links are resolved by slug through path_for_slug, so moved files resolve automatically.
        self.category_path_for_slug = {a["slug"]: self.article_path(a) for a in self.articles}
        self.path_for_slug = dict(self.category_path_for_slug)
        self.category_link_paths = None  # structure mode: {category id: folder README path}

    def cat_chain(self, cid):
        chain = []
        while cid and cid in self.cats:
            chain.insert(0, self.cats[cid])
            cid = self.cats[cid]["parent"]
        return chain

    def primary_chain(self, art):
        chains = [self.cat_chain(c) for c in art["category"]]
        chains.sort(key=lambda ch: (-len(ch), ch[-1]["slug"] if ch else ""))
        return chains[0] if chains else []

    def article_path(self, art):
        chain = self.primary_chain(art)
        parts = [c["slug"] for c in chain] or ["uncategorized"]
        return CONTENT.joinpath(*parts, f"{art['slug']}.md")

    def category_index_path(self, cat):
        return CONTENT.joinpath(*[c["slug"] for c in self.cat_chain(cat["id"])], "README.md")

    def category_link_path(self, cat):
        """Target of a /documentation/category/<slug>/ link in the current layout."""
        if self.category_link_paths is not None:
            return self.category_link_paths[cat["id"]]
        return self.category_index_path(cat)

    # ---- assets -----------------------------------------------------------
    def normalise_url(self, url):
        url = html.unescape(url.strip())
        if url.startswith("//"):
            url = "https:" + url
        u = urllib.parse.urlsplit(url)
        if PHOTON_RE.match(u.netloc):  # Jetpack Photon CDN: i0.wp.com/<host>/<path>
            host, _, path = u.path.lstrip("/").partition("/")
            u = urllib.parse.urlsplit(f"https://{host}/{path}")
        if u.netloc in DOCS_HOSTS and (u.path.startswith("/documentation/files/") or u.path.startswith("/support/files/")):
            return urllib.parse.urlunsplit(("https", "wordpress.org", u.path, "", ""))
        return urllib.parse.urlunsplit((u.scheme or "https", u.netloc, u.path, u.query, ""))

    def asset(self, url, slug, kind=None, extra=None):
        """Register an asset; return (local Path, normalised source url, notes list)."""
        notes = []
        src = self.normalise_url(url)
        u = urllib.parse.urlsplit(src)
        ext = pathlib.PurePosixPath(u.path).suffix.lower()
        if kind is None:
            kind = "image" if ext in IMAGE_EXT else "video" if ext in VIDEO_EXT else "file"
        folder = {"image": "images", "video": "videos", "file": "files", "poster": "images"}[kind]
        m = re.match(r"^/(documentation|support)/files/(.+)$", u.path) if u.netloc == "wordpress.org" else None
        if m:
            sub = pathlib.Path(folder, urllib.parse.unquote(m.group(2)))
            if m.group(1) == "support":
                notes.append(f"legacy /support/files/ URL: {src}")
        else:
            base = urllib.parse.unquote(pathlib.PurePosixPath(u.path).name) or "file"
            base = re.sub(r"[^A-Za-z0-9._-]+", "-", base)[-60:]
            if kind in ("image", "poster") and not pathlib.PurePosixPath(base).suffix:
                # extension-less URL (lh3.googleusercontent.com/...): type from the media library,
                # else from the downloader's Content-Type / magic-byte cache, else unknown (.img)
                mime = self.media_mime.get(src) or (self.asset_types.get(src) or {}).get("mime")
                base += MIME_EXT.get(mime, ".img")
            h = hashlib.sha1(src.encode()).hexdigest()[:10]
            sub = pathlib.Path(folder, "external", u.netloc, f"{h}-{base}")
            notes.append(f"external {kind} host {u.netloc}: {src}")
        local = ASSETS / sub  # what the Markdown links to (relative to the output tree)
        entry = self.manifest.setdefault(src, {
            "source_url": src, "local_path": os.path.relpath(CANON_ASSETS / sub, ROOT), "kind": kind,
            "host": u.netloc, "in_media_library": src in self.media_urls, "used_by": []})
        if extra:
            entry.update(extra)
        if slug not in entry["used_by"]:
            entry["used_by"].append(slug)
        return local, src, notes

    def best_image_url(self, img):
        """Prefer the unsized original when it is known to exist (in srcset or media library)."""
        src = self.normalise_url(img.get("src", ""))
        full = SIZE_SUFFIX_RE.sub("", src)
        if full != src:
            srcset_urls = {self.normalise_url(p.strip().split(" ")[0]) for p in img.get("srcset", "").split(",") if p.strip()}
            if full in srcset_urls or full in self.media_urls:
                return full, src
        return src, src


# ---------------------------------------------------------------------------
# Per-document conversion context
# ---------------------------------------------------------------------------
class Ctx:
    def __init__(self, site, slug, out_path):
        self.site, self.slug, self.out = site, slug, out_path
        self.warnings = []
        self.info = []
        self.counts = collections.Counter()
        self.videos = []
        self.heading_ids = set()

    def warn(self, msg):
        if msg not in self.warnings:
            self.warnings.append(msg)

    def note(self, msg):
        if msg not in self.info:
            self.info.append(msg)

    def rel(self, path):
        return posix_rel(path, self.out)


def md_link(text, url):
    return f"[{text}]({url})"


def esc_md_text(s):
    return re.sub(r"([\[\]])", r"\\\1", " ".join(s.split()))


# ---------------------------------------------------------------------------
# Link rewriting
# ---------------------------------------------------------------------------
BARE_FRAGMENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def rewrite_href(href, ctx: Ctx):
    site = ctx.site
    href = html.unescape(href.strip())
    if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return href
    if href.startswith("/"):
        href = "https://wordpress.org" + href
        ctx.counts["relative_url_made_absolute"] += 1
    elif BARE_FRAGMENT_RE.match(href):
        # "create-group-block-from-selected-multiple-blocks": a same-page anchor missing its "#"
        # (a relative URL with no slash/dot would 404 on the live site)
        ctx.note(f"bare relative link '{href}' treated as same-page anchor #{href}")
        ctx.counts["bare_fragment_links_fixed"] += 1
        return "#" + href
    elif not re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):
        ctx.warn(f"odd relative link left as-is: {href}")
        return href
    u = urllib.parse.urlsplit(href)
    host = u.netloc.lower()
    if PHOTON_RE.match(host) or (host in DOCS_HOSTS and re.match(r"^/(documentation|support)/files/", u.path)):
        local, src, notes = site.asset(href, ctx.slug)
        ctx.counts["file_links_localised"] += 1
        return ctx.rel(local)
    if host not in DOCS_HOSTS:
        return href
    frag = ("#" + u.fragment) if u.fragment else ""
    m = re.match(r"^/(documentation|support)/article/([^/]+)/?$", u.path)
    if m:
        legacy = m.group(1) == "support"
        slug = urllib.parse.unquote(m.group(2)).lower()
        target = slug if slug in site.path_for_slug else None
        if not target and slug in site.redirects:
            r = site.redirects[slug]
            if r.get("slug"):
                target = r["slug"]
                ctx.note(f"link to old slug '{slug}' rewritten to '{target}' (via 301)")
            elif r.get("final_url") and r.get("status") != 404 and "/documentation/article/" not in r["final_url"]:
                ctx.note(f"link to '{slug}' points to moved page {r['final_url']}")
                ctx.counts["links_to_moved_external"] += 1
                return r["final_url"] + frag
        if target:
            if legacy:
                ctx.counts["legacy_support_links_fixed"] += 1
            ctx.counts["internal_links_rewritten"] += 1
            if target == ctx.slug and frag:
                return frag
            return ctx.rel(site.path_for_slug[target]) + frag
        ctx.warn(f"unresolved article link: {href}")
        return f"https://wordpress.org/documentation/article/{slug}/" + frag
    m = re.match(r"^/documentation/category/(?:.+/)?([^/]+)/?$", u.path)
    if m and m.group(1) in site.cat_by_slug:
        ctx.counts["category_links_rewritten"] += 1
        return ctx.rel(site.category_link_path(site.cat_by_slug[m.group(1)])) + frag
    if u.path.startswith("/documentation/wordpress-version/"):
        ctx.counts["version_links_kept_absolute"] += 1
    return href


# ---------------------------------------------------------------------------
# Pre-pass: normalise WordPress markup
# ---------------------------------------------------------------------------
def html_fragment(nodes):
    """Serialise already-rewritten nodes as compact HTML (for raw HTML blocks, where Markdown
    is not parsed by Jetpack): attributes cleaned, no blank lines, mdraw/mdinline expanded."""
    import copy
    parts = []
    for n in nodes:
        if isinstance(n, NavigableString):
            if isinstance(n, Comment):
                continue
            t = html.escape(str(n), quote=False)
            if t.strip():
                parts.append(t.strip())
            continue
        c = copy.copy(n)
        clean_attrs(c)
        parts.append(str(c))
    out = "\n".join(parts)
    out = re.sub(r'<(mdraw|mdinline) data-md="([^"]*)"></\1>', lambda m: html.unescape(m.group(2)), out)
    out = re.sub(r"\n\s*\n", "\n", out)
    return out.strip()


def embed_block(soup, comment, url, caption=""):
    """Bare URL on its own paragraph -> WordPress auto-embeds it (oEmbed) after import;
    GitHub shows it as a link. kses would strip an <iframe>."""
    md = f"<!-- {comment} -->\n\n{url}"
    if caption:
        md += f"\n\n*{caption}*"
    return raw_block(soup, md)


def callout_kind_for_background(el):
    m = re.search(r"background(?:-color)?:\s*([^;]+)", el.get("style", ""))
    if m and m.group(1).strip().lower() in CALLOUT_BG_INFO:
        return "info"
    for c in el.get("class", []):
        if c in CALLOUT_BG_CLASSES:
            return CALLOUT_BG_CLASSES[c]
    return None


def emit_callout(soup, el, inner_nodes, kind, ctx: Ctx, style=None):
    """THE single place that decides callout syntax (switch with CALLOUT_STYLE)."""
    style = style or CALLOUT_STYLE
    if style == "gfm-alert":
        bq = soup.new_tag("blockquote")
        bq["data-alert"] = GFM_ALERT_FOR_KIND[kind]
        for n in list(inner_nodes):
            bq.append(n.extract())
        el.replace_with(bq)
        return
    # Gutenberg handbook convention: raw HTML, inner content must be HTML (not Markdown)
    blocks, inline = [], []
    for n in list(inner_nodes):
        if isinstance(n, Tag) and n.name in ("p", "ul", "ol", "pre", "table", "figure", "blockquote", "div", "mdraw", "h3", "h4", "h5"):
            if inline:
                blocks.append("<p>" + html_fragment(inline) + "</p>")
                inline = []
            frag = html_fragment([n])
            if n.name == "figure":
                frag = re.sub(r"</?figure>", "", frag)
            blocks.append(frag)
        else:
            inline.append(n)
    if inline and html_fragment(inline):
        blocks.append("<p>" + html_fragment(inline) + "</p>")
    body = "\n".join("    " + ln for b in blocks for ln in b.split("\n"))
    el.replace_with(raw_block(soup, f'<div class="callout callout-{kind}">\n{body}\n</div>'))


def handle_details(soup, ctx: Ctx):
    for d in list(soup.find_all("details")):
        if not d.parent:
            continue
        summary = d.find("summary")
        st = html.escape(" ".join(summary.get_text(" ", strip=True).split())) if summary else "Details"
        if summary:
            summary.extract()
        body = html_fragment(list(d.children))
        d.replace_with(raw_block(soup, f"<details>\n<summary>{st}</summary>\n{body}\n</details>"))
        ctx.note("contained <details> (emitted as raw HTML details/summary)")


def raw_block(soup, md):
    t = soup.new_tag("mdraw")
    t["data-md"] = md
    return t


def caption_text(fig):
    cap = fig.find("figcaption")
    if not cap:
        return ""
    return esc_md_text(cap.get_text(" ", strip=True))


def handle_videos_and_embeds(soup, ctx: Ctx):
    site = ctx.site
    # VideoPress (block or embed), YouTube and any other iframes
    for iframe in list(soup.find_all("iframe")):
        if not iframe.parent:
            continue
        src = html.unescape(iframe.get("src", ""))
        u = urllib.parse.urlsplit(src)
        container = iframe.find_parent("figure") or iframe
        caption = caption_text(container) if container.name == "figure" else ""
        m = re.match(r"^/embed/([A-Za-z0-9_-]+)", u.path)
        if u.netloc in ("videopress.com", "video.wordpress.com") and m:
            guid = m.group(1)
            watch = f"https://videopress.com/v/{guid}"
            info = {"type": "videopress", "guid": guid, "url": watch}
            mi = site.videopress.get(guid)
            if mi:
                vp = mi["media_details"]["videopress"]
                info.update({"original": vp.get("original"), "poster": vp.get("poster"), "media_id": mi["id"]})
                if vp.get("poster"):
                    site.asset(vp["poster"], ctx.slug, kind="poster", extra={"videopress_guid": guid})
                if vp.get("original"):
                    site.asset(vp["original"], ctx.slug, kind="video", extra={"videopress_guid": guid})
            ctx.videos.append(info)
            ctx.counts["videopress"] += 1
            ctx.warn("contained VideoPress embed (now a bare oEmbed URL; verify it auto-embeds after import)" +
                     ("" if mi else f"; guid {guid} not found in media library"))
            container.replace_with(embed_block(soup, f"VideoPress embed (iframe removed): {src.split('?')[0]}", watch, caption))
        elif "youtube" in u.netloc or "youtu.be" in u.netloc:
            vid = m.group(1) if m else ""
            watch = f"https://www.youtube.com/watch?v={vid}" if vid else src
            ctx.videos.append({"type": "youtube", "url": watch})
            ctx.warn("contained YouTube embed (now a bare oEmbed URL)")
            container.replace_with(embed_block(soup, f"YouTube embed (iframe removed): {src.split('?')[0]}", watch, caption))
        else:
            ctx.warn(f"contained iframe embed from {u.netloc} (now a bare URL; may not auto-embed)")
            container.replace_with(embed_block(soup, f"iframe embed removed: {src}", src, caption))

    # Self-hosted <video>: kept as raw HTML (allowed by kses) with a local src
    for video in list(soup.find_all("video")):
        if not video.parent:
            continue
        src = video.get("src") or (video.find("source") or {}).get("src", "") if video.find("source") else video.get("src", "")
        container = video.find_parent("figure") or video
        caption = caption_text(container) if container.name == "figure" else ""
        if not src:
            ctx.warn("video tag without src removed")
            container.decompose()
            continue
        local, norm, notes = site.asset(src, ctx.slug, kind="video")
        for n in notes:
            (ctx.note if n.startswith("legacy") else ctx.warn)(n)
        video_src = norm if VIDEO_SRC == "remote" else ctx.rel(local)
        attrs = f'controls preload="metadata" src="{html.escape(video_src)}"'
        if video.get("poster"):
            plocal, _, _ = site.asset(video["poster"], ctx.slug, kind="poster")
            attrs += f' poster="{html.escape(ctx.rel(plocal))}"'
        ctx.videos.append({"type": "self-hosted", "url": norm, "local_path": os.path.relpath(CANON_ASSETS / local.relative_to(ASSETS), ROOT)})
        ctx.counts["self_hosted_videos"] += 1
        md = f"<video {attrs}></video>"
        if caption:
            md += f"\n\n*{caption}*"
        container.replace_with(raw_block(soup, md))

    # oEmbed blocks without iframes (X/Twitter, Bluesky, etc.)
    for fig in list(soup.select("figure.wp-block-embed")):
        if not fig.parent:
            continue
        provider = next((c[len("is-provider-"):] for c in fig.get("class", []) if c.startswith("is-provider-")), "embed")
        wrapper = fig.find(class_="wp-block-embed__wrapper")
        url = None
        if wrapper and re.match(r"^\s*https?://\S+\s*$", wrapper.get_text()):
            url = wrapper.get_text().strip()
        links = [x["href"] for x in fig.find_all("a", href=True)]
        if not url and links:
            url = links[-1]
        caption = caption_text(fig)
        if not url:
            ctx.warn(f"{provider} embed with no URL removed")
            fig.decompose()
            continue
        ctx.warn(f"contained {provider} embed (now a bare oEmbed URL; check provider support)")
        fig.replace_with(embed_block(soup, f"{provider} embed", url, caption))


def strip_label(el, remove=True):
    """Detect (and optionally remove) a leading 'Note:' style label; return the callout kind or None."""
    for s in el.find_all(string=True):
        if not s.strip():
            continue
        m = LABEL_RE.match(s)
        if not m:
            return None
        # require the label to be followed by ':' (in this node or the next text) to avoid "Note that..."
        rest = s[m.end():]
        has_colon = ":" in s[:m.end()]
        nxt = None
        if not has_colon:
            nxt = s.find_next(string=lambda x: x.strip())
            if not (rest.strip() == "" and nxt is not None and nxt.strip().startswith(":")):
                return None
        if remove:
            if nxt is not None:
                nxt.replace_with(nxt.replace(":", "", 1).lstrip())
            s.replace_with(rest)
            for t in el.find_all(["strong", "em", "b", "i"]):
                if not t.get_text(strip=True) and not t.find("img"):
                    t.decompose()
        return KIND_FOR_LABEL[m.group(1).lower()]
    return None


def handle_callouts(soup, ctx: Ctx):
    candidates = []
    for el in soup.find_all(class_=True):
        cls = el.get("class", [])
        if "changelog" in cls:
            continue
        if "wp-block-wporg-notice" in cls or "callout" in cls:
            candidates.append((el, None))
        elif "has-background" in cls and el.name in ("p", "div", "ul", "ol"):
            if el.find_parent(class_=["callout", "wp-block-wporg-notice"]):
                continue
            if el.name == "div" and el.find(["table", "figure", "h2", "h3", "h4"]) is not None:
                continue  # layout group with a background colour - just unwrap
            bg_kind = callout_kind_for_background(el)
            if not bg_kind:
                ctx.counts["background_colour_dropped"] += 1
                continue
            candidates.append((el, bg_kind))
    for el, bg_kind in candidates:
        if not el.parent or el.find_parent(attrs={"data-callout": True}):
            continue
        cls = el.get("class", [])
        kind = next((KIND_FOR_NOTICE_CLASS[c] for c in cls if c in KIND_FOR_NOTICE_CLASS), None)
        inner = el.find(class_="wp-block-wporg-notice__content") or el
        icon = el.find(class_="wp-block-wporg-notice__icon")
        if icon:
            icon.decompose()
        # In GFM-alert mode the alert title replaces a "Note:" label; in HTML mode the text stays.
        label_kind = strip_label(inner, remove=(CALLOUT_STYLE == "gfm-alert"))
        kind = label_kind or kind or bg_kind or "info"
        if el.name in ("p", "ul", "ol"):
            el.attrs = {}
            wrapper = soup.new_tag("div")
            el.wrap(wrapper)
            emit_callout(soup, wrapper, [el], kind, ctx)
        else:
            emit_callout(soup, el, list(inner.children), kind, ctx)
        ctx.counts["callouts"] += 1
        ctx.counts[f"callouts_{kind}"] += 1


def handle_images(soup, ctx: Ctx):
    site = ctx.site
    for img in list(soup.find_all("img")):
        src = img.get("src", "")
        if not src:
            img.decompose()
            continue
        if src.startswith("data:"):
            ctx.warn("inline data: URI image removed")
            img.decompose()
            continue
        best, shown = site.best_image_url(img)
        local, norm, notes = site.asset(best, ctx.slug, kind="image")
        for n in notes:
            # /support/files/ URLs are still served (also under /documentation/files/): note only
            (ctx.note if n.startswith("legacy") else ctx.warn)(n)
        if best != shown:
            site.manifest[norm].setdefault("displayed_variant", shown)
        ctx.counts["images"] += 1
        if not img.get("alt", "").strip():
            ctx.counts["images_missing_alt"] += 1
        # Keep display width for deliberately small (resized) images such as UI icons.
        width = None
        style = img.get("style", "")
        mw = re.search(r"(?<![-\w])width:\s*(\d+)px", style)
        if mw:
            width = int(mw.group(1))
        elif img.get("width") and img.find_parent(class_="is-resized"):
            try:
                width = int(img["width"])
            except ValueError:
                width = None
        img.attrs = {"src": ctx.rel(local), "alt": img.get("alt", "")}
        if img.get("title"):
            img["title"] = img.get("title")
        if width and width <= 240:
            img["width"] = str(width)
            ctx.counts["small_images_kept_as_html"] += 1
        # Unwrap links that just point at the image file itself.
        a = img.find_parent("a")
        if a is not None and a.get("href"):
            href = site.normalise_url(a["href"])
            hpath = urllib.parse.urlsplit(href).path
            ext = pathlib.PurePosixPath(hpath).suffix.lower()
            if ext in IMAGE_EXT or "/files/" in hpath or SIZE_SUFFIX_RE.sub("", href) == SIZE_SUFFIX_RE.sub("", norm):
                a.unwrap()
                ctx.counts["image_self_links_removed"] += 1


def table_is_simple(tb):
    if tb.find(attrs={"rowspan": True}) or tb.find(attrs={"colspan": True}):
        return False
    if tb.find("table"):
        return False
    for cell in tb.find_all(["td", "th"]):
        if cell.find(["ul", "ol", "pre", "table", "figure", "blockquote", "mdraw", "h2", "h3", "h4"]):
            return False
        if len(cell.find_all("p")) > 1:
            return False
    return True


def promote_bold_header_row(tb, ctx):
    """Tables without <th>: if every cell of the first row is fully bold, treat it as the header."""
    if tb.find("th"):
        return
    first = tb.find("tr")
    if not first:
        return
    cells = first.find_all("td")
    def all_bold(td):
        txt = td.get_text(strip=True)
        bold = "".join(b.get_text(strip=True) for b in td.find_all(["strong", "b"]))
        return txt == "" or (txt and bold.replace(" ", "") == txt.replace(" ", ""))
    if cells and all(all_bold(td) for td in cells) and any(td.get_text(strip=True) for td in cells):
        for td in cells:
            for b in td.find_all(["strong", "b"]):
                b.unwrap()
            td.name = "th"
        ctx.counts["tables_header_inferred_from_bold_row"] += 1
    else:
        ctx.counts["tables_without_header_row"] += 1


def clean_attrs(el):
    for t in [el] + list(el.find_all(True)):
        t.attrs = {k: v for k, v in t.attrs.items() if k in KEEP_ATTRS}


def handle_tables(soup, ctx: Ctx):
    for tb in list(soup.find_all("table")):
        if not tb.parent or tb.find_parent("table"):
            continue
        fig = tb.find_parent("figure")
        caption = caption_text(fig) if fig else ""
        if table_is_simple(tb):
            ctx.counts["tables_gfm"] += 1
            promote_bold_header_row(tb, ctx)
            continue
        clean_attrs(tb)
        for t in tb.find_all(["mdraw"]):
            t.replace_with(NavigableString(t["data-md"]))
        html_str = str(tb)
        html_str = re.sub(r"\n\s*\n", "\n", html_str)
        ctx.counts["tables_raw_html"] += 1
        ctx.warn("complex table kept as raw HTML (rowspan/colspan or block content in cells)")
        repl = raw_block(soup, html_str + (f"\n\n*{caption}*" if caption else ""))
        (fig if fig else tb).replace_with(repl)


def handle_math(soup, ctx: Ctx):
    for m in list(soup.find_all("math")):
        ann = m.find("annotation", attrs={"encoding": "application/x-tex"})
        tex = ann.get_text().strip() if ann else m.get_text(" ", strip=True)
        display = m.get("display") == "block"
        ctx.warn("contained MathML (converted to $TeX$, check renderer support)")
        md = f"$${tex}$$" if display else f"${tex}$"
        t = soup.new_tag("mdinline")
        t["data-md"] = md
        m.replace_with(t)


def handle_headings(soup, ctx: Ctx):
    """Keep the live site's anchors working.

    Live ids come from wporg/table-of-contents: explicit id attribute, else sanitize_title(text),
    de-duplicated with -2, -3. After import the headings have no explicit ids, so the TOC will
    generate sanitize_title ids. Where the two differ, an <a id="old"></a> is emitted."""
    used_old, used_new = set(), set()
    ctx.heading_ids = set()
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        if h.name == "h1":
            h.name = "h2"
            ctx.counts["h1_demoted_to_h2"] += 1
        for t in h.find_all(["strong", "b", "em", "i", "span", "mark"]):
            t.unwrap()
        plain_html = re.sub(r"<[^>]*>", "", h.decode_contents())
        if not html.unescape(plain_html).strip():
            continue  # TOC ignores headings without text
        base = sanitize_title(plain_html)
        old = unique_id(h["id"], used_old) if h.get("id") else unique_id(base, used_old)
        new = unique_id(base, used_new)
        ctx.heading_ids |= {old, new}
        if old != new:
            anchor = soup.new_tag("mdraw")
            anchor["data-md"] = f'<a id="{html.escape(old)}"></a>'
            h.insert_before(anchor)
            ctx.counts["preserved_heading_anchors"] += 1


def handle_other_anchors(soup, ctx: Ctx):
    """Keep ids on non-heading elements (p, ol, li...) when some link targets them."""
    for el in soup.find_all(id=True):
        if re.match(r"^h[1-6]$", el.name) or el.name in ("mdraw", "mdinline"):
            continue
        hid = el["id"]
        if hid not in ctx.site.referenced_frags or hid in ctx.heading_ids:
            continue
        tag = soup.new_tag("mdinline")
        tag["data-md"] = f'<a id="{html.escape(hid)}"></a>'
        if el.name in ("p", "li", "td", "th", "dt", "dd", "span", "strong", "em", "a", "code"):
            el.insert(0, tag)
        else:
            blk = soup.new_tag("mdraw")
            blk["data-md"] = tag["data-md"]
            el.insert_before(blk)
        ctx.counts["custom_element_anchors"] += 1


def code_language(pre):
    classes = pre.get("class", []) + ((pre.find("code") or {}).get("class", []) if pre.find("code") else [])
    for c in classes:
        if c.startswith("language-"):
            return c[len("language-"):]
    cls = " ".join(classes)
    m = re.search(r"brush:\s*([a-z0-9]+)", cls)
    if m:
        return {"plain": "", "xml": "html"}.get(m.group(1), m.group(1))
    if pre.find("code") and pre.find("code").get("lang"):
        return pre.find("code")["lang"]
    return ""


def fix_inline_structure(soup, ctx):
    """Repair inline markup that markdownify would mangle."""
    for sp in soup.find_all(["span", "font"]):
        if not sp.get("id"):
            sp.unwrap()
    # nested same emphasis (<strong>a <strong>+</strong></strong>) renders as "**a **+****"
    for t in soup.find_all(["strong", "b"]):
        if t.find_parent(["strong", "b"]):
            t.unwrap()
            ctx.counts["nested_emphasis_unwrapped"] += 1
    for t in soup.find_all(["em", "i"]):
        if t.find_parent(["em", "i"]):
            t.unwrap()
            ctx.counts["nested_emphasis_unwrapped"] += 1
    # adjacent <strong>a</strong><strong>b</strong> -> one element (else "**a****b**")
    for t in soup.find_all(["strong", "b", "em", "i", "code"]):
        nxt = t.next_sibling
        while t.parent is not None and isinstance(nxt, Tag) and nxt.name == t.name:
            for c in list(nxt.contents):
                t.append(c.extract())
            nxt.decompose()
            nxt = t.next_sibling
            ctx.counts["adjacent_emphasis_merged"] += 1
    # <br> at the edges of links/emphasis -> move outside (a blank line inside [...] breaks the link)
    for t in soup.find_all(["a", "strong", "em", "b", "i"]):
        while t.contents and (getattr(t.contents[-1], "name", None) == "br" or
                              (isinstance(t.contents[-1], NavigableString) and not t.contents[-1].strip() and len(t.contents) > 1)):
            t.insert_after(t.contents[-1].extract())
        while t.contents and getattr(t.contents[0], "name", None) == "br":
            t.insert_before(t.contents[0].extract())
    # <br> as first/last content of a block (e.g. "<details><summary/><br/>", "<p>text<br></p>") is noise
    BLOCKS = ("p", "li", "details", "div", "td", "th", "blockquote", "figcaption", "dd", "dt")
    for br in [b for _ in range(3) for b in soup.find_all("br")]:
        if br.parent is None:
            continue
        par = br.parent
        if par is None or par.name not in BLOCKS:
            continue
        sibs = [c for c in par.contents if not (isinstance(c, NavigableString) and not c.strip())
                and getattr(c, "name", None) != "summary"]
        if sibs and (sibs[0] is br or sibs[-1] is br):
            br.decompose()
            ctx.counts["edge_br_removed"] += 1
    # <code><a href>x</a></code> -> <a href><code>x</code></a> (links inside code spans are dropped)
    for code in soup.find_all("code"):
        if code.find_parent("pre"):
            continue
        links = code.find_all("a", href=True)
        if not links:
            continue
        if len(links) == 1 and links[0].get_text() == code.get_text():
            a = links[0]
            a.unwrap()
            code.wrap(soup.new_tag("a", href=a["href"]))
            ctx.counts["code_links_swapped"] += 1
        else:
            ctx.warn("inline code contained partial links (link dropped)")


# Shortcode examples that WordPress rendered away inside <pre> and that cannot be recovered from
# the HTML (an attachment-less "[video]" renders as nothing). Keyed by slug; filled in order.
EMPTY_PRE_FILL = {"video-shortcode": ["[video]", "[video]"]}
WP_MEDIA_DEFAULT_SIZE = ("640", "360")  # wp_video_shortcode() defaults when no width/height given


def shortcode_from_player(media):
    """Rebuild the [video]/[audio] shortcode text from the player WordPress rendered for it."""
    tag = media.name  # video | audio
    def clean(u):
        u = re.sub(r"[?&]_=\d+$", "", html.unescape(u))
        # esc_url() prefixed bare file names with http:// ("video-source.mp4" -> "http://video-source.mp4")
        m = re.match(r"^https?://([^/]+\.(?:mp4|m4v|webm|ogv|ogg|wmv|flv|mp3|m4a|wav|wma))$", u, re.I)
        return m.group(1) if m else u
    srcs = [clean(x["src"]) for x in media.find_all("source", src=True)] or ([clean(media["src"])] if media.get("src") else [])
    attrs = []
    if tag == "video" and (media.get("width"), media.get("height")) != WP_MEDIA_DEFAULT_SIZE:
        attrs += [f'width="{media["width"]}"', f'height="{media["height"]}"'] if media.get("width") else []
    if len(srcs) == 1:
        attrs.append(f'src="{srcs[0]}"')
    else:
        for u in srcs:
            ext = pathlib.PurePosixPath(urllib.parse.urlsplit(u).path).suffix.lstrip(".").lower() or "src"
            attrs.append(f'{ext}="{u}"')
    for flag in ("loop", "autoplay", "muted"):
        if media.has_attr(flag):
            attrs.append(f'{flag}="on"')
    if media.get("poster"):
        attrs.append(f'poster="{media["poster"]}"')
    return "[" + " ".join([tag] + attrs) + "]"


def freeze_preformatted(soup, ctx: Ctx):
    """Content inside <pre> is emitted verbatim as a fenced code block. Collapse every <pre> to a
    single text node *before* any other pre-pass step, so that nothing inside it (players, images,
    links, anchors, emphasis) is rewritten, registered as an asset or turned into Markdown."""
    fills = list(EMPTY_PRE_FILL.get(ctx.slug, []))
    for pre in soup.find_all("pre"):
        lang = code_language(pre)
        pre.attrs = {"data-lang": lang} if lang else {}
        # WordPress executed shortcode examples inside <pre> (players instead of "[video ...]" text)
        for media in pre.find_all(["video", "audio"], class_=re.compile(r"^wp-(video|audio)-shortcode$")):
            wrap = media.find_parent(class_=["wp-video", "wp-audio"]) or media
            wrap.replace_with(NavigableString(shortcode_from_player(media)))
            ctx.counts["rendered_shortcodes_restored_in_pre"] += 1
            ctx.note("live article shows a rendered media player inside a code example (content bug); "
                     "converted back to the shortcode text. WordPress runs shortcodes inside <pre> too, so after "
                     "import this needs [[video ...]] escaping or an importer filter, or the players come back")
        if pre.find("a"):
            ctx.warn("preformatted block contained links (URLs lost inside code fence)")
        if pre.find(["strong", "em", "b"]):
            ctx.note("preformatted block contained bold/italic (formatting dropped in fence)")
        for br in pre.find_all("br"):
            br.replace_with(NavigableString("\n"))
        text = pre.get_text()
        if not text.strip() and fills:
            text = fills.pop(0)
            ctx.counts["empty_pre_filled"] += 1
            ctx.note(f"empty <pre> (shortcode rendered to nothing on the live site) filled with {text!r}; "
                     "reconstructed, check against the original Codex page")
        pre.clear()
        if text:
            pre.append(NavigableString(text))


def prepass(html_str, ctx: Ctx):
    soup = BeautifulSoup(html_str, "html.parser")
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in soup.find_all(["script", "style", "noscript", "svg", "form", "button"]):
        t.decompose()
    for t in soup.select(".wp-block-spacer"):
        t.decompose()
    # Gutenberg artifact: whitespace-only <strong> </strong> etc. markdownify would drop the space.
    for t in soup.find_all(["strong", "em", "b", "i", "span", "mark", "code", "u", "s"]):
        if t.parent and not t.find(True) and not t.get_text().strip():
            t.replace_with(" " if t.get_text() else "")
    # text-level: detect known shortcodes outside code
    for s in soup.find_all(string=KNOWN_SHORTCODES):
        if not s.find_parent(["code", "pre"]):
            ctx.note(f"literal shortcode text outside code: {KNOWN_SHORTCODES.search(s).group(0)[:40]}")
    freeze_preformatted(soup, ctx)
    fix_inline_structure(soup, ctx)
    handle_videos_and_embeds(soup, ctx)
    handle_images(soup, ctx)
    for a in soup.find_all("a", href=True):
        a["href"] = rewrite_href(a["href"], ctx)
    handle_math(soup, ctx)
    handle_headings(soup, ctx)
    handle_other_anchors(soup, ctx)
    handle_callouts(soup, ctx)
    handle_details(soup, ctx)
    handle_tables(soup, ctx)
    clean_attrs(soup)
    return soup


# ---------------------------------------------------------------------------
# Markdown emitter
# ---------------------------------------------------------------------------
EMPHASIS_STATS = collections.Counter()
INLINE_TAGS = {"a", "strong", "b", "em", "i", "span", "code", "u", "s", "del", "sup", "sub", "mark", "kbd", "mdinline"}


def _is_punct(c):
    import unicodedata
    return unicodedata.category(c)[0] in "PS"


def _adjacent_char(el, direction):
    """First visible character before (-1) or after (+1) el inside the same block; '' at a block edge."""
    node = el
    while node is not None:
        sib = node.previous_sibling if direction < 0 else node.next_sibling
        while sib is not None:
            if isinstance(sib, Comment):
                pass
            elif isinstance(sib, NavigableString):
                if str(sib):
                    return str(sib)[-1] if direction < 0 else str(sib)[0]
            elif isinstance(sib, Tag):
                if sib.name == "br":
                    return " "
                t = sib["data-md"] if sib.name in ("mdinline", "mdraw") else sib.get_text()
                if sib.name not in INLINE_TAGS:
                    return " "
                if t:
                    return t[-1] if direction < 0 else t[0]
            sib = sib.previous_sibling if direction < 0 else sib.next_sibling
        node = node.parent
        if node is None or node.name not in INLINE_TAGS:
            return ""
    return ""


def _plain_text_edge(el, chars, first):
    """True if `chars` at the start/end of el's content is plain text owned by el (not a link/code end)."""
    strings = [s for s in el.find_all(string=True) if s.strip()]
    if not strings:
        return False
    edge = strings[0] if first else strings[-1]
    if edge.parent is not el:
        return False
    t = edge.strip()
    return t.startswith(chars) if first else t.endswith(chars)


class HelpHubConverter(MarkdownConverter):
    class Options(MarkdownConverter.DefaultOptions):
        heading_style = ATX
        bullets = "-"
        newline_style = BACKSLASH
        escape_underscores = False
        escape_asterisks = True
        table_infer_header = False
        keep_inline_images_in = ["td", "th"]
        sup_symbol = "<sup>"
        sub_symbol = "<sub>"
        code_language_callback = staticmethod(lambda el: el.get("data-lang", ""))

    def escape(self, text, parent_tags):
        text = super().escape(text, parent_tags)
        # Literal text that looks like HTML or entities must not be re-interpreted by
        # the Markdown renderer (e.g. "&lt;h1&gt;" or "&amp;copy;" in prose).
        text = re.sub(r"&(?=#?[A-Za-z0-9]+;)", "&amp;", text)
        text = re.sub(r"<(?=[A-Za-z/!?])", "&lt;", text)
        text = text.replace("`", "\\`")
        return text

    # ---- emphasis ---------------------------------------------------------
    # CommonMark only closes "**" when it is right-flanking: "**None –**removes" does NOT render bold
    # (closer preceded by punctuation and followed by a letter), and "Menus**,** and" never opens.
    # markdownify's chomp() only moves plain spaces outside the markers (not &nbsp;), so the
    # common WordPress paste artefact "<strong>Undo:&nbsp;</strong>Undo" ends up as "**Undo:**Undo".
    def convert_strong(self, el, text, parent_tags):
        return self._emphasis(el, text, parent_tags, "**")

    convert_b = convert_strong

    def convert_em(self, el, text, parent_tags):
        return self._emphasis(el, text, parent_tags, "*")

    convert_i = convert_em

    def _emphasis(self, el, text, parent_tags, marker):
        if "_noformat" in parent_tags:
            return text
        prefix = " " if text[:1].isspace() else ""
        suffix = " " if text[-1:].isspace() else ""
        inner = text.strip()
        if not inner:
            return prefix or suffix
        before = "" if prefix else _adjacent_char(el, -1)
        after = "" if suffix else _adjacent_char(el, +1)
        if not any(c.isalnum() for c in inner) and (before.isalnum() or after.isalnum()):
            # bold/italic punctuation glued to a word ("top<strong>.</strong>", "Menus<strong>,</strong>"):
            # the delimiters cannot flank, and the emphasis is invisible anyway
            EMPHASIS_STATS["punctuation_only_dropped"] += 1
            return prefix + inner + suffix
        if before.isalnum() and _is_punct(inner[0]):
            # opener would not be left-flanking: move leading plain-text punctuation outside
            lead = re.match(r"[^\w\s\\`\[!<*_]+", inner)
            if lead and _plain_text_edge(el, lead.group(0), first=True):
                rest = inner[lead.end():]
                prefix, inner = lead.group(0) + rest[:len(rest) - len(rest.lstrip())], rest.lstrip()
            else:
                prefix = " "
            EMPHASIS_STATS["opener_fixed"] += 1
        if after.isalnum() and _is_punct(inner[-1]):
            # closer would not be right-flanking: move trailing plain-text punctuation outside
            trail = re.search(r"[^\w\s\\`\]>*_]+$", inner)
            if trail and _plain_text_edge(el, trail.group(0), first=False):
                rest = inner[:trail.start()]
                inner, suffix = rest.rstrip(), rest[len(rest.rstrip()):] + trail.group(0)
            else:
                suffix = " "
            EMPHASIS_STATS["closer_fixed"] += 1
        if not inner.strip():
            return prefix + inner + suffix
        return f"{prefix}{marker}{inner}{marker}{suffix}"

    def convert_pre(self, el, text, parent_tags):
        if not text:
            return ""
        text = text.strip("\n")
        fence = "`" * max(3, max((len(m) for m in re.findall(r"`+", text)), default=0) + 1)
        return f"\n\n{fence}{el.get('data-lang', '')}\n{text}\n{fence}\n\n"

    def convert_mdraw(self, el, text, parent_tags):
        return "\n\n" + el["data-md"] + "\n\n"

    def convert_mdinline(self, el, text, parent_tags):
        return el["data-md"]

    def convert_p(self, el, text, parent_tags):
        out = super().convert_p(el, text, parent_tags)
        if "_inline" in parent_tags:
            return out
        # Paragraph text that merely looks like a list/heading (e.g. "1. foo<br>2. bar")
        # must stay a paragraph in Markdown.
        out = re.sub(r"(?m)^(\s*)(\d+)([.)]) ", r"\1\2\\\3 ", out)
        out = re.sub(r"(?m)^(\s*)([-+*]) ", r"\1\\\2 ", out)
        out = re.sub(r"(?m)^(\s*)(#{1,6}) ", r"\1\\\2 ", out)
        return out

    def convert_figure(self, el, text, parent_tags):
        return "\n\n" + text.strip("\n") + "\n\n"

    def convert_figcaption(self, el, text, parent_tags):
        text = " ".join(text.split())
        if not text:
            return ""
        if "*" in text and "_" not in text:
            return f"\n\n_{text}_\n\n"
        return f"\n\n*{text}*\n\n"

    def convert_img(self, el, text, parent_tags):
        alt = esc_md_text(el.get("alt", ""))
        src = el.get("src", "")
        if el.get("width"):
            return f'<img src="{html.escape(src)}" alt="{html.escape(el.get("alt", ""))}" width="{el["width"]}">'
        title = el.get("title")
        tp = ' "%s"' % title.replace('"', r"\"") if title else ""
        return f"![{alt}]({src}{tp})"

    def convert_a(self, el, text, parent_tags):
        href = el.get("href", "")
        if href and (" " in href or href.count("(") != href.count(")")):
            el["href"] = "<" + href.replace(" ", "%20") + ">"
        # markdownify's <autolink> shortcut is only valid for absolute URLs
        self.options["autolinks"] = bool(re.match(r"^https?://", el.get("href", "")))
        return super().convert_a(el, text, parent_tags)

    def convert_blockquote(self, el, text, parent_tags):
        alert = el.get("data-alert")
        text = (text or "").strip(" \t\r\n")
        if not text:
            return "\n"
        if alert:
            text = f"[!{alert}]\n" + text
        lines = [("> " + ln) if ln.strip() else ">" for ln in text.split("\n")]
        return "\n\n" + "\n".join(lines) + "\n\n"

    def convert_kbd(self, el, text, parent_tags):
        t = text.strip()
        return f"<kbd>{t}</kbd>" if t else ""

    def convert_br(self, el, text, parent_tags):
        if el.find_parent("pre"):
            return "\n" + text
        if el.find_parent(["td", "th"]):
            return "<br>"
        if "_inline" in parent_tags:
            return " "
        # PHP Markdown (Jetpack) has no backslash hard break; trailing double spaces get eaten
        # by editors. An explicit <br> works everywhere.
        return "<br>\n" + text

    def convert_li(self, el, text, parent_tags):
        """List items with 4-space continuation indent: PHP Markdown (Jetpack) needs 4 spaces for
        nested lists / paragraphs inside items; CommonMark accepts it too."""
        text = (text or "").strip()
        if not text:
            return "\n"
        parent = el.parent
        if parent is not None and parent.name == "ol":
            start = int(parent["start"]) if str(parent.get("start", "")).isdigit() else 1
            bullet = "%d." % (start + len(el.find_previous_siblings("li")))
        else:
            bullet = "-"
        bullet = (bullet + " ").ljust(4) if len(bullet) < 3 else bullet + " "
        indent = " " * 4
        lines = text.split("\n")
        out = [bullet + lines[0]] + [(indent + ln) if ln.strip() else "" for ln in lines[1:]]
        return "\n".join(out) + "\n"

    def _cell(self, el, text):
        colspan = 1
        t = text.strip().replace("\n", " ").replace("|", r"\|")
        return " " + t + " |" * colspan

    def convert_td(self, el, text, parent_tags):
        return self._cell(el, text)

    def convert_th(self, el, text, parent_tags):
        return self._cell(el, text)

    def convert_mark(self, el, text, parent_tags):
        return text

    def convert_span(self, el, text, parent_tags):
        return text


CONVERTER = HelpHubConverter()


def postprocess(md):
    md = re.sub(r"(?m)^( *)\u00a0[\u00a0 ]*", r"\1", md)  # leading nbsp would create code blocks
    md = md.replace("\u00a0", " ").replace("\ufeff", "")  # nbsp; stray BOM / zero-width no-break space
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def html_to_md(html_str, ctx):
    soup = prepass(html_str, ctx)
    md = postprocess(CONVERTER.convert_soup(soup))
    # sanity checks on the output
    scan = re.sub(r"```.*?```", "", md, flags=re.S)
    scan = re.sub(r"(`+).+?\1", "", scan)
    leftovers = re.findall(r"<(?!/?(?:kbd|details|summary|sup|sub|br|img|a|table|thead|tbody|tr|td|th|ul|ol|li|p|strong|em|code|b|i|div|video|pre|del|s|!--)\b)[a-z][a-z0-9-]*[\s>]", scan)
    if leftovers:
        ctx.warn(f"unexpected HTML left in output: {sorted(set(l.strip() for l in leftovers))[:5]}")
    return md


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------
class Dumper(yaml.SafeDumper):
    pass


def _str_rep(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, _str_rep)


def write_md(path, fm, title, body):
    """Frontmatter (ignored by the importer) + '# Title' as the very first body line."""
    path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.dump(fm, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000)
    # the importer strips frontmatter with #^---(.+)---#Us (ungreedy): a "---" inside would cut it short
    front = front.replace("---", "- - -")
    title = " ".join(title.split())
    path.write_text(f"---\n{front}---\n\n# {title}\n\n{body}")


def plain(s):
    return " ".join(html.unescape(BeautifulSoup(s or "", "html.parser").get_text(" ")).split())


def convert_article(site, art, placement=None, remove_nav_links=False):
    """Convert one article. `placement` (structure mode only) is {"position": n | None, "index_of": Folder | None};
    without it the output is exactly the category-mode file."""
    slug = art["slug"]
    out = site.path_for_slug[slug]
    ctx = Ctx(site, slug, out)
    body = html_to_md(art["content"]["rendered"], ctx)
    chain = site.primary_chain(art)
    all_cats = [site.cats[c]["slug"] for c in art["category"] if c in site.cats]
    chain_slugs = [c["slug"] for c in chain]
    others = [c for c in all_cats if c not in chain_slugs]
    if others:
        ctx.note(f"also in categories not on primary path: {others}")
    title = plain(art["title"]["rendered"])
    fm = {"title": title, "slug": slug}
    if placement is not None:
        if placement.get("index_of") is not None:
            fm["section"] = True  # this article is the folder's README.md (structure `index:`)
        else:
            fm["position"] = placement["position"]
    fm.update({
        "original_url": art["link"],
        "wp_id": art["id"],
        # top-level first, then sub-category (breadcrumb order)
        ("legacy_categories" if placement is not None else "categories"): chain_slugs + others,
        "date": art["date"],
        "modified": art["modified"],
    })
    if art.get("menu_order"):
        fm["menu_order"] = art["menu_order"]
    if art.get("featured_media"):
        fmed = (art.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0]
        if fmed.get("source_url"):
            local, src, notes = site.asset(fmed["source_url"], slug, kind="image")
            fm["featured_image"] = ctx.rel(local)
    fm["migration"] = migration_block(ctx)
    ctx.body_full = body
    ctx.nav_link_removed = False
    if first_paragraph_is_nav_link(body):
        if remove_nav_links:
            body = strip_first_nav_paragraph(body)
            fm["migration"]["nav_link_removed"] = True
            ctx.nav_link_removed = True
            ctx.counts["nav_link_removed"] += 1
        else:
            # the importer/WordPress would use this as the excerpt; content decision, so only flagged
            fm["migration"]["first_paragraph_is_nav_link"] = True
            ctx.counts["first_paragraph_is_nav_link"] += 1
    ctx.body_final = body
    write_md(out, fm, title, body)
    return ctx


def first_paragraph_is_nav_link(body):
    """True when the first body paragraph is nothing but one link (e.g. "Go back to the list of Blocks")."""
    for block in re.split(r"\n\s*\n", body.strip()):
        b = block.strip()
        if not b or re.fullmatch(r'<a id="[^"]*"></a>', b) or b.startswith("<!--"):
            continue
        return bool(re.fullmatch(r"\[[^\]]+\]\([^)\s]+\)", b))
    return False


def strip_first_nav_paragraph(body):
    """Drop the paragraph that first_paragraph_is_nav_link() matched (anchors/comments before it are kept)."""
    blocks = re.split(r"(\n\s*\n)", body.strip())  # keep separators so the rest is byte-identical
    for i in range(0, len(blocks), 2):
        b = blocks[i].strip()
        if not b or re.fullmatch(r'<a id="[^"]*"></a>', b) or b.startswith("<!--"):
            continue
        assert re.fullmatch(r"\[[^\]]+\]\([^)\s]+\)", b)
        del blocks[i:i + 2]
        break
    return "".join(blocks).strip() + "\n"


def finalize_warnings(ctx):
    """Collapse per-URL external asset warnings into one line per host."""
    ext = collections.Counter()
    keep = []
    for w in ctx.warnings:
        m = re.match(r"^external (image|video|poster) host (\S+):", w)
        if m:
            ext[(m.group(1), m.group(2))] += 1
        else:
            keep.append(w)
    for (kind, host), n in sorted(ext.items()):
        keep.append(f"external {kind}s hotlinked from {host}: {n} (see assets/images-manifest.json)")
    legacy = [w for w in keep if w.startswith("legacy /support/files/")]
    if len(legacy) > 1:
        keep = [w for w in keep if not w.startswith("legacy /support/files/")] + [f"legacy /support/files/ image URLs: {len(legacy)}"]
    ctx.warnings = keep


def migration_block(ctx):
    finalize_warnings(ctx)
    mig = {"status": "warnings" if ctx.warnings else "clean"}
    if ctx.warnings:
        mig["warnings"] = ctx.warnings
    if ctx.info:
        mig["notes"] = ctx.info
    if ctx.videos:
        mig["videos"] = ctx.videos
    c = {k: v for k, v in sorted(ctx.counts.items()) if v}
    if c:
        mig["counts"] = c
    return mig


# Observed live order of sub-categories on the topic landing pages (term meta sort_order, not in REST)
# and of the top-level topics in the local navigation. Everything else: alphabetical by name.
CATEGORY_ORDER = {None: ["wordpress-overview", "technical-guides", "support-guides", "customization"],
                  "wordpress-overview": ["faqs", "where-to-start", "about-wp"]}
STATIC_PAGES = ("site-health", "update-php")


def convert_page(site, page):
    slug = page["slug"]
    out = DOCS / f"{slug}.md"
    ctx = Ctx(site, slug, out)
    body = html_to_md(page["content"]["rendered"], ctx)
    title = plain(page["title"]["rendered"])
    fm = {"title": title, "slug": slug, "original_url": page["link"], "wp_id": page["id"],
          "date": page["date"], "modified": page["modified"]}
    if page.get("template"):
        ctx.note(f"live page uses theme template {page['template']} (chrome-less page)")
    fm["migration"] = migration_block(ctx)
    write_md(out, fm, title, body)
    return ctx


# ---------------------------------------------------------------------------
# Layouts: the folder tree an output is written in. Two sources produce the same shape:
#   category_layout()   today's tree, derived from the HelpHub categories (default)
#   structure_layout()  a hand-designed tree from data/structure.yaml (--structure)
# Everything downstream (READMEs, manifest, move map, metrics) works on a Layout.
# ---------------------------------------------------------------------------
class Folder:
    def __init__(self, parts, title, parent, readme, intro=None, index_slug=None, source="category", cat=None):
        self.parts = list(parts)
        self.key = "/".join(self.parts)
        self.slug = self.parts[-1]
        self.title = title
        self.parent = parent              # Folder or None (top level)
        self.readme = readme              # Path of the folder's README.md
        self.intro = intro                # structure mode: Markdown body of the generated README
        self.index_slug = index_slug      # structure mode: article converted into README.md instead
        self.source = source              # "category" | "structure"
        self.cat = cat                    # category mode: the category dict
        self.children = []                # ordered sub-folders
        self.articles = []                # ordered article slugs (excluding index_slug)

    @property
    def depth(self):
        return len(self.parts)

    def title_chain(self):
        f, chain = self, []
        while f:
            chain.insert(0, f.title)
            f = f.parent
        return chain


class Layout:
    def __init__(self, kind):
        self.kind = kind
        self.top = []                     # ordered top-level Folders
        self.path_for_slug = {}           # slug -> output Path (index articles -> folder README.md)
        self.folder_of = {}               # slug -> Folder
        self.position = {}                # slug -> 1-based position within its folder (None for index articles)
        self.remove_nav_links = False

    def folders(self):
        out = []

        def walk(f):
            out.append(f)
            for c in f.children:
                walk(c)
        for t in self.top:
            walk(t)
        return out


def sort_title(t):
    return t.lower()


def build_tree(site):
    """Return ({category id: [articles]}, has_content(cat)) for the category layout."""
    by_cat = collections.defaultdict(list)
    for a in site.articles:
        chain = site.primary_chain(a)
        by_cat[chain[-1]["id"] if chain else None].append(a)

    def has_content(cat):
        return bool(by_cat.get(cat["id"])) or any(has_content(c) for c in site.cats.values() if c["parent"] == cat["id"])
    return by_cat, has_content


def category_layout(site):
    """Today's tree: non-empty categories as folders (top/sub), articles in their deepest category.

    Order follows the live site: sub-categories by CATEGORY_ORDER then name, articles by
    menu_order DESC, then title ASC (case-insensitive)."""
    by_cat, has_content = build_tree(site)
    lay = Layout("category")

    def cat_children(parent_id):
        kids = [c for c in site.cats.values() if c["parent"] == (parent_id or 0) and has_content(c)]
        pref = CATEGORY_ORDER.get(site.cats[parent_id]["slug"] if parent_id else None, [])
        return sorted(kids, key=lambda c: (pref.index(c["slug"]) if c["slug"] in pref else len(pref), sort_title(c["name"])))

    def add(cat, parent):
        f = Folder([c["slug"] for c in site.cat_chain(cat["id"])], html.unescape(cat["name"]), parent,
                   site.category_index_path(cat), cat=cat)
        f.children = [add(c, f) for c in cat_children(cat["id"])]
        arts = sorted(by_cat.get(cat["id"], []), key=lambda a: (-(a.get("menu_order") or 0), sort_title(plain(a["title"]["rendered"]))))
        f.articles = [a["slug"] for a in arts]
        for i, s in enumerate(f.articles, 1):
            lay.folder_of[s], lay.position[s] = f, i
            lay.path_for_slug[s] = site.category_path_for_slug[s]
        return f
    lay.top = [add(c, None) for c in cat_children(None)]
    return lay


SECTION_KEYS = {"slug", "title", "intro", "children", "articles", "index"}
TOP_KEYS = {"version", "remove_nav_links", "sections"}


def structure_layout(site, path):
    """Load and validate a structure file (schema: README "Structure mode and before/after").

    Returns (Layout, warnings). Every error is collected first; on any error the offending slugs are
    printed and the process exits with status 2 before anything is written."""
    errors, warnings = [], []
    try:
        data = yaml.safe_load(pathlib.Path(path).read_text())
    except (OSError, yaml.YAMLError) as e:
        sys.exit(f"structure: cannot read {path}: {e}")
    if not isinstance(data, dict):
        sys.exit(f"structure: {path} is not a mapping")
    if data.get("version") != 1:
        errors.append(f"version must be 1 (got {data.get('version')!r})")
    unknown = set(data) - TOP_KEYS
    if unknown:
        errors.append(f"unknown top-level keys: {sorted(unknown)}")
    lay = Layout("structure")
    lay.remove_nav_links = bool(data.get("remove_nav_links", False))
    placed = collections.defaultdict(list)  # slug -> [folder keys]
    raw_slugs = {a["slug"] for a in site.articles}
    reserved_top = {"assets"} | set(STATIC_PAGES) | {"manifest"}

    def build(node, parent, where):
        if not isinstance(node, dict):
            errors.append(f"{where}: section must be a mapping, got {type(node).__name__}")
            return None
        slug = node.get("slug")
        label = f"{where}/{slug}" if where else str(slug)
        if not isinstance(slug, str) or not slug:
            errors.append(f"{where or '<top>'}: section without a slug")
            return None
        if sanitize_title(slug) != slug:
            errors.append(f"{label}: slug is not sanitize_title-clean (expected '{sanitize_title(slug)}')")
        if parent is None and slug in reserved_top:
            errors.append(f"{label}: top-level slug '{slug}' is reserved (assets/, static pages)")
        bad = set(node) - SECTION_KEYS
        if bad:
            errors.append(f"{label}: unknown keys {sorted(bad)}")
        index = node.get("index")
        title, intro = node.get("title"), node.get("intro")
        if index is not None:
            if not isinstance(index, str):
                errors.append(f"{label}: index must be an article slug")
                index = None
            else:
                placed[index].append(label + " (index)")
                if title is not None or intro is not None:
                    warnings.append(f"{label}: title/intro ignored because index '{index}' is set")
        if index is None and not (isinstance(title, str) and title.strip()):
            errors.append(f"{label}: title is required when index is not set")
        if index in site.art_by_slug:
            title = plain(site.art_by_slug[index]["title"]["rendered"])
            intro = None
        parts = (parent.parts if parent else []) + [slug]
        f = Folder(parts, " ".join(str(title or slug).split()), parent, CONTENT.joinpath(*parts, "README.md"),
                   intro=intro if isinstance(intro, str) else ("" if intro is None else str(intro)),
                   index_slug=index if index in raw_slugs else None, source="structure")
        arts = node.get("articles") or []
        if not isinstance(arts, list) or not all(isinstance(a, str) for a in arts):
            errors.append(f"{label}: articles must be a list of slugs")
            arts = [a for a in arts if isinstance(a, str)] if isinstance(arts, list) else []
        for a in arts:
            placed[a].append(label)
        f.articles = [a for a in arts if a in raw_slugs]
        kids = node.get("children") or []
        if not isinstance(kids, list):
            errors.append(f"{label}: children must be a list")
            kids = []
        f.children = [c for c in (build(k, f, label) for k in kids) if c]
        seen = collections.Counter(c.slug for c in f.children)
        for s, n in seen.items():
            if n > 1:
                errors.append(f"{label}: duplicate child section slug '{s}'")
        clash = sorted({c.slug for c in f.children} & set(arts))
        if clash:
            errors.append(f"{label}: article slug(s) equal a sibling section slug (manifest key collision): {clash}")
        if not f.children and not arts and index is None:
            warnings.append(f"{label}: empty section (no articles, children or index)")
        return f

    secs = data.get("sections")
    if not isinstance(secs, list) or not secs:
        errors.append("sections must be a non-empty list")
        secs = []
    lay.top = [f for f in (build(s, None, "") for s in secs) if f]
    tops = collections.Counter(f.slug for f in lay.top)
    errors += [f"duplicate top-level section slug '{s}'" for s, n in tops.items() if n > 1]

    unknown_slugs = sorted(s for s in placed if s not in raw_slugs)
    dupes = {s: locs for s, locs in placed.items() if len(locs) > 1 and s in raw_slugs}
    missing = sorted(raw_slugs - set(placed))
    if unknown_slugs:
        errors.append(f"{len(unknown_slugs)} unknown article slug(s) (not in raw/articles.json): " + ", ".join(
            f"{s} [{'; '.join(placed[s])}]" for s in unknown_slugs))
    if dupes:
        errors.append(f"{len(dupes)} article slug(s) placed more than once: " + ", ".join(
            f"{s} [{'; '.join(l)}]" for s, l in sorted(dupes.items())))
    if missing:
        errors.append(f"{len(missing)} article slug(s) not placed anywhere: " + ", ".join(missing))
    if errors:
        print(f"structure: {path}: {len(errors)} error(s); nothing written", file=sys.stderr)
        for e in errors:
            print(f"  ERROR {e}", file=sys.stderr)
        for w in warnings:
            print(f"  warning {w}", file=sys.stderr)
        sys.exit(2)

    for f in lay.folders():
        if f.index_slug:
            lay.folder_of[f.index_slug], lay.position[f.index_slug] = f, None
            lay.path_for_slug[f.index_slug] = f.readme
        for i, s in enumerate(f.articles, 1):
            lay.folder_of[s], lay.position[s] = f, i
            lay.path_for_slug[s] = CONTENT.joinpath(*f.parts, f"{s}.md")
    folder_slugs = {f.slug for f in lay.folders()}
    rep = sorted(f"{s} ({n}x)" for s, n in collections.Counter(f.slug for f in lay.folders()).items() if n > 1)
    if rep:
        warnings.append(f"section slug(s) used more than once in the tree (importer slug_only fallback can mis-match): {rep}")
    same = sorted(folder_slugs & raw_slugs - {f.index_slug for f in lay.folders() if f.index_slug == f.slug})
    if same:
        warnings.append(f"section slug(s) equal to an article slug (importer slug_only fallback can mis-match): {same}")
    return lay, warnings


def category_link_targets(site, lay):
    """Structure mode: where a /documentation/category/<slug>/ link should point.

    The deepest folder that contains every article of the category (and its sub-categories); if that is
    the root, the folder holding most of them. Returns {category id: README path}."""
    targets = {}
    for cid, cat in site.cats.items():
        folders = [lay.folder_of[a["slug"]] for a in site.articles
                   if any(c["id"] == cid for c in site.primary_chain(a))]
        if not folders:
            targets[cid] = DOCS / "README.md"
            continue
        common = folders[0].parts
        for f in folders[1:]:
            n = 0
            while n < min(len(common), len(f.parts)) and common[n] == f.parts[n]:
                n += 1
            common = common[:n]
        if not common:
            common = collections.Counter(tuple(f.parts) for f in folders).most_common(1)[0][0]
        targets[cid] = CONTENT.joinpath(*common, "README.md")
    return targets


# ---------------------------------------------------------------------------
# Folder READMEs and the importer manifest
# ---------------------------------------------------------------------------
def write_root_readme():
    write_md(DOCS / "README.md",
             {"title": "WordPress Documentation", "original_url": "https://wordpress.org/documentation/",
              "migration": {"status": "generated", "notes": ["repository index; the live front page is a theme pattern and is not imported"]}},
             "WordPress Documentation",
             "We've got a variety of resources to help you get the most out of WordPress.\n")


def write_category_readmes(site):
    by_cat, has_content = build_tree(site)
    written = 0
    for cat in site.cats.values():
        if not has_content(cat):
            continue
        path = site.category_index_path(cat)
        name = html.unescape(cat["name"])
        fm = {"title": name, "slug": cat["slug"], "original_url": cat["link"], "wp_category_id": cat["id"],
              "migration": {"status": "generated",
                            "notes": ["folder index generated from the category; the live landing/archive page is theme-generated"]}}
        desc = plain(cat.get("description", ""))
        write_md(path, fm, name, (desc + "\n") if desc else "")
        written += 1
    write_root_readme()
    return written


def write_section_readmes(lay):
    """Structure mode: README.md per folder from title + intro (index sections are written by convert_article)."""
    written = 0
    for f in lay.folders():
        if f.index_slug:
            continue
        intro = (f.intro or "").strip()
        write_md(f.readme, {"title": f.title, "section": True}, f.title, (intro + "\n") if intro else "")
        written += 1
    write_root_readme()
    return written


def build_manifest(site, lay):
    """docs/manifest.json in wporg-markdown Importer format, keyed by URL path below the base.

    Keys mirror the folder tree. Parents are the folder README entries. Within a folder the sub-folders
    come first, then the articles; `order` counts both (so article order = sub-folder count + position)."""
    manifest = {}

    def add_folder(f, order):
        manifest[f.key] = {"title": f.title, "slug": f.slug,
                           "markdown_source": posix_rel(f.readme, DOCS / "manifest.json"),
                           "parent": f.parent.key if f.parent else None, "order": order}
        n = 0
        for child in f.children:
            n += 1
            add_folder(child, n)
        for s in f.articles:
            n += 1
            a = site.art_by_slug[s]
            manifest[f"{f.key}/{s}"] = {"title": plain(a["title"]["rendered"]), "slug": s,
                                        "markdown_source": posix_rel(lay.path_for_slug[s], DOCS / "manifest.json"),
                                        "parent": f.key, "order": n}

    n = 0
    for top in lay.top:
        n += 1
        add_folder(top, n)
    for slug in STATIC_PAGES:
        n += 1
        page = next(p for p in site.pages if p["slug"] == slug)
        manifest[slug] = {"title": plain(page["title"]["rendered"]), "slug": slug,
                          "markdown_source": f"{slug}.md", "parent": None, "order": n}
    return manifest


def build_move_map(site, before, after, nav_removed):
    """data/restructure-map.json: one entry per article, category layout -> structure layout.
    Paths are relative to the output root (docs/)."""
    rows = []
    for a in site.articles:
        s = a["slug"]
        fb, fa = before.folder_of[s], after.folder_of[s]
        rows.append({
            "slug": s,
            "title": plain(a["title"]["rendered"]),
            "before_path": posix_rel(before.path_for_slug[s], DOCS / "x"),
            "after_path": posix_rel(after.path_for_slug[s], DOCS / "x"),
            "before_section": fb.title_chain(),
            "after_section": fa.title_chain(),
            "before_depth": fb.depth,
            "after_depth": fa.depth,
            "position_after": after.position[s],
            "after_is_section_index": fa.index_slug == s,
            "nav_link_removed": bool(nav_removed.get(s)),
        })
    return rows


def layout_summary(site, lay):
    """Plain-dict view of a Layout for scripts/structure_metrics.py (paths relative to the output root)."""
    folders = [{"key": f.key, "title": f.title, "parent": f.parent.key if f.parent else None, "depth": f.depth,
                "top": f.parts[0], "articles": list(f.articles), "index_slug": f.index_slug,
                "hand_written": f.source == "structure"}
               for f in lay.folders()]
    arts = {s: {"title": plain(site.art_by_slug[s]["title"]["rendered"]), "folder": f.key, "top": f.parts[0],
                "depth": f.depth, "path": posix_rel(lay.path_for_slug[s], DOCS / "x")}
            for s, f in lay.folder_of.items()}
    return {"kind": lay.kind, "top": [{"key": f.key, "title": f.title} for f in lay.top],
            "folders": folders, "articles": arts}


def load_sibling(name):
    """Import scripts/<name>.py by path (python -I does not put the script directory on sys.path)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, pathlib.Path(__file__).resolve().parent / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def set_output_root(path):
    global DOCS, CONTENT, ASSETS
    DOCS = CONTENT = path
    ASSETS = path / "assets"


def prepare_output_root():
    """Wipe the generated Markdown/manifests in the output root, but keep assets/: the image/video files in
    docs/assets/ are fetched by scripts/download_assets.py (~1.7 GB) and are not regenerated here.
    A non-default output root gets assets -> docs/assets as a relative symlink, so the Markdown's
    ../../assets/... paths resolve exactly as they do in docs/ and docs/assets is never written to."""
    out = DOCS.resolve()
    canon = CANON_DOCS.resolve()
    if out in canon.parents or out == ROOT:
        sys.exit(f"--out {out}: refusing to wipe a directory that contains docs/ or the repository")
    if out != canon and canon in out.parents:
        sys.exit(f"--out {out}: must not be inside docs/")
    if out.exists():
        for child in out.iterdir():
            if child.name == "assets":
                continue
            shutil.rmtree(child) if child.is_dir() and not child.is_symlink() else child.unlink()
    out.mkdir(parents=True, exist_ok=True)
    if out != canon:
        link = out / "assets"
        if not link.exists() and not link.is_symlink():
            link.symlink_to(os.path.relpath(CANON_ASSETS, out), target_is_directory=True)
        elif not link.is_symlink():
            print(f"note: {link} is a real directory, not a symlink to docs/assets; images resolve against it")


def main():
    global CALLOUT_STYLE, VIDEO_SRC
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="convert only these article slugs")
    ap.add_argument("--callout-style", choices=["gutenberg", "gfm-alert"], default=CALLOUT_STYLE)
    ap.add_argument("--out", help="output directory (default: docs/). Outside docs/ it gets an assets -> docs/assets symlink")
    ap.add_argument("--video-src", choices=["remote", "local"], default=VIDEO_SRC,
                    help="self-hosted <video src>: original wordpress.org URL (default) or local docs/assets path")
    ap.add_argument("--structure", help="structure file (e.g. data/structure.yaml): lay the tree out by it instead of by category; "
                                        "also writes data/restructure-map.json and data/structure-metrics.json")
    ap.add_argument("--check-structure", action="store_true", help="validate --structure and exit without writing")
    args = ap.parse_args()
    CALLOUT_STYLE = args.callout_style
    VIDEO_SRC = args.video_src
    if args.out:
        set_output_root(pathlib.Path(args.out).resolve())

    site = Site()
    before = category_layout(site)
    lay = before
    if args.structure:
        lay, swarn = structure_layout(site, args.structure)
        for w in swarn:
            print(f"structure warning: {w}")
        print(f"structure: {args.structure} OK: {len(lay.folders())} sections, {len(lay.folder_of)} articles placed, "
              f"remove_nav_links={lay.remove_nav_links}")
        if args.check_structure:
            return
        site.path_for_slug = dict(lay.path_for_slug)
        site.category_link_paths = category_link_targets(site, lay)
    elif args.check_structure:
        sys.exit("--check-structure needs --structure")
    if not args.only:
        prepare_output_root()
    report = {"callout_style": CALLOUT_STYLE, "articles": {}, "pages": {}}
    if args.structure:
        report = {"callout_style": CALLOUT_STYLE, "layout": "structure", "structure_file": args.structure,
                  "articles": {}, "pages": {}}
    arts = [a for a in site.articles if not args.only or a["slug"] in args.only]
    ctxs = {}
    for a in arts:
        placement = None
        if args.structure:
            f = lay.folder_of[a["slug"]]
            placement = {"position": lay.position[a["slug"]], "index_of": f if f.index_slug == a["slug"] else None}
        ctx = convert_article(site, a, placement, remove_nav_links=bool(args.structure) and lay.remove_nav_links)
        ctxs[a["slug"]] = ctx
        report["articles"][a["slug"]] = {"path": os.path.relpath(ctx.out, ROOT), "warnings": ctx.warnings,
                                         "notes": ctx.info, "counts": dict(ctx.counts)}
    if not args.only:
        for p in site.pages:
            if p["slug"] not in STATIC_PAGES:
                continue  # front page + 4 empty landing pages are theme-generated (notes/site-structure.md)
            ctx = convert_page(site, p)
            report["pages"][p["slug"]] = {"path": os.path.relpath(ctx.out, ROOT), "warnings": ctx.warnings,
                                          "notes": ctx.info}
        if args.structure:
            report["section_readmes"] = write_section_readmes(lay)
        else:
            report["category_readmes"] = write_category_readmes(site)
        manifest = build_manifest(site, lay)
        (DOCS / "manifest.json").write_text(json.dumps(manifest, indent="\t") + "\n")
        if DOCS.resolve() == CANON_DOCS.resolve():
            ASSETS.mkdir(parents=True, exist_ok=True)
            assets = sorted(site.manifest.values(), key=lambda e: e["local_path"])
            (ASSETS / "images-manifest.json").write_text(json.dumps(assets, indent=1))
        if DATA.exists() and not args.out:
            (DATA / "convert-report.json").write_text(json.dumps(report, indent=1))
        if args.structure:
            structure_metrics = load_sibling("structure_metrics")
            nav_removed = {s: c.nav_link_removed for s, c in ctxs.items()}
            move_map = build_move_map(site, before, lay, nav_removed)
            (DATA / "restructure-map.json").write_text(json.dumps(move_map, indent=1, ensure_ascii=False) + "\n")
            # link graph: both body variants were written for the structure layout's paths
            out_paths = {s: posix_rel(p, DOCS / "x") for s, p in lay.path_for_slug.items()}
            metrics = structure_metrics.compute(
                before=layout_summary(site, before), after=layout_summary(site, lay),
                bodies_before={s: c.body_full for s, c in ctxs.items()},
                bodies_after={s: c.body_final for s, c in ctxs.items()},
                link_paths=out_paths, structure_file=args.structure)
            (DATA / "structure-metrics.json").write_text(json.dumps(metrics, indent=1, ensure_ascii=False) + "\n")
            print(f"move map: data/restructure-map.json ({len(move_map)} articles); metrics: data/structure-metrics.json")
            structure_metrics.print_summary(metrics)

    # summary
    warn_types = collections.Counter()
    for r in report["articles"].values():
        for k in {re.split(r"[:;(]", w)[0].strip() for w in r["warnings"]}:
            warn_types[k] += 1
    n = len(report["articles"])
    clean = sum(1 for r in report["articles"].values() if not r["warnings"])
    print(f"callout style: {CALLOUT_STYLE}")
    print(f"articles: {n}  clean: {clean}  with warnings: {n - clean}")
    print("articles affected per warning type:")
    for k, v in warn_types.most_common():
        print(f"  {v:4d}  {k}")
    if not args.only:
        kinds = collections.Counter(e["kind"] for e in site.manifest.values())
        readmes = report.get("category_readmes", report.get("section_readmes"))
        print(f"output: {os.path.relpath(DOCS, ROOT)}  layout: {lay.kind}")
        print(f"asset manifest entries: {len(site.manifest)} {dict(kinds)}; "
              f"{'section' if args.structure else 'category'} READMEs: {readmes}; "
              f"pages: {len(report['pages'])}; importer manifest entries: {len(manifest)}")


if __name__ == "__main__":
    main()
