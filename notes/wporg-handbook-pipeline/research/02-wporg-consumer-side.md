# How WordPress.org imports GitHub Markdown and publishes it as handbooks

Research date: 2026-10-11. This covers the consumer side: the WordPress.org code that pulls, imports, renders and deploys GitHub-hosted Markdown, mainly for developer.wordpress.org/block-editor/. The Gutenberg (source) side is covered in a separate report.

## Sources inspected

| Repo | Commit inspected | What was read |
|---|---|---|
| [WordPress/wporg-developer](https://github.com/WordPress/wporg-developer) | `4cc3ba3671ecf8ca70b8c99792d4ede1ea38d462` (2026-10-08) | `source/wp-content/themes/wporg-developer-2023/` (`functions.php`, `inc/import-*.php`, `inc/rest-api.php`, `inc/cli.php`, `inc/handbooks.php`, `inc/shortcodes.php`, `inc/formatting.php`, `inc/search.php`, templates, patterns), `composer.json`, `.wp-env.json`, `env/setup.sh`, `.github/workflows/*`, `readme.md`, `getting-started.md` |
| [WordPress/wordpress.org](https://github.com/WordPress/wordpress.org) (Git mirror of meta.svn) | `cddeb14946258e306fafd2c6151bbc9f9947a835` (2026-10-09) | `plugins/wporg-markdown/`, `plugins/handbook/`, `plugins/wporg-cli/` |
| [Automattic/jetpack](https://github.com/Automattic/jetpack) | `afba8e94500dc60c2a2d80977f0f75555f925ecc` (2026-10-09) | `projects/plugins/jetpack/_inc/lib/markdown/{gfm,extra}.php` (the Markdown parser the importer uses) |
| [WordPress/wporg-mu-plugins](https://github.com/WordPress/wporg-mu-plugins) | `1faffaca1853159f5f5a5fda30242e8192cc6b68` (2026-10-05) | `mu-plugins/blocks/{chapter-list,table-of-contents,sidebar-container}` |
| [WordPress/wporg-documentation-2022](https://github.com/WordPress/wporg-documentation-2022) | `7ee3f93b85311c54b25a3d02a80a3cd9b7443cb0` (2026-09-09) | `support-helphub` post types, `mu-plugins/site-documentation.php`, workflows |
| WordPress/wordpress-develop `src/wp-includes/kses.php` | trunk, fetched 2026-10-11 | `$allowedposttags`, `wp_filter_post_kses()`, `kses_init()` |
| Live sites | fetched 2026-10-11 | All 8 manifests, plus HTML of several developer.wordpress.org and make.wordpress.org handbook pages |

The local `notes/reference/wporg-markdown/` copy (2026-10-07) is **byte-identical** to `wporg-markdown` at `cddeb14`. Its last functional commits were `8048fc9f7c` (2026-06-10, "Reject any manifest items that have invalid slugs") and `870a792194` (2026-04-16, "Query for all handbook entries").

Labels used in this report: **[verified]** means read in code or seen on the live site. **[inferred]** means reasoned from code paths or WordPress core behavior, not observed. **[unverified]** means not checked.

---

## 1. Importer subclasses

### 1.1 Class hierarchy

```
WordPressdotorg\Markdown\Importer                (wordpress.org: plugins/wporg-markdown/inc/class-importer.php, abstract)
├── DevHub_Docs_Importer                          (wporg-developer: theme inc/import-docs.php)  ← developer.wordpress.org
│   ├── DevHub_Block_Editor_Importer              inc/import-block-editor.php
│   ├── DevHub_Playground_Importer                inc/import-playground.php
│   ├── DevHub_REST_API                           inc/rest-api.php
│   ├── DevHub_Coding_Standards_Importer          inc/import-coding-standards.php
│   ├── DevHub_Advanced_Admin                     inc/import-advanced-admin.php
│   └── DevHub_SCF                                inc/import-scf.php
└── WPorg_Handbook_Importer                       (wordpress.org: plugins/handbook/inc/importer.php)  ← config-driven, any site running the handbook plugin

NOT subclasses (separate, older copies of the same logic):
- WPOrg_Cli\Markdown_Import   (wordpress.org: plugins/wporg-cli/inc/class-markdown-import.php) ← make.wordpress.org/cli/handbook
- DevHub_CLI                  (wporg-developer: theme inc/cli.php)                              ← developer.wordpress.org/cli/commands
```

The theme loads the importers only when the base class exists (`functions.php`):

```php
if ( class_exists( '\\WordPressdotorg\\Markdown\\Importer' ) ) {
	require __DIR__ . '/inc/import-docs.php';          // base class
	require __DIR__ . '/inc/import-block-editor.php';
	require __DIR__ . '/inc/import-coding-standards.php';
	require __DIR__ . '/inc/rest-api.php';
	require __DIR__ . '/inc/import-scf.php';
	require __DIR__ . '/inc/import-advanced-admin.php';
	require __DIR__ . '/inc/import-playground.php';
}
```

### 1.2 `DevHub_Docs_Importer`, the developer.wordpress.org base class (`inc/import-docs.php`)

- Each importer is a singleton. `do_init( $post_type, $base, $manifest_url )` sets three things:
  - `get_post_type()` returns `"{$post_type}-handbook"`.
  - `get_base()` returns `home_url( "{$base}/" )`.
  - `get_manifest_url()` returns the hard-coded URL.
- Hooks it registers:
  - `devhub_handbook_post_types`: adds the post type, which in turn feeds the handbook plugin's `handbook_post_types` filter through `Devhub_Handbooks::filter_handbook_post_types()`.
  - `handbook_post_type_defaults`: rewrites `rewrite.slug` to `$base` when the base differs from the post type, for example `blocks` → `block-editor`.
  - `cron_schedules`: adds `15_minutes`.
  - `init`: runs `register_cron_jobs()`.
  - The actions `devhub_{post_type}_import_manifest` and `devhub_{post_type}_import_all_markdown`.
  - `new Editor( $this )`, stored in `$GLOBALS['devhub_handbook_editors']`.
- The theme then removes the Editor's `the_title` edit-link filter (`functions.php`: "Remove GitHub edit links from handbooks"). The block theme renders its own "Improve it on GitHub" link instead (see §3).

### 1.3 Per-handbook table

| Handbook (URL) | Class / file | Post type | Base (rewrite slug) | Manifest URL (repo @ branch) | Manifest shape (live) |
|---|---|---|---|---|---|
| Block Editor, `/block-editor/` | `DevHub_Block_Editor_Importer`, `inc/import-block-editor.php` | `blocks-handbook` | `block-editor` | `https://raw.githubusercontent.com/WordPress/gutenberg/trunk/docs/manifest.json` | **JSON list**, 551 entries, keys `title, slug, markdown_source, parent`. Sources are relative (`../docs/README.md`). Root slug `handbook`. 0 duplicate slugs. |
| Playground, `/playground/` | `DevHub_Playground_Importer`, `inc/import-playground.php` | `playground-handbook` | `playground` | `https://raw.githubusercontent.com/WordPress/wordpress-playground/trunk/packages/docs/site/manifest.json` | object, 88 entries, with `order`. Sources relative to the manifest (`docs/main/intro.md`). Root slug `handbook`. |
| REST API, `/rest-api/` | `DevHub_REST_API`, `inc/rest-api.php` | `rest-api-handbook` | `rest-api` | `https://raw.githubusercontent.com/WP-API/docs/master/bin/manifest.json` | object, 62 entries, no `title` or `order`. Sources are `github.com/.../blob/...` |
| Coding Standards, `/coding-standards/` | `DevHub_Coding_Standards_Importer`, `inc/import-coding-standards.php` | `wpcs-handbook` | `coding-standards` | `https://raw.githubusercontent.com/WordPress-Coding-Standards/docs/master/manifest.json`. The sources point at `WordPress/wpcs-docs`; the old repo name redirects. | object, 12 entries |
| Advanced Administration, `/advanced-administration/` | `DevHub_Advanced_Admin`, `inc/import-advanced-admin.php` | `adv-admin-handbook` | `advanced-administration` | `https://raw.githubusercontent.com/WordPress/Advanced-administration-handbook/main/bin/handbook-manifest.json` | object, 75 entries, `order` (root `-1`) |
| Secure Custom Fields, `/secure-custom-fields/` | `DevHub_SCF`, `inc/import-scf.php` | `scf-handbook` | `secure-custom-fields` | `https://raw.githubusercontent.com/WordPress/secure-custom-fields/trunk/docs/bin/manifest.json` | object, 147 entries |
| WP-CLI commands, `/cli/commands/` | `DevHub_CLI`, `inc/cli.php` (**not** a subclass) | `command` (registered here, hierarchical) | `cli/commands` | `https://raw.githubusercontent.com/wp-cli/handbook/main/bin/commands-manifest.json` | (not fetched) |
| *(handbook plugin, config-driven)* | `WPorg_Handbook_Importer` | `{key}-handbook` | `config['slug']` | `config['manifest']` | e.g. Data Liberation, below |

Handbooks on developer.wordpress.org that are **edited in WordPress, not imported**: `apis-handbook` (Common APIs), `plugin-handbook` (`/plugins/`), and `theme-handbook` (`/themes/`). They come from the default list `apply_filters( 'devhub_handbook_post_types', [ 'apis', 'plugin', 'theme' ] )` in `inc/handbooks.php`. **[verified in code]**

### 1.4 Block Editor importer details (`inc/import-block-editor.php`)

**Hooks it adds:**

- `template_redirect` (priority 1): the `redirects()` method (below).
- `handbook_label`: sets the label to "Block Editor Handbook".
- `handbook_display_toc`: returns false. This disables the legacy in-content TOC; the theme disables it globally anyway.
- `get_post_metadata`: `fix_markdown_source_meta()`, described under "Edit link".
- `wporg_markdown_before_transform` and `wporg_markdown_after_transform`.
- `wporg_markdown_edit_link`.
- `pre_post_update` / `edit_post_blocks-handbook`: adds and removes `allow_extra_tags`, which allows a `<style>` element. **[inferred] This is ineffective for imports.** The importer already ran `wp_filter_post_kses()` on the HTML before it calls `wp_update_post()`, and `content_save_pre` kses runs inside `sanitize_post()` before `pre_post_update` fires. Any `<style>` is stripped before the filter is added.

**`before_transform`, Markdown-level rewriting:**

1. Strips a leading `# H1`. As a result, block-editor titles always come from the manifest `title`, never from the Markdown, because the base class's title regex no longer matches.
2. Removes `.md` and `readme.md` from relative links that point into `(../)+docs/`, `/docs/` or `/packages/`.
3. Rewrites `(../)+docs/X` and `/docs/X` to `https://developer.wordpress.org/block-editor/X/`. The URL is **absolute and hard-coded**.
4. Rewrites `/packages/components(/src)/X` to `https://developer.wordpress.org/block-editor/reference-guide/components/X/`, and `/packages/X` to `.../reference-guide/packages/packages-X/`.
   - Note the singular `reference-guide`. The real path is `reference-guides/`, so these links depend on a redirect. **[unverified whether one exists]** The `$path_redirects` table below has no `reference-guide/` entry.
5. Converts `~~x~~` to `<s>x</s>`.
6. Strips the trailing "Code is Poetry" footer image from package READMEs.

The rewriting only handles inline `[text](url)` links. Reference-style links, links to other directories (for example `/schemas/`) and links from other docs roots are not rewritten. **[inferred from the regexes]**

**`after_transform`, HTML-level rewriting:**

- Converts `{% codetabs %}{% JSX %}...{% Plain %}...{% end %}` into `<div class="code-tabs"><button data-language=… class="code-tab …">` plus `<div class="code-tab-block …">`.
- Converts the classes `php`, `js`, `jsx` and `css` to `language-*`. This is legacy: the current parser already emits `language-*` (§4.2), so the replacements are no-ops today.

**Redirects:** `redirects()` hooks `template_redirect` at priority 1 and acts on any `REQUEST_URI` starting with `/block-editor/`. It checks three hard-coded PHP arrays, then returns a 301 via `wp_safe_redirect`:

- `$redirects`: exact old path → new path, about 50 entries dated 2021–2025.
- `$path_redirects`: prefix rewrites, mostly from the March 2021 restructure.
- `$handbook_redirects`: paths that leave the handbook, for example `how-to-guides/themes/block-theme-overview` → `/themes/block-themes/`.

**This table is the only mechanism for slug or path changes.** Every Gutenberg docs restructure has needed a matching PR to wporg-developer, for example `c4ea9779f8` (2026-02-24, IAPI) and `034722c393` (2024-09-30, Navigator).

**Edit link:**

- The manifest gives relative sources. `generate_markdown_source_url()` resolves them against the manifest URL, so the stored meta `wporg_markdown_source` is a raw URL: `https://raw.githubusercontent.com/WordPress/gutenberg/trunk/docs/...md`.
- `fix_markdown_source_meta()` short-circuits `get_post_meta()` outside cron and WP-CLI. It rewrites `https://raw.githubusercontent.com/WordPress/gutenberg/` to `https://github.com/WordPress/gutenberg/edit/`, which produces `.../edit/trunk/docs/...md`.
- `wporg_markdown_edit_link()` replaces `/wp/{WP_CORE_STABLE_BRANCH}/` with `/trunk/`. This is legacy from when the manifest pointed at a `wp/X.Y` branch.
- Live check: `https://github.com/WordPress/gutenberg/edit/trunk/docs/reference-guides/block-api/block-supports.md`. **[verified live]**

**Index page:** the manifest's first entry has `slug: "handbook"`, `parent: null`. Top-level chapters such as `getting-started` also have `parent: null`. They are root-level posts, not children of `handbook`, so their URLs are `/block-editor/getting-started/`. The `handbook`-slug post is the landing page (§3.1).

### 1.5 Playground importer (`inc/import-playground.php`, 1,196 lines, added 2026-07-15 in `5a36e40ddd`)

This is the most elaborate subclass and the closest template for a non-trivial source. Commit history: `5a36e40ddd` added the importer (#569). `af7657d23e` added image import (#572). `6f708fa186` imported the Blueprint step reference (#574). `b1486a733d`, `ddec5b8de4` and `7cbec8dad5` (2026-09) added translation links.

**`before_transform` (`transform_mdx`): makes MDX importable.**

- Removes `import … from '…';` lines.
- Replaces `<BlueprintExample …/>` with a fenced JSON block plus a "Try it out!" `wp-block-button` linking to `playground.wordpress.net/?mode=seamless#<base64>`.
- Replaces `<PhpCodeSnippet…/>` with a `[playground_php_snippet encoded="<base64 HTML>"]` shortcode. The shortcode is rendered at display time, which gets raw HTML (a `<php-snippet>` web component plus an ES-module script) **past kses**. This is the pattern to copy whenever imported content needs markup that kses would strip.
- Replaces the dynamic Blueprint steps `.map()` React block with Markdown fetched from `https://wordpress.github.io/wordpress-playground/handbook/blueprints-steps.md`.

**`after_transform`, applied in priority order:**

| Priority | Callback | What it does |
|---|---|---|
| 10 | `parse_callout_markdown` | Runs Markdown inside `<div class="callout…">`, because the Jetpack parser leaves raw HTML blocks alone |
| 15 | `format_run_blueprint_links` | Turns `<a><kbd>Run Blueprint</kbd></a>` into a button |
| 20 | `rewrite_root_relative_links` | Prefixes `/foo` links with the handbook base, and maps Docusaurus filename-derived paths (`01-foo.md` → `foo`) to manifest keys. The map is built by re-fetching the manifest and is cached in a transient for 15 minutes |
| 20 | `rewrite_root_relative_image_sources` | Rewrites `/img` to `https://wordpress.github.io/wordpress-playground/img` |
| 25 | `import_images` | Sideloads images (below) |

**Image sideloading** (`import_images`, production only, `wp_get_environment_type() === 'production'`):

- Only standalone images are handled, meaning an image alone in a `<p>` or on its own line.
- Each one is sideloaded with `media_sideload_image()` into the media library and attached to the post.
- Status is tracked in post meta `_playground_image`, with values `downloaded` or `failed`.
- Existing attachments are reused, matched by `_source_url`.
- The `<img>` is replaced with **serialized block markup**: `<!-- wp:image {"id":…,"sizeSlug":"full","linkDestination":"none"} --><figure class="wp-block-image size-full"><img … class="wp-image-ID"></figure><!-- /wp:image -->`.
- Live: `/playground/handbook/web-instance/` serves `https://i0.wp.com/developer.wordpress.org/files/2026/07/dock-overview.webp` with `srcset`. **[verified live]**

**Rendering bug caused by the block markup [verified live]:**

1. The parser strips bare `<p>` tags (§4.2) and relies on `wpautop` at render time.
2. When `post_content` contains any block comment, core's `do_blocks()` removes `wpautop`.
3. As a result, `/playground/handbook/web-instance/` renders its paragraphs as bare text nodes with no `<p>` elements. Headings and lists are unaffected.
4. Block Editor pages have no block comments, so they get proper `<p>` elements (§3.3).

Anyone copying the sideloading approach must also wrap paragraphs, for example by setting `strip_paras = false` or emitting `wp:paragraph`/`wp:freeform`.

**ETag bypasses** (filter `wporg_markdown_check_etags`):

- `CONTENT_TRANSFORM_VERSION = 3` is stored per post. When the importer's own transform logic changes, bumping it re-imports pages whose source has not changed.
- The ETag is always bypassed for the steps page, because it is generated from TypeDoc.
- The ETag is bypassed while images are still pending.

The Block Editor importer has **no equivalent**. After a transform change, unchanged Gutenberg docs keep their old HTML until each file changes upstream, or until someone runs the import with `add_filter( 'wporg_markdown_check_etags', '__return_false' )`, as `getting-started.md` documents for Playground. **[inferred]**

**Translations:** reads `https://wordpress.github.io/wordpress-playground/translation-availability.json` and stores locales in `_playground_translation_locales`. A `render_block` filter on `core/post-title` adds "Also available in: …" links to the **upstream Docusaurus site** (`wordpress.github.io/wordpress-playground/{locale}/…`). The translations are not imported.

**Edit link bug [verified live]:**

- `rewrite_markdown_edit_link` only filters `get_edit_post_link`. The theme's `[article_edit_link]` shortcode (§3.2) reads the meta directly.
- As a result, the live "Improve it on GitHub" link on `/playground/` is the raw URL `https://raw.githubusercontent.com/WordPress/wordpress-playground/trunk/packages/docs/site/docs/main/intro.md`.
- `[article_changelog_link]` returns `#`, because `raw.githubusercontent.com` does not contain `github.com`.

### 1.6 The other subclasses

- **REST API, Advanced Administration, SCF:** label override only. No transforms, no redirect table.
- **Coding Standards:** label override, plus a `the_content` filter `fix_double_encoding()` that repairs `&amp;amp;`, `&amp;lt;` and similar inside code shortcodes (meta trac #5346).
- **REST API styling:** `inc/handbooks.php` adds the body class `rest-api-handbook-reference` to children of the `reference` page.

### 1.7 The `Editor` class (`wporg-markdown/inc/class-editor.php`)

**Frontend:**

- `get_edit_post_link`: points at GitHub (frontend only, `! is_admin()`).
- `the_title`: appends `<a class="github-edit">`. The icon is loaded from `plugins/wporg-cli/assets/images/github-mark.svg`, a hidden dependency on the wporg-cli plugin's assets. DevHub removes this filter.
- `o2_filter_post_actions`: swaps o2's inline edit for a GitHub link. This matters on make/P2 sites.

**Admin:**

- `edit_form_top` prints a warning: "This page is maintained on GitHub. Content, title, and slug edits here will be discarded on next sync."
  - **[inferred] That is only partly true.** Because of ETag 304 short-circuiting, a manual content edit survives until the upstream file next changes.
  - Title and parent edits are overwritten on the next 304 pass, but only when they differ from the manifest.

**URL logic in `get_markdown_edit_link()`:**

- If the host is not exactly `github.com`, the stored URL is returned **unchanged**, so raw URLs stay raw.
- Otherwise `/blob/` becomes `/edit/`.
- The result is then filtered through `wporg_markdown_edit_link`.

**How each handbook ends up with a correct edit link:**

- REST API, WPCS, Advanced Administration and SCF have correct links because their manifests use `github.com/.../blob/` URLs.
- Block Editor has a correct link only because of its meta-read hack (§1.4).
- Playground does not (§1.5).

---

## 2. Scheduling and triggering

### 2.1 Cron events

| Importer | Hook names | Interval | Where |
|---|---|---|---|
| DevHub handbooks | `devhub_{blocks,playground,rest-api,wpcs,adv-admin,scf}_import_manifest` and `…_import_all_markdown` | `15_minutes`, the class default `$cron_interval` | `DevHub_Docs_Importer::register_cron_jobs()` on `init` |
| DevHub CLI commands | `devhub_cli_manifest_import`, `devhub_cli_markdown_import` | `twicedaily` | `inc/cli.php` |
| Handbook plugin importer | `handbook_{base}_import_manifest`, `handbook_{base}_import_all_markdown` | `config['cron_interval']`, default `15_minutes`. An unknown interval falls back to `hourly`. | `plugins/handbook/inc/importer.php` |
| make/cli handbook | `wporg_cli_manifest_import`, `wporg_cli_markdown_import` | `15_minutes` | `plugins/wporg-cli/wporg-cli.php` |

**How the jobs are scheduled and run:**

- There is **no webhook and no push trigger**. The import is purely a poll of `raw.githubusercontent.com`. **[verified: no webhook/REST route exists in any of the code read]**
- The two events are scheduled independently with `wp_schedule_event( time(), … )`, so the manifest pass and the content pass are not ordered relative to each other. **[inferred]**
- A page newly added to the manifest is therefore created with the manifest title and **empty content**, and is published as such until the next `import_all_markdown` tick. That can take up to about 15 minutes. **[inferred]**
- Worst-case latency from merge to live: about 15 minutes of cron, plus raw.githubusercontent.com's CDN cache (about 5 minutes, **[unverified]**). Each Markdown request carries a `?v=time()` cache-buster, but the manifest request does not.

**Running an import by hand:**

- No dedicated wp-cli command exists. The importer methods print `WP_CLI::log()`/`success()` because they are run through `wp cron event run devhub_blocks_import_manifest`, and so on.
- `env/setup.sh` runs `wp cron-concurrent run --filter=import_manifest && wp cron-concurrent run`. `dd32/wpcli-cron-concurrent` is a composer dev dependency, which suggests production cron is driven by WP-CLI. **[inferred]**
- `getting-started.md` documents the manual PHP route: `do_action( 'devhub_playground_import_manifest' ); add_filter( 'wporg_markdown_check_etags', '__return_false' ); do_action( 'devhub_playground_import_all_markdown' );`.
- `package.json` has `playground:import-docs` (`IMPORT_POST_TYPE=playground yarn playground:import-docs`), which runs both actions inside WordPress Playground for local preview.

### 2.2 Lifecycle behavior (from `class-importer.php`)

| Situation | What happens | Basis |
|---|---|---|
| Manifest fetch fails (WP_Error or non-200) | `import_manifest()` returns a `WP_Error`, or `WP_CLI::error`. Nothing is created or changed. `import_all_markdown` still runs on its own using the per-post meta URLs. | [verified in code] |
| Manifest is invalid JSON, empty or `[]` | `invalid-manifest` WP_Error. No changes. | [verified] |
| Markdown fetch is non-200 (for example the file was deleted) | WP_Error for that post. The post keeps its old content and **stays published**. | [verified] |
| Page removed from the manifest | **Nothing.** The importer has no delete or trash code path. The post stays published at its old URL, and `import_all_markdown` keeps refreshing it from its stored source URL for as long as that file exists. If the file is gone, the post keeps its last content. Cleanup is manual in wp-admin. | [verified: no `wp_delete_post`/`wp_trash_post` anywhere in wporg-markdown] |
| Slug or key change | The lookup tries `existing[key]`, `existing['slug_only'][key]`, `existing[slug]` and `existing['slug_only'][slug]`. If all miss, it creates a **new post** and the old one is left behind, still published. Hence the redirect tables, and old posts must be trashed by hand. | [verified lookup; orphaning inferred] |
| Parent change in the manifest | `update_post_from_manifest()` compares `manifest_entry['parent']` with the current parent's `post_name`, then calls `get_page_by_path( parent_slug )`. A bare slug resolves only for a **top-level** page, so moving a page under a nested parent likely fails silently and the old parent is kept. | [inferred from core `get_page_by_path`] |
| Title change | If the Markdown has a `# H1`, it becomes the title on the next 200 response. Otherwise the manifest `title` is used. Block Editor always strips the H1, so its titles come from the manifest. On a 304, the manifest-derived fields (`menu_order`, `post_title`, `post_parent`) are re-applied only if they differ. | [verified] |
| Change detection | Per-post ETag. `If-None-Match` is sent with the ETag stored in `wporg_markdown_etag`. A 304 skips the content update. No content hashing. The manifest itself is not ETagged and is fetched in full on every run. | [verified] |
| `post_modified` | Bumped only on a 200 (`wp_update_post`), or when a manifest-derived field actually differs (the fix in `a1c3f68199`, 2024-01: "Don't constantly update posts which have fields derived from the manifest"). The theme shows "Last updated" only when `modified > date` (`[last_updated]` shortcode). | [verified] |
| Post IDs | Kept. Updates go by ID through `wp_update_post`, and each update creates a revision because the post type `supports` includes `revisions`. | [verified] |
| Non-published posts | Only `post_status = publish` posts are loaded as "existing". A drafted or trashed imported page is therefore **re-created** on the next manifest run, and `wp_unique_post_slug` would probably give it a `-2` slug. | [inferred] |
| Slug validation | `create_post_from_manifest_doc` refuses any doc whose `sanitize_title_with_dashes( slug ) !== slug` (since 2026-06). `index` is mapped to the post type name. | [verified] |
| `order` | Set only when the manifest is a JSON **list**, where the index becomes `order`, or when `order` is given explicitly. Applied as `menu_order`. `update_post_from_manifest()` uses `! empty( order )`, so order `0` is never re-applied. | [verified] |
| Slug uniqueness | For a list manifest such as Gutenberg's, the key **is** the slug, so slugs must be unique across the whole handbook. `parent` is a slug, not a path. | [verified] |
| Post author | DevHub sets none, so posts are created with `post_author = 0` under cron **[inferred]**. `WPorg_Handbook_Importer` sets the `wordpressdotorg` user through `wporg_markdown_post_data_pre_insert`. | [verified] |
| Excerpt | The first line of `wp_strip_all_tags( html )`. | [verified] |

---

## 3. Rendering

### 3.1 The `handbook` plugin (`wordpress.org/.../plugins/handbook/`, v2.0)

**Registration:**

- `WPorg_Handbook_Init::init()` runs on `after_setup_theme`.
- It reads the deprecated `handbook_post_types` filter (a list of names, which DevHub uses) and the newer `handbooks_config` filter (keyed config with `label`, `slug`, `manifest` and `cron_interval`).
- The filter name is **`handbook_post_types`**, not `wporg_handbook_post_types`.
- Post type naming: `{key}-handbook`, unless the key is `handbook` or already contains `-handbook`.
- With no config at all, it falls back to a single `handbook` post type. That is the normal make.wordpress.org case.

**`register_post_type` (on `widgets_init`):**

- Arguments: `public`, `show_in_rest`, `hierarchical => true`, `has_archive => true`, `capability_type => 'handbook_page'`, `map_meta_cap`, `rewrite.slug`.
- `supports`: `title, editor, author, thumbnail, page-attributes, custom-fields, revisions, wpcom-markdown`.
- Filterable through `handbook_post_type_defaults`. DevHub uses that filter to add `show_in_rest`, pluralize `plugins/` and `themes/`, and swap the base slug.

**Landing page:**

- A top-level post whose slug is `welcome`, `handbook`, `{base}` or `{base}-handbook` becomes the landing page.
- Its permalink is rewritten to the post type archive URL, and direct hits on it are 301'd to the archive.
- `pre_get_posts` and `posts_pre_query` make the archive URL render that page.
- This is why `index` maps to the post type name and why manifests use the `handbook` slug.

**Other features in the plugin:**

- Legacy in-content TOC (`table-of-contents.php`, `wporg_handbook_toc_should_add_toc` / `handbook_display_toc`). **The DevHub theme disables it** (`add_filter( 'wporg_handbook_toc_should_add_toc', '__return_false' )`).
- Breadcrumbs (`handbook_breadcrumbs` action).
- Previous/next navigation from a menu or the pages widget.
- Watchlist (o2/P2 "Watch" action plus the Email Post Changes integration). DevHub hooks `WPorg_Handbook_Watchlist::display_action_link` to `wporg_action_links`.
  - **[unverified]** whether imported updates send watch emails.
- Callout shortcodes `[info] [tip] [alert] [tutorial] [warning]`, rendered as `<div class='callout callout-{type}'>` plus a screen-reader prefix.
- A `wporg/callout` block (`inc/blocks.php`).
- A glossary.
- Admin notices, including "This is an imported handbook! … Any local changes will be overwritten …" when `config['manifest']` is set.
- A "Not Imported" post state on posts without manifest meta.

### 3.2 How wporg-developer-2023 themes the handbook pages

**Template selection.** `add_handbook_templates()` in `functions.php` filters the template hierarchy:

```php
if ( $is_handbook )      array_unshift( $templates, 'single-handbook.php' );
if ( $is_github_source ) // ! empty( get_post_meta( id, 'wporg_markdown_source', true ) )
	get_post_type() === 'blocks-handbook'
		? array_unshift( $templates, 'single-handbook-block-editor.php' )
		: array_unshift( $templates, 'single-handbook-github.php' );
```

The selected block templates are `templates/single-handbook{,-github,-block-editor}.html`. They share one layout:

- `header-alt` and `search-wide` template parts.
- A three-column group:
  - `<main><article>`: `core/post-title` (h1), then the `article-sidebar` pattern (`wporg/sidebar-container` > **`wporg/table-of-contents`**), then **`core/post-content`**, then the article-meta pattern, then the `handbook-pagination` pattern (`core/post-navigation-link` previous/next).
  - `wporg/sidebar-container` > **`wporg/chapter-list`**.
- The footer.

**The article-meta patterns:**

- `article-meta.php`: for handbooks edited in WordPress.
- `article-meta-github.php`: "First published" (`post-date`), `[last_updated]` with the modified date, "Edit article → Improve it on GitHub" (`[article_edit_link]`), and "Changelog → See list of changes" (`[article_changelog_link]`, which turns `/edit/` into `/commits/`).
- `article-meta-block-editor.php`: the same, but **without** the Changelog item.

The shortcodes live in `inc/shortcodes.php`. `get_markdown_edit_link()` duplicates the Editor class logic **without** the `wporg_markdown_edit_link` filter.

**The mu-plugins blocks (from `WordPress/wporg-mu-plugins`):**

- **`wporg/chapter-list`** (`mu-plugins/blocks/chapter-list/index.php`):
  - Calls `wp_list_pages( [ 'post_type' => current type, 'sort_column' => 'menu_order, title', 'walker' => new Chapter_Walker() ] )` and renders a "Chapters" heading.
  - The walker hides orphaned pages, meaning pages with an unpublished ancestor.
  - Sidebar order is therefore entirely `menu_order` (manifest order), then title.
- **`wporg/table-of-contents`** (`mu-plugins/blocks/table-of-contents/index.php`):
  - Regex-parses `<h1-6>` out of `get_the_content()` (filter `wporg_table_of_contents_post_content`) and lists h2–h3 under "In this article".
  - Renders nothing if there are fewer than 2 headings.
  - Adds a priority-5 `the_content` filter that injects `id`s and anchor links into the headings. Live output: `<h2 id="customize-playground" class="is-toc-heading" tabindex="-1"><a href="#…">`.
  - Heading ids are generated at render time from the heading text, not taken from the Markdown. Explicit `{#id}` syntax is not supported. **[inferred]**

### 3.3 Classic HTML inside a block theme

- The stored `post_content` is classic HTML with **bare `<p>` stripped** by the parser. Paragraphs are separated by blank lines.
- `core/post-content` runs `the_content`, so `wpautop`, shortcodes, `wptexturize`, DevHub filters (autolinking of `function()` references, `make_doclink_clickable`, `fix_unintended_markdown`) and the TOC id injection all apply.
- Without block comments, the content is treated as freeform/classic and `wpautop` restores `<p>`. The live Block Editor page `/block-editor/getting-started/fundamentals/block-json/` shows proper `<p>` elements, `<div class="callout callout-info">` and `<pre><code class="language-json">`. **[verified live]**
- With any block comment, as on Playground pages that have sideloaded images, `wpautop` is dropped and paragraphs lose their `<p>` (§1.5). **[verified live]**

---

## 4. Content constraints

### 4.1 kses

The importer calls `wp_filter_post_kses( $html )` explicitly. That function is `wp_kses( $data, 'post' )` and applies **regardless of user**. Under cron there is no current user, so `kses_init()` also attaches `content_save_pre` kses, and the content is filtered twice. **[verified core]**

The importer's own `wp_kses_allowed_html` hook only re-adds `<a>` if it is missing.

What core `$allowedposttags` allows (trunk, 2026-10-11):

- **Allowed:** `details`/`summary` (`open`, `name`), `video` (`src`, `controls`, `autoplay`, `loop`, `muted`, `playsinline`, `poster`, `preload`, `width`, `height`), `audio`, `track`, `figure`/`figcaption`, the table elements, `button`, `kbd`, `mark`, `dialog`, `img`, `div`, `span`, `pre`, `code`, `section`, `nav`, and others.
- **Global attributes:** `class`, `id`, `style` (CSS-filtered), `role`, `aria-*`, `data-*`, `title`, `lang`, `dir`, `hidden`, `tabindex`.
- **Stripped:** `iframe`, `script`, `style`, `svg`, `source`, `picture`, `input`, `select`, `form`, and `object` beyond its narrow attributes. So `<video><source>` loses the source, and only `<video src>` works. YouTube or other iframes cannot be embedded. There is also no oEmbed, because a bare URL is not on its own line in the classic sense after wpautop. **[unverified whether oEmbed autoembed fires on these posts]**
- HTML comments survive, which is why the Playground `wp:image` block comments work.
- Any markup that has to bypass kses must go through a display-time shortcode or a `the_content` filter. Playground's `[playground_php_snippet]` is the working example.

### 4.2 Code blocks

The parser is `WPCom_GHF_Markdown_Parser` (Jetpack `_inc/lib/markdown/gfm.php`, which extends Markdown Extra). The importer sets `preserve_shortcodes = false`.

**How fenced code is emitted:**

- If the `SyntaxHighlighter` class exists, fenced code becomes `[code lang=X]…[/code]`.
- Otherwise it becomes `<pre><code class="language-X">` (Markdown Extra's `MARKDOWN_CODE_CLASS_PREFIX = "language-"`).
- On developer.wordpress.org the live output is `<pre><code class="language-json">`, so SyntaxHighlighter is **not** active there. **[verified live]**

**How it is highlighted:**

- The highlighter is **Code Syntax Block** (mkaz, Prism), a composer dependency.
- The theme forces it to load on every page (`mkaz_code_syntax_force_loading`) and points it at its own Prism theme (`mkaz_prism_css_path` → `/build/prism/style-index.css`).
- Prism highlights any `code[class*=language-]` client-side. **[inferred]**

**Code shortcodes:** the theme also registers `[code]`, `[php]`, `[js]` and `[css]` shortcodes (`inc/formatting.php`). They render a `core/code` block with `language-X` and line numbers when there are more than 4 lines. The language whitelist is `js json sh bash html css scss php markdown yaml`; anything else becomes `php`; `sh`/`bash` become `shell`. That matters only if the Markdown contains literal `[code]` shortcodes.

**Parser details:**

- `strip_paras = true`, so bare `<p>` is removed (`unp()`).
- `~~` becomes `<del>`. Block Editor pre-converts it to `<s>`.
- Markdown Extra supports tables, footnotes, `{#id .class}` header attributes, and definition lists. **[inferred from the parser lineage; header-attribute support not tested]**
- Raw HTML blocks are **not** Markdown-parsed inside. That is why Playground re-parses callout contents.
- GFM admonitions (`> [!NOTE]`) are **not** supported. They would render as a blockquote containing literal `[!NOTE]`. **[inferred]**

### 4.3 Images

- **Block Editor:** no sideloading. The Markdown references absolute URLs that were uploaded to developer.wordpress.org's media library by hand (`https://developer.wordpress.org/files/2023/11/block-json.png`). Jetpack Photon rewrites them to `i0.wp.com` on output. **[verified live]** Relative image paths are not rewritten, so they would 404.
- **Playground:** rewrites root-relative paths to the Docusaurus site, then sideloads in production (§1.5).
- **Other handbooks:** no image handling. Images must be absolute URLs (developer.wordpress.org/files, raw GitHub, and so on). **[inferred]**

### 4.4 Relative links

The base importer does **nothing** with links. Every handbook-specific rewrite lives in its subclass:

- Block Editor: regexes in `before_transform` producing absolute developer.wordpress.org URLs.
- Playground: root-relative `href`s plus the Docusaurus path map.

A relative `./foo.md` link in REST API or WPCS sources stays as `foo.md` and breaks. **[inferred]**

### 4.5 Callouts

There are three working forms:

1. Raw `<div class="callout callout-{info|tip|alert|warning|tutorial}">…</div>`, styled by `handbook/stylesheets/callout-boxes.css`. Gutenberg docs use this.
2. Handbook shortcodes `[info]…[/info]` and the like, expanded at render time.
3. The `wporg/callout` block, which only works in block markup and is not useful for imported HTML.

Markdown inside a raw `<div>` is **not** parsed unless a subclass re-parses it, as Playground does. Gutenberg docs therefore write inline HTML (`<a>`, `<code>`) inside callouts.

---

## 5. Search and i18n (brief)

**Search on developer.wordpress.org:**

- `inc/search.php` scopes searches made from a handbook page to the current handbook post type (`$query->is_handbook` → `post_type = wporg_get_current_handbook()`).
- Otherwise it searches the parsed code-reference types.
- It runs on plain `WP_Query` with custom orderby. **[unverified whether an Elasticsearch/Jetpack Search backend is attached on production]**
- Handbook post types are added to the Jetpack sitemap (`jetpack_sitemap_post_types`).

**HelpHub search:** `mu-plugins/site-documentation.php` in wporg-documentation-2022 redirects all searches to `https://wordpress.org/search/{q}/?in=support_docs` (WordPress.org's global search). How that index is built is **[unverified]**.

**i18n:**

- There is no translation path for imported handbooks. Content is English only.
- There is no GlotPress or Rosetta pipeline in any of the code read. Only theme UI strings use the `wporg` textdomain.
- The only "translation" feature is Playground's links to the upstream Docusaurus translations (§1.5).

---

## 6. Deployment, and where a HelpHub importer would live

### 6.1 How code reaches production

**WordPress.org repo** (`wporg-markdown`, `handbook`, `wporg-cli` plugins):

- The GitHub repo describes itself as "WordPress.org Meta, Git-ified … just a mirror of the WordPress Meta subversion repository. Please include a link to a pre-existing ticket on https://meta.trac.wordpress.org/ with every pull request."
- Changes land as **SVN commits to meta.svn.wordpress.org by a Meta committer**, against a Meta Trac ticket. GitHub PRs are for review only.
- The mirror has PHPCS and unit-test GitHub workflows.
- Deploying to the live servers is done by the systems/meta team. **[unverified mechanics]**
- wporg-developer's `composer.json` pulls `wporg-markdown` and `handbook` straight from `https://meta.svn.wordpress.org/sites/trunk/...` for local dev.

**wporg-developer repo:**

- Work goes through GitHub PRs to `trunk`.
- `.github/workflows/build.yml` runs on every push to trunk. It builds with `yarn workspaces run build` (`@wordpress/scripts`) and `composer install`, trims the repo down to the theme directory, appends `-{sha7}` to the `style.css` version, and force-pushes the result to the **`build`** branch.
- `build-branch.yml` builds every other branch to `dist/<branch>` "exactly as the live SVN theme expects", so a sandbox can check it out.
- Getting from `build` into the production SVN or servers is a WordPress.org-internal sync and deploy that is not in the public repo. **[unverified]**
- The HelpHub mu-plugin header hints at the same model: "This file is synced from github … sync the changes with ./bin/sync/wporg-documentation.sh", a script in the private dotorg repo.

**wporg-documentation-2022:** the same pattern. GitHub PR → `build.yml` → `build` branch → internal sync.

**The documentation repos themselves** (Gutenberg, Playground, and others) need no deploy. A merged change is live within about 15 minutes through cron, *unless* it renames or moves pages. Then it also needs a wporg-developer PR for the redirects and a manual wp-admin cleanup of orphaned posts.

### 6.2 What a HelpHub importer would need

**Background.** HelpHub (WordPress.org/documentation/) runs `wporg-documentation-2022`, which contains:

- The theme.
- The `support-helphub` plugin.
- `mu-plugins/site-documentation.php`.

The article post type is `helphub_article`:

- `hierarchical => false`, `rewrite.slug => 'article'`, `has_archive => 'articles'`.
- `supports`: `title, editor, excerpt, thumbnail, author, page-attributes, revisions, comments`.
- It is categorized by the core-named `category` taxonomy, registered by HelpHub on `post` and `helphub_article`.
- Its URLs are flat: `/documentation/article/{slug}/`.

**Where the code would live:** a `HelpHub_Importer extends WordPressdotorg\Markdown\Importer` belongs in `support-helphub` (or the theme), guarded by `class_exists`, the same way DevHub does it. The `wporg-markdown` plugin would also have to be activated on the documentation site, which is a systems or meta request. **[unverified whether it is already active there]**

**What the importer assumes, and what would have to change:**

| Importer assumption | HelpHub reality | Needed change |
|---|---|---|
| Hierarchical post type; `post_parent` from `parent`; keys derived from `get_permalink()` minus `get_base()` | Flat `article/{slug}` | Set `get_base()` to `home_url('article/')`, so the key is the slug. Use a flat manifest with `parent: null`. `post_parent` is stored but ignored by the permalinks. |
| Grouping and navigation through `post_parent` + `menu_order` (chapter list) | Grouping is the `category` taxonomy plus curated category landing pages | The importer has **no taxonomy support**. A manifest `meta` key only writes post meta. Add a manifest field such as `categories` and assign it in a subclass with `wp_set_object_terms()`. `tax_input` on `wp_insert_post` will not work under cron, because there is no user with `assign_terms`. **[inferred]** |
| Only `publish` posts are "existing"; match by key or slug | About a thousand existing hand-edited articles | Matching by slug is useful: a manifest entry whose slug equals an existing article **adopts it**, keeping its ID, URL and comments. Its content is overwritten from Markdown on the next run, because the ETag is empty. That is the migration path, and also the risk. |
| Stored HTML is classic, with bare `<p>` stripped | HelpHub articles are block-editor content | Mixed formats render fine in `core/post-content`. Avoid emitting any block comments unless paragraphs are also wrapped (§1.5 bug). |
| Editor class adds the `the_title` edit link and redirects `get_edit_post_link` to GitHub | Block theme with a `core/post-title` block | Remove the `the_title` filter as DevHub does, and add an "Edit on GitHub" element to the HelpHub article template. |
| No delete or trash; slug changes orphan posts | HelpHub already keeps a redirect array in `site-documentation.php` | Same process: add redirects for renames and trash orphans manually, or add a reconciliation step to the subclass. |
| Images: absolute URLs only | HelpHub uses its own media library | Either upload by hand and reference absolute URLs, as the Block Editor handbook does, or copy Playground's sideloading. |
| Relative links are not rewritten | — | A `before_transform`/`after_transform` link map, with Playground's `rewrite_root_relative_links` as the model. |

---

## 7. Other sites that use the same pipeline

| Site / handbook | Mechanism | Evidence |
|---|---|---|
| developer.wordpress.org: Block Editor, Playground, REST API, Coding Standards, Advanced Administration, SCF | `DevHub_Docs_Importer` subclasses of wporg-markdown | Code plus live "Improve it on GitHub" links **[verified]** |
| developer.wordpress.org: WP-CLI commands (`/cli/commands/`) | `DevHub_CLI`, a standalone copy (`twicedaily`, no ETag, no redirects) | Code **[verified]** |
| developer.wordpress.org: Plugin, Theme and Common APIs handbooks | Edited in WordPress (handbook plugin) | Default `devhub_handbook_post_types` list **[verified]** |
| make.wordpress.org/cli/handbook/ | `WPOrg_Cli\Markdown_Import` in the `wporg-cli` plugin. Standalone, the ancestor of wporg-markdown. Post type `handbook`. Manifest `wp-cli/handbook@main/bin/handbook-manifest.json`. `15_minutes`. **No ETag.** Allowlists the hosts `github.com` and `raw.githubusercontent.com` and the owner `wp-cli`. Has an admin "Markdown source" field with an "Import" button. | Code, plus live edit link `github.com/wp-cli/handbook/edit/main/index.md` **[verified]** |
| make.wordpress.org/hosting/handbook/ | GitHub-backed (`WordPress/hosting-handbook`, `bin/handbook-manifest.json`). Most likely `WPorg_Handbook_Importer` through a non-public `handbooks_config` entry with `manifest`. | Live edit link `github.com/wordpress/hosting-handbook/edit/main/index.md` **[verified]**; config location **[unverified, not in any public repo found]** |
| WordPress.org/data-liberation/and/ ("Data Liberation Guides") | `WPorg_Handbook_Importer` through `handbooks_config` in `wporg-main-2022/inc/data-liberation-handbook.php` (`'and' => [ 'manifest' => 'https://raw.githubusercontent.com/WordPress/data-liberation/add/manifest/assets/manifest.json', 'slug' => 'data-liberation/and' ]`) | Code **[verified]**. The manifest still returns 200 (9 entries), but `/data-liberation/and/` returns **404** live, so it is probably inactive. |
| make.wordpress.org/docs, core, meta, themes, accessibility, training, polyglots, test, plugins, performance, marketing handbooks | **Edited in WordPress** (default `handbook` post type, o2/P2) | No GitHub edit links on their live landing pages **[verified, landing pages only]** |

### How `handbook/inc/importer.php` (`WPorg_Handbook_Importer`) differs from DevHub's subclass

- **It is configuration-driven, not code-driven.** Any site running the handbook plugin can declare `handbooks_config[ key ] = [ 'manifest' => URL, 'slug' => …, 'cron_interval' => … ]`. On `after_handbooks_init`, `WPorg_Handbook::init_importer()` creates an importer for each handbook whose config has a `manifest`. No subclass file is needed.
- **Cron hook names** are `handbook_{base}_import_manifest` and `handbook_{base}_import_all_markdown`, instead of `devhub_…`. The interval comes from config, and an unknown interval falls back to `hourly`.
- **Post author:** imported posts get the `wordpressdotorg` user as author (filter `handbooks_import_default_author_slug`).
- **Admin UI:** adds a "Not Imported" post state, plus the "This is an imported handbook!" notice showing the manifest link and the import interval.
- **Bug:** `instance()` reads `$instances` (an undefined local variable) instead of `self::$instances`, so the duplicate-instance guard never triggers. **[verified in code; impact minor]**
- **No transform hooks of its own.** Per-handbook Markdown or HTML fixes would still need `wporg_markdown_before_transform`/`after_transform` filters keyed on the post type.
- **Same base behavior otherwise:** ETags, no deletion, hierarchical `post_parent`, kses, and the Jetpack parser.

---

## Key takeaways for the migration

1. **Polling, not push.** There are two independent 15-minute cron passes, with no webhook. Expect about 15–20 minutes from merge to live, and a window where new pages exist with empty content.
2. **Renames and removals are manual work on the WordPress.org side.**
   - The importer never deletes or trashes.
   - Changing a slug creates a new post and leaves the old one published.
   - Every restructure needs a redirect PR to wporg-developer (`import-block-editor.php` `$redirects`) and a wp-admin cleanup.
3. **Each handbook's link, image and callout conventions live in PHP regexes in wporg-developer, not in the docs repo.**
   - Block Editor links resolve only for `(../)+docs/`, `/docs/` and `/packages/` inline links, and are rewritten to absolute developer.wordpress.org URLs.
   - Images must be absolute (developer.wordpress.org/files).
   - Only Playground sideloads images.
4. **Rendering constraints.**
   - Content is classic HTML with `<p>` restored by `wpautop`; block comments break it.
   - kses strips `iframe`, `script`, `style`, `svg` and `source`.
   - Code is `<pre><code class="language-X">`, highlighted by Prism.
   - Heading anchors are generated at render time.
   - Sidebar order comes from `menu_order`, which is the manifest order.
5. **Edit links are fragile.** Block Editor works only through a `get_post_metadata` hack. Playground's live edit link is a raw URL and its changelog link is `#`. A manifest that uses `github.com/.../blob/` URLs avoids both problems.
6. **A HelpHub importer is feasible as a subclass in `support-helphub`, but needs three things:**
   - Taxonomy assignment via `wp_set_object_terms`.
   - A flat key/base.
   - Its own redirect and orphan handling.

   Slug-matching would adopt existing articles in place, keeping their IDs, URLs and comments.
