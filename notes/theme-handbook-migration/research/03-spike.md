# 03: Hands-on spike: Theme Handbook through the Markdown importer

Date: 2026-10-12. Environment: the local DevHub site (`wporg-developer`, wp-env, http://localhost:8888).
Spike branch: `spike/theme-handbook-import` (local only, commit `233c422`). Scripts, importer, manifest,
samples and results are in `../spike/`. The rerun steps are in `../spike/README.md`.

## Bottom line

**Organization survives the round trip, but only with importer changes.**

- **Stock importer (Run A): organization breaks.** The handbook reuses slugs under different parents
  (16 pages share 7 slugs), and the stock `Importer::import_manifest()` matches by slug.
  - Run A produced 149 posts instead of 140.
  - About 57 pages ended up at wrong URLs.
  - `settings` was re-created 15 times, as `settings-2` to `settings-15`.
- **Fixed subclass (Run B onward): one-to-one.**
  - All 139 URLs return 200 at the same path.
  - All 139 titles, chapter lists (order, labels, links) and previous/next links are identical.
  - 940 of 941 headings match on text, level and anchor id.
  - Images 152/152, notices 148/148 (same kinds), tables 29/29.
- **130 of 139 pages are identical on every measure.** All 9 remaining differences are explained below.
  None changes organization.
- **The round trip is fast.**
  - Converting 139 pages takes about 1 s.
  - A full import takes about 2 s: manifest 0.2 s, Markdown about 1 to 1.5 s.
  - A no-change re-run takes 0.13 s (139 × 304).

## What I did

1. **Export.** Pulled all 139 pages from `wp-json/wp/v2/theme-handbook` (id, slug, title, parent,
   menu_order, link, modified, `content.rendered`). I also saved each rendered front-end page, because
   the TOC ids, chapter list and prev/next links exist only there.
   - The other agent's `research/data/theme-handbook-pages.json` appeared mid-spike. It has the same 139
     ids and the same `modified` stamps (newest 2026-07-22), so both exports describe the same content.
2. **Converter decision** (below), then convert to Markdown plus `manifest.json`.
3. **Serving.** Served the Markdown from the host with an ETag-aware static server (`spike/scripts/serve.py`).
   The importer relies on ETag/304 to skip unchanged files, as raw.githubusercontent.com provides, and
   plain `python3 -m http.server` sends no ETag. The container reached `http://host.docker.internal:8765`
   with no extra setup.
4. **Importer.** Added `inc/import-theme.php` (`do_init( 'theme', 'themes', <manifest> )`, modelled on
   `import-scf.php` / `import-advanced-admin.php`) and required it from `functions.php`.
   - Run A used the stock class to record what breaks.
   - Run B onward used the fixed subclass.
5. **Measure.** Ran a per-page structural comparison of the rendered pages (`compare.py`), then Playwright
   side-by-sides of 10 pages (`screenshots.mjs`), then the cutover-behaviour tests.
6. **Clean up.** Deleted the imported posts, unscheduled the cron events, and switched back to `add/copy-page-sidebar`.

## Converter decision: this repo's converter, adapted

| | dmsnell/html-to-md (`wp_html_to_markdown()`) | Repo converter (`scripts/convert.py`) |
|---|---|---|
| Code blocks | Fences indented 4 spaces, so they render as literal text; info string `language-json` | Clean fences with the language (`php`, `json`, `markup`, `css`, ...) |
| Tables | No `---` separator row, so not valid GFM | GFM tables; bold first row promoted to header |
| Images | Turned into `⌊alt⌉` text; image lost | `![alt](src)`, link wrapper kept |
| Notices | Flattened to plain paragraphs | Recognises `wp-block-wporg-notice is-*-notice` |
| Links (spacing page) | 5 of 11 kept | 11 of 11 |
| Line wrapping | Hard 80-column wrap (noisy diffs) | None |
| Speed | 6 to 13 ms per page | About 7 ms per page |

html-to-md is built to produce readable Markdown for LLM consumers (`?output_format=md`), not a source
format that has to round-trip through Jetpack's parser. The repo converter already handles WordPress
block markup, the importer's constraints (single `# H1`, frontmatter regex, kses, PHP Markdown list
indent) and the TOC id rules.

The adapter (`spike/scripts/convert_theme.py`) imports `convert.py` and replaces only the
HelpHub-specific steps:

- **Links:** kept absolute, the AAH/SCF convention.
- **Images:** keep their production URLs.
- **Callouts:** become `[info]` / `[tip]` / `[alert]` / `[warning]` shortcodes, the AAH and WPCS form.
  DevHub renders these to exactly the `wp-block-wporg-notice is-*-notice` markup production uses.
- **Heading ids:** follow DevHub's TOC rule. `{#id}` is emitted only where production's id would
  otherwise differ (3 headings).
- **Embeds and video:** become bare URLs and `<video>`.
- **`<tt>`:** treated as `<code>`.

The fixes the spike forced on the converter are listed in the fidelity table.

## Manifest

`spike/manifest.json` has 140 entries: 139 pages plus 1 private stub.

- **Keys:** the URL path below `/themes/`. The landing page is `index` with slug `theme-handbook`.
- **`parent`:** the parent's **full path**, not its slug as in AAH/SCF. A bare slug is ambiguous here
  (`templates` exists four times).
- **`order`:** production `menu_order`. 70 pages have 0, and ties sort by title on both sides.
- **`markdown_source`:** relative (`getting-started/what-is-a-theme.md`; parents use `<dir>/index.md`).
- **Entry order:** depth-first tree order.

For the real repo, `markdown_source` would be `https://github.com/.../blob/trunk/...`. The importer
rewrites that form to raw URLs, as it does for AAH.

The other agent's draft `research/data/theme-handbook-manifest.json` also uses path parents, which is
correct. But it has no entry for the non-public `theme-security` parent, so
`theme-security/theme-security-issues` would fail (see below).

## Importer: what broke, and the fixes in the subclass

| # | Problem (Run A, stock importer) | Fix in `import-theme.php` | Belongs upstream? |
|---|---|---|---|
| 1 | **Duplicate slugs.** `import_manifest()` falls back to `existing[$doc['slug']]` / `slug_only[...]`, so `templates/templates` matched the already-created top-level `templates` and was "updated" instead of created. Result: 131 created + 9 "updated", 149 posts, about 57 wrong URLs. | Match on the exact path first. Fall back to the slug only when it is unique in the manifest (keeps the "page moved between parents" case working). | Yes, in `wporg-markdown/inc/class-importer.php`. The bug is latent for every handbook with a repeated slug. |
| 2 | `process_manifest_doc()` creates a missing parent recursively but then drops the new parent ID, so the child is created at top level. | Re-read the parent after creating it. | Yes |
| 3 | **Non-public parent.** `theme-security-issues` (public) sits under parent 11394, which the REST API returns 401 for. Its URL contains `/theme-security/`. The importer considers only published posts, so a non-public stub would be re-created on every cron run. | Manifest `status: private` (spike-only field). Existing posts are loaded with `publish` + `private`. | Decide first (see fixes list). |
| 4 | Existing-post keys come from `get_permalink()`. Under WP-CLI a private post's permalink is `?post_type=…&p=ID`, so the stub never matched and was duplicated (`theme-security-2`). | Key by `get_page_uri()`. | Yes, more robust for everyone. |
| 5 | **Literal shortcodes.** The media pages use `[audio]`, `[video]`, `[gallery]`, `[caption]` literally. Jetpack passes them through, and even decodes `&#91;`, so `do_shortcode()` ran them. | `wporg_markdown_after_transform`: escape every registered shortcode as `[[tag]]`, except the callout shortcodes outside code. | Handbook-level transform |
| 6 | **Code UI.** Imported code is `<pre><code class="language-x">`. DevHub's Copy / Expand code buttons (`js/function-reference.js`) attach only to `.wp-block-code`, so all 658 blocks on 94 pages lost them. Long blocks were not collapsed: the local Patterns and Block Locking page was 51% taller. | `after_transform` rewrites to `<pre class="wp-block-code"><code lang="x" class="language-x">`. | Yes. The Block Editor, AAH and SCF handbooks have the same gap. |

## Fidelity

### Totals (final run)

| Check | Production | Local | Pages identical |
|---|---|---|---|
| URL path, HTTP 200 | 139 | 139 | 139/139 |
| Title (h1) | — | — | 139/139 |
| Chapter list (order, labels, links) | — | — | 139/139 |
| Previous / next links | — | — | 139/139 |
| Breadcrumbs | — | — | 138/139 |
| Headings h2–h4 (level, text, anchor id) | 941 | 940 | 138/139 |
| Images | 152 | 152 | 139/139 |
| Notices, by kind (79 info, 30 tip, 33 alert, 6 warning) | 148 | 148 | 139/139 |
| Tables | 29 | 29 | 139/139 |
| Code blocks | 661 | 658 | 137/139 |
| Links in content | 1,882 | 1,874 | 135/139 |
| Embeds (iframes and embed cards) | 18 | 0 | 136/139 |
| Text similarity ≥ 0.999 | — | — | 134/139 |
| **All checks** | | | **130/139** |

### Every difference, classified

The counts are as found during the spike. "Fixed" means fixed in the spike's converter or importer;
the final numbers above already include those fixes.

| Class | Difference | Count | Example | Status |
|---|---|---|---|---|
| Converter bug | html-to-md: unusable fences, images, tables and notices | all pages | spacing | Rejected that converter |
| Converter bug | A "Note:"/"Important:" label overrode the notice class, so the callout changed colour | 4 notices | — | Fixed: class wins |
| Converter bug | `<p><pre>` (invalid nesting) let the paragraph escaper add `\*` inside code fences | 7 pages | 404-pages, customize-api/tools-for-improved-user-experience | Fixed: unwrap `<p>` around block elements (63 places) |
| Converter bug | Link inside inline code next to other text (`<code><a>fn()</a> - </code>`) lost the link | 10 links, 5 pages | custom-logo, custom-front-page-templates | Fixed: split into `` [`fn()`](url) `` + code |
| Converter bug | `<br>` inside inline code printed literally | 3 | custom-logo | Fixed |
| Converter bug | Single-heading page: the TOC adds no ids when there are fewer than 2 headings, so production's explicit id was lost | 1 | releasing-your-theme/required-theme-files | Fixed: emit `{#id}` (Jetpack honours it) |
| Importer transform needed | Duplicate slugs / parent matching / private parent / permalink keys | 9 pages wrong in Run A (57 URLs) | templates/templates, global-settings-and-styles/** | Fixed in subclass (#1–4); should go upstream |
| Importer transform needed | Literal shortcodes executed | 7 literals, 4 pages | media/audio, media/video, media/images, media/galleries | Fixed in subclass (#5) |
| Importer transform needed | No Copy / Expand code buttons | 658 blocks, 94 pages | patterns-and-block-locking | Fixed in subclass (#6) |
| Content needing a manual touch | 4 post embeds of make.wordpress.org/themes/2015/… return **404** today. Production still shows the stale cached embed cards; locally they are bare URLs. | 4 embeds, 1 page | theme-security/theme-security-issues | Replace with links or drop |
| Content needing a manual touch | Parent `theme-security` (id 11394) is not public, but the child's URL contains it; production breadcrumbs show "Theme Security". Locally the stub is private, so the breadcrumb reads "Private: Theme Security". | 1 page | theme-security-issues | **Decision needed** (see fixes list) |
| Content needing a manual touch | Live links inside a code example ("click here" markup shown rendered) | 2 links | advanced-topics/ui-best-practices | Rewrite the example as escaped HTML source |
| Content needing a manual touch | Nested `<pre>` inside `<pre><code>` in production. The same code is in one clean block locally. | 2 pages (3 blocks) | custom-logo, post-template-files | None; local is cleaner |
| Content needing a manual touch | Production shows `[[audio …]]` (double-escaped) in code; local shows the intended `[audio …]` | 1 page | media/audio | None; local is correct |
| Content needing a manual touch | Empty `<h2></h2>` dropped | 1 | classic-themes/customize-api | None |
| Content needing a manual touch | Legacy `[html]…[/html]` pseudo code block in prose; quotes get texturized locally | 1 page | classic-themes/functionality/navigation-menus | Convert to a real fenced block |
| Content needing a manual touch | Page with no content (empty on production too) | 1 | customize-api/other-resources | Write it or remove it |
| Environment (verify on sandbox) | Post embeds of developer.wordpress.org/reference/… do not render locally (no parsed code reference); oEmbed should work on .org | 2 pages, 6 embed elements, 2 links | including-css-javascript, conditional-tags | Check on a sandbox |
| Cosmetic | Code line numbers (`line-numbers` class) not reproduced | 54 blocks, 10 pages | customizer-objects | Optional: fence attribute + transform |
| Cosmetic | Images have no width/height (no space reserved, layout shift). Old classic-editor images display at natural width instead of the 640 px production chose. | 152 images | customize-api/customizer-objects | Optional: carry `width`/`height` |
| Cosmetic | Images still point at Photon (`i0.wp.com/developer.wordpress.org/files/…`) | 149 of 152 | all | Decide where assets live (repo vs /files/) |
| Cosmetic | `id`/`class` attribute order and `wp-block-paragraph` classes differ | all | — | Invisible |

Screenshots: `../spike/screenshots/`. After the fixes, page heights match production within 2% on 8 of 10
sampled pages; the other two are the embed pages.

## Importer behaviour relevant to cutover

| Scenario | Observed |
|---|---|
| **Re-run with no changes** | Idempotent. Manifest: "Created 0 and updated 0". Markdown: 139 × 304 "No updates". Post count stable at 140. 0.13 s in PHP. |
| **Re-run after 11 files changed** | Only those 11 re-rendered; 128 × 304. |
| **Change to an importer transform only** | **Nothing happens** until each source file changes: the 304 path skips the re-render. Clear `wporg_markdown_etag` meta to force a full re-render (done twice in the spike). |
| **Page edited in wp-admin, Markdown unchanged** | Content and title edits **survive** re-import (304). `menu_order` is **reset** from the manifest. The page silently drifts from Git. |
| **Page edited in wp-admin, then the Markdown changes** | The wp-admin edits are **silently overwritten**: content, and the title from `# H1`. There is no warning. |
| **Entry removed from the manifest** | The page stays published, stays in the chapter list and prev/next, and keeps re-importing from its stored `markdown_source`. The importer never unpublishes or deletes. |
| **Entry removed and its file deleted** | Every run logs "Markdown source returned non-200 http code" and the page keeps its last content indefinitely. |
| **Failed fetch on first import** | The manifest step creates every post empty, then the Markdown step fills it. A fetch failure leaves the page **published and empty** until the next successful run (15-minute cron). |
| **Transient failures seen** | 1 to 4 fetches per full run timed out at 5 s (Docker Desktop host networking, not the importer). All self-healed on the next run, because no ETag is stored on failure. |

## Round-trip timings

| Step | Time |
|---|---|
| Export from production (REST + 139 front-end pages, 0.3 s spacing) | about 1.5 min |
| Convert 139 pages + manifest | about 1.0 s |
| Manifest import, clean (140 posts created) | 0.2 s in PHP (1.1 s wall with wp-env overhead) |
| Markdown import, clean (139 pages) | 0.8 to 1.5 s in PHP (1.7 s wall); plus 5 s per timed-out fetch |
| No-change re-run (manifest + Markdown) | 0.13 s in PHP |
| Compare + local fetch | about 45 s |

In production, the import is cron-driven: both `devhub_theme_import_*` events every 15 minutes.
A merged change appears within 15 minutes, or immediately with `wp cron event run`.

## Fixes before a real migration, ranked

1. **Upstream the manifest-matching fix to `wporg-markdown`.** Match on the exact path first, fall back
   to the slug only when it is unique, keep the parent ID after recursive creation, and key existing posts
   by `get_page_uri()`. Without this, organization breaks on the first import (Run A). It is a small,
   self-contained PR, and it hardens the other handbooks too.
2. **Decide the `theme-security` parent.** Either publish a real "Theme Security" section page (one new
   visible page, so not strictly one-to-one), or support a non-public parent in the importer (the
   spike's `status` field plus loading private posts). The private route shows "Private:" in breadcrumbs;
   using draft status, or filtering the title, would avoid that. Fold in the 4 dead make.wordpress.org
   embeds on that page at the same time.
3. **Add `.wp-block-code` + `lang` to imported code blocks** (importer transform). It restores Copy and
   Expand code on 658 blocks. Do it in the base importer or DevHub, so every Markdown handbook gains it.
4. **Escape literal shortcodes** in the Theme Handbook transform (only the callouts run). It affects 4 media pages.
5. **Plan the cutover around the import behaviours:**
   - Freeze wp-admin edits for the handbook from the moment the Markdown is exported. Edits made after
     that are kept only until the file changes, then silently lost.
   - Run the Markdown import until it reports 139 of 139 before announcing.
   - Clear ETags after any transform change.
   - Removing or renaming a page needs a manual unpublish plus a redirect (the Block Editor importer keeps a redirect map for this).
6. **Land the converter fixes in the shared converter** (`scripts/convert.py`): `<p>` around blocks,
   partial code links, `<br>` in code, empty headings, and class-over-label for notices. They are generic
   WordPress-HTML fixes, so HelpHub benefits too. Then regenerate.
7. **Decide on assets.** Either keep the Photon `/files/` URLs (zero work; images stay in the WordPress
   media library) or move the 152 images into the repo with relative paths plus an importer rewrite.
   Carrying width/height would also remove layout shift.
8. **Content touch-ups** (small, can follow migration):
   - ui-best-practices: code example with live links.
   - navigation-menus: legacy `[html]` block.
   - customize-api/other-resources: empty page.
   - custom-logo and post-template-files: nested `<pre>` (the converter already cleans it).
9. **Optional cosmetics:** code line numbers (54 blocks), image dimensions, the 640 px display width on old classic images.
10. **Verify on a sandbox** what the local site cannot show: oEmbeds of developer.wordpress.org
    reference pages, and Photon behaviour.
