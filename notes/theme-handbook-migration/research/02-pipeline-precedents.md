# Wiring the Theme Handbook into the GitHub Markdown importer: pipeline, precedents, draft code

Research date: 2026-10-12. Scope: what code, config and cutover steps make developer.wordpress.org import
`theme-handbook` (https://developer.wordpress.org/themes/, 139 published pages) from a GitHub repo instead of
wp-admin, with **zero URL changes**. Owner constraint: slugs, titles, parents and order stay exactly as they are.
Content conversion (block markup to Markdown) is covered by `01-content-inventory.md`; this report covers the
pipeline and links to 01 where the two meet.

## Sources

| Source | State inspected | Notes |
|---|---|---|
| `~/Developer/wordpress-org/wporg-developer` | `upstream/trunk` = `4cc3ba3` (2026-10-08). The checked-out branch `add/copy-page-sidebar` differs only in `patterns/article-sidebar.php` (+2 lines) | Theme `source/wp-content/themes/wporg-developer-2023/` (abbreviated `T/` below). Read only, plus `git show`/`git log` |
| `wporg-markdown` plugin | `source/wp-content/plugins/wporg-markdown/` (Composer copy from meta SVN), byte-identical to `notes/reference/wporg-markdown/` | `inc/class-importer.php` (601 lines), `inc/class-editor.php` |
| `handbook` plugin | `source/wp-content/plugins/handbook/` (Composer copy from meta SVN) | `inc/init.php`, `inc/handbook.php`, `inc/importer.php`, `inc/admin-notices.php`, `inc/email-post-changes.php` |
| `wporg-mu-plugins` | `~/Developer/wordpress-org/wporg-mu-plugins` | `blocks/notice/index.php`, `blocks/table-of-contents/index.php` |
| Jetpack Markdown | `source/wp-content/plugins/jetpack/_inc/lib/markdown/{gfm,extra}.php` | The parser the importer calls |
| Live site | REST `wp/v2/theme-handbook` (unauthenticated, 139 posts), page HTML, redirect probes, fetched 2026-10-12 | Rendered HTML only. Raw `post_content` needs `context=edit` (see 01) |
| GitHub | `gh` against `WordPress/Advanced-administration-handbook`, `WordPress/developer-plugins-handbook`, `WordPress/plugins-handbook`, `WordPress/wporg-developer`, `WordPress/wporg-documentation-2022` | PRs, commits, manifests |
| wp-meta mailing list | lists.wordpress.org/pipermail/wp-meta (mirrors Meta Trac, which returns 403 to scripts) | Tickets #6411, #7358, #7361, #7520 |
| Prior research | `notes/wporg-handbook-pipeline/` (README, research 02, 03, 04, 05) | Cited as "pipeline 02" and so on |
| **Spike** (this report, Appendix A) | Local wp-env DevHub (WordPress 7.2-alpha), 140 `theme-handbook` posts with the live structure | The real importer plus the draft subclass, run inside a MySQL transaction that was rolled back |

Labels: **[verified]** read in code, observed live, or reproduced in the spike. **[inferred]** reasoned from code, not
observed. **[unverified]** not checked.

> **Heads-up for the caller.** The local `wporg-developer` checkout is **not clean** any more. Another agent's spike
> added `T/inc/import-theme.php` (class `DevHub_Theme_Handbook_Importer`, manifest at
> `http://host.docker.internal:8765/md/manifest.json`) and modified `T/functions.php` at 09:32 local time, and it has
> been writing `theme-handbook` posts in the local database (for example 10 posts at 14:37:41 UTC). I did not touch
> either file. My spike renamed its class, detached the other class's filters inside its own process, and rolled
> back every write. Row count and `MAX(post_modified)` were checked after each run.

---

## 0. Summary

1. **The wiring is about 15 lines.** A `DevHub_Docs_Importer` subclass calling `do_init( 'theme', 'themes', $manifest_url )`
   plus one `require` in `functions.php`. `handbooks.php` needs no change: `theme` is already a handbook post type
   (`T/inc/handbooks.php:126`) and its pluralized `themes` slug (`:202-215`) agrees with the importer's base.
   The `'themes'` base is load-bearing. Any other value breaks path matching, so the duplicated slugs collide and
   pages get moved (§1.3).
2. **Existing posts are adopted in place, by permalink path.** The importer keys each existing published post by its
   permalink minus `home_url( 'themes/' )` (`class-importer.php:84-100`). A manifest keyed by the same paths matches
   all 139. In the spike: **0 created, 139 updated, every ID, permalink, parent, `menu_order`, title, author and
   `post_date` unchanged**. Only `post_modified` moved, and the second run was 139 × HTTP 304 with no writes.
   **[verified]**
3. **Use an object manifest keyed by path, with `parent` set to the parent's key.** Do not use a list manifest. The Theme
   Handbook has 7 duplicated slugs on 14 pages, and a list manifest keys by slug. A list also renumbers `menu_order`,
   while 70 pages use order 0 and 64 pages tie with a sibling, so the sidebar order currently falls back to title.
4. **New pages must never reuse an existing slug.** The lookup chain falls back to slug (`class-importer.php:168-173`).
   In the spike, adding `features/testing` silently **took over** the existing `/themes/advanced-topics/testing/`
   post: it moved it to `/themes/features/testing/` and retitled it. **[verified]** CI has to block this.
5. **The importer never deletes, never trashes, and only "sees" published posts.** Trashing or drafting a page in
   wp-admin after cutover makes the next run re-create it under a new ID. Slug edits in wp-admin also create
   duplicates. Editing is only *warned* against (`class-editor.php:62-74`). The draft adds a `map_meta_cap` lock
   (admins only), which the spike verified.
6. **The page changes template automatically.** The template switches to `single-handbook-github` as soon as
   `wporg_markdown_source` meta exists (`T/functions.php:602-619`). That adds "Improve it on GitHub" and "See list of
   changes" links. "Last updated" will read the cutover date on every page, because the first import bumps
   `post_modified`.
7. **Transforms the Theme Handbook needs**, all in the draft and all spike-tested:
   - GitHub alerts become the theme's `.callout-*` divs (148 `wporg/notice` blocks today).
   - `{#id}` keeps the 162 explicit heading anchors (Markdown Extra, no code needed).
   - Relative `.md` links are rewritten to permalinks.
   - Registered shortcodes inside code samples get `[[…]]` escaping. Entity escaping does not work, because kses
     decodes `&#91;`.
   - `wp-block-code` is added to `<pre>` for visual parity.

   Images can stay as absolute `developer.wordpress.org/files/` URLs with no transform (all 152 are already there).
8. **The redirect map is empty.** Every slug and parent is preserved, and the existing "redirects" are WordPress's
   404 slug-guessing (`x-redirect-by: WordPress`), which depends only on `post_name` and status (§6).
9. **Precedent.**
   - Advanced Administration (AAH) went live 2023-03-28 → 2023-04-03 after dd32 fixed the manifest himself
     (AAH PR #190) and added the importer to the old theme (`f511687`, `652bd6a`). It was then ported to the 2023
     theme (`wporg-developer#237`, 2023-05-09).
   - The Plugin Handbook mirror diverged because its Meta ticket, **#7361**, stalled after one comment in
     January 2024. The importer was never switched, and both sides kept being edited: 65 of the 102 live pages were
     edited in wp-admin after the mirror was made, and 34 repo PRs were merged that never reached the site.
   - The Plugins *Team* handbook (#7358) was switched and does sync.

---

## 1. The importer contract

### 1.1 How a handbook is wired (per subclass)

| Setting | Where | Value for the Theme Handbook |
|---|---|---|
| Post type | `DevHub_Docs_Importer::get_post_type()` returns `"{$post_type}-handbook"` (`T/inc/import-docs.php:81-83`) | `do_init( 'theme', … )` → `theme-handbook`, the existing type. 14 characters, under the 20-character limit that forced `adv-admin` and `scf` (`import-advanced-admin.php:9`) |
| URL base, which is also the match base | `get_base()` → `home_url( "{$base}/" )` (`import-docs.php:63-65`) | `themes` → `https://developer.wordpress.org/themes/` |
| Rewrite slug | `override_post_type_slug()` sets `rewrite.slug = $base` when the base differs from the post type (`import-docs.php:133-141`). `Devhub_Handbooks::filter_handbook_post_type_defaults()` independently sets `themes` (`handbooks.php:202-215`). Both are on `handbook_post_type_defaults` at priority 10. The importer's runs first because `functions.php:71-92` loads before `:102` | Both produce `themes`. No conflict **[verified in code]** |
| Handbook list | `amend_post_types()` adds the type to `devhub_handbook_post_types` if missing (`import-docs.php:115-121`) | `theme` is already in the default list `['apis','plugin','theme']` (`handbooks.php:126`), so this is a no-op |
| Manifest URL | Third `do_init()` argument, hard-coded (`import-docs.php:92-95`). Examples: AAH `…/Advanced-administration-handbook/main/bin/handbook-manifest.json` (`import-advanced-admin.php:11`), SCF `…/secure-custom-fields/trunk/docs/bin/manifest.json` (`import-scf.php:11`) | Placeholder `https://raw.githubusercontent.com/WordPress/theme-handbook/trunk/manifest.json` |
| Cron | `$cron_interval = '15_minutes'` (`import-docs.php:41`). The schedule is added by `filter_cron_schedules()` (`:149-158`). `register_cron_jobs()` on `init` schedules `devhub_{type}_import_manifest` and `devhub_{type}_import_all_markdown` independently with `wp_schedule_event( time(), … )` (`:163-176`) | `devhub_theme_import_manifest`, `devhub_theme_import_all_markdown`. The two passes are **unordered** (pipeline 02 §2.1) |
| Editor integration | `new Editor( $this )` stored in `$GLOBALS['devhub_handbook_editors']` (`import-docs.php:104-106`). The theme removes its `the_title` edit link (`functions.php:211-216`) | Automatic |
| Label | `handbook_label` filter (AAH and SCF each override it, `import-advanced-admin.php:26-32`). The default is `get_option( "{$post_type}_name" )`, then config, then `ucfirst( 'theme' ) . ' Handbook'` (`handbook/inc/handbook.php:122-151`) | No override needed. The current label ("Theme Handbook") is unaffected by the importer |

Loading: the theme requires importers only `if ( class_exists( '\\WordPressdotorg\\Markdown\\Importer' ) )`
(`T/functions.php:71-92`). The new `require` goes after `import-playground.php` on line 91.

### 1.2 Manifest format

Parsed in `Importer::import_manifest()` (`class-importer.php:107-197`):

| Field | Meaning | Code |
|---|---|---|
| *(object key)* | **Match key.** If the top-level JSON is an object, its keys are used verbatim and compared with the existing posts' permalink paths. If it is a list, the importer re-keys it by `slug` and sets `order` from the array index (`:133-144`). "Not explicitly specifying a key means the slugs defined must be unique" (`:134`) | `:135-144`, `:167-177` |
| `slug` | `post_name` on create. Rejected unless `sanitize_title_with_dashes( slug ) === slug` (`:240-244`); all 139 pass (01 §structure). `index` maps to the post type name (`:236-238`). Also the **fallback match** (§1.3) | `:236-251` |
| `title` | `post_title` on create (`:256-258`), and on every 200 import **if the Markdown has no leading `# H1`** (`:489-493`, `:367-371`). The H1 wins when present. On a 304, titles are never re-applied (`update_post_from_manifest( $id )` passes `$title = false`, `:473`, `:353`) | `:256-258`, `:367-374` |
| `parent` | Create: looked up in `existing[parent]` or `existing['slug_only'][parent]`, else `$manifest[parent]` is created recursively (`:208-220`). Update: compared with the current parent's `post_name`. If that differs, `get_page_by_path( parent, …, post_type )` is called (`:384-404`). Both paths work when `parent` is the parent's **key** (path). A bare slug only resolves for top-level parents in `get_page_by_path` | `:206-230`, `:376-404` |
| `order` | `menu_order`. Set on create when `isset` (`:253-255`). Re-applied on update only when `! empty` (`:363-365`), so **0 is never re-applied** | `:253`, `:363` |
| `markdown_source` | Stored as meta `wporg_markdown_source` after `esc_url_raw( generate_markdown_source_url() )` (`:274`, `:289`). A relative value resolves against the manifest's directory, with at most one `../` level (`:570-588`). A `github.com/…/blob/…` URL is fetched as `raw.githubusercontent.com` (`:449`) with `?v=time()` (`:450`). Blob URLs also give correct edit and changelog links (§3) | `:274`, `:449-450`, `:570-588` |
| `meta` (optional) | Arbitrary post meta, written only when the source URL changed (`:289-298`) | `:294-298` |

The whole entry is also stored as meta `wporg_markdown_manifest_entry` (`:275`, `:287`). Live examples: AAH is an object of
75 entries keyed by path (`before-install/creating-database`). Its nested entries use the **bare parent slug**
(`server/web-server/httpd` → `parent: "web-server"`). That works only because AAH slugs are unique. SCF is the same
(147 entries, `parent: "admin"`). **[verified, fetched 2026-10-12]** The sibling report's generated manifest
(`research/data/theme-handbook-manifest.json`, 139 entries) already uses parent **keys**
(`templates/templates` → `parent: "templates"`, `classic-themes/basics/template-hierarchy` → `parent: "classic-themes/basics"`),
which is what the Theme Handbook needs.

Theme Handbook entries in the required shape:

```json
{
  "index": { "title": "Theme Handbook", "slug": "theme-handbook", "markdown_source": "https://github.com/WordPress/theme-handbook/blob/trunk/index.md", "parent": null, "order": 0 },
  "templates": { "title": "Templates", "slug": "templates", "markdown_source": "https://github.com/WordPress/theme-handbook/blob/trunk/templates/index.md", "parent": null, "order": 40 },
  "templates/templates": { "title": "Templates", "slug": "templates", "markdown_source": "https://github.com/WordPress/theme-handbook/blob/trunk/templates/templates.md", "parent": "templates", "order": 20 },
  "core-concepts/templates": { "title": "Templates", "slug": "templates", "markdown_source": "https://github.com/WordPress/theme-handbook/blob/trunk/core-concepts/templates.md", "parent": "core-concepts", "order": 30 },
  "theme-security/theme-security-issues": { "title": "Theme security issues", "slug": "theme-security-issues", "markdown_source": "https://github.com/WordPress/theme-handbook/blob/trunk/theme-security/theme-security-issues.md", "parent": "theme-security", "order": 0 }
}
```

Chapters are `parent: null`, **not** children of the landing page. That is the exact mistake dd32 fixed in AAH PR #190
(`"parent": "handbook"` → `null`, §4.1).

### 1.3 How posts are matched on re-import

1. All **published** posts of the type are loaded (`post_status => 'publish'`, `class-importer.php:147-151`).
2. Each gets a key: `rtrim( str_replace( get_base(), '', get_permalink( $id ) ), '/' )` (`:85`).
   - For the landing page the permalink is the archive URL, so the key is empty. It becomes the `post_name` if that
     is `handbook`, the post type, `{post_type}-handbook` or `welcome`, and `index` otherwise (`:86-94`).
   - The Theme Handbook landing slug is `theme-handbook` (live REST), which equals the post type, so its key is
     `theme-handbook`.
   - Keys that contain `/` are also indexed by bare slug in `existing['slug_only']` (`:161-163`). Later duplicates
     overwrite earlier ones.
3. For each manifest entry, the lookup order is `existing[key]`, then `slug_only[key]`, then `existing[slug]`, then
   `slug_only[slug]`, then (for key `index`) the post type name (`:168-177`).
   - **Hit:** `update_post_from_manifest_doc()` writes the manifest-entry and source meta. Nothing else changes until
     the Markdown pass (`:286-301`).
   - **Miss:** a new post is created (`:186`, `:235-277`).
4. There is **no stored-URL matching** on the manifest pass. The `wporg_markdown_source` meta is only used by the
   Markdown pass (`import_all_markdown()`, `:308-335`, `get_markdown_source()`, `:593-600`).

Consequences for the Theme Handbook:

| Case | Behaviour | Status |
|---|---|---|
| Path-keyed manifest, `base = 'themes'` | Every entry hits `existing[key]`. 139 adopted, 0 created | **[verified in spike]** |
| Base set to anything else (for example `'theme'`) | `str_replace` finds nothing, so every existing key is a full URL. Full URLs contain `/`, so every post also lands in `slug_only` by `post_name` (`:161-163`). Path keys miss, and matching falls through to `slug_only[slug]`. The 125 pages with unique slugs still match. Each of the 7 duplicated slugs resolves to **one** post, so two to four manifest entries update and re-parent that same post, moving pages, while the other same-slug posts stay unmanaged | **[inferred from `:85`, `:161-173`]** |
| Landing page entry `"index"` with slug `theme-handbook` | `existing['index']` misses, then `existing['theme-handbook']` hits | **[verified in spike]** (ID kept, `/themes/`) |
| A **new** page whose slug equals an existing slug at another path | Falls through to `slug_only[slug]` and **adopts that other post**: it overwrites its meta, then the Markdown pass moves and retitles it | **[verified in spike]**: new `features/testing` took over `/themes/advanced-topics/testing/` |
| Existing duplicate slugs (7 slugs, 14 pages) | Safe, because the exact path key hits first. `slug_only` collisions are never consulted | **[verified in spike]** |
| `theme-security/theme-security-issues` (published, parent ID 11394 not public; REST returns 401) | Its permalink still includes `theme-security/`, so the key matches. On update `manifest.parent === parent.post_name`, so the parent is not touched (`:391`). **Do not** add a `theme-security` manifest entry: only published posts are "existing", so the importer would create a second, published `theme-security` page (`theme-security-2`) | Match **[verified in spike, local private parent]**. The create path is **[inferred]** |
| Child listed before its parent, parent not yet existing | `process_manifest_doc()` creates the parent recursively but then **drops the new parent's ID** (`$parent` is still `false` at `:217`), so the child is created top-level until the Markdown pass re-parents it. That only works when the parent's key resolves through `get_page_by_path` | **[verified in code]**. Irrelevant for adoption; it matters for new chapters |

### 1.4 Lifecycle: deletions, dates, authors, wp-admin edits

| Question | Answer | Basis |
|---|---|---|
| Post in the DB but not in the manifest | Untouched and still published. There is no delete or trash path anywhere in `wporg-markdown`. If it never had `wporg_markdown_source`, the Markdown pass skips it with a `missing-markdown-source` error (`:595-597`). It also keeps the **wp-admin template**, because template choice is per post (§3) | **[verified in code]** |
| `post_modified` | Set by every `wp_update_post()`: the 200 path (`:511-524`), and the 304 path when a manifest field actually differs (`:406-424`). The 304 path unsets unchanged fields first (`:409-415`). At cutover **all 139 pages get the cutover time**. Later runs are no-ops | **[verified in spike]** (139 changed, then 0) |
| `post_date` ("First published") | Never written | **[verified in spike]** |
| Author | Create path: no `post_author` is set (`:246-252`), so `wp_insert_post` falls back to the current user, 0 under cron **[inferred]**. Adopted posts **keep their authors**, because `wp_update_post` merges the existing row. The `wordpressdotorg` default author belongs only to the handbook plugin's importer (`handbook/inc/importer.php:134`, `:222-253`), not DevHub's | **[verified in spike]** (0 author changes) |
| Revisions | `supports` includes `revisions` (`handbook/inc/handbook.php:374`), so each content import adds one revision | **[verified in spike]** (sample went from 1 to 2) |
| Content edit in wp-admin after cutover | It **survives** until the upstream file changes. The next run sends the stored ETag, gets a 304, and skips content (`:462-474`). A title edit also survives (304 passes `$title = false`). `menu_order` and parent edits are reverted on the next 304 pass if the manifest value differs and the order is non-zero (`:363`, `:406-424`). The admin warning "Content, title, and slug edits here will be discarded on next sync" (`class-editor.php:69`) is therefore inaccurate | **[inferred from code]**, consistent with pipeline 02 §1.7 |
| Slug edit in wp-admin | The permalink changes, so the old path key misses. The slug fallback misses too, because the slug changed. The importer **creates a duplicate** at the original URL. The edited post stays live at its new URL | **[inferred]** |
| Trash or draft in wp-admin | Only `publish` posts are "existing", so the next manifest run **re-creates** the page under a new ID. Trashed slugs get `__trashed` and do not collide. Drafts collide, giving `-2` (core `wp_unique_post_slug` ignores status for hierarchical types) | **[inferred]** |
| Watchers | `WPorg_Handbook_Email_Post_Changes` adds `_wporg_watchlist` users to Email Post Changes recipients on update (`handbook/inc/email-post-changes.php:16-27`). If that plugin is active on DevHub, the cutover sends one diff email per watched page | **[unverified]** whether EPC is active on developer.wordpress.org |

### 1.5 How the `handbook` plugin's importer differs (make.wordpress.org route)

`WPorg_Handbook_Importer` (`handbook/inc/importer.php`) is the config-driven sibling used for make/hosting, make/plugins
and similar. It is activated per handbook by `handbooks_config[ key ]['manifest']` (`handbook/inc/handbook.php:218-230`).

| | DevHub subclass | `WPorg_Handbook_Importer` |
|---|---|---|
| Activation | PHP class in the theme | Config only (`handbooks_config` filter, `handbook/inc/init.php:111-150`). DevHub registers its handbooks with the deprecated `handbook_post_types` list (`handbooks.php:39`, `:124-130`), which carries no `manifest` |
| Cron hooks | `devhub_{type}_…` | `handbook_{base}_import_manifest` and `…_import_all_markdown`. Interval from config, with an unknown value falling back to `hourly` (`importer.php:131-132`, `:148-157`) |
| Author on create | none | `wordpressdotorg` (`:222-253`) |
| Admin UI | per-post warning (`class-editor.php:62-74`) | Also "This is an imported handbook!" with the manifest link (`admin-notices.php:143-182`), and a "Not Imported" post state (`importer.php:167-176`) |
| Transforms | per-subclass filters | none of its own |
| Known bug | — | `instance()` reads an undefined `$instances` (`importer.php:62-64`) |

For the Theme Handbook the subclass route is the right one: all six DevHub precedents use it, it can carry transforms,
and `functions.php` already loads it. The config route would need `handbooks_config` support added in `handbooks.php`,
and it gives no transform hook point.

---

## 2. Content transforms

### 2.1 What the base importer does, in order (`update_post_from_markdown_source()`, `class-importer.php:435-530`)

1. Fetch the raw URL, sending `If-None-Match` with the stored ETag. The `wporg_markdown_check_etags` filter can disable
   this (`:462-466`).
2. Strip the YAML front matter `^---…---` (`:483`).
3. Apply **`wporg_markdown_before_transform`** with `( $markdown, $post_type )` (`:487`). The post ID is **not** passed.
4. Extract the title from a leading `# ` line, then remove it (`:489-493`).
5. Run Jetpack `WPCom_GHF_Markdown_Parser` with `preserve_shortcodes = false` (`:497-499`).
   - `strip_paras` removes bare `<p>` (`gfm.php:79`, `:309-311`).
   - Fenced code becomes `<pre><code class="language-x">`, unless the SyntaxHighlighter class exists
     (`gfm.php:67`, `:406-409`). It does not on DevHub (pipeline 02 §4.2).
   - Markdown Extra provides tables, `{#id}` header attributes and `markdown="1"` on HTML blocks
     (`extra.php:1786-1839`, `:2178`).
6. Apply **`wporg_markdown_after_transform`** with `( $html, $post_type )` (`:501`).
7. Excerpt = the first text line (`:503-507`).
8. `wp_filter_post_kses()` (`:509-515`). The importer re-adds `<a>` only if it is missing (`:545-560`).
9. Merge the manifest fields (`:519-521`), call `wp_update_post` (`:524`), and store the ETag (`:527`).

Per-handbook hooks already in use:

| Subclass | Hooks | Purpose |
|---|---|---|
| Block Editor (`import-block-editor.php:16-40`) | `template_redirect` (~70 redirects, `:46-188`), `get_post_metadata` (edit-link hack, `:224`), `before_transform` (`:284-363`: strip H1, rewrite `/docs/` and `/packages/` links to absolute URLs, `~~`), `after_transform` (`:365-385`: `{% codetabs %}`), `wporg_markdown_edit_link`, kses `<style>` (ineffective, pipeline 02 §1.4) | The largest set of link rewrites |
| Playground (`import-playground.php:46-59`) | `before_transform` (MDX), `after_transform` at priority 10/15/20/20/25 (callout re-parse `:783-821`, links `:863`, images `:961`, sideload `:980`), `wporg_markdown_check_etags` ×3 (transform version `:69-80`), overrides `update_post_from_markdown_source()` to know the post (`:163-190`) | The pattern copied by the draft |
| Coding Standards (`import-coding-standards.php:14-15`, `:53-62`) | `the_content` `fix_double_encoding` | Render-time repair |
| AAH, SCF, REST API | `handbook_label` only | No transforms at all |

### 2.2 Theme Handbook constructs and what each needs

Counts are from the live REST content (139 pages, 2026-10-12). `01-content-inventory.md` has the per-page detail.

| Construct (live) | Today | In Markdown | Importer transform? | Draft method |
|---|---|---|---|---|
| Callouts: 148 `wporg/notice` blocks on 72 pages (info 79, alert 33, tip 30, warning 6). No `[info]`-style shortcodes or `div.callout` in rendered output | `<div class="wp-block-wporg-notice is-{type}-notice">` | GitHub alerts `> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` (they render on GitHub) | **Yes.** `before_transform` turns each alert into `<div class="callout callout-{info,tip,alert,warning}" markdown="1">`, so Markdown inside is parsed with no Playground-style re-parse. The theme's `.callout` CSS is written to "match notice block styles" (`T/src/style/style.scss:577-623`) | `convert_github_alerts()`. Spike output: `<div class="callout callout-info">` with `<strong>`/`<code>` parsed, and `wpautop` adds `<p>` at render **[verified]**. Pixel parity with the notice block is **[unverified]** |
| Alternative for callouts: `[info]…[/info]` shortcodes | — | — | No (the mu-plugin re-registers `info/tip/alert/tutorial/warning` and renders real notice markup at display, `wporg-mu-plugins/mu-plugins/blocks/notice/index.php:24-27`, `:82-93`) | Not chosen. Enclosing shortcodes that span Markdown paragraphs interact badly with `wpautop` **[unverified, likely]**, and they do not render on GitHub |
| Do **not** emit notice block comments (`<!-- wp:wporg/notice -->`) | — | — | — | Any block comment makes `has_blocks()` true, and `wpautop` is then skipped on the whole page (Playground bug, pipeline 02 §1.5) |
| Code: 657 `pre.wp-block-code` blocks (php 432, json 98, markup 46, css 38, javascript 23, js 5, bash 4, xml 1), plus 3 `wp-block-syntaxhighlighter-code` | Code Syntax Block, Prism | Fenced code with a language | Parity only. Imported `<pre>` would otherwise get the `pre:not(.wp-block-code)` grey style (`style.scss:34-40`). The draft adds `class="wp-block-code"` | `add_code_block_class()` **[verified output; visual unverified]** |
| `line-numbers` on 54 blocks (10 pages), likely `[php]`/`[code]` shortcodes in source (01) | `inc/formatting.php:886-909` | Keep the `[php]…[/php]` shortcodes in Markdown, or drop line numbers | No | Content decision |
| Block markup inside code samples (56 blocks, 15 pages) | escaped | Fenced code | No. The parser HTML-escapes fences and inline code, and `has_blocks()` stays false | **[verified in spike]** (`&lt;!-- wp:paragraph --&gt;`, `has_blocks=false`) |
| Shortcodes inside code samples (`[video mp4=…]`, `[gallery]`; 8 blocks plus 4 pages of prose, per 01) | displayed literally | Fenced or inline code | **Yes.** `do_shortcode` runs on stored HTML at render and does not skip `<code>`. `&#91;` does **not** work, because kses turns it back into `[` | `escape_shortcodes_in_code()` wraps registered shortcodes inside `<code>` as `[[…]]`. Spike: stored `[[video mp4="a.mp4"][/video]]`, rendered `[video mp4="a.mp4"][/video]` **[verified]**. Shortcodes in prose must be written `[[audio]]` in the Markdown |
| Heading anchors: 162 explicit `id`s on 18 pages. A few cannot be derived from the heading text (for example `theme_unit_test`, `database-schema`) | `<h2 id>` | `## Heading {#id}` | No (Markdown Extra). The TOC keeps existing ids (`table-of-contents/index.php:173-192`) | **[verified in spike]** (`<h2 id="custom-anchor">`) |
| Images: 152 `<img>`, all `developer.wordpress.org/files/…` served through `i0.wp.com` | Media library | `![alt](https://developer.wordpress.org/files/YYYY/MM/x.webp)`, or raw `<figure>`/`<figcaption>` HTML for the 12 captions (kses allows `figure`) | **No.** Same model as the Block Editor handbook (absolute URLs to the DevHub media library, pipeline 02 §4.3). No sideloading | Without a `wp-image-ID` class, `srcset`/`sizes` will not be generated **[inferred]**; keep the class in raw HTML if that matters |
| Links: 431 absolute `/themes/` links, 558 `/reference/` links, 145 Codex links | absolute | Keep absolute: zero transform, zero risk | Optional | `rewrite_relative_links()` supports relative `.md` links (`page.md`, `../x/y.md#frag`, `/repo-root.md`) by resolving against the post's stored source and mapping to permalinks. Unresolved links are left as-is with a `WP_CLI::warning`. **[verified in spike]** (`../getting-started.md#intro` → `/themes/getting-started/#intro`) |
| Code reference links | absolute, plus render-time autolinking of `function()` names (`T/inc/formatting.php:35`, `autolink_references` on `the_content` for every post type) | absolute | No | — |
| Embeds: 7 WordPress oEmbeds (iframes) on 3 pages | `wp-block-embed` | `[embed]https://…[/embed]`, expanded at render. kses strips `iframe` | No transform; content convention | **[unverified]**: the spike did not test `[embed]` |
| `<video src>` (1) | `<video controls src>` | raw HTML (kses allows `video src`, pipeline 02 §4.1) | No | — |
| Cover, buttons, columns, group layouts (on about 17 pages, mostly `patterns/*`, `templates/*`) | block markup | Raw HTML keeps classes, but core block CSS for blocks absent from the parsed content may not be enqueued **[inferred]** | Optional | Options: a screenshot, or a Playground-style display-time shortcode that `do_blocks()` a base64 attribute (`import-playground.php:678-718` precedent). Not drafted, because it changes how these pages are authored |
| Tables (4 pages) | `wp-block-table` | GFM tables | No. `filter_standards_content()` wraps every handbook `<table>` in `figure.wp-block-table` at render (`T/functions.php:660-680`) | — |
| `@username` on `credits` | `autolink_credits` on `is_single( 'credits' )` (`handbooks.php:227-245`) | plain text | No (render time) | — |
| Titles containing `&` (7) | Production REST shows `&amp;`, so the stored titles already contain `&amp;` **[inferred]**; the local copy has a raw `&` | Write `&` in the H1 and manifest | No | `sanitize_text_field` keeps `&`. Under HTTP-triggered cron, kses turns it into `&amp;` (pipeline 04). Both render identically |

Title source: keep the base behaviour, where the leading `# H1` is the title (`:489-493`), and have CI require that the
H1 equal the manifest `title`. Do not copy the Block Editor's H1 stripping (`import-block-editor.php:290-294`):
manifest-only titles are never re-applied on 304 passes, so a title-only change would not ship until the file
changes (pipeline 04).

Transform changes after go-live: bump `CONTENT_TRANSFORM_VERSION` in the draft. That copies Playground's ETag bypass
(`import-playground.php:13`, `:69-80`), so unchanged files are re-rendered once. The Block Editor importer lacks this.

---

## 3. What a GitHub-backed page shows that a wp-admin page does not

**Template selection is per post, not per post type.** `add_handbook_templates()` (`T/functions.php:602-619`, hooked on
`single_template_hierarchy` at `:193`) puts `single-handbook-github` first whenever `get_post_meta( id,
'wporg_markdown_source' )` is non-empty. `single-handbook-block-editor` is used only for `blocks-handbook`. So the
switch happens **per page, on the manifest pass**, before its content is replaced: for up to one cron tick a page shows
the GitHub template around its old block content. That is harmless. Pages not in the manifest keep `single-handbook`.

| Element | `single-handbook` (wp-admin today) | `single-handbook-github` |
|---|---|---|
| Template file | `T/templates/single-handbook.html` | `T/templates/single-handbook-github.html`. It differs only at line 22: the `article-meta-github` pattern |
| Layout | title, `article-sidebar` (TOC; Copy Page on the open #600 branch), `post-content`, meta, pagination, chapter list (`single-handbook-github.html:18-34`) | identical |
| "First published" | `post-date` (`patterns/article-meta.php:13-21`) | identical (`patterns/article-meta-github.php:13-21`) |
| "Last updated" | `[last_updated]` label plus `post-date displayType=modified`, shown only when modified > published (`T/inc/shortcodes.php:75-84`; `article-meta.php:23-31`) | identical. After cutover **every page shows the cutover date**, because the first import bumps `post_modified`. History: removed in `ebe83c6` (#462, 2024-01-04), restored in `7b5a3df` (2024-01-08). Open requests to use the last commit date: wporg-developer #464 and #505 (pipeline 05) |
| "Edit article → Improve it on GitHub" | — | `[article_edit_link]` (`shortcodes.php:31-41`). A `github.com/…/blob/…` source becomes `/edit/` (`:91-114`). Raw URLs are returned unchanged, which is why the manifest must use **blob** URLs (the Playground bug, pipeline 02 §1.5). With no meta it falls back to `get_edit_post_link()` or login |
| "Changelog → See list of changes" | — | `[article_changelog_link]`: `/edit/` → `/commits/`, else `#` (`shortcodes.php:46-60`) |
| Admin-bar "Edit" on the front end | wp-admin | GitHub edit URL (`class-editor.php:103-126`; front end only, `is_admin()` returns early) |
| wp-admin edit screen | normal | Warning notice plus an "Edit on GitHub" link (`class-editor.php:62-74`). Editing is **not** disabled |
| Title edit badge | — | Added by `Editor::filter_the_title_edit_link`, then removed by the theme (`functions.php:211-216`) |

---

## 4. Precedents

### 4.1 Advanced Administration (AAH): how it went live

| Date | Event | Source |
|---|---|---|
| 2022-07-18 | Meta #6411 "Advanced Administration – New DevHub Handbook" opened. The initial plan was wp-admin; it switched to GitHub after the Hosting team joined | [wp-meta 2022-July/050234](https://lists.wordpress.org/pipermail/wp-meta/2022-July/050234.html); pipeline 05 §5 |
| 2022-08-13 | Workflow agreed (Milana): inventory project #47, a Docs-tracker label plus automation, a content repo with a manifest, shared Docs/Hosting maintenance "just as we have Themes handbook being shared between Themes and Docs teams" | [wp-meta 2022-August/050446](https://lists.wordpress.org/pipermail/wp-meta/2022-August/050446.html) |
| 2022-08 → 2022-11-23 | Personal repo `zzap/…`, then transferred to `WordPress/Advanced-administration-handbook` via dd32. Docs and Hosting GitHub teams get maintain, Javier and Milana get admin | pipeline 05 §5 |
| 2022-08-16 → 2023-01-15 | Manifest hand-edited by Javier Casares and Milana (commits "first base example" through "Manifest updated") | `gh api …/commits?path=bin/handbook-manifest.json` |
| **2023-03-28** | **AAH PR #190, "Changes needed for WordPress.org handbook import"**, by dd32, merged by dd32 at 05:59 UTC. Files: `bin/handbook-manifest.json` (+77/−76), `README.md`, `themes/index.md`, `wordpress/feeds.md`. It replaced every `markdown_source` (`WordPress/WordPress-Advanced-administration-handbook/blob/master/…` → `WordPress/Advanced-administration-handbook/blob/main/…`), changed chapters from `"parent": "handbook"` to `null`, gave `index` `"order": -1`, and renamed `feed` → `feeds` (pipeline 03). Body: "This PR is just for the changes I needed to make to get this on WordPress.org. TODO for the team: REMOVE or fill out the empty pages." | `gh pr view 190 -R WordPress/Advanced-administration-handbook` **[verified]** |
| 2023-03-28 | Meta r12504 (cited by pipeline 05 as the import setup) | pipeline 05 **[content of r12504 unverified]** |
| 2023-03-29 | Javier: "Manifest with ordered pages" (`485143dab0`) | manifest commit log |
| 2023-04-03 | dd32 adds `DevHub_Advanced_Admin` to the **old** theme `wporg-developer` (`f511687`) and loads it from `functions.php` (`652bd6a`), on the `old` branch with its workflow (`3e55cb4`) | `git log origin/old` **[verified]** |
| 2023-04-04 | #6411 closed | pipeline 05 |
| 2023-04-06 | Kelly Dwan: `single-adv-admin-handbook.php` template for the old theme ("Syncs [20168-dotorg]", `cea2fa4`) and a landing-page link (`6940c86`) | `git show` **[verified]** |
| 2023-04-07 → 2024-01-17 | wporg-documentation-2022 #59 "Add redirects to Advanced Admin handbook" (HelpHub → AAH), closed by ryelle | `gh issue view 59` **[verified]** |
| 2023-04-10 | "Introducing the Advanced Administration Handbook" on make/docs | pipeline 05 |
| 2023-05-09 | wporg-developer **#237** "Import the Advanced Admin handbook" by dd32 (`5d6956e`): `functions.php` +3, `inc/import-advanced-admin.php` +35, `composer.lock`. Body: "This has been committed to production for the old theme, creating this to import it with the new theme. I haven't tested this in this theme, but it appears that it should work." | `gh pr view 237` **[verified]** |

**How wp-admin editing was handled.** It wasn't, beyond the built-in notice. AAH was a *new* post type with no
wp-admin-authored content, so there was nothing to freeze or adopt, and no capability lock exists in the code.
`Devhub_Handbooks::adjust_handbook_editor_caps()` (`handbooks.php:167-188`) treats imported and non-imported handbooks
alike. **The Theme Handbook is the first DevHub migration of an existing wp-admin handbook**, so the freeze, adoption
and lock steps in §5 have no direct precedent. The closest analogue is the Plugins Team handbook (§4.2), and the README
of every imported repo says removals are done by hand on the .org side (pipeline 03).

**Playbook distilled from AAH.**
1. The content repo is created in, or transferred to, the WordPress org by a Meta person, with team access set.
2. The manifest is reviewed by a Meta committer *before* the first import. AAH's was wrong on repo, branch, parents
   and order.
3. Committing the importer class is the go-live switch, and it needs a Meta committer plus a deploy.
4. Redirects from the *old* location are a separate PR in the old site's repo.
5. Announce on make/docs.

For the Theme Handbook, step 4 is empty, and step 2 can be automated (§5.6).

### 4.2 Why the Plugin Handbook mirror diverged, and what a cutover must do

- **Two tickets, two outcomes.** Javier Casares opened both on 2023-12-01:
  - [Meta #7358](https://lists.wordpress.org/pipermail/wp-meta/2023-December/056322.html), "Plugins Team
    (make.wordpress.org/plugins) Handbook sync". dd32 closed it as fixed in January 2024: "This has been done, but
    turns out the Github repo contents was outdated and appears to have missed a lot of headings", with two fix-up
    commits ([wp-meta 2024-January/056995](https://lists.wordpress.org/pipermail/wp-meta/2024-January/056995.html)).
    make.wordpress.org/plugins/handbook/ still prints the importer's `a.github-edit` CSS, and dd32 has commits in
    `WordPress/plugins-handbook` (2024-01-24). **[verified]** This corrects pipeline 03 §9, which said there was no
    import evidence.
  - [Meta #7361](https://lists.wordpress.org/pipermail/wp-meta/2023-December/056436.html), "DevHub Plugins Team
    (developer.wordpress.org/plugins) Handbook sync". It received one recorded comment, from dd32: "Repo name probably
    makes more sense as `plugin-developer-handbook`"
    ([2024-January/056994](https://lists.wordpress.org/pipermail/wp-meta/2024-January/056994.html)). No later
    activity appears in the wp-meta subject indexes checked (2024-02 through 2025-06), and wporg-developer contains no
    plugin-handbook importer. **[status of #7361 unverified, Trac returns 403]**
- **What divergence looks like (measured 2026-10-12).**
  - `WordPress/developer-plugins-handbook` (created 2023-11-12) has an 80-entry manifest, while the live
    `plugin-handbook` has **102** published pages. **65** of those were modified in wp-admin after the repo was
    created. **34** repo PRs have been merged (most recently #78 on 2026-10-07), and none of them reached the site.
  - Example: PR #76 (GIF banner support, merged 2026-09-23) is absent from
    https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/, which was last modified 2025-01-31.
  - The 2023-12-05 Docs meeting recorded the intent: "Once completed, it will be migrated to WordPress.org"
    ([summary](https://make.wordpress.org/docs/2023/12/12/summary-of-docs-team-meeting-december-5-2023/)).
- **Root cause.** The repo was opened to contributors *before* the importer existed, and wp-admin stayed writable. Two
  sources of truth then evolved independently. Even #7358, which did ship, imported stale content ("missed a lot of
  headings"), because the repo snapshot predated later wp-admin edits.
- **What the Theme Handbook cutover must do instead.**
  1. Do not open the repo for content PRs until the importer is deployed. Keep it private or archived, or accept only
     tooling PRs.
  2. Freeze wp-admin edits, then regenerate the Markdown from a **fresh export taken after the freeze**.
  3. Diff the regenerated content against the live rendered HTML (01's `compare.py` approach).
  4. Merge the manifest at the configured path and run both cron events immediately.
  5. Lock editing (the draft's `map_meta_cap`), and update the Docs handbook's "how to update" pages the same day.

---

## 5. Draft implementation

### 5.1 `T/inc/import-theme.php`

Modelled on `import-advanced-admin.php` and `import-scf.php` (`do_init` plus nothing else), with the
`update_post_from_markdown_source()` override and ETag-version pattern from `import-playground.php:13`, `:69-80`,
`:163-190`. Every transform below was exercised in the spike (Appendix A). The PHP lints clean with `php -l`.

```php
<?php
/**
 * Theme Handbook importer.
 *
 * Imports developer.wordpress.org/themes/ (post type `theme-handbook`) from a
 * GitHub-hosted Markdown repository. Existing posts are adopted in place: the
 * manifest keys are the current permalink paths relative to /themes/, so the
 * importer matches every existing post by path and never creates a duplicate.
 */
class DevHub_Theme_Handbook_Importer extends DevHub_Docs_Importer {
	/**
	 * Bump when the transforms below change, so unchanged files are re-imported.
	 */
	const CONTENT_TRANSFORM_VERSION  = 1;
	const CONTENT_TRANSFORM_META_KEY = '_devhub_theme_content_transform_version';

	/**
	 * GitHub alert type => handbook callout class (styled in src/style/style.scss).
	 */
	const ALERT_TYPES = array(
		'NOTE'      => 'info',
		'TIP'       => 'tip',
		'IMPORTANT' => 'alert',
		'WARNING'   => 'warning',
		'CAUTION'   => 'alert',
	);

	/**
	 * Post currently being imported (the transform filters do not receive it).
	 *
	 * @var int
	 */
	protected $current_post_id = 0;

	/**
	 * Normalized GitHub source URL => permalink, built once per request.
	 *
	 * @var array|null
	 */
	protected $source_map = null;

	/**
	 * Initializes object.
	 */
	public function init() {
		parent::do_init(
			// Post type base. get_post_type() appends '-handbook', giving the existing 'theme-handbook'.
			'theme',
			// Must equal the live rewrite slug. Keys are permalinks minus home_url( 'themes/' ); any other
			// value breaks path matching and the 7 duplicated slugs collide (pages get moved).
			'themes',
			// PLACEHOLDER: final repo, branch and path to be decided.
			'https://raw.githubusercontent.com/WordPress/theme-handbook/trunk/manifest.json'
		);

		add_filter( 'wporg_markdown_before_transform', array( $this, 'convert_github_alerts' ), 10, 2 );
		add_filter( 'wporg_markdown_after_transform', array( $this, 'rewrite_relative_links' ), 10, 2 );
		add_filter( 'wporg_markdown_after_transform', array( $this, 'escape_shortcodes_in_code' ), 15, 2 );
		add_filter( 'wporg_markdown_after_transform', array( $this, 'add_code_block_class' ), 20, 2 );
		add_filter( 'wporg_markdown_check_etags', array( $this, 'check_content_transform_etag' ) );
		add_filter( 'map_meta_cap', array( $this, 'restrict_editing_imported_pages' ), 10, 4 );
	}

	/**
	 * Tracks the post being imported so the transforms can resolve relative links.
	 *
	 * @param int $post_id Post ID.
	 * @return bool|WP_Error
	 */
	protected function update_post_from_markdown_source( $post_id ) {
		$this->current_post_id = (int) $post_id;

		try {
			$result = parent::update_post_from_markdown_source( $post_id );
			if ( true === $result ) {
				update_post_meta( $post_id, self::CONTENT_TRANSFORM_META_KEY, self::CONTENT_TRANSFORM_VERSION );
			}
			return $result;
		} finally {
			$this->current_post_id = 0;
		}
	}

	/**
	 * Ignores the stored ETag when the page was imported by an older transform version.
	 *
	 * @param bool $check_etags Whether to send If-None-Match.
	 * @return bool
	 */
	public function check_content_transform_etag( $check_etags ) {
		if ( ! $check_etags || ! $this->current_post_id ) {
			return $check_etags;
		}

		$version = (int) get_post_meta( $this->current_post_id, self::CONTENT_TRANSFORM_META_KEY, true );

		return self::CONTENT_TRANSFORM_VERSION === $version;
	}

	/**
	 * Converts GitHub alerts (`> [!NOTE]`) into handbook callouts.
	 *
	 * Markdown Extra parses the body because of markdown="1". The output carries no
	 * block comments, so wpautop still runs at render time.
	 *
	 * @param string $markdown  Markdown source.
	 * @param string $post_type Post type being imported.
	 * @return string
	 */
	public function convert_github_alerts( $markdown, $post_type ) {
		if ( $this->get_post_type() !== $post_type ) {
			return $markdown;
		}

		return preg_replace_callback(
			'/^>[ \t]*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*\r?\n((?:>.*(?:\r?\n|$))*)/mi',
			function ( $m ) {
				$type = self::ALERT_TYPES[ strtoupper( $m[1] ) ];
				$body = preg_replace( '/^>[ \t]?/m', '', $m[2] );

				return "<div class=\"callout callout-{$type}\" markdown=\"1\">\n\n" . trim( $body ) . "\n\n</div>\n\n";
			},
			$markdown
		);
	}

	/**
	 * Rewrites links to other Markdown files in the repo into handbook permalinks.
	 *
	 * Handles `page.md`, `../dir/page.md`, `/repo-root/path.md`, with or without #fragment.
	 * Unknown targets are left untouched and reported under WP-CLI.
	 *
	 * @param string $html      Transformed HTML.
	 * @param string $post_type Post type being imported.
	 * @return string
	 */
	public function rewrite_relative_links( $html, $post_type ) {
		if ( $this->get_post_type() !== $post_type || ! $this->current_post_id ) {
			return $html;
		}

		$source = $this->normalize_source( (string) get_post_meta( $this->current_post_id, $this->meta_key, true ) );
		if ( ! $source ) {
			return $html;
		}

		$map = $this->get_source_map();

		return preg_replace_callback(
			'#href="(?![a-z][a-z0-9+.-]*:|\#)([^"\#]+\.md)(\#[^"]*)?"#i',
			function ( $m ) use ( $source, $map ) {
				$target = $this->resolve_path( $source, html_entity_decode( $m[1] ) );
				if ( isset( $map[ $target ] ) ) {
					return 'href="' . esc_url( $map[ $target ] . ( $m[2] ?? '' ) ) . '"';
				}
				if ( class_exists( 'WP_CLI' ) ) {
					WP_CLI::warning( "Unresolved link {$m[1]} in post {$this->current_post_id}" );
				}
				return $m[0];
			},
			$html
		);
	}

	/**
	 * Stops shortcodes quoted in code samples (`[video mp4="…"]`) from executing at render time.
	 *
	 * do_shortcode() does not skip <pre>/<code>. Entities do not help: kses turns `&#91;` back
	 * into `[`. So registered shortcodes inside <code> get core's own escape, `[[tag]]`, which
	 * do_shortcode() prints as `[tag]`. Already-escaped `[[tag]]` is left alone.
	 *
	 * @param string $html      Transformed HTML.
	 * @param string $post_type Post type being imported.
	 * @return string
	 */
	public function escape_shortcodes_in_code( $html, $post_type ) {
		if ( $this->get_post_type() !== $post_type ) {
			return $html;
		}

		$pattern = '/' . get_shortcode_regex() . '/s';

		return preg_replace_callback(
			'#(<code\b[^>]*>)(.*?)(</code>)#is',
			function ( $m ) use ( $pattern ) {
				$code = preg_replace_callback(
					$pattern,
					function ( $s ) {
						return ( '[' === $s[1] && ']' === $s[6] ) ? $s[0] : '[' . $s[0] . ']';
					},
					$m[2]
				);
				return $m[1] . $code . $m[3];
			},
			$html
		);
	}

	/**
	 * Gives fenced code the class the block-edited pages use today, for visual parity.
	 *
	 * @param string $html      Transformed HTML.
	 * @param string $post_type Post type being imported.
	 * @return string
	 */
	public function add_code_block_class( $html, $post_type ) {
		if ( $this->get_post_type() !== $post_type ) {
			return $html;
		}

		return str_replace( '<pre><code class="language-', '<pre class="wp-block-code"><code class="language-', $html );
	}

	/**
	 * Only administrators may edit or delete pages that are imported from GitHub.
	 *
	 * The importer itself runs without a user and does not check capabilities.
	 *
	 * @param string[] $caps    Primitive caps required.
	 * @param string   $cap     Meta cap being checked.
	 * @param int      $user_id User ID.
	 * @param array    $args    Extra args; $args[0] is the post ID.
	 * @return string[]
	 */
	public function restrict_editing_imported_pages( $caps, $cap, $user_id, $args ) {
		if ( ! in_array( $cap, array( 'edit_post', 'delete_post' ), true ) || empty( $args[0] ) ) {
			return $caps;
		}

		$post = get_post( $args[0] );
		if ( $post && $this->get_post_type() === $post->post_type && get_post_meta( $post->ID, $this->meta_key, true ) ) {
			$caps[] = 'manage_options';
		}

		return $caps;
	}

	/**
	 * Builds the map of normalized source URL => permalink for every imported page.
	 *
	 * @return array
	 */
	protected function get_source_map() {
		if ( null !== $this->source_map ) {
			return $this->source_map;
		}

		$this->source_map = array();
		$ids = get_posts(
			array(
				'post_type'      => $this->get_post_type(),
				'post_status'    => 'publish',
				'posts_per_page' => -1,
				'fields'         => 'ids',
				'meta_key'       => $this->meta_key, // phpcs:ignore WordPress.DB.SlowDBQuery
			)
		);
		foreach ( $ids as $id ) {
			$source = $this->normalize_source( (string) get_post_meta( $id, $this->meta_key, true ) );
			if ( $source ) {
				$this->source_map[ $source ] = get_permalink( $id );
			}
		}

		return $this->source_map;
	}

	/**
	 * Normalizes a GitHub blob or raw URL to `/{owner}/{repo}/{branch}/{path}` (lower-case owner/repo).
	 *
	 * @param string $url Source URL.
	 * @return string Empty string if not a GitHub URL.
	 */
	protected function normalize_source( $url ) {
		if ( preg_match( '#^https?://github\.com/([^/]+)/([^/]+)/(?:blob|edit)/(.+?)(?:[?\#].*)?$#i', $url, $m )
			|| preg_match( '#^https?://raw\.githubusercontent\.com/([^/]+)/([^/]+)/(.+?)(?:[?\#].*)?$#i', $url, $m ) ) {
			return strtolower( "/{$m[1]}/{$m[2]}" ) . "/{$m[3]}";
		}
		return '';
	}

	/**
	 * Resolves a link path against the normalized source of the current file.
	 *
	 * @param string $source Normalized source, `/{owner}/{repo}/{branch}/{path}`.
	 * @param string $link   Relative (`../x.md`) or repo-root (`/x.md`) path.
	 * @return string Normalized target.
	 */
	protected function resolve_path( $source, $link ) {
		$parts  = explode( '/', ltrim( $source, '/' ) );
		$prefix = array_slice( $parts, 0, 3 ); // owner, repo, branch.
		$dir    = array_slice( $parts, 3, -1 );

		$segments = ( '/' === $link[0] ) ? array() : $dir;
		foreach ( explode( '/', $link ) as $segment ) {
			if ( '' === $segment || '.' === $segment ) {
				continue;
			}
			if ( '..' === $segment ) {
				array_pop( $segments );
				continue;
			}
			$segments[] = $segment;
		}

		return '/' . implode( '/', array_merge( $prefix, $segments ) );
	}
}

DevHub_Theme_Handbook_Importer::instance()->init();
```

Design notes:
- **Minimal variant.** If links stay absolute and callouts are written as raw `<div class="callout …">`, then
  `init()` with only `parent::do_init()` is a complete, AAH-identical importer. The four transforms and the lock are
  separable, and each could be a separate commit.
- **The `map_meta_cap` lock.**
  - In the spike, a `handbook_editor` went from `edit_post: true` (baseline) to `false` on imported pages, and an
    administrator stayed `true`. **[verified]**
  - It also blocks `delete_post`, which keeps "trash nothing" enforceable.
  - It only bites once a page carries `wporg_markdown_source`, so pages outside the manifest stay editable.
  - Whether to lock at all is a Docs and Themes team decision (Q6).
- **No redirect code.** The redirect map is empty because every slug and parent is preserved. If one is ever needed,
  copy the `template_redirect` / `$redirects` shape from `import-block-editor.php:46-188`. HelpHub-side redirects live in
  `wporg-documentation-2022` (AAH #59 precedent).

### 5.2 `T/functions.php`

```diff
 	// Playground handbook.
 	require __DIR__ . '/inc/import-playground.php';
+
+	// Theme handbook.
+	require __DIR__ . '/inc/import-theme.php';
 }
```

That is line 91 on `upstream/trunk`, inside the `class_exists( '\\WordPressdotorg\\Markdown\\Importer' )` block (`:71-92`).
It must load before `handbooks.php` (`:102`), which it does.

### 5.3 `T/inc/handbooks.php`

**No change is required.**
- `theme` is in the default list (`:126`), so `amend_post_types()` is a no-op.
- The pluralized `themes` rewrite (`:202-215`) equals the importer base.
- The `credits` autolinker (`:227-245`) and the `handbook_editor` role (`:138-154`) run at render or admin time and are
  unaffected.

One optional cleanup: the `'theme'` entry could be removed from the default list, since the importer now adds it.
Leaving it avoids touching shared code.

### 5.4 Deploy steps (code)

1. **Ticket and proposal.** File a Meta Trac ticket (component Handbooks or Developer Hub), linked from a make/docs post
   cross-posted to make/themes (the handbook is co-owned by the Themes team, §4.1). Precedent tickets: #6411, #7358,
   #7361.
2. **Content repo.** Created in, or transferred to, the WordPress org by a Meta admin (dd32 transferred AAH; for #7361
   he weighed in on naming). Give Docs and Themes reps maintain access. **Do not** commit `manifest.json` at the
   configured path yet (§5.5). Name and branch are open (Q1).
3. **wporg-developer PR.** Add `inc/import-theme.php` and the `functions.php` line. CI runs `build.yml` on merge to
   `trunk` and force-pushes `build`.
4. **Sync and deploy** by a Meta committer: `bin/sync/wporg-developer.sh`, then `deploy-dotorg.sh`
   (`~/Developer/wordpress-org/README.md`, "How a change reaches production").
   - Deploying this **before** the manifest exists is safe. `import_manifest()` gets a 404, returns a WP_Error and
     changes nothing (`class-importer.php:108-119`). `import_all_markdown()` finds no post with source meta
     (`:593-600`).
   - The two cron events are scheduled on the first `init` after deploy (`import-docs.php:163-176`).

### 5.5 Cutover steps (content, wp-admin, WP-CLI)

The go-live switch is **the manifest appearing at the configured URL**. Until then the deployed code is inert.

| # | Step | Who | Notes |
|---|---|---|---|
| 1 | Announce a wp-admin **freeze** on `theme-handbook` (make/docs, make/themes, #docs, #themereview) | Docs reps | Edits after the export are lost on import |
| 2 | Export **raw** content: `wp post list --post_type=theme-handbook --post_status=any --fields=ID,post_name,post_parent,menu_order,post_status,post_title --format=json`, plus `wp export --post_type=theme-handbook`. Also `wp db export` of the affected rows, or a full backup, as the rollback source | Meta | Raw titles and shortcodes are needed (01 caveat). REST `context=view` is texturized (`&#8211;`) |
| 3 | Inventory **non-published** posts (drafts, private, pending; at least ID 11394 `theme-security`). The importer ignores them. Decide per post whether it stays wp-admin-only (Q4) | Docs and Themes | Do not publish 11394: that changes the chapter list |
| 4 | Regenerate Markdown and manifest from the step-2 export. CI checks pass (§5.6) | Converter (01) | Manifest keys = permalink paths. `order` = current `menu_order` verbatim. `title` = raw `post_title` = H1. `parent` = parent key, except the orphan's `theme-security` |
| 5 | Dry run on a sandbox or wp-env with a copy of production rows: run both events, then compare IDs, paths, parents, orders and titles (Appendix A harness) and diff the rendered HTML (01 `compare.py`) | Meta + us | The expected result is "created 0 and updated 139" |
| 6 | Merge the PR that adds `manifest.json` at the configured path | Repo maintainers | raw.githubusercontent.com can serve stale content for a few minutes **[unverified, ~5 min]** |
| 7 | Run immediately, in order: `wp cron event run devhub_theme_import_manifest`, then `wp cron event run devhub_theme_import_all_markdown` | Meta committer on production | Otherwise the unordered 15-minute ticks leave a window of up to about 15 minutes with the GitHub template around old content (§3) |
| 8 | Verify: `wp post list --post_type=theme-handbook --post_status=any --format=count` is unchanged; there are no new IDs; all 139 URLs return 200 with the "Improve it on GitHub" link; `/themes/` is still the landing page | Meta + us | |
| 9 | wp-admin: **trash nothing, move nothing, re-slug nothing.** Pages not in the manifest stay as they are. Remove "update via the dashboard" wording from the Docs handbook role pages (pipeline 03 §9) | Docs reps | Trashing an imported page makes the importer re-create it with a new ID (§1.4) |
| 10 | Rollback, if needed: revert the `functions.php` line and redeploy. Then delete `wporg_markdown_source`, `wporg_markdown_etag`, `wporg_markdown_manifest_entry` and `_devhub_theme_content_transform_version` meta on `theme-handbook` posts, which reverts the template. Restore `post_content` from the step-2 backup or the pre-import revision. Unschedule the events with `wp cron event delete devhub_theme_import_manifest` and `…_import_all_markdown` | Meta | IDs and URLs never changed, so rollback is content-only |

### 5.6 CI invariants the content repo should enforce

Generated in CI and compared, the way SCF does it (`docs-manifest.yml` fails on a stale manifest, pipeline 03 §8):

- Keys are unique, match the file paths, and equal the frozen list of 139 live paths. Additions are allowed; removals
  and renames fail unless a redirect PR is linked.
- **A new entry's `slug` must not equal any existing slug in the manifest.** This prevents the takeover in §1.3.
- `parent` is `null` or an existing key. The one documented exception is `theme-security`.
- `order` is an integer equal to the frozen value for existing pages. Changing it to `0` is rejected, because the
  importer never re-applies 0 (`class-importer.php:363`).
- The H1 equals `title`. There is exactly one H1, and it is plain text.
- `markdown_source` is a `github.com/…/blob/{branch}/…` URL. Raw URLs break the edit link (§3).
- No unescaped `<!-- wp:` outside code fences, because it would disable `wpautop` (01, pipeline 04).

---

## 6. Open questions and risks for keeping URLs identical

| # | Topic | Risk / question | Evidence | Mitigation |
|---|---|---|---|---|
| 1 | Repo, branch, manifest path | Undecided. dd32 has opinions on naming (#7361) | §4.2 | Decide in the Meta ticket. The placeholder is in `do_init()` |
| 2 | Slug collisions | 7 duplicated slugs (`templates` ×4, `template-parts`, `patterns`, `testing`, `internationalization`, `global-settings-and-styles`, `template-hierarchy`) are safe for adoption, but a new page reusing any existing slug **hijacks** an existing post | Spike: `features/testing` took over post 2930 | CI rule §5.6. Optionally, upstream `wporg-markdown` could skip the slug fallback when the slug is ambiguous (the sibling spike class does this) |
| 3 | Parent paths | `update_post_from_manifest()` resolves changed parents with `get_page_by_path( parent )`. Path keys work. Bare slugs only resolve top-level parents | `class-importer.php:391-403` | Use parent **keys** (the sibling manifest already does) |
| 4 | Non-published posts | Unknown number of drafts and private posts (at least 11394). They are invisible to the importer and stay wp-admin-only | REST 401 for 11394; local copy has 1 private | Inventory them at the freeze (§5.5 step 3) |
| 5 | Orphan `theme-security/theme-security-issues` | Public page under a non-public parent. It matches by path and keeps its parent. It is hidden from the chapter list by the walker. `/themes/theme-security/` 301s to it through core slug-guessing | live probe | Keep as-is. Do **not** list `theme-security` in the manifest (it would create a published `theme-security-2`) |
| 6 | Editing after cutover | wp-admin content edits survive until the next upstream change, then vanish. Slug edits create duplicates. Trash or draft re-creates the page | §1.4 | `map_meta_cap` lock (draft) or a policy. Decide with the Docs and Themes reps, who currently publish through wp-admin (pipeline 05) |
| 7 | Landing page | The `theme-handbook` slug (ID kept) must be in the manifest as `index`/`theme-handbook`, `parent: null`, `order: 0`. Copying AAH's `handbook` slug would still match through the `index` fallback, but would diverge on any re-create | `class-importer.php:86-94`, `:174-177`; `handbook/inc/handbook.php:395-433` | Use `"index": { "slug": "theme-handbook" }` |
| 8 | Chapter order source of truth | After cutover it is the manifest `order` plus `post_title` tie-break (`chapter-list`: `menu_order, title`; `get_adjacent_handbook_post_link` the same, `T/functions.php:727-…`). 70 pages at order 0 and 64 sibling ties depend on titles staying byte-identical | live REST | Copy `menu_order` verbatim. Later renumbering is a separate, explicit change |
| 9 | Fragment URLs | 162 explicit heading ids. A few are not derivable from the text | §2.2 | `{#id}` on every one (converter, 01) |
| 10 | "Last updated" | Every page shows the cutover date. wporg-developer #464 and #505 (use last commit date) are open | §3 | Accept, or have a one-off `wp_insert_post_data` filter during cutover keep `post_modified`. Not drafted |
| 11 | Old-location redirects | The 301s from pre-2023 paths (`/themes/basics/…` → `/themes/classic-themes/basics/…`) are `x-redirect-by: WordPress`, which is core `redirect_guess_404_permalink` (slug guess). `_wp_old_slug` is never recorded for hierarchical types (core `wp_check_for_changed_slugs` returns early for them). One path uses `x-redirect-by: DevNet-redirect`, which is in no public repo | live `curl -I`; core `post.php:7741-7743` in wp-env | Adoption preserves `post_name` and status, so these keep working **[verified for the probed URLs; DevNet-redirect source unverified]**. 01's "depends on IDs and `_wp_old_slug`" should read "depends on `post_name`" |
| 12 | Search | `inc/search.php:99-102` scopes handbook searches by post type (unchanged). IDs and URLs are unchanged. Content is re-indexed once. The handbook plugin adds handbooks to Jetpack sitemaps (Meta r13070, from the wp-meta subject index), so `lastmod` moves for all 139 | — | None needed. Whether an external index (Jetpack Search or ES) is used is **[unverified]** |
| 13 | Documentation-Issue-Tracker | 146 open Themes issues (pipeline 03). The `feedback` page links to the tracker and its `themes` label, and `color` links issue #563. URLs stay valid, but "who fixes it" moves to PRs | live REST | Keep the tracker for intake (the AAH model: label plus PRs in the content repo). Have the repo README point there. Update the `feedback` page text in the first content PR |
| 14 | Visual parity | Callout `.callout-*` styles versus the `wporg-notice` block; plain `<pre>` versus `wp-block-code`; captions and `srcset`; cover, buttons and columns on about 17 pages | §2.2 | Screenshot diff on a sandbox before cutover (the screenshot toolkit in this repo). **[unverified]** |
| 15 | Watch emails | If Email Post Changes is active, cutover mails every watcher a full diff | `email-post-changes.php:16-27` | Ask Meta. Temporarily remove `email_post_changes_emails` during step 7 if so **[unverified]** |
| 16 | Monitoring | Import failures are silent (WP_Error under cron) | pipeline 05 §3.4 | Same gap as every other handbook. Out of scope here |

---

## Appendix A. Spike: adoption in place, against the real importer

**Environment.** Local wp-env DevHub (`~/Developer/wordpress-org/wporg-developer`, WordPress 7.2-alpha-64298). The local DB
holds 139 published plus 1 private `theme-handbook` posts. Their paths, `menu_order`s and titles are identical to
production (the comparison differed only in `&#038;` versus `&amp;` in 7 titles), though their IDs differ.

**Method.** The scripts were kept in the scratchpad, not the repo.
- One `wp eval` per run (`npx wp-env run cli wp eval "$CODE"`), with the code built from the draft class (renamed
  `DevHub_Theme_Draft_Importer` to avoid the other agent's class) plus a harness.
- The harness opens `START TRANSACTION`. All tables involved are InnoDB.
- It **deletes all `wporg_markdown_*` meta** on `theme-handbook` posts to simulate wp-admin-authored posts.
- It snapshots every post, builds a path-keyed manifest from the published posts (parent = parent key, or the bare
  slug for the private parent), and stubs HTTP with `pre_http_request`: manifest JSON, and per-page Markdown with H1,
  alerts, `{#id}`, a relative link and PHP code, with stable ETags and 304 on match.
- It runs `import_manifest()` and `import_all_markdown()`, diffs, runs both again, runs a hijack test, then
  `ROLLBACK`.
- DB row count and `MAX(post_modified)` were confirmed unchanged by my runs afterwards. The only intervening writes
  came from the other agent's import at 14:37:41 UTC.

**Results (run 3, final draft).**

```
deleted 419 importer meta rows (simulated wp-admin state)
BEFORE: {"publish":139,"private":1}
MANIFEST ENTRIES: 139
Success: Successfully created 0 and updated 139 handbook pages.
Success: Successfully updated 139 of 139 pages.
AFTER: 140 posts; new posts: []
FIELDS CHANGED (count of posts): {"status":0,"link":0,"parent":0,"order":0,"title":0,"author":0,"date":0,"modified":139,"name":0}
HTTP: {"200":139,"304":0}
LANDING: 2868 http://localhost:8888/themes/ src=https://github.com/WordPress/theme-handbook/blob/trunk/handbook/index.md
SECOND PASS HTTP: {"200":0,"304":139} max(modified) 2026-10-12 14:39:09 -> 2026-10-12 14:39:09
existing "testing" posts: [2930 /themes/advanced-topics/testing/, 2941 /themes/releasing-your-theme/testing/]
Success: Successfully created 0 and updated 1 handbook pages.      <- new key features/testing, slug "testing"
after hijack test: post 2930 title='New Testing Page' link=/themes/features/testing/   <- existing page moved
post count 140 -> 140
ROLLED BACK
```

Sample stored content, and the same content after `the_content`:

```html
<!-- stored -->
Intro for getting-started/what-is-a-theme. See <a href="http://localhost:8888/themes/getting-started/#intro">the parent</a> and <a href="./nope.md">a missing page</a>.
<div class="callout callout-info">
A note with <strong>bold</strong> and <code>code</code>.
Second line of the note.
</div>
<h2 id="custom-anchor">Custom heading</h2>
<pre class="wp-block-code"><code class="language-php">&lt;?php echo 'x'; ?&gt;
</code></pre>

<!-- rendered -->
<p>Intro for … <a href="http://localhost:8888/themes/getting-started/#intro">the parent</a> …</p>
<div class="callout callout-info">
<p>A note with <strong>bold</strong> and <code>code</code>.<br />
Second line of the note.</p>
</div>
```

Separate checks:
- Shortcodes in code were stored `[[video mp4="a.mp4"][/video]]` and rendered `[video mp4="a.mp4"][/video]`. The
  first attempt with `&#91;` was decoded by kses and the video shortcode executed.
- Block comments in fenced and inline code were stored escaped, with `has_blocks() === false`.
- Capabilities: `handbook_editor` baseline `edit_post` was `true`; with the draft, `edit_post` and `delete_post` were
  `false`, and administrator stayed `true`.

Not covered by the spike:
- HTTP-triggered cron (the kses-on-title difference; pipeline 04 measured it).
- Real GitHub fetches and CDN caching.
- Raw production `post_content`.
- Visual rendering in a browser.
- `[embed]`.
- Behaviour with posts that have no prior revisions.
