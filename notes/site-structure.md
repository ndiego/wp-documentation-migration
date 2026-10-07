# HelpHub (wordpress.org/documentation) — site structure beyond the REST `content` field

Investigated 2026-10-07. Sources: live HTML (curl), Jetpack sitemaps, and source code from
`WordPress/wporg-documentation-2022` (theme + bundled `support-helphub` plugin + mu-plugin),
`WordPress/wporg-mu-plugins` (shared `wporg/*` blocks), and the legacy `WordPress/HelpHub` repo.
Scratch copies of the HTML, sitemaps and cloned repos are in the session scratchpad (not in the project).

**Key fact:** the live code is the repo **`wporg-documentation-2022`**, not `WordPress/HelpHub`.
- Theme: `source/wp-content/themes/wporg-documentation-2022/` (block child theme of `wporg-parent-2021`)
- Plugin: `source/wp-content/plugins/support-helphub/` (CPTs, taxonomies, read time, roles, legacy TOC)
- MU plugin: `source/wp-content/mu-plugins/site-documentation.php` (search redirect + a hard-coded redirect map)
- Shared blocks (`wporg/global-header`, `global-footer`, `local-navigation-bar`, `site-breadcrumbs`,
  `sidebar-container`, `table-of-contents`, `notice`, `link-wrapper`, `language-suggest`) come from
  `WordPress/wporg-mu-plugins/mu-plugins/blocks/*`.
- `WordPress/HelpHub` is the older (2017–2022) classic-theme version (`wporg-support` theme). Its plugin code
  is mostly the same as the bundled `support-helphub`, plus a `helphub-contributors` module that is no longer used.

---

## 1. Page anatomy

Every template wraps the content in the same global chrome:

| Region | Block | Source | Derivable from API? |
|---|---|---|---|
| Global w.org header (logo, Showcase/Plugins/Themes/Hosting/News, **Resources** menu → Learn WordPress, Documentation, Education, Forums, Developers, Blocks, Patterns, Photos, Openverse, WordPress.tv; About menu; Swag; Get WordPress; w.org search) | `wporg/global-header` | wporg-mu-plugins | No, it's site-wide chrome. Can be hard-coded or skipped |
| Local nav bar (sticky, dark): site title "Documentation" + menu **WordPress Overview · Technical Guides · Support Guides · Customization · Get Involved (make.wordpress.org/docs)**. On single pages it also shows the post title or query title once you scroll | `wporg/local-navigation-bar` + `core/navigation {menuSlug:"documentation"}` | menu hard-coded in theme `functions.php` → `add_site_navigation_menus()` | No (hard-coded, 5 items) |
| "Get more help" footer band: Support forums (+ a search box), Developers, Content suggestions (github.com/WordPress/Documentation-Issue-Tracker/issues), Get involved (make.wordpress.org/docs) | `patterns/footer.php` | theme | No (static) |
| Global w.org footer (About/News/Hosting/Privacy, Showcase/Themes/Plugins/Patterns, Learn/Documentation/Developers/WordPress.tv, Get Involved/Events/Donate/Swag, WordPress.com/Matt/bbPress/BuddyPress, social links, "Code is Poetry") | `wporg/global-footer` | wporg-mu-plugins | No (site-wide) |

### 1a. Front page `/documentation/` (page ID 8, slug `support-forums`, template `front-page.html`)
- Header variant `parts/header-home.html`: global header, local nav, then a dark hero with
  `<h1>Documentation</h1>` (EB Garamond), a `wporg/language-suggest` banner (JS, suggests a localized Rosetta
  site), and a search box ("Search documentation").
- Main area: the pattern `wporg-documentation-2022/front-page-content`, which is **hard-coded in the theme**.
  It has 4 sections, one per top-level topic (h2 linking to the landing page plus a one-line description).
  Each section is a `is-style-cards-grid` of `wporg/link-wrapper` cards (h3 + short blurb) linking to
  hand-picked sub-categories:
  - **WordPress overview** (/overview/), "Learn about WordPress and its community.": Where to start? · FAQs · About WordPress
  - **Technical guides** (/technical-guides/), "Learn how to install WordPress and keep it secure and healthy.": Installation · Maintenance · Security
  - **Support guides** (/support-guides/), "Get to know how to publish with WordPress.": Dashboard · Publishing · Media
  - **Customization** (/customization/), "Get the look and feel you want on your site.": Appearance · Default themes · Media Blocks · Text Blocks · Design Blocks · Embed Blocks · Widget Blocks · Theme Blocks
    (Block Editor and Site Editor have **no** card.)
  - The card blurbs ("Are you new to WordPress? Learn how to get started now." etc.) exist **only** in the
    pattern. They are not category descriptions (sub-category descriptions are empty in the API).
- Page 8's REST `content` holds a near-copy of this markup (hero, search, cards), but the template ignores it.
  Use the pattern as the source of truth. The REST copy is a usable fallback with the same links.
- Footer band + global footer. No breadcrumbs.

### 1b. Topic landing pages `/overview/`, `/technical-guides/`, `/support-guides/`, `/customization/`
- WP pages with **empty `content`** (verified in raw/pages.json). Everything is rendered by the templates
  `page-{slug}.html`.
- Layout: header (`header-topic-landing`, no breadcrumbs) → search bar part → `<h1>` = page title →
  `core/term-description`, which the theme filters (`inject_term_description`) to show the **description of the
  matching top-level category** (`overview` maps to category `wordpress-overview`) → `wporg/article-list {category: <slug>}`.
- `wporg/article-list` landing render (`src/article-list/index.php::render_landing_block`):
  - Child categories of the topic (`hide_empty:false`, ordered by name), **then re-sorted by term meta
    `sort_order`**. That meta is set via wp-cli only, has no UI and is **not exposed in REST**.
  - For each child: `<h2>` with the category name, a Query Loop of **the first 10 articles**
    (2 columns, title links only), and "Show all articles in {Category}" linking to `/category/{slug}/`.
  - Query order is forced by `modify_query_loop_block_query_vars`: **`menu_order DESC, title ASC`**.
- No TOC, no feedback form, no dates.

### 1c. Category archive `/category/{slug}/` (e.g. /category/block-editor/), template `archive.html`
- Header with breadcrumbs **Home › {Topic landing page} › {Category}** (built by `set_site_breadcrumbs`; the
  parent links to `/{parent-slug}/`, except `wordpress-overview`, which links to `/overview/`).
- Search bar → `<h1>` (query title = category name) → term description (only *Theme blocks* has one) →
  `wporg/article-list`, which renders a plain `<ul>` of linked titles from the main query:
  - `pre_get_posts` (theme): **50 per page, `menu_order DESC, title ASC`**, followed by query pagination
    ("Newer/Older Posts"). *Theme blocks* has 51 articles, so `/category/theme-blocks/page/2/` exists.
  - Special case **`default-themes`** (`render_default_themes_block`): any article whose slug ends in
    `-changelog` is skipped from the main list and **nested under its theme** (e.g. "Twenty Twenty-Five" →
    "Twenty Twenty-Five changelog"). The match is by slug: `{theme-slug}-changelog`. There are 15 changelog articles.
- Top-level categories also have archives (`/category/customization/` etc.). They work, but the site's nav
  links to the landing pages instead.

### 1d. Article `/article/{slug}/` (`helphub_article`, template `single.html`)
Order on the page:
1. Header, then breadcrumbs **Home › {top-level category → landing page} › {first child category → archive} › Title**.
   The logic takes the first category with parent 0 and the first category with a parent. Articles in
   only one category (twenty-twenty-four, background-settings-overview, and the 2 "Uncategorized" ones)
   get a shorter trail. **Derivable** from `category` IDs plus the category tree.
2. Search bar.
3. `<h1>` = title.
4. `wporg/sidebar-container`, which holds `wporg/table-of-contents` ("In this article", collapsible on mobile)
   and a "↑ Back to top" link. **TOC is generated at render time from headings, not stored** (see §3).
5. `post-content`. The headings get injected `id`s, an `is-toc-heading` class, a self-link `<a href="#id">`
   and `tabindex=-1`.
6. **Changelog**: this is **part of the stored content**, not a separate field. It is a hand-authored
   `core/group` with class `changelog`, a background color (usually `#dce5ec` or `very-light-gray`),
   `<h2>Changelog</h2>` and a nested `<ul>` with "Created/Updated YYYY-MM-DD (props @user …)" items.
   213/321 articles mention a changelog, and 187 have `id="changelog"`. The `revision_note` REST field
   is empty for all 321 articles, so the changelog is only in content.
7. **Feedback form** ("Was this article helpful? How could it be improved?"). This is the core
   `post-comments-form` with text overridden in `comment_form_defaults`. Login is required
   (`pre_option_comment_registration`), and logged-out users see "Log in to submit feedback… support forums".
   Submissions are private comments that go to the docs team (comments are never displayed). After posting,
   the user is redirected to `?feedback_submitted=1#reply-title` and sees "Thank you for your feedback!".
   The form is shown when `comment_status=open` (320/321; `wordpress-versions` is closed).
   **Not derivable / not migratable as-is.** It needs a replacement (GitHub issue link, form service, etc.).
8. **"First published"** (`post_date`) and **"Last updated"** (`post_modified`). Both are **derivable** (`date`, `modified`).
9. Footer band + global footer.

What's absent: no related articles, no read time display (the `_read_time` meta is computed but never
shown), no author, no category list or tags, no prev/next, no comments list, no sharing buttons (even
though `jetpack_sharing_enabled: true`), no hreflang.
`<head>`: canonical, Jetpack OG/Twitter tags, `meta description` = excerpt (`get_the_excerpt`),
og:image = first image, plus RSS feed links for comments.

### 1e. WordPress version `/wordpress-version/{slug}/` (`helphub_version`, also `single.html`)
- Same template as articles, but: breadcrumbs are just **Home › Version X.Y** (no category); there is
  **no feedback form** (the CPT doesn't support comments); the TOC appears only when there are ≥2 headings
  (version-6-7 has 1, so the sidebar shows only "Back to top"); "First published" and "Last updated" are shown.
- Content is hand-written: release date and codename, a link to the news post, db_version and Trac revision,
  install info, then summary and change lists.
- Grouped by taxonomy `helphub_major_release` (REST field on each version; 37 terms such as `6-7`→"6.7" and
  `4_0`→"4.0". Slug styles are mixed, with `_` for ≤5.1 and some `-`). **The terms are not in raw/**. They are at
  `/wp-json/wp/v2/helphub_major_release?per_page=100` (a copy is saved in the scratchpad as `html/mr.json`).
- Meta `_version_date` and `_musician_codename` exist in the plugin's meta box but are **not exposed in REST**
  and not rendered. They're probably empty for modern versions, and the same info is written into the content.

### 1f. `/site-health/` (page 11655921, `page-full-width.php`) and `/update-php/` (page 9948338, `page-update-php.php`)
- Legacy classic-template names that the block theme doesn't have, so they **fall back to `index.php`**: global header →
  `post-content` → global footer only. **No h1/title, no local nav, no breadcrumbs, no search, no TOC, no dates.**
- These pages are linked from wp-admin (Site Health screen, "Update PHP" notice). The **same pages are also served at
  `https://wordpress.org/support/site-health/` and `/support/update-php/`**, which return 200 with their own canonical on the
  forums theme (`pub/wporg-support-2024`, same page IDs, so it's a shared table). Core's `wp_get_update_php_url()`
  points at the `/support/` URL. Treat both URLs as live and don't break them.

### 1g. Other rendered surfaces
- Search: any `?s=` request redirects (302) to `https://wordpress.org/search/{q}/?in=support_docs` (mu-plugin). No local search UI beyond the forms.
- `/wordpress-version/` (no slug) redirects (301) to the article `/article/wordpress-versions/` (the "Release archive").
  That page is a **hand-maintained article** (tables: Planned Versions; Released Versions grouped by major with codename,
  then rows of version, date, Changelog link, Blog link, DB version; about 696 links to version pages). Its sibling is `wordpress-versions-0-7-to-4-9`.
- `/wordpress-versions/` (CPT archive), `/articles/` (CPT archive) and `/major_release/{slug}/` (taxonomy archive) all return 200
  but **render an empty list** (`article-list` only renders for categories). They are effectively dead pages.

---

## 2. Ordering

| Surface | Ordering rule | Data needed |
|---|---|---|
| Local nav (4 topics) | Hard-coded: Overview, Technical, Support, Customization (+ Get Involved) | Hard-code |
| Front page sections and cards | Hard-coded in the pattern (a subset of sub-categories, custom blurbs) | Copy from the pattern (listed in §1a) |
| Sub-category sections on a landing page | term meta `sort_order` ASC (ties broken by name) | **Not in REST**. Observed live order below |
| Articles within a section or category | `menu_order DESC, title ASC` | `menu_order` + `title` (in REST) |
| Default themes | Same as above, plus `-changelog` articles nested under their theme | slug convention |

- `menu_order` is non-zero only for the 13 default-theme articles (`twenty-ten`=10 … `twenty-twenty-five`=25).
  Everything else is 0, so ordering is alphabetical by title, using a case-insensitive MySQL collation. Punctuation sorts
  first: "(Deprecated) Button block" and "(Deprecated) Post Author block" come first. Note that titles ≠ slugs
  (e.g. `verse-block` = "Poetry block", which sorts under P).
- The landing pages show **only the first 10 per section**, and "Show all" goes to the category archive (50/page).
- **Observed section order (captures the hidden `sort_order`):**
  - **/overview/**: FAQs, Where to start, About WordPress (*not alphabetical*, so `sort_order` is set here)
  - **/technical-guides/**: Installation, Maintenance, Security
  - **/support-guides/**: Dashboard, Media, Publishing
  - **/customization/**: Appearance, Block Editor, Default themes, Design blocks, Embed blocks, Media blocks, Site Editor, Text blocks, Theme blocks, Widget blocks
- The 4 landing pages contain **no hand-curated link lists** (empty content). The only curated lists are the front-page
  pattern, the hand-written cross-links in article bodies, and the Release archive article.
- Empty categories `devhub`, `mobile-app` and its child `post-and-pages` don't appear in nav. Their archives would render empty.
  `uncategorized` (2 articles: `site-editor-identity`, `responsive-styles`) is reachable only by direct URL.

---

## 3. Source code findings

### Post types (support-helphub `class-helphub-post-types.php`)
| CPT | Rewrite slug | REST base | Supports | Notes |
|---|---|---|---|---|
| `helphub_article` | `article` | `articles` | title, editor, excerpt, thumbnail, author, page-attributes (menu_order), revisions, **comments** | `has_archive: articles` |
| `helphub_version` | `wordpress-version` | `wordpress-versions` | title, editor, excerpt, thumbnail, author, page-attributes, revisions | no comments; `has_archive` |
| `post` | — | — | also gets page-attributes | unused (0 posts) |

### Taxonomies
- `category` registered for `post` + `helphub_article`, hierarchical, rewrite `category`.
- `helphub_major_release` for `helphub_version`, hierarchical, rewrite **`major_release`**, REST base `helphub_major_release`.
- No `helphub_major_release` taxonomy for articles. No tags.

### Post / term meta
- `_read_time`, `_custom_read_time` (articles; auto-calculated on save; **not displayed**).
- `_version_date`, `_musician_codename` (versions; meta box "Display Settings"; not in REST, not displayed).
- `_helphub_image_gallery` (legacy gallery meta, unused).
- Term meta `sort_order` on categories (landing-page section order; not in REST).
- REST `revision_note` field: empty everywhere. REST `meta` has only Jetpack SEO keys, all empty.

### Table of contents
- Live TOC = **`wporg/table-of-contents`** (wporg-mu-plugins `blocks/table-of-contents/index.php`), placed by the theme pattern
  `article-sidebar` for both CPTs. The older `handbook-toc` filter in support-helphub is **disabled** by the theme
  (`add_filter('wporg_handbook_toc_should_add_toc','__return_false')`). `table-of-contents-lite` is not loaded.
- Algorithm (reimplement this to keep anchors stable):
  1. Regex all `<h1>`–`<h6>` in the raw post content. Drop headings with no plain text. **If fewer than 2 headings remain → no TOC.**
  2. ID = the existing `id` attribute if present (stored for ~1,060 of ~3,840 headings; e.g. `id="changelog"`),
     otherwise `sanitize_title(heading text)`. Collisions with reserved IDs (`main, masthead, menu-header, page, primary,
     secondary, secondary-content, site-navigation, wordpress-org, wp-toolbar, wpadminbar, wporg-footer, wporg-header`) or earlier
     headings get `-2`, `-3`, … suffixes.
  3. The TOC list shows only **h2 and h3** (nested `<ul>`). h4+ are skipped in the list but still get IDs.
  4. Every heading is rewritten as `<hN id="…" class="is-toc-heading …" tabindex="-1"><a href="#id">PLAIN TEXT</a></hN>`.
     **Inline markup inside headings (code, links, strong) is stripped** on the live site.
  5. Title "In this article". The Changelog h2 appears as the last TOC entry.
- Because IDs are generated, **external deep links like `/article/paragraph-block/#transforms` depend on `sanitize_title`
  rules**. A Markdown slugger (GitHub-style) differs: it keeps underscores, handles `&`/entities and accents differently, and uses `-1` instead of `-2` for duplicates.

### Custom blocks / shortcodes found in content (rendered HTML in REST)
- `wporg/notice`: `<div class="wp-block-wporg-notice is-{info|tip|alert|warning|success}-notice"><div class="…__icon"></div><div class="…__content"><p>…</p></div></div>`.
  Used in only 5 articles (4 info, 1 tip). Maps naturally to admonitions (`> [!NOTE]`/`:::info`).
- **Callout paragraphs** (far more common): `<p class="has-background" style="background-color:#e5f5fa">` (773 instances,
  plus 40 × `#e5f4fa`), used for "Learn more about…" and "Note:" boxes. Groups with `#dce5ec`/`very-light-gray`/`#e0e0e0`
  are mostly changelog boxes. Decide on a mapping, otherwise the styling is lost.
- Jetpack: `wp-block-jetpack-videopress` (21 articles, iframe to videopress.com with inline `<script>`), `jetpack-tiled-gallery` (2).
- Core blocks: paragraph, heading, list, image (261), group (190), **video (95, self-hosted .mp4/.mov in /files/)**, preformatted, spacer,
  gallery, embed (20), columns (20), table (13), code, quote, media-text, separator, details (1).
- `wporg/link-wrapper`, `wporg/article-list`, `wporg/sidebar-container`, `wporg/language-suggest`: theme/template only, never in content.
- Shortcodes: support-helphub registers `[codex_languages]`, which appears in **no** content. The only `[audio]`/`[embed]` strings are literal
  examples inside the Audio Shortcode / Shortcode block articles (escape these in Markdown).

### Other behaviors
- `comment_post_redirect`, `comment_form_defaults` and `hide_field_after_submission` handle the feedback UX (§1d).
- `custom_open_graph_tags`: front page has a fixed description ("We've got a variety of resources to help you get the most out of WordPress.")
  and image `https://wordpress.org/files/2022/08/embed-image.png`. Categories use the same image. Landing pages use the category description as their description.
- `helphub-customroles`, `helphub-manager` (bbPress profile section) and `helphub-front-page-blocks` (widget) are admin- or forums-side only.

---

## 4. URL patterns under /documentation/

| Pattern | What | Count | In REST? | In sitemap? |
|---|---|---|---|---|
| `/` | Front page (page 8, hard-coded pattern) | 1 | yes (page) | yes |
| `/overview/`, `/technical-guides/`, `/support-guides/`, `/customization/` | Topic landing pages | 4 | yes (empty content) | yes |
| `/site-health/`, `/update-php/` | Standalone wp-admin landing pages (also at `/support/…`) | 2 | yes | yes |
| `/article/{slug}/` | Articles | 321 | yes | yes |
| `/wordpress-version/{slug}/` | Version pages | 935 | yes | yes |
| `/category/{slug}/` (+ `/page/N/`) | Category archives (27 terms, ~21 meaningful) | 27 | yes | **no** |
| `/category/{slug}/feed/`, `/article/{slug}/feed/`, `/feed/` | RSS (main feed is empty; article feed = comments) | — | — | no |
| `/wordpress-version/` | 301 → `/article/wordpress-versions/` (Release archive) | — | — | no |
| `/wordpress-versions/`, `/articles/`, `/major_release/{slug}/` | CPT/taxonomy archives, render empty | 37 terms | yes (terms not in raw/) | no |
| `/files/YYYY/MM/*` | Uploads (media library, 7,201 items) | 7201 | yes (media) | image/video sitemaps |
| `/{attachment-slug}/`, `/?attachment_id=N` | Attachment pages → **301 to the file** | ~6,300 | — | yes (image sitemap `<loc>`) |
| `/article/{slug}/embed/` | oEmbed iframe view | — | — | no |
| `/?p=ID`, `/article/{partial}/`, `/article/{slug}/2/` | WP canonical/guess redirects to the article | — | — | no |
| `/?s=…` | 302 → `wordpress.org/search/{q}/?in=support_docs` | — | — | no |
| `/support-forums/` | 301 → `/` (front page's own slug) | — | — | no |
| `/wp-json/…` | REST API | — | — | no |

**Redirects that must survive** (`mu-plugins/site-documentation.php`, prefix match, 301):
- Removed articles: `article/wordpress-features/` → wordpress.org/about/features/, `article/requirements/` → /about/requirements/
- Renamed categories: `category/basic-administration/` → `category/dashboard/`, `category/troubleshooting/` → `category/faqs/`,
  `category/getting-started/` → `category/where-to-start/`, `category/customizing/` → `/customization/`, `category/basic-usage/` → `/support-guides/`
- Phantom releases: `version-6-5-1` → `version-6-5-2`, `version-6-8-4` → `version-6-8-5`
- **62 articles moved to the Advanced Administration handbook** (`developer.wordpress.org/advanced-administration/…`), e.g.
  `article/backing-up-your-database/`, `article/htaccess/`, `article/editing-wp-config-php/`, `article/debugging-in-wordpress/`.
  Copy the full map from the file.
- Server-level (outside this repo): `wordpress.org/support/article/*`, `/support/wordpress-version/*`, `/support/category/*` → `/documentation/…` (301).
- WordPress old-slug redirects (`_wp_old_slug` meta) are **not exposed in REST**. Any renamed articles' old URLs only resolve through WP
  (`/article/paragrap/` → paragraph-block is the 404-guess, not old-slug). If needed, ask a site admin for `_wp_old_slug` rows.

Rosetta (localized) sites, e.g. `es.wordpress.org/support/…`, run separate HelpHub instances and are out of scope. The `language-suggest` banner points users to them.

---

## 5. Sitemap comparison

- `sitemap.xml` → `sitemap-index-1.xml` (→ `sitemap-1.xml` 1,000 + `sitemap-2.xml` 263 = **1,263 URLs**),
  `image-sitemap-index-1.xml` (7 files, **6,316 attachment URLs**), `video-sitemap-1.xml` (**711 entries**: 261 article URLs with embedded
  videos plus about 450 video attachment pages).
- 1,263 = **321 articles + 935 versions + 7 pages** exactly. The set comparison against raw/ `link`s shows zero differences in either direction.
- **Categories (27) are not in the sitemap** (Jetpack doesn't emit term archives). No URL types are missing from the REST dump.
  The only extra URL types are attachment pages (which 301 to files) and the dead CPT/taxonomy archives.

---

## Implications for the Markdown migration

1. **Front-matter per article**: `title`, `slug` (≠ title-derived; keep it), `id`, `date`, `modified` (rendered as "First published / Last updated"),
   `categories` (keep order: top-level + child, since breadcrumbs use the first of each), `menu_order` (only default themes ≠ 0), `excerpt` (used for meta
   description/OG), `comment_status`/`feedback: true|false`, featured image (2 articles). For versions: `major_release` (fetch the 37 terms, not in raw/), date.
2. **Navigation config to hand-author** (not derivable from REST): the 4-topic local nav + Get Involved; the front-page cards and blurbs (§1a); the landing-page
   **section order** (`sort_order`: Overview = FAQs, Where to start, About WordPress; the rest alphabetical); the 10-per-section limit and "Show all" link.
3. **Article order** in listings = `menu_order DESC, title ASC` (case-insensitive, punctuation first). The Default themes category needs `{theme}-changelog` nesting.
4. **TOC**: generate at build time (don't store). Use h2/h3, need ≥2 headings, title "In this article", Changelog included. **Port WordPress `sanitize_title` + `-2` dedupe
   + reserved IDs** so existing `#anchors` keep working. Preserve stored heading `id`s (≈1,060) verbatim, e.g. as `{#id}` attributes.
5. **Changelog** lives in the body as a styled `changelog` group. Either keep it as a body section with a marker (`<div class="changelog">`/admonition) or lift it into
   structured front-matter. 26 articles have it without `id="changelog"`, and 108 have none.
6. **Feedback widget** (login-gated private comments) can't be reproduced statically. Replace it with a link to the Documentation Issue Tracker or another form. Old
   comment data isn't in the export (and was never public).
7. **Callouts**: map `p.has-background` (#e5f5fa etc.) and `wporg/notice` (5) to a Markdown admonition syntax. Map VideoPress (21) and self-hosted `<video>` (95)
   to a video shortcode or raw HTML. Escape literal `[audio]`/`[embed]` shortcode examples.
8. **Media**: 7,201 uploads under `/documentation/files/YYYY/MM/`. Keep those paths, or redirect them, since content and external sites hot-link them. Attachment-page URLs only
   need to keep 301-ing to the file.
9. **Redirects** to carry over: the mu-plugin map (71 entries, 62 of them Advanced Administration moves), `/wordpress-version/` → Release archive, `/support-forums/` → `/`,
   `?s=` → wordpress.org/search, `/support/{article,wordpress-version,category}/*` → `/documentation/…`, trailing-slash canonicalization, and `/category/{slug}/page/N/`
   for Theme blocks (51 articles).
10. **Special pages**: `/site-health/` and `/update-php/` render as chrome-less pages (no title or breadcrumbs) and are duplicated at `/support/site-health/` and
    `/support/update-php/`, which wp-admin links to. Keep both. The 4 landing pages are generated, not content. The Release archive (`/article/wordpress-versions/`)
    is a hand-maintained table that could be auto-generated from version front-matter instead.
11. **Breadcrumbs, OG tags and "Back to top"** are fully derivable from front-matter plus the category tree. Landing pages use the top-level category description as their subtitle and meta description.
