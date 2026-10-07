# Converter notes (HelpHub HTML → Markdown)

Status as of 2026-10-07. The target is the **wporg-markdown Importer** (the Block Editor handbook
pipeline, `notes/reference/wporg-markdown/`). The conventions are in `notes/markdown-conventions.md`.

## How to run

```sh
python3 -m venv .venv && .venv/bin/pip install beautifulsoup4 markdownify pyyaml markdown-it-py
python3 -I scripts/resolve_redirects.py          # once: stale slugs -> data/redirects.json (HEAD requests)
.venv/bin/python -I scripts/convert.py            # -> docs/ (wipes and rebuilds it)
.venv/bin/python -I scripts/convert.py --callout-style gfm-alert --out /tmp/docs-gfm   # comparison build
.venv/bin/python -I scripts/check_links.py        # links, anchors, importer constraints, manifest
.venv/bin/python -I scripts/qa_textdiff.py        # text/structure fidelity vs the WP HTML (markdown-it)
php scripts/jetpack_render.php $JP docs $OUT && .venv/bin/python -I scripts/qa_textdiff.py --rendered $OUT
                                                  # same check through the real Jetpack parser (setup in the file header)
```

Outputs:

- `docs/<top>/<sub>/<slug>.md`: 321 articles.
- `docs/**/README.md`: 24 category folder indexes plus the repository root.
- `docs/site-health.md` and `docs/update-php.md`.
- `docs/manifest.json`: importer manifest, 347 entries.
- `docs/assets/images-manifest.json`: 2,558 assets (source URL → local path), for the separate download step. **Nothing is downloaded yet.**
- `data/convert-report.json`: per-file warnings, notes and counters.
- `data/link-check.json`, `data/qa-*.json`.

## Approach chosen: BeautifulSoup pre-pass + markdownify subclass

| Option | Verdict |
|---|---|
| pandoc | Not installed. Its GFM writer keeps unknown `div`/`figure` as raw HTML and needs Lua filters for every WordPress-specific rule (callouts, VideoPress, srcset originals, link resolution). It is also another binary to install. |
| html2text | Fast, but hard to extend. It glues figure captions onto images, puts odd spaces around emphasis, and drops `<video>`. |
| markdownify alone | Good baseline output and every tag has an overridable `convert_*` hook. But by itself it mangles WordPress paste artefacts. |
| **BS4 pre-pass + markdownify subclass (chosen)** | The pre-pass rewrites WordPress semantics in the DOM: callouts, videos, embeds, images and assets, link resolution, anchors, complex tables, details, emphasis clean-up. The subclass controls the Markdown dialect (4-space list indent, `<br>`, escaping, tables, fences). It is all Python, about 1,200 lines, and runs over 323 docs in about 3 s. |

## Output conventions (importer-driven)

- **File:** YAML frontmatter, then `# Title` as the first line, then the body.
  - The importer strips frontmatter with `#^---(.+)---#Us` (ungreedy), so any `---` inside frontmatter is rewritten to `- - -`.
  - The importer takes the title from `/^#\s(.+)/`.
  - In-body H1s are demoted to H2. There are none in the articles.
- **Frontmatter** (ignored on import): `title`, `slug`, `original_url`, `wp_id`, `categories` (top-level first, then sub-category, in breadcrumb order), `date`, `modified`. Some files also have `menu_order` (13 default-theme articles) and `featured_image` (2).
  - There is also a `migration:` block with `status` (clean/warnings), `warnings`, `notes`, `videos` (VideoPress guid, original file, poster) and `counts`. **Delete this block after review.**
- **Callouts:** all callout syntax is decided by one function, `emit_callout()`, switched by `CALLOUT_STYLE` or `--callout-style`.
  - The default `gutenberg` mode emits `<div class="callout callout-info|tip|warning|alert">` with **HTML** inside, because Jetpack does not parse Markdown inside HTML blocks. The visible "Note:" label is kept in this mode.
  - `gfm-alert` emits `> [!NOTE]` / `[!TIP]` / `[!WARNING]` / `[!CAUTION]` and strips the "Note:" label.
  - Jetpack renders `[!NOTE]` as literal text in a blockquote, so this mode needs an importer filter.
  - Which elements become callouts, and with which kind, is described in content-audit §2.
- **Headings and anchors:** after import, the live TOC (`wporg/table-of-contents`) generates ids with `sanitize_title(text)` and `-2`/`-3` de-duplication. The converter ports that rule (`sanitize_title()`, `unique_id()` in convert.py).
  - Where the old live id (an explicit `id`, or the de-dupe order) differs from what the new TOC will generate, an `<a id="old-id"></a>` line is emitted before the heading. There are 507 of these.
  - Ids on non-heading elements that some link targets are kept the same way (36).
- **Links:** internal links become relative `.md` links, with the fragment kept.
  - `/support/article/*` links, both relative and absolute, are resolved by slug.
  - Stale slugs are resolved through `data/redirects.json`. 40 go to existing articles. 33 moved to developer.wordpress.org/advanced-administration and are rewritten to the new URL.
  - Category links point to the folder `README.md`.
  - Release-page links stay absolute (1,369).
  - `/documentation/files/*` links point to the local asset.
- **Images:** `![alt](../../assets/images/YYYY/MM/file.png)`, mirroring `/documentation/files/YYYY/MM/`. The converter picks the **unsized original** when it is known to exist (585 cases).
  - Captions go on a separate `*italic*` line under the image.
  - Images that are deliberately small (resized to ≤240 px, 40 of them) stay as `<img … width="N">`.
  - Links that only point at the image file itself are dropped (116).
  - External images are mapped to `docs/assets/images/external/<host>/<hash>-<name>`.
- **Video:**
  - VideoPress, YouTube and iframes are emitted as `<!-- VideoPress embed (iframe removed): … -->`, a blank line, then the bare `https://videopress.com/v/<guid>` URL in its own paragraph. WordPress auto-embeds this; kses would strip an iframe.
  - Self-hosted video becomes `<video controls preload="metadata" src="../../assets/videos/…"></video>`, which kses allows. The file is added to the asset manifest.
  - The VideoPress originals (`videos.files.wordpress.com/<guid>/<file>.mov`) and posters are also in the manifest, matched via the media library guid, in case we ever want to self-host them.
- **Lists:** 4-space continuation indent, because PHP Markdown needs it for nesting. CommonMark accepts it too.
- **Line breaks:** `<br>` followed by a newline. Jetpack has no backslash breaks, and editors eat trailing double spaces.
- **Tables:** GFM. Cells with `<br>` become inline `<br>` and `|` is escaped. A bold first row becomes the header (13 tables). Tables with no header get an empty header row (13). `colspan`/`rowspan` or block content keeps the table as cleaned raw HTML (1 table).
- **Code:** fenced, with a language from `language-*` or SyntaxHighlighter `brush:` classes when present (only a handful). `<br>` inside `<pre>` becomes a newline.
- **Escaping:** `*`, `` ` ``, and leading `1.`, `-` and `#` in paragraphs are escaped. Text that looks like HTML or entities (`<h1>`, `&amp;copy;`) becomes `&lt;` / `&amp;`. Underscores are not escaped, because PHP Markdown Extra and GFM both ignore intraword `_`.
- **Details:** `<details><summary>` as raw HTML, with HTML inside (2 articles).
- **Dropped:** classes and inline styles, srcset/sizes/loading/decoding, `wp-image-*`, lightbox buttons and SVG, VideoPress and embed scripts, spacers, layout wrappers (groups, columns, media-text), and background colours on non-callout paragraphs (23 swatches).
- **Manifest:** keys are `top/sub/slug`, and the category `README.md` entries are the parents.
  - Order is `menu_order DESC, title ASC`, the same as the live site. Default themes come out newest first, then changelogs alphabetically.
  - Sub-category order follows the observed live `sort_order` for Overview (FAQs, Where to start, About WordPress). The other folders are alphabetical. Top-level folders follow the nav order.

## Results

| | v1 (GFM target, `content/`) | **v2 (importer target, `docs/`)** |
|---|---|---|
| Articles converted | 321 | 321 |
| Clean (no warnings) | 243 | **244** |
| With warnings | 78 | **77** |

Articles affected per warning type (v2):

| Articles | Warning |
|---|---|
| 38 | VideoPress embed, now a bare oEmbed URL. Verify that it auto-embeds after import |
| 29 | External images hotlinked: googleusercontent.com in 18, user-images.githubusercontent.com in 7, codex.wordpress.org in 2, support.files.wordpress.com in 1, a signed private GitHub URL that is already 404 in 1, and a `wp-includes` smiley in 1 |
| 2 | `<pre>` with links inside: the URLs are lost in the fence (`use-character-entities`, `video-shortcode`) |
| 2 | Unresolved article link, which is also 404 on the live site (`weblog-client`, `wordpress-lessons`) |
| 1 each | X embed, Bluesky embed, MathML (→ `$TeX$`), complex raw-HTML table, odd relative link (`keyboard-shortcuts-block-editor`, a `href` without `#`), external video (news/files, GitHub), fake videos in `video-shortcode` (a content bug) |

The only change between v1 and v2 is that legacy `/support/files/` video URLs are now a note rather than a warning, because they still resolve.

### Fidelity checks

These cover all 321 articles.

- **Text:** a word-sequence ratio of source HTML vs. converted output, rendered both with markdown-it and with the **real Jetpack `WPCom_GHF_Markdown_Parser`** (`scripts/jetpack_render.php`).
  - Median 1.000. 318/321 score ≥ 0.99 and none score below 0.95.
  - The 3 lowest are `bluesky-embed` and `twitter-embed`, where the quoted post text is replaced by the oEmbed URL, and `video-shortcode`, which loses its fake players.
- **Structure:** counts of headings, list items, images, links, `<pre>` and table rows, comparing Jetpack HTML with the source HTML. 10 articles differ, all explained:
  - +1 table row where an empty header row was added (6 articles).
  - Empty `<li></li>` dropped (3).
  - Links inside `<pre>` (1).
  - `video-shortcode` fake players (1).
- **Links** (`check_links.py`): 5,328 relative links and images resolve. 1 broken relative link exists in the source (`create-group-block-from-selected-multiple-blocks`). 43 fragment links are not found, and **all 43 are already broken on the live site** when checked with the live TOC id rule, so there are 0 regressions.
- **Importer checks:** every file starts with `# Title`, has exactly one H1, and has frontmatter that is safe for the importer regex. There are no iframes outside code. Every manifest source exists, every parent exists, and every slug is `sanitize_title`-clean. The one duplicate slug is noted below.
- **Assets:** HEAD-checked 7 URLs from the manifest:
  - an original that was chosen over a sized variant
  - a legacy `/support/files/` URL (also served under `/documentation/files/`)
  - a googleusercontent image
  - a self-hosted .mov
  - a VideoPress original `.mov`

  All returned 200. The signed `private-user-images.githubusercontent.com` URL returned **404**.

## Manual QA: 5 hard articles vs. the rendered HTML

1. **`customize-date-and-time-format`** (tables, the only colspan table)
   - The format-character table has `<th colspan=3>` section rows and per-cell `text-align`. It stays as cleaned raw HTML (no attributes except colspan), which renders the same in Jetpack and on GitHub.
   - Code samples become unlabelled fences. The callouts are info boxes.
   - *Issue:* alignment styling is lost, which is acceptable.
2. **`zoom-out-view`** (VideoPress and callouts)
   - Two VideoPress blocks become comment + bare `videopress.com/v/…` URL, and the Jetpack output is `<p>URL</p>`, which `WP_Embed::autoembed` handles.
   - Three `#e5f5fa` boxes become `callout-info`. The changelog is a normal `## Changelog` list.
   - The VideoPress guids, originals and posters are in `migration.videos`.
   - *Issue:* on GitHub the video is just a link.
3. **`buttons-block`** (17 images, 18 callouts, a self-hosted video)
   - All screenshots map to their unsized originals. `<video>` becomes local-src HTML. The "Learn more" boxes become `callout-info`, with the link kept as a relative `.md` HTML link.
   - The explicit heading id `block-toolbar-for-entire-block` differs from the TOC id `block-toolbar`, so it is preserved as `<a id>`.
   - *Issue:* most callouts here are "Learn more →" links, not notes, so a lighter "see also" style might suit them better.
4. **`query-total-block`** (Theme blocks)
   - The `div.callout.callout-info` inline-styled box becomes a callout. The Photon and sized images become originals. The heading structure (h2/h3 per toolbar button) is preserved.
   - The "Go to the list of Blocks" link becomes `../block-editor/blocks-list.md`, resolved via the 301 from `blocks`.
   - *Issue:* that link is the first paragraph, so it becomes the WordPress excerpt (73 block articles share this).
5. **`faq-installation`** (FAQ)
   - The quoted IIS error stays a Markdown blockquote. `brush: php` code becomes ```` ```php ````.
   - Links to legacy `/support/article/ftp-clients/` and `using-filezilla` are rewritten to their new developer.wordpress.org advanced-administration URLs (via the 301 map).
   - h3 questions under h2 sections are kept.
   - *Issue:* none found.

I also checked:

- `twenty-twenty-one`: `<details>` font list as raw HTML. Theme colour-swatch paragraphs are no longer turned into callouts.
- `keyboard-shortcuts-block-editor`: nested `<strong>`, `<p id>` anchor targets, and 10 header-less tables.
- `use-character-entities`: literal entities are escaped correctly.
- `keyboard-shortcuts-classic-editor`: `<br>` inside `<pre>`.
- `reset-your-password`: 3-level mixed lists render correctly in Jetpack.

## Known issues / not done

- **Videos on GitHub** show only as links (VideoPress URL, or a `<video>` that GitHub strips). There is no poster image inline.
- **The excerpt** will be the first line. For 73 block articles that is "Go back to the list of Blocks". This needs either an importer filter or moving that link below the intro.
- **Resized images over 240 px** lose their display width, which is fine for screenshots. Floats and alignment (`alignright`, 51) are lost.
- **External hotlinked images** (125 files in 29 articles, including the wp-includes smiley) need downloading. The 84 googleusercontent images have no extension, so the downloader must sniff the content type (they are mapped to `*.img` for now).
- **The asset paths are relative to the repo** (`../../assets/…`). After import they only work if the HelpHub importer subclass rewrites them, either to the existing `/documentation/files/…` URLs (possible because the path mirrors them) or to sideloaded attachments.
- **MathML** in `math-block` becomes `$…$`. Jetpack's own LaTeX syntax is `$latex …$`. Check this by hand.
- **Code language hints** are almost always absent in the source (most `<pre>` are `wp-block-preformatted`). Fences are mostly unlabelled.
- **Duplicate slug `site-editor`:** both a category folder and an article (`customization/appearance/site-editor`). The keys are unique, but the importer's `slug_only` fallback lookup could match the wrong post when updating.
- **Empty `<li>`** items and the source's broken fragments (43) are carried over as they are.
- `README.md` folder pages contain only H1 + description. Only Theme blocks has a description. The live landing-page listings (10 per section, "Show all") are theme logic and are not reproduced.

## Open questions for a human

1. **URL scheme / hierarchy.** The manifest uses `top/sub/slug` keys with category READMEs as parents. This is a placeholder: HelpHub URLs are flat (`/documentation/article/<slug>/`) and use categories, not parent pages. Either a HelpHub importer subclass ignores `parent` and assigns categories (no redirects), or we switch to hierarchical URLs and add 321+ redirects. **Undecided.**
2. **Callout style.** `gutenberg` (HTML, works with no importer change, ugly to edit) or `gfm-alert` (`> [!NOTE]`, nice on GitHub, needs a ~10-line importer filter). Also: should "Learn more" link boxes (about a third of callouts) be callouts at all?
3. **Video.** Should VideoPress become bare oEmbed URLs (current), should we download the 50 VideoPress originals and self-host them as `<video>`, or should we add a shortcode? Also: self-hosted `.mov` files (40) may not play in all browsers.
4. **Images.** Keep them in the repo (reviewable, needs sideloading on import), or point at the existing wordpress.org media URLs (zero work, but screenshots can't be updated via PR)? What about the ~4,400 unreferenced media items?
5. **Multi-category articles.** Not a real problem: every article's categories are a parent+child pair (4 have only one), so the deepest category is unambiguous.
6. **Release pages (935).** Recommendation: treat them as a separate structured data set, not as docs pages. See content-audit §7.
7. **Changelog sections** (184 articles): keep them in the body, or drop them in favour of git history?
8. **Feedback form replacement** ("Was this article helpful?"): an "Edit on GitHub" or issue link?

## 2026-10-07 fixes

These came from a review of the rendered output. Default callout style is still `gfm-alert`.

- **Rebuilds keep `docs/assets/`.** `convert.py` used to `rmtree(docs/)`, which would have deleted the ~1.7 GB of downloaded assets. It now wipes everything except `docs/assets/` (and rewrites `images-manifest.json`).
- **Bold/italic that did not render** (`**None –**removes`, `**Undo:**Undo`, `top**.**`). The cause was `<strong>Undo:&nbsp;</strong>`: markdownify only moves plain spaces outside the markers, not `&nbsp;`. The fix is a custom emphasis emitter (`HelpHubConverter._emphasis`):
  - All edge whitespace goes outside the markers.
  - If the closer would sit between punctuation and a letter, the plain-text punctuation moves outside (`**Undo**:Undo`). When that is not possible (the content ends in a link or code), a space is added. The opener gets the mirror-image rule.
  - Emphasis on punctuation alone that touches a word (`Menus<strong>,</strong>`) is dropped. Standalone symbol emphasis such as `**⇧ + ⌘ + ,**` is kept.
  - Stray U+FEFF characters are removed.
  - Checked with markdown-it (CommonMark): 76 unrendered `*`/`**` in 20 files went to 0.
- **`<pre>` is now verbatim.** `freeze_preformatted()` runs first and collapses each `<pre>` to plain text, so later steps cannot rewrite anything inside it.
  - **`video-shortcode`:** its source has real `<video class="wp-video-shortcode">` players inside `<pre>` (WordPress ran the examples). They are rebuilt as shortcode text: `[video src="video-source.mp4"]` and `[video mp4="source.mp4" webm="source.webm" ogv="source.ogv"]`. Width and height are left out because they were WordPress's 640×360 defaults.
  - The two empty `<pre>` (an attachment-less `[video]` renders as nothing) are filled from `EMPTY_PRE_FILL` with `[video]`. This is a reconstruction, so check it against the old Codex page.
  - The bogus `source.mp4` and `video-source.mp4` assets are gone from the manifest and from disk.
  - **Open:** WordPress also runs shortcodes inside `<pre>`. After import these examples need `[[video]]` escaping or an importer filter.
- **Bare fragment hrefs:** `href="create-group-block-from-selected-multiple-blocks"` (no `/`, no `.`) becomes `#…`. The target `<a id>` exists, so `check_links.py` now finds 0 broken relative links.
- **Extension-less external images** (googleusercontent):
  - The converter picks the extension from the media library `mime_type`, else from `data/external-asset-types.json` (written by `download_assets.py` from magic bytes or Content-Type), else `.img`.
  - On its next run the downloader renames an existing `X.img` to the new `local_path` and deletes orphaned `.img` files.
  - Result: 42 `.png` and 22 `.jpg`, renamed in place. The 17 that return 403 stay `.img` (type unknown) and are listed in `notes/missing-assets.md`.
  - Workflow: `download_assets.py`, then `convert.py`, then `download_assets.py`.
- **`migration.first_paragraph_is_nav_link: true`** is set when the first body paragraph is only a link. This is a flag only; the link is not removed. It hits **128** articles. All 128 link to `blocks-list.md`, in 5 wording variants ("Go back to the list of Blocks", "Go to the List of Blocks", …). The earlier figure of 73 counted only one variant.
