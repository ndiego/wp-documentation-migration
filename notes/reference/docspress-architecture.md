# DocsPress: technical architecture dossier

Source: `git clone --depth 1 https://github.com/Automattic/docspress` at commit `8584e707` (main, 2026-08-03), read on 2026-10-08. Paths below are relative to the repo root. Supplemented with the repo's `docs/`, the GitHub API (issues, PRs, releases, contributors), and docs.press itself. No repo code was executed.

## Key facts for the HelpHub evaluation

- **DocsPress is three separable pieces, and the sync engine is not a WordPress plugin.** The sync engine is a **Node 20 GitHub Action / npm CLI** (`action.yml`, `src/`, bundled into `dist/index.js`, 2.8 MB). It runs on a GitHub Actions runner and talks to WordPress only through the core REST API. Two packages are optional: a **block theme** (`theme/`) and a **"DocsPress Blocks" plugin** (`plugins/docspress-blocks/`). Nothing on the WordPress side pulls from GitHub. There is no webhook receiver, no cron job inside WordPress, and no GitHub App.
- **Content model: core `page` posts and nothing else.** There are no custom post types and no custom tables. Hierarchy uses `post_parent`, ordering uses `menu_order`, and the URL is the page path under a root page (default `/docs/`). Sync identity lives in an **HTML-comment "sentinel" inside `post_content`**. That sentinel holds a JSON blob with key, source path, hash, and the **full base64-encoded Markdown source**. The REST collection is hard-coded to `pages` (`src/wordpress.js:28`), and the PHP side hard-codes `'page'` throughout. HelpHub's `helphub_article` CPT and its category taxonomy are not supported without a fork.
- **Markdown pipeline:** gray-matter frontmatter plus unified/remark-parse/remark-gfm. Each Markdown node maps to one core block (paragraph, heading, list, quote, code, table, image, separator, html). Custom blocks travel in a JSON envelope inside an HTML comment (`<!-- docspress:block {...} -->`). **Images are not uploaded:** URLs pass through unchanged. **Redirects are placeholder pages that say "This page moved to …"**, not HTTP 301s. **There is no i18n or locale model at all.**
- **Two-way sync exists.** `propose` and `reconcile` modes poll WordPress on a schedule. An editor's change to an *existing managed* page becomes a rolling GitHub PR via a block-level LCS diff back into the Markdown. Pages created in WordPress, deleted pages, and slug, parent, or status changes are out of scope. A change made on both sides at once is reported as a conflict and fails the job.
- **Separability:** the Action works with any theme. The navigation sidebar, table of contents, search, breadcrumbs, edit links, "was this helpful", llms.txt and `.md` endpoints, and the sidebar and feedback post-meta registration all live **in the theme** (`theme/inc/blocks.php`, `theme/inc/llms.php`). Under wporg-parent-2021 you would have to port them. Versioning lives in the plugin.
- **Auth and host:** WordPress.com OAuth is the primary path (`public-api.wordpress.com/wp/v2/sites/{site}`). For self-hosted sites it sends `Authorization: Bearer <token>` only. Core WordPress Application Passwords use Basic auth and are not supported, so WordPress.org would need a Bearer-token auth plugin. docs.press itself runs on WordPress.com Atomic (`x-ac: … _atomic_dca`, Batcache).
- **Project health:** created 2026-07-09, so about 3 months old. One human author wrote about 138 of roughly 142 commits. There have been **no commits on main since 2026-08-03**. Three outside PRs have sat unmerged since late July. An open PR (#44, 2026-09-16, +14k/−13k lines) **renames the whole project to "Autodocs Publish"**, including the block namespace, package, and repo. Versions are pre-1.0 (Action v0.5.0, theme/plugin 0.10.7). There are no PHP tests.

---

## 1. What DocsPress is

### Components

| Piece | Location | Runtime | Required? |
|---|---|---|---|
| Sync engine (GitHub Action + `docspress` npm CLI) | `action.yml` (`runs: using: node20, main: dist/index.js`), `src/*.js`, `bin/docspress.mjs` | Node 20 on a GitHub Actions runner | Yes, this is the product |
| DocsPress theme | `theme/` (`style.css`: v0.10.7, "Requires at least: 6.6", "Requires PHP: 7.4") | WordPress block theme (theme.json v3, HTML templates) | Optional |
| DocsPress Blocks plugin | `plugins/docspress-blocks/docspress-blocks.php` (v0.10.7, WP 6.6+, PHP 7.4+) | WordPress plugin, no build step, uses WP-bundled editor packages | Optional. Required for versioning (README "Optional WordPress packages") |

README: "You do not have to install the DocsPress theme. An unversioned DocsPress sync works with the site's existing theme and native WordPress blocks." There is also a "stock WordPress" Playground example (`examples/stock-wordpress/blueprint.json`) that installs neither package.

### Dependencies

`package.json` runtime dependencies:
- `@actions/core` and `@actions/github`
- `@wordpress/block-serialization-default-parser`
- `fast-glob` and `gray-matter`
- `unified`, `remark-parse`, `remark-gfm`, `mdast-util-to-string`
- `turndown` and `turndown-plugin-gfm`, for the HTML-to-Markdown reverse direction

Dev dependencies are `@vercel/ncc` (bundler), `eslint`, and `vitest`. The PHP side has no Composer packages and no npm build. The theme bundles fonts: Inter, Nunito Sans, and EB Garamond.

`action.yml` pins `node20`. Node 20 reached end of life in April 2026 and GitHub has been moving JavaScript actions to Node 24, so this runtime pin should be checked before relying on it.

### Host assumptions

- **REST API:** the engine reads and writes pages, the version taxonomy, and settings through the REST API (`src/wordpress.js`). It lists every page in the five statuses `publish, future, draft, pending, private` with `context=edit`, 100 per page, on every run (`listPages`, lines 31–60). That means the token needs page-editing rights over the whole site, not just the docs tree.
- **WordPress.com:** the default `wordpress-url` is `https://public-api.wordpress.com`, which becomes `/wp/v2/sites/{site}/pages` (`restEndpoint`, lines 14–25). The token helper (`scripts/create-wordpress-token.mjs`, `npx docspress token`) runs a WordPress.com OAuth flow and requests the `global` scope (see the error hint in `formatApiError`). Code comments mention Atomic quirks (`wordpress.js:35`, "some WordPress.com and Atomic sites reject [`status=any`]"). Commits #26 and #28 deal with the "Atomic docs sync target".
- **Self-hosted:** `{wordpress-url}/wp-json/wp/v2/pages` with a Bearer header (README "Self-hosted WordPress (.org)": "Core WordPress does not create this key itself").
- **Multisite:** no `is_multisite` or `switch_to_blog` anywhere. The engine targets one site per Action invocation.
- **Theme:** the theme is a block theme only and is Site Editor-first. The Action and the plugin are theme-agnostic, and the plugin's blocks are dynamic API v3 blocks.
- **Jetpack:** no Jetpack or VIP dependency in the runtime code. The only `jetpack` reference is a Playground setup check (`theme/playground/setup.php:824`) and the "Jetpack" style variation (`theme/styles/theme/jetpack.json`). The theme ships WordPress.org, WordPress.com, and Jetpack global style families.

## 2. Content model

### Posts, meta, taxonomy, settings

- **Post type:** core `page` only.
  - `pagesEndpoint()` returns `restEndpoint("pages")` (`src/wordpress.js:27–29`).
  - The PHP side uses `get_pages()`, `get_page_by_path(..., 'page')`, `register_post_meta( 'page', ... )` and `register_taxonomy( ..., array( 'page' ) )`.
  - There is no filter to change the post type.
- **Hierarchy:** `post_parent`. Each desired page gets a `key`, which is its full route such as `docs/guides/versioning`, plus a `parentKey`. The parent ID is resolved at sync time (`src/sync.js` `pagePayload`: `parent: parentId`). Directories without an `index.md` get generated placeholder pages ("This section is generated from the docs directory.", `src/docs.js` `ensurePlaceholderHierarchy`/`placeholderPage`). A root page (default slug `docs`, input `root-slug`) is always managed.
- **Ordering:** `menu_order` comes from the frontmatter integer `sidebar_position` (`src/docs.js` `normalizeSidebarFrontmatter`; `src/sync.js` `payload.menu_order`). Ties sort by title (`theme/functions.php` `docspress_get_docs_pages`: `'menu_order,post_title'`). `sidebar_collapsed: true|false` is also accepted.
- **Sync identity (the sentinel):** `src/sentinel.js` and `src/docs.js` `finalizePage` prepend `<!-- docspress:{"version":1,"key":…,"source":…,"hash":…,"sourceContentBase64":…,"sidebarPosition":…} -->` to `post_content`.
  - The hash is SHA-256 over `{key, sourcePath, title, slug, parentKey, status, body}` (`src/page-state.js`).
  - A page is "managed" if and only if this sentinel is present (`src/sync.js` `indexExistingPages`).
  - The theme strips the sentinel on output with a `the_content` filter at priority 1 (`theme/inc/llms.php` `docspress_strip_managed_source_metadata`). **Without the theme, the comment, including the base64 Markdown, ships in page HTML**, because it is not a `wp:` block delimiter and passes through as freeform content.
  - Every revision stores a second, base64 copy of the article.
- **Post meta** (all `show_in_rest`):
  - `_docspress_sidebar_id`, `_docspress_sidebar_root`, `docspress_helpful_votes`, `docspress_unhelpful_votes`, `docspress_feedback_enabled`. Registered by the **theme** (`theme/inc/blocks.php:14–97`).
  - `_docspress_version_id`, `_docspress_logical_route`, `_docspress_page_identity`, `_docspress_source_type`, `_docspress_source_path`, `_docspress_github_{path,repository,ref,server_url}`, `_docspress_docs_root`, `_docspress_version_container`. Registered by the **plugin** (`plugins/docspress-blocks/includes/versioning.php:63–107`).
- **Taxonomy:** `docspress_versions` on `page`. It is non-public and non-hierarchical, has a REST base, and carries term meta `docspress_version_order/active/repository_latest/effective_latest` (`versioning.php:19–61`). It is used only for versioning.
- **Options** (`register_setting`, written over the REST `settings` endpoint): `docspress_repository_latest_version`, `docspress_version_override`, `docspress_docs_root_slug` (`versioning.php:109–137`).

### Doc sets, versions, URLs, redirects

- **Multiple doc sets:**
  - One managed root per Action run (`root-slug`). Deletions are scoped to pages whose sentinel key is under that root (`src/sync.js` `isUnderRoot`).
  - "Contextual sidebars" (`sidebars-file`, `src/sidebars.js`; example in `examples/contextual-sidebars/docs/sidebars.yml`) split one tree into several sidebar scopes through `_docspress_sidebar_id`.
  - Issue #36 (open) documents that several repos cannot share a common parent. `root-slug` is both URL prefix and ownership boundary, it is slugified flat (so it is single-segment only), and two repos sharing one root delete each other's pages.
- **Versioning** (opt-in, `versions-file`, `src/versions.js`, `docs/guides/versioning.md`):
  - Each version is a **separate managed page tree** tagged with a `docspress_versions` term.
  - Sources can be the repo root, a directory (`docs/v2/`), a filename suffix (`hello.v1.md`), or a manifest.
  - The plugin adds rewrite rules so the "effective latest" version serves at clean `/docs/...` URLs and historical versions serve below version prefixes. It 301s explicit-latest URLs to clean ones (`versioning.php:412–440` rules, `512–546` `template_redirect`) and disables `redirect_canonical` for those requests.
  - It provides `version-switcher` and `version-notice` blocks.
  - A site option `docspress_version_override` lets an admin choose which version is "latest".
- **URL structure:** standard page permalinks (`/docs/<dir>/<file>/`). Slugs are slugified file and directory names. `index.md`/`README` become the directory page (`routeSegmentsForFile`). Two files that map to the same route are a hard error.
- **Rewrite rules added by the theme:** `^llms\.txt/?$` and `^(.+)\.md/?$` (`theme/inc/llms.php:15–18`). `/any/page.md` returns the original Markdown decoded from the sentinel, with password-protected pages excluded since issue #10.
- **Redirects:** `redirects-file` is a JSON map of old path to new path or URL. Each entry creates a **managed placeholder page** at the old path with the body "This page moved to <a…>" (`src/docs.js` `applyRedirects`). There is no HTTP redirect and no hook into Redirection or `wp_redirect`.
- **Manifest:** `manifest-file` is a JSON array, or an object with a `pages`/`items` array, of `{id|key|slug, parent, slug, title, source|markdown_source|markdownSource}` (`src/docs.js` `collectManifestPages`/`normalizeManifestEntry`).
  - Sources must be repo-relative local paths. Anything containing `:` or `..` is rejected (`resolveManifestSource`, hardened after issue #12).
  - **The wporg-markdown/Gutenberg `manifest.json` shape is not compatible.** That manifest is an object keyed by slug, whose `markdown_source` values are absolute GitHub URLs. Against it, `data.pages || data.items || []` yields an empty list. That empty list would read as "zero desired pages", so every managed page under the root would become a deletion candidate. An adapter would be needed.

## 3. Authoring and sync

### Pipeline and triggers

The pipeline is Git-centric:
1. Collect Markdown: `**/*.md`, `**/*.markdown` under `docs-dir`, or the manifest (`src/docs.js`).
2. Convert it to serialized block markup in Node (`src/markdown.js`).
3. Create, update, or delete pages over REST (`src/sync.js`).

Triggers are whatever GitHub Actions events the workflow declares. The README examples use `push` on `docs/**`, `workflow_dispatch`, and `schedule: "3/5 * * * *"` for reverse polling. The repo's own `.github/workflows/sync-docs.yml` runs `mode: reconcile` against `https://docs.press` every 5 minutes.

### Markdown support (`src/markdown.js`, `src/gutenberg.js`, `src/block-markdown.js`)

- **Frontmatter** (gray-matter):
  - `title` overrides the title. Otherwise the first H1 is used and removed from the body (`titleFromMarkdown`).
  - `sidebar_position` and `sidebar_collapsed` are read.
  - Other keys are parsed but unused. There is no `slug`, `id`, `redirect_from`, or `description` handling.
- **GFM:** tables (`core/table`, with column alignment), strikethrough, task lists (rendered as disabled checkboxes inside `core/list`). Footnote references render as `<sup>` and footnote definitions are dropped.
- **Code fences:** `core/code`, with the language stored but no highlighter. Highlighting exists only in the plugin's `colorful-code` and `code-tabs` blocks, through a small hand-written tokenizer (`plugins/docspress-blocks/assets/view.js:13–90`). `{% codetabs %}…{% end %}` (Liquid-style) becomes a code-tabs block (`transformCodetabs`).
- **Callouts:** plain GFM `> [!NOTE]` alerts become an ordinary `core/quote`. Callout blocks only come from a `<!-- docspress:block {"version":1,"name":"docspress/callout","attrs":{…}} --> …preview… <!-- /docspress:block -->` envelope. The visible GitHub preview inside the envelope is a `> [!TIP]` alert, and the JSON is authoritative (`markdownBlockSyntaxToGutenberg`, `docs/authoring/markdown-and-gutenberg.md`). Envelopes can also carry any core or third-party block as a lossless `serialized` string, validated with the WordPress block parser.
- **Raw `<!-- wp:… -->` markup:** passed through and normalized for backward compatibility. Other raw HTML becomes `core/html`.
- **Images:** a standalone image becomes `core/image` with the URL unchanged. The docs say: "DocsPress preserves the image URL; it does not upload repository files to the WordPress Media Library." docs.press hot-links `raw.githubusercontent.com`.
- **Relative links:** `rewrite-links` (default on) rewrites `.md` links to generated page URLs (`createLinkResolver`/`rewriteMarkdownLink`). The rewritten URLs are absolute paths baked into `post_content`, which issue #36 says breaks re-parenting.
- **Mermaid:** only as the GitHub preview of the `docspress/diagram` block. WordPress renders its own SVG.
- **MDX:** not supported. The theme's source-path normalizer accepts `.mdx` filenames (`theme/functions.php:888`), but the collector only globs `.md`/`.markdown`.

### Files to posts, renames, deletions

- **Mapping:** the identity is the **route path**, not an ID. The key is derived from the file path, or from the manifest id/parent chain, and stored in the sentinel. There is no WordPress post ID in frontmatter.
- **Renames:** a renamed file is a new key, so the old page is deleted and a new page with a new ID is created. The only alias mechanism is the versioning `legacyKeys` path. Use `redirects-file` to leave a "moved" stub.
- **Deletions:** managed pages under the root whose key is no longer desired are trashed (`delete-mode: trash`) or force-deleted, deepest first (`src/sync.js:129–150`).
- **Collisions:** an unmanaged page already at a desired path is a conflict, and the engine does not overwrite it. A desired page whose parent cannot be resolved is also a conflict.

### Two-way sync (`src/bidirectional.js`, `src/reconcile.js`, `src/reverse.js`, `src/github.js`)

Modes are `publish` (one-way), `propose` (WordPress to a PR only), and `reconcile` (both directions).

**Classification:** each page is compared on three hashes (`planReconciliation`): the desired hash from Git, the base hash stored in the sentinel, and the live hash recomputed from WordPress. That yields one of these states:
- `github-only`
- `wordpress-only`
- `converged`
- `conflict`, when both sides changed, or when the source was deleted while WordPress also changed
- `github-only-delete`

**How a WordPress-only edit gets back to Markdown:**
- Live blocks are split into top-level chunks, normalized, and fingerprinted. An LCS diff rewrites only the corresponding Markdown regions (`mergeWordPressIntoSource`, `blockChangeHunks`).
- Turndown with GFM converts plain core blocks back to Markdown. Custom or styled blocks go back into envelopes.
- If the regions cannot be mapped one-to-one, the run errors instead of rewriting the whole file.

**What reverse sync cannot carry:** WordPress-side changes to `slug`, `parentKey`, `status`, or `sourcePath` produce a conflict ("WordPress changed unsupported field(s)", `reconcile.js:99–102`). WordPress-created pages are never exported. An `export to Markdown` capability does exist, but only as `blocksToMarkdown` for managed pages.

**The PR:** a single rolling branch `docspress/wordpress-sync`, marker `<!-- docspress:wordpress-sync -->`, with a conventional-commit title. The PR uses `GITHUB_TOKEN`, and the repo must allow Actions to create PRs. Merges of that branch are skipped to prevent loops (`src/github-event.js`, the job condition shown in the README).

**Latency:** reverse sync is poll-based, so a WordPress save reaches Git on the next schedule tick at the earliest.

## 4. Rendering features

Unless noted, each feature lives in the **theme** (`theme/inc/blocks.php`, `theme/functions.php`).

**Navigation and page furniture**
- **Sidebar navigation:** the `docspress/docs-navigation` dynamic block. It calls `get_pages()` for **all published pages** on each request, filters them to the root's subtree by walking `post_parent` (`docspress_get_docs_pages`, `functions.php:476–546`), and renders a nested tree (`docspress_render_page_tree`). An option uses a `wp_navigation` menu as the source instead (`menuSlug`). The block also offers a filter box, collapse, and depth limits.
- **Table of contents:** `docspress/table-of-contents`. It parses H2–H3 from rendered content and adds anchors (`docspress_prepare_content`; `render_block_core/post-content` filter `docspress_post_content_anchors`).
- **Breadcrumbs:** `docspress/breadcrumbs`, from `get_post_ancestors`.
- **Previous/next:** `docspress/adjacent-navigation`.
- **Page summary:** `docspress/page-summary`, from the excerpt.
- **Edit links:** `docspress/edit-links` shows "Edit this page in WordPress" plus "Propose changes on GitHub". The GitHub URL is built from the sentinel source path, and `repositoryUrl` is a block attribute that defaults to `https://github.com/Automattic/docspress`. The Action can separately append an "Edit this page on GitHub" link block into the content (`edit-link` input, `src/docs.js` `editUrlForPage`).
- **Last updated:** none. There is no modified-date rendering in the templates or blocks.

**Search:** `docspress/command-search`, a ⌘K dialog.
- The **full search index is inlined as JSON in every page**: up to 12,000 characters of stripped text for every docs page (`docspress_search_index`/`docspress_searchable_text`, `blocks.php:437–492`). The index is filterable through `docspress_search_index`.
- Matching happens client-side in `theme/assets/js/docs.js`. Pressing Enter falls back to native WordPress search (`s` plus `post_type=page`).
- There is no Jetpack Search, Algolia, or ElasticPress.
- docs.press's `/docs/` HTML weighs about 253 KB for roughly 40 pages. An article set the size of HelpHub's would push this to megabytes per page view.

**Feedback:** `docspress/was-this-helpful` posts to `POST /wp-json/docspress/v1/feedback/{id}`, which is **unauthenticated, with no nonce or rate limit**. It increments post-meta counters with a read-then-write (`blocks.php:139–211`) and fires the `docspress_page_feedback_recorded` action. There is no free-text comment field. Counts are aggregate, so the endpoint is open to vote-stuffing and race conditions.

**Content blocks** (the **plugin**): callout, code-tabs, colorful-code, terminal-session, api-request (with an optional browser runner), fields/schema, code-playground (sandboxed iframe), diagram, flow, troubleshooter, file-tree, result, prompt, hero, audience-paths, version-switcher, and version-notice (`plugins/docspress-blocks/blocks/*`, each with `block.php` and its own editor/view JavaScript). There are also patterns in `includes/patterns.php`.

**Other theme features:** a color-mode toggle (localStorage), `llms.txt`, and `.md` endpoints.

**i18n:**
- The theme and plugin use text domains (`load_theme_textdomain( 'docspress', …/languages )`), but no `languages/` directory ships and `wp_set_script_translations` is never called.
- There is **no content-translation model**: no locale field, no hreflang, no linking between translations, and no awareness of per-locale sites. The sync engine has no locale code at all.
- Rosetta-style per-locale sites would need one workflow and one root per locale, with no linkage between them.

## 5. Extensibility

**PHP hooks:**
- Filters: `docspress_search_index`, `docspress_llms_txt`, `docspress_markdown_source_path`, `docspress_github_source`, `docspress_github_source_url`, `docspress_effective_latest_version`, `docspress_version_switcher_choices`, `docspress_version_target_url`, `docspress_version_notice_message`.
- Action: `docspress_page_feedback_recorded`.

There are no hooks for post type, root query, or navigation source.

**REST:** one custom route, `docspress/v1/feedback/(?P<id>\d+)`. Sync uses only core `wp/v2/pages`, `wp/v2/{docspress_versions}` and `wp/v2/settings`.

**WP-CLI:** none. The only CLI is the Node `docspress` binary (`bin/docspress.mjs`), which handles token creation and related helpers. Local preview uses `@wp-playground/cli` with `theme/blueprint-local-docs.json` and `theme/playground/import-local-docs.php`.

**Blocks registered:**
- The theme registers `docspress/docs-navigation`, `command-search`, `breadcrumbs`, `table-of-contents`, `page-summary`, `edit-links`, `adjacent-navigation`, `was-this-helpful`, `color-mode-toggle`, and `docs-menu-toggle`, all API v3 dynamic blocks (`blocks.php:~900–1052`), plus block styles.
- The plugin registers 17 `docspress/*` content blocks.
- Open PR #44 would rename the namespace (with legacy compatibility, per its description).

**Templates:** pure block theme. `theme/templates/*.html` (page, page-wide, page-no-sidebar, front-page, single, home, archive, search, 404, index) and `theme/parts/{header,footer,comments}.html`. `page.html` composes the theme blocks around `core/post-content`. There are no PHP templates.

**Separability:**
- The Action needs no WordPress-side code for unversioned docs, but without the theme the sentinel shows up in HTML (see section 2).
- The plugin is theme-agnostic.
- The documentation shell (navigation, table of contents, search, breadcrumbs, feedback, llms/`.md` routes, sidebar and feedback meta registration) is **coupled to the DocsPress theme**, which is a block theme. wporg-parent-2021 child themes are also block themes. Moving these blocks into a plugin or mu-plugin is mechanically straightforward, since they are self-contained render callbacks plus `assets/js/docs.js`. It would still be a fork. The plugin's versioning code already calls theme functions defensively through `function_exists`, which shows a loose coupling in that direction too.

## 6. Project health

- **License:** the root `LICENSE` is GPL-3.0-or-later (npm `license` field), copyright Fatih Kadir Akın. The theme and plugin headers say GPL-2.0-or-later. GitHub reports the license as `NOASSERTION`.
- **Maintainers:** effectively one person. GitHub contributor `f` (Fatih Kadir Akın) has 138 commits, with 3 from github-actions[bot] and 1 from dependabot. Many branches are named `codex/*`, which points to agent-assisted development.
- **Activity:**
  - Repo created 2026-07-09.
  - About 142 commits in total, nearly all between 2026-07-09 and 2026-08-03. **No commits on main since 2026-08-03.**
  - Since then: dependabot PRs and the open rename PR #44 ("Rename project to Autodocs Publish", 299 files, which plans to rename the GitHub repo to `Automattic/autodocs-publish` and the npm package to match).
- **Releases:** many in a short burst. Action `v0.3.0`–`v0.5.0` (2026-07-23 to 07-30). Theme/plugin `wordpress-0.9.9`–`0.10.7` (2026-07-27 to 08-03), sometimes several per hour.
- **Issues and PRs:** 10 open, of which 6 are PRs. Open issues:
  - #37: a WAF on Pressable blocks `../` inside code samples sent over REST.
  - #36: multi-repo roots.
  - #7: a comments bug.

  Three security issues from an outside reporter (#10 `.md` endpoint leaking password-protected content, #11 search index leaking password-protected content, #12 manifest path traversal) were filed and fixed within days in July. Community PRs #13–#15 have been open since 2026-07-28.
- **Tests:** 18 Vitest files in `test/`, with about 150 `it`/`test` cases; PR #44 reports 312 passing including parameterized cases. They cover the converter, reverse sync, reconcile, versioning, and sidebars. **There are no PHP tests** for the theme or plugin, and no PHPCS configuration.
- **Docs:** extensive and self-hosted (`docs/`, synced to docs.press/docs). There are also AI agent skills (`.claude/skills/`, `.agents/skills/`) for installation and for generating docs from source.
- **Users:** docs.press itself, on WordPress.com Atomic. It was 29 stars and 7 forks at time of reading. No other Automattic product is named on the site or in the repo. Issue reporters show third-party experimentation (for example, issue #36's author running self-hosted plugin docs).

## 7. Conflicts with the WordPress.org environment

1. **Post type mismatch.** Everything assumes the `page` type: REST `pages`, `get_pages()`, `register_post_meta('page')`, the feedback endpoint's `'page' !== $post->post_type` check, and llms. HelpHub's `helphub_article` posts, category-based organization, and existing article IDs and URLs would require either migrating to pages or forking the engine (`src/wordpress.js`) and the theme queries.
2. **Hierarchy model mismatch.** DocsPress's tree is `post_parent` plus folder paths. HelpHub's is a category taxonomy, so URLs would change (`/documentation/article/<slug>/` versus `/documentation/<dir>/<file>/`) unless rewrites are added.
3. **Auth.** Bearer-only. WordPress.org would need a Bearer-token auth layer and a privileged token held in GitHub secrets that can list and edit every page on the site.
4. **Sentinel in `post_content`.** This doubles stored content per revision (base64 Markdown), leaks into HTML under any theme that does not strip it, and is fragile. An editor or another importer removing the comment silently "unmanages" the page, after which the next sync reports a path conflict. It also clashes with `wporg-markdown`, which uses its own post meta (`wporg_markdown_source`, `wporg_markdown_etag`) to track source.
5. **No per-locale model.** It is incompatible with Rosetta and translate.wordpress.org workflows. Each locale site would be a separate, unlinked tree.
6. **Scalability of the theme shell.** `get_pages()` on all published pages runs every request. Search inlines up to 12 KB of text per article into every page. Native search is the only server-side fallback.
7. **No media handling.** Images stay external (GitHub raw URLs), so HelpHub's media-library images would need a separate migration or hosting plan.
8. **Placeholder "moved" pages instead of 301s.** This is a poor fit for preserving HelpHub's SEO and inbound links. Real redirects would have to come from wporg's own redirect layer.
9. **Polling-based reverse sync** on GitHub-hosted cron every 5 minutes, using the shared `GITHUB_TOKEN`. Two-sided edits fail the job. Editor-side structural changes (moving or renaming pages) are rejected.
10. **Feedback endpoint** is anonymous and unthrottled. WordPress.org would likely want nonces or rate limiting, or to use its existing feedback mechanisms.
11. **Single-root ownership.** `root-slug` cannot be multi-segment (issue #36), so it cannot natively sit at `/documentation/` beside other managed trees from other repos. One workflow owns one root.
12. **JavaScript and bundles.** The front end is vanilla JavaScript with no framework: theme `docs.js` about 29 KB and `block-components.js` about 40 KB, plus per-block view scripts. That is modest. Editor scripts use WordPress-bundled packages with no build. The 2.8 MB bundle is the Action's `dist/`, which runs only on CI.
13. **Project identity churn.** The pending rename to "Autodocs Publish" changes the block namespace, package, and repo URL. Adopting now means tracking a rename and pinning to commit SHAs (as the project's own docs do).

**What transfers well:** the converter's block mapping, the envelope idea for lossless custom blocks, the hash/base three-way reconcile, the LCS-based reverse merge, and the `.md`/`llms.txt` endpoints. These are reusable ideas or code for an importer that targets wporg-markdown, independent of the theme.
