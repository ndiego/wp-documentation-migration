# 04: Hands-on spike: running wporg-markdown against our docs/

Date: 2026-10-11. Spike files and re-run instructions: `../spike/` (README.md there).

## TL;DR

- The importer works on our tree with no changes to the manifest. All 362 entries became 362 posts on the first try. Every `post_parent`, `menu_order`, permalink path and title matched the manifest, and there were zero PHP warnings or notices. It ran in about 1 s for the manifest and about 3 s for the Markdown, against a local server.
- **It does no link or asset rewriting at all.** After import, 2,254 `href="….md"` links on 273 pages and 2,300 `<img src="../../assets/…">` on 261 pages are left relative. All of them are broken on the live site. A HelpHub subclass needs an `after_transform` rewrite. A working proof of concept is in the spike plugin.
- **`> [!NOTE]` callouts aren't supported.** They are stored as `<blockquote>[!NOTE]<br/>…`, and the literal `[!NOTE]` shows on the page: 865 callouts on 174 pages.
- **Block markup (`<!-- wp:… -->`) must never appear in our Markdown.** Its presence makes `has_blocks()` true, so core skips `wpautop`. The Jetpack parser stores paragraphs *without* `<p>` (it relies on wpautop), so the whole page renders with no paragraphs.
- **Sync semantics:** posts are updated in place (same ID). With ETags (as on GitHub raw), an unchanged re-run touches nothing. Nothing is ever deleted or unpublished. A slug change creates a new post and leaves the old one. **A duplicate slug anywhere in the manifest silently takes over an existing page** and moves it.
- Title = first `# H1` *if the file starts with it* after frontmatter is stripped. Otherwise the manifest `title` is used, but only when the file itself changes.

## Environment and method

- **Docker wasn't available** (`docker: command not found`; no colima, podman or OrbStack). Instead of the PHP-stub fallback, I ran a **full native WordPress**: PHP 8.4.26, WP-CLI 2.12, WordPress 7.1.3 on SQLite (sqlite-database-integration 3.1.0 drop-in), and Jetpack 16.3 activated. The importer loads `JETPACK__PLUGIN_DIR/_inc/lib/markdown.php` itself, and that file still exists in 16.3. So post insertion, kses, revisions, permalinks and `the_content` rendering are all real. `.wp-env.json` is provided for Docker machines (untested).
- **Importer version:** current trunk of `wordpress.org/…/plugins/wporg-markdown` (plugin.php, inc/class-importer.php, inc/class-editor.php, README.md) is byte-identical to `notes/reference/wporg-markdown/`. There is no drift.
- **Subclass:** `HelpHub_Spike_Importer`, modelled on wporg-developer `DevHub_Docs_Importer` (`import-docs.php`) and `import-block-editor.php`:
  - post type `helphub_doc`, hierarchical, with REST support
  - `get_base()` = `home_url('documentation/')`
  - the same two cron hooks
  - an `Editor` instance
  - for the main runs, none of the Block Editor's link-rewriting filters, so what was observed is the base importer.
- **Source:** a copy of `docs/*.md` + `manifest.json` (no assets) served by `bin/etag_server.py`. It mimics raw.githubusercontent.com: a strong ETag, 304 on `If-None-Match`, and the query string is ignored (the importer appends `?v=time()`). The manifest was used **as is**, because its `markdown_source` values are already relative (`overview/README.md`), and the importer resolves those against `dirname(manifest_url)`. There was no need to rewrite them to the private repo URL.
- **Fixtures:** 13 extra pages under `spike-fixtures/` (a kitchen-sink page plus title/frontmatter edge cases) were added to the served manifest so that untested features could be tested.
- The runs went manifest → markdown, five times in total, plus one run under real HTTP `wp-cron.php`.

## 1. First import (whole tree)

| Check | Result |
|---|---|
| Posts created | 362 / 362 manifest entries (`Created post N for <slug>` ×362; "Successfully created 362 and updated 0") |
| Run time | `import_manifest` 1.17 s; `import_all_markdown` 3.09 s for 362 local HTTP fetches. Against GitHub raw, expect roughly 362 × RTT (serial `wp_remote_get`), so 1–2 min per cron tick. |
| PHP errors, warnings, notices | None (WP_DEBUG on, CLI output and debug.log clean) |
| Hierarchy | 0 mismatches. Every permalink path relative to `/documentation/` equals the manifest key, and every `post_parent` equals the post of the manifest `parent`. Our manifest lists parents before children, which matters (see §4 K). |
| `menu_order` | Matches `order` for all 362 (but see §4: an `order` of `0` is ignored on updates) |
| Slugs | `post_name` = manifest `slug` for all. Slugs must already be sanitized: `Bad_Slug` was **silently skipped**, with no log line. |
| Titles | All 362 equal the manifest title, because every one of our files has `title:` frontmatter followed by an identical `# H1`. The H1 wins (see §2). |
| README.md pages | Folder index pages are ordinary entries (`overview` → `overview/README.md`) and work like any other page. Root `docs/README.md` isn't in the manifest, so there is no landing page. Adding an `index` key (tested in run 3) creates a post whose **slug is the post type name** (`helphub_doc`, permalink `/documentation/helphub_doc/`). That is the DevHub `{post_type}` landing-page convention, and it needs theme/handbook support to serve it at `/documentation/`. |
| Excerpt | First line of the tag-stripped HTML. A page starting with an H2 gets the heading text as its excerpt (e.g. `Section`). |
| Revisions | One revision per content change (our CPT supports revisions). Unchanged re-runs create none. |

## 2. Titles and frontmatter (observed)

The importer does three things in order:
1. Strips frontmatter with `preg_replace('#^---(.+)---#Us', '', $md)`.
2. Runs `trim()`.
3. Takes the title from `/^#\s(.+)/`, with no multiline flag, so it only matches at the very start of the remaining text.

| Fixture | Stored `post_title` | Notes |
|---|---|---|
| frontmatter + `# H1` (all our files) | the H1 | The H1 line is removed from the body. The frontmatter `title:` is ignored. |
| no frontmatter, `# H1` | the H1 | |
| frontmatter, no H1 | manifest `title` | |
| paragraph, then `# Late H1` | manifest `title` | `<h1>Late H1</h1>` stays in the body |
| `#Title` (no space) | manifest `title` | `#Title…` is rendered as a paragraph |
| Setext `Title\n=====` | manifest `title` | `<h1>` stays in the body |
| H1 containing `` `code` `` and `[link](url)` | the raw text **including the Markdown syntax**: ``Kitchen sink with `code` and [a link](https://example.com) in the H1`` | sanitize_text_field doesn't render Markdown |
| H1 `Title with <em>html</em> &amp; entity` | `Title with html &amp; entity` | tags stripped |
| frontmatter value containing `---` (`note: "a value with --- inside it"`) | manifest `title`. **The body is corrupted:** `<h2>inside it"</h2><h1>Title after tricky frontmatter</h1>` | the non-greedy regex ends the frontmatter at the first `---` anywhere |
| UTF-8 BOM before `---` | manifest `title`. **The frontmatter is rendered:** `<hr /><h2>title: x</h2><h1>…` | `^---` fails |
| CRLF line endings | the H1 (`\r` removed by sanitize_text_field) | OK |

## 3. Markdown feature → importer result → what it means for our conventions

"Stored" means `post_content`. "Rendered" means `apply_filters('the_content')` in a default theme context.

| Feature (count in our corpus) | What the importer stored | Rendered / implication |
|---|---|---|
| Paragraphs | **No `<p>` tags.** Jetpack's parser strips them and leaves blank-line-separated text. `wpautop` adds them at render time. | Fine *only while wpautop runs*. See block comments below. |
| Relative `.md` links (2,254 in 273 pages), `README.md` links (294 in 95 pages), `../` (1,743) | Left verbatim: `<a href="introduction-to-blogging.md">`, `<a href="../README.md">`, `<a href="wordpress-glossary.md#text-editor">` | **Broken.** The browser resolves them against `/documentation/a/b/page/`. They must be rewritten (subclass filter or converter). |
| Root-relative `/docs/…` | verbatim | broken |
| Images `![alt](../../assets/images/…png)` (2,300 in 261 pages), raw `<img src="../assets/…" width class style>` | `<img src="../../assets/images/2021/01/….png" alt="…" />`, no `<figure>` or caption. Raw `<img>` keeps width, class and safe style. | **Broken paths.** Assets also have to be hosted somewhere (they aren't imported into the media library). |
| Fenced code with a language (36 files) | `<pre><code class="language-php">` with contents HTML-escaped (`<script>` inside a fence is safe) | OK. Tilde fences and indented code also work. |
| **Literal `<code>…</code>` inside a fenced block** (1 page: `write-code-in-your-posts-classic-editor`) | **Jetpack bug:** the inner HTML is *unescaped*: `&lt;code&gt;<div class="header">&lt;/code&gt;` and `<p class="&amp;">` | Real `<div>`/`<h1>` elements get injected into the page. Avoid `<code>` tags inside fences (use entities or drop the inner `<code>`). |
| GFM tables (15 pages) | `<table><thead>…<th align="left">`, `\|` → `&#124;`, `<kbd>` and links work inside cells | OK |
| Nested lists (4-space and 2-space), code inside list items | Correct nesting. A loose list item gets `<li><p>…</p></li>`; one fixture produced a stray `Step three</p></li>` (unbalanced) after a fenced block inside an `<ol>`. | Mostly OK. 10 real pages have `<li><p>`. |
| Headings | `<h2>Text</h2>`, **no automatic ids**. Markdown Extra `## Heading {#custom-id}` → `<h2 id="custom-id">`. | 319 same-page `#anchor` links: 68 hit explicit ids, 231 only work if the theme adds GitHub-style heading ids, and 20 resolve to nothing. The handbook TOC's id algorithm decides this (untested here). Prefer `{#id}` for anchors we rely on. |
| `<a id="…">` anchors (544 in 54 pages) | kept | OK |
| `> [!NOTE]` / `[!CAUTION]` / `[!TIP]` / `[!WARNING]` (865 in 174 pages) | `<blockquote>\n  [!NOTE]\n  text…` → rendered `<blockquote><p>[!NOTE]<br />text</p></blockquote>` | **The literal `[!NOTE]` is visible.** Two blockquotes separated only by a blank line **merge into one** (fixture). A subclass needs to convert these (e.g. to the HelpHub callout markup) or the converter has to emit something else. |
| Plain `>` blockquote | `<blockquote>` | OK |
| `<video controls preload src="…">` (202 in 87 pages, all using `src=`) | kept as is (kses allows video with src, controls, autoplay, loop, muted, playsinline, poster, preload, width, height) | OK. The `poster` path is relative and broken like images. |
| `<video><source src…></video>` | **`<source>` stripped by kses**, leaving an empty `<video>` | Never use `<source>`. Keep the `src=` attribute form. |
| `<iframe>` (fixture; 0 real outside code) | **removed** entirely by kses | As expected. |
| Bare URL alone on a line (72 in 46 pages) | stored verbatim | **Auto-embedded at render.** The VideoPress URL `https://videopress.com/v/FmtB9Wcw` became the VideoPress `<iframe>` player. This is the correct way to embed videos. A bare URL *inside* a sentence is not linked. |
| `<details><summary>` (3 pages) | kept. Markdown inside `<details>` (after a blank line) *is* converted. | OK |
| `<kbd>` (70), `<br>` (67 files), `<span class>` | kept (`<span class="dashicons …">` kept) | OK |
| `<div class style data-foo onclick>` | `class`, safe `style` and `data-*` kept; `onclick` removed | OK for styled callouts if we choose div markup |
| `<script>` / `<style>` (fixture) | **Tags stripped, but the inner text stays visible** (`alert('x')`, `.x{color:red}` show on the page) | Never emit them outside code fences. |
| `<form>`/`<input>` | stripped | — |
| HTML comments (66 in 42 pages) | kept in `post_content`. wpautop wraps them in `<p><!-- … --></p>` (invisible). | Harmless, but they ship to the page source. |
| **`<!-- wp:paragraph -->…` block markup** | Passed through, but the parser stripped the inner `<p>` and inserted blank lines inside `<figure>` | **Breaks the whole page:** `has_blocks()` → core removes `wpautop` → *every* paragraph on the page renders without `<p>`. Never put block comments in our Markdown. |
| Emoji 🎉 ✅, `’`, `&amp; &lt; &copy; &nbsp;` (13 files) | preserved byte for byte | OK. wptexturize applies at render. |
| `~~strike~~` | not tested in body (Block Editor subclass adds it manually; base parser: untested) | avoid, or test |
| Footnotes `[^1]` | Jetpack generates footnotes, but kses mangles `href="#fn:1"` to `href="1"` (it treats `#fn:` as a protocol) | Broken links. We have none; keep it that way. |
| Shortcodes `[gallery …]` | stored verbatim (`preserve_shortcodes=false` only affects parsing) | Would execute at render. We have none outside code. |
| Emphasis directly after a URL (`https://example.com/**[slug]**`) | literal `**` | minor; 6 occurrences |
| YAML frontmatter | stripped (but see BOM and `---`-in-value cases in §2) | Our frontmatter has no `---` inside values today. Keep it that way, or switch to a stricter delimiter check upstream. |

## 4. Re-run, update and delete semantics

The test sequence was:
- **Run 2:** no changes.
- **Run 2b:** no changes, server without ETags.
- **Run 3:** edits.
- **Run 4:** more edits.
- **Run 5:** no changes.

Every test kept the same post ID unless noted.

| Scenario | Observed |
|---|---|
| Unchanged, ETag server (GitHub raw behaviour) | Manifest: "No updates detected". Markdown: 375 × "No updates" (304). **0 fields changed, `post_modified` untouched.** |
| Unchanged, server without ETag | All 375 posts went through `wp_update_post`: content identical, **`post_modified` bumped on every post every run**, no new revisions. The source host must send ETags. |
| A. Body edit | Same ID; content, etag and `post_modified` updated; revision added |
| B. H1 changed in file | Title updated in place |
| C. Manifest `title` changed, file (with H1) unchanged | **Ignored.** The H1 always wins, and the 304 path never touches titles. |
| D. Manifest `title` changed, file has no H1, file unchanged | **Ignored** until the file changes. Run 4 edited the body and the new manifest title was then applied. |
| E. Entry removed from manifest | Post **stays published** and keeps syncing from its file (`import_all_markdown` iterates all published posts, not the manifest). After the file is deleted: `Warning: 10 returned an error: Markdown source returned non-200 http code.` **on every run**, with stale content left live. Removing a page needs a manual unpublish or a subclass. |
| F. Slug changed (new key + slug, same file) | **New post created** (754 `supported-wordpress-versions`). The old post 17 `supported-versions` stays published with identical content, so there are duplicates. There's no redirect or `_wp_old_slug`; redirects must be handled separately (as the Block Editor subclass does with its hard-coded map). |
| G. Moved to a new parent, same slug | Same ID 22. Matched through the importer's `slug_only` fallback, `post_parent` 19 → 5, permalink moved. The old URL isn't redirected by the importer. |
| H. `order` 1 → 42 | Applied on the 304 path (`menu_order` 42). **`order` → 0 is ignored** (`! empty()`), so the page kept `menu_order` 2. Never use 0 as a meaningful order. |
| I. `markdown_source` changed | Manifest stage counts it as "updated"; content re-fetched from the new file |
| J. `index` key added | Post `helphub_doc` (slug = post type), title from the H1 of root README ("WordPress Documentation"), permalink `/documentation/helphub_doc/` |
| K. New child listed **before** its new parent | Parent created recursively, but **the child is created with `post_parent` 0** (permalink `/documentation/c2/`). It's fixed only in the following `import_all_markdown` (`get_page_by_path`). That's a window of wrong URLs between the two cron events. Keep the manifest parent-first (ours is). |
| **N. Duplicate slug in another section** (`spike-fixtures/wordpress-glossary`) | **It took over the existing glossary post (ID 9):** moved it under spike-fixtures, replaced its 125 KB content with the new page, and changed its title and order. No new post. Afterwards both manifest entries map to that one post, the manifest stage reports "updated 2" on every run, and the real glossary is gone. **Slugs must be globally unique across the manifest *and* every post still in the CPT** (including removed and orphan posts). |
| Un-sanitized slug (`Bad_Slug`) | Silently not created |

## 5. kses: which rules apply

- The importer always calls `wp_filter_post_kses()` explicitly on the HTML, so the `post` context and `$allowedposttags` apply. A filter re-adds `<a>` if it's missing. Under that, `<iframe>`, `<source>`, `<script>`, `<style>` and `<form>` go, `on*` attributes go, and `<video>`, `<details>`, `<kbd>`, `class`, safe `style`, `data-*`, `id` and `aria-*` stay.
- **Under WP-CLI** (`wp cron event run`, or our `wp spike`), WP-CLI adds `kses_remove_filters` on `init` priority 11 when no `--user` is given (seen in `WP_CLI/Runner.php`). So *only* the explicit pass runs.
- **Under real cron** (HTTP `wp-cron.php`, user 0, no `unfiltered_html`), logged inside the hook:
  ```
  {"wp_doing_cron":true,"user":0,"unfiltered_html":false,"content_save_pre_post_kses":10,"title_save_pre_kses":10}
  ```
  So kses runs **again** on `content_save_pre`, `excerpt_save_pre` and `title_save_pre`. Content came out identical for all pages (double kses is idempotent on our corpus). But **titles and excerpts differ by runner:** `Writing & publishing` → `Writing &amp; publishing` (8 titles), and `Tools > Site Health` → `Tools &gt; Site Health` (5 excerpts). This renders the same in HTML, but REST/raw consumers and title comparisons will see different values depending on how wordpress.org runs the cron.
- The Block Editor subclass widens kses with a `pre_post_update` hook (allows `<style>`). A HelpHub subclass can widen it the same way, for example if we wanted `<source>`.

## 6. Other observations

- **`markdown_source` resolution:** anything without the substring `https://` is treated as relative to `dirname(manifest_url)`.
  - `http://example.com/a.md` → `http://127.0.0.1:8882/http://example.com/a.md` (mangled). Use https or relative.
  - `../` only works when the manifest sits in a subfolder. With the manifest at the server root, `../docs/x.md` → `http:/docs/x.md`.
  - `./x.md` keeps the `./`, which is harmless.
  - Our `docs/manifest.json` + `overview/README.md` style is correct.
- **"Edit on GitHub" link:** `Editor::get_markdown_edit_link()` only converts `github.com/…/blob/…` sources into edit URLs. With relative sources the stored meta is a raw.githubusercontent.com URL, so the edit link points at the raw file. The Block Editor subclass works around this with a `get_post_metadata` filter. Either use `https://github.com/<org>/<repo>/blob/trunk/docs/...` sources in the manifest (the importer converts blob → raw for fetching) or copy that filter.
- **The filters don't receive the post or file:** `wporg_markdown_before_transform`/`after_transform` only get `($text, $post_type)`. To resolve relative paths, the subclass must override the protected `update_post_from_markdown_source($post_id)` to remember the current post, then read its `wporg_markdown_manifest_entry` meta. A working proof of concept is in `spike/helphub-spike-importer` (option `helphub_spike_rewrite_links`).
  - Test: it rewrote every `.md`, `README.md`, `#fragment`, `<img src>` and `poster` reference that maps to a current manifest entry: `../../classic-wordpress/classic-editor/first-steps-with-wordpress-classic.md` → `/documentation/classic-wordpress/classic-editor/first-steps-with-wordpress-classic/`, and images → `<asset_base>/assets/images/…`.
  - The only links left unrewritten were the ones the spike itself broke (removed or renamed pages) or that point outside the manifest.
  - Production code should use `WP_HTML_Tag_Processor`, not my regex, which would also hit `href="…"` text inside escaped code samples.
- `get_existing_for_post()` keys posts by **permalink path**, so the CPT's rewrite base must equal the `get_base()` the subclass returns, or every run will create duplicates (not tested by breaking it; follows from the code).

## 7. What our converter, manifest and pipeline must change

1. **Links:** either emit final absolute URLs (`https://wordpress.org/documentation/<key>/#frag`), or (preferably, so GitHub previews keep working) keep relative `.md` links and ship a HelpHub subclass `after_transform` rewrite like the proof of concept. In both cases add a CI link check that every relative `.md` target is in the manifest.
2. **Images and posters:** decide where assets live on wordpress.org (keep `/documentation/files/…` originals, a CDN, or raw GitHub). Then either emit absolute URLs or rewrite them in the subclass. Relative `../../assets/` paths never work as is.
3. **Callouts:** stop relying on `> [!NOTE]`. Either the subclass converts `<blockquote>[!TYPE]` to HelpHub notice markup, or the converter emits HTML (`<div class="callout callout-info">` survives kses). Always separate consecutive callouts with non-blockquote content, or they merge.
4. **Never emit `<!-- wp:… -->` block markup**, `<iframe>`, `<source>`, `<script>`, `<style>`, footnotes, or literal `<code>` tags inside fenced code (fix `write-code-in-your-posts-classic-editor`).
5. **Videos:** keep the `<video src=… controls>` form (it survives), and keep VideoPress/YouTube as a bare URL on its own line (oEmbed renders the player). The current `<!-- VideoPress embed (iframe removed): … -->` comments are redundant but harmless.
6. **Title:** every file must have the `# H1` as the *first non-frontmatter line*, with plain text only (no backticks, links or HTML). The manifest `title` acts only as a fallback and won't propagate on its own. Treat the H1 as the single source of truth and have CI check H1 == manifest title.
7. **Frontmatter:** no BOM, LF endings preferred, and no `---` anywhere inside frontmatter values (the strip regex ends at the first `---`). Make that a CI check.
8. **Anchors:** add explicit `{#id}` (Markdown Extra) to headings that are link targets, or confirm the HelpHub/handbook TOC id algorithm matches GitHub's. 20 links currently target nothing either way (`pages-screen#Selection`, `posts-screen#action`, …).
9. **Manifest invariants (CI):**
   - globally unique, pre-sanitized (`[a-z0-9-]`) slugs
   - parents listed before children
   - `order` ≥ 1 (0 is ignored)
   - `markdown_source` relative, or `https://github.com/…/blob/…` for working edit links
   - never reuse a removed page's slug elsewhere
10. **Lifecycle the importer lacks:** removal and unpublish of pages dropped from the manifest, and redirects for slug or parent changes. Plan for a subclass hook (e.g. unpublish posts whose manifest key disappeared) or a manual runbook, plus a redirect map like the Block Editor's.
11. **HelpHub specifics:** the importer only does parent/child. Categories (`helphub_article` + taxonomy) would need `meta` in the manifest (the importer only writes `meta` on manifest *updates*, not on create — read from code, not exercised) or a subclass.

## Not tested / caveats

- wp-env/Docker (`.wp-env.json` provided, unverified). Multisite (wordpress.org runs multisite; kses behaviour for super admins doesn't apply to cron user 0, so I'd expect the same).
- The real wordpress.org handbook theme and plugin (TOC heading ids, the callout CSS, the landing page for `index`), and how wordpress.org actually triggers cron (WP-CLI vs HTTP changes title/excerpt escaping, §5).
- Fetching from GitHub raw (repo is private). Rate limits and latency are estimated, not measured.
- `meta` entries in the manifest; `~~strikethrough~~` in the base parser; old-URL behaviour after a move (WordPress's own 404 guessing may redirect by slug).
