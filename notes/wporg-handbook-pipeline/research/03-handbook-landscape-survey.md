# WordPress.org documentation landscape: how each handbook is authored and published

Research date: 2026-10-11. Sources are the live sites, GitHub repos (shallow clones and `gh api`), the WordPress.org meta code mirror (`WordPress/wordpress.org` and `WordPress/wporg-developer`), and make.wordpress.org posts. Anything marked **[unverified]** is inferred, not confirmed. meta.trac.wordpress.org returned 403 to automated fetches, so Trac ticket contents are cited only through search snippets.

## TL;DR

- **Two publishing models exist on WordPress.org.**
  - (a) **Edited in wp-admin**: HelpHub, the Plugin, Theme and Common APIs handbooks, Learn, most make.wordpress.org team handbooks, and the Developer Blog.
  - (b) **Markdown in GitHub, pulled by the `wporg-markdown` importer on WP-Cron**, driven by a JSON manifest.
- **Model (b) uses one shared engine with three entry points:**
  1. DevHub importer classes in the `wporg-developer-2023` theme: Block Editor, REST API, Coding Standards, Advanced Administration, Playground, SCF, and CLI commands.
  2. The `handbook` plugin's built-in importer, added March 2021 and configured per handbook through a `manifest` URL setting. It serves make-site handbooks such as Hosting, Test, Accessibility, the Docs Style Guide and the Contributor Handbook.
  3. Bespoke plugin importers: `wporg-cli` for make.wordpress.org/cli/handbook, and `wporg-learn` for legacy lesson plans.
- **Nothing pushes to WordPress.org.** Every GitHub-backed handbook is *pulled* by cron, every 15 minutes by default and twice daily for CLI commands. No GitHub Action deploys to WordPress.org. Actions are used only to *regenerate or check the manifest* (WP-CLI handbook, SCF, Playground's Docusaurus build).
- **Manifest generation is the clearest variable between repos.** Three approaches are in use:
  - **By hand:** Advanced Administration, Coding Standards, Style Guide, developer-plugins-handbook.
  - **A script in `bin/` run by hand:** REST API, Hosting, Accessibility.
  - **CI:** WP-CLI regenerates the manifest on push to `main` and opens a bot PR. SCF fails the PR if the manifest is stale. Playground generates it from the Docusaurus sidebar during the docs build, as of 2026-09-30.
- **Images are the weak spot everywhere.** The importer does not side-load images, except the Playground importer, added 2026-08. Repos therefore hot-link `raw.githubusercontent.com`, GitHub issue attachments (`user-images.githubusercontent.com`), or files manually uploaded to a WordPress.org media library. Hosting and Accessibility tell mergers to "upload the assets to the handbook's media library before merge".
- **Deletions are not propagated.** The importer only creates and updates. The wpcs-docs README says a removed page "needs to be manually deleted from DevHub".
- **The Docs team has already proposed moving HelpHub to GitHub and Markdown.** Javier Casares proposed it on make/project on 2023-09-06, with per-language folders, a manifest and a Markdown-to-blocks conversion. The `WordPress/documentation-end-user` repo was created on 2023-09-01 and announced on 2023-09-25.
  - The effort **stalled**. The repo has 37 files, a one-entry manifest per language and no commits since 2024-02-16.
  - Javier also created GitHub mirrors of the Plugin Developer Handbook and the Plugins Team handbook in Nov 2023. The `developer-plugins-handbook` mirror still receives PRs (latest merge 2026-10-07), but developer.wordpress.org/plugins is **not** imported from it.
  - The Docs team's current direction is to keep HelpHub *in WordPress*, as in Estela Rueda's Dec 2025 workflow proposal. The 2026 posts do not mention moving content to GitHub.
  - Details are in the last section.

## Comparison table

| Site | Source of truth | Post type / hierarchy | Source → site | How contributors propose changes | Review / merge | Images | Manifest | Versions / i18n |
|---|---|---|---|---|---|---|---|---|
| **wordpress.org/documentation** (HelpHub) | WordPress DB (wp-admin) | `helphub_article` (non-hierarchical; `category` taxonomy plus persona/experience taxonomies; nav menus give structure), `helphub_version`, `post`, `page` | Direct editing | GitHub issue in `WordPress/Documentation-Issue-Tracker` (templates, `/review` automation); Slack #docs; on-site feedback form → issue | Users with the HelpHub Editor role publish; HelpHub Manager can grant roles | WordPress media library (`wordpress.org/documentation/files/YYYY/MM/`) | None | Manual per-article "Changelog" section; `helphub_version` pages per WP release; translations are separate Rosetta HelpHubs edited by locale teams |
| **developer.wordpress.org/block-editor** | `WordPress/gutenberg` `trunk` `docs/` | Handbook CPT, `post_parent` from manifest | DevHub importer (`import-block-editor.php`) pulls `docs/manifest.json` on cron | Gutenberg PR / issue | Gutenberg committers | Repo-relative files rewritten to `raw.githubusercontent.com` | Generated from `docs/toc.json` by `npm run docs:gen` (@wordpress/docs-tools); CI checks it | Tracks trunk only; no i18n |
| **developer.wordpress.org/advanced-administration** | `WordPress/Advanced-administration-handbook` `main` | Handbook CPT, `post_parent` | DevHub importer (`import-advanced-admin.php`) pulls `bin/handbook-manifest.json` | PR; issues in the Documentation-Issue-Tracker (label `advanced administration`) | Docs/Hosting maintainers merge PRs | Mixed: HelpHub media library (31, plus 10 via `i*.wp.com`), GitHub issue attachments (27), raw repo `assets/` (5), Codex (1) | **Hand-edited JSON** (titles, slugs, parents, `order`); no GitHub Actions at all | None |
| **developer.wordpress.org/playground** | `WordPress/wordpress-playground` `trunk` `packages/docs/site/docs` | Handbook CPT, `post_parent` | DevHub importer (`import-playground.php`, added 2026-07-15) pulls the committed `packages/docs/site/manifest.json`; also transforms MDX and callouts and **downloads images into the media library** | PR in the Playground monorepo | Playground maintainers | Imported into the WP media library by the importer (2026-08) | Was hand-made (2026-07); since PR #4332 (2026-09-30) generated in the Docusaurus `postBuild` hook and deployed to `wordpress.github.io/wordpress-playground/manifest.json`; the committed snapshot is kept until the importer URL switches | English on devhub; translations stay on the Docusaurus GitHub Pages site (`i18n/`), with "Also available in" links driven by `translation-availability.json` |
| **developer.wordpress.org/cli** (commands) + **make.wordpress.org/cli/handbook** | `wp-cli/handbook` `main` (long-form `.md` plus generated command pages) | `command` CPT (devhub); handbook CPT (make/cli) | devhub `inc/cli.php` pulls `bin/commands-manifest.json` twice daily; make/cli `wporg-cli` plugin pulls `bin/handbook-manifest.json` every 15 min | PR to wp-cli/handbook; command docs come from docblocks in wp-cli repos | WP-CLI maintainers (bot PRs request @swissspidy) | Rare | **Generated** by `wp handbook gen-hb-manifest` / `gen-commands-manifest` (`bin/Handbook_Command.php`); GitHub Actions regenerate on push or `repository_dispatch` and open a bot PR | `bin/command-history.json` records "Available since WP-CLI X.Y.Z"; no i18n |
| **developer.wordpress.org/rest-api** | `WP-API/docs` `master` | Handbook CPT, `post_parent` | DevHub importer (`inc/rest-api.php`/`import-docs.php`) pulls `bin/manifest.json` | PR / issue on WP-API/docs | REST API maintainers | Few | `bin/generate-manifest.php`, a glob over `*.md`, **run by hand**; no CI | None |
| **developer.wordpress.org/coding-standards** | `WordPress/wpcs-docs` `master` (the importer still uses the old `WordPress-Coding-Standards/docs` URL, which redirects) | Handbook CPT, `post_parent` | DevHub importer (`import-coding-standards.php`) | PR | WPCS maintainers | Few | **Hand-edited** `manifest.json`; README says to add and remove entries by hand and to delete removed pages on DevHub manually; CI only runs `typos` | Repo-level `changelog.md` |
| **developer.wordpress.org/secure-custom-fields** | `WordPress/secure-custom-fields` `trunk` `docs/` | Handbook CPT (`scf-handbook`) | DevHub importer (`import-scf.php`, 2025-02) | PR | SCF maintainers | — | `docs/bin/generate-manifest.php` via `composer docs:manifest`; **GitHub Action fails PRs with a stale manifest** | None |
| **developer.wordpress.org/plugins** | WordPress DB | Handbook CPT `plugin-handbook`, `post_parent` | Direct editing | Issues in the Documentation-Issue-Tracker (`plugins` label) | Project reps with the `handbook_editor`/editor role | Media library | None | None |
| **developer.wordpress.org/themes** | WordPress DB | `theme-handbook` | Direct editing | Issues in the Documentation-Issue-Tracker (`themes`) | Project reps / Themes team | Media library | None | None |
| **developer.wordpress.org/apis** | WordPress DB | `apis-handbook` | Direct editing | Issues in the Documentation-Issue-Tracker (`APIs`) | Project reps | Media library | None | None |
| **developer.wordpress.org/reference** | Generated from core PHP docblocks (phpdoc parser) plus "More information" and user notes in WP | `wp-parser-*` CPTs | Parser import | Core Trac for docblocks; Docs tracker / dashboard for "More information" | Curators | — | — | Per WP version ("since") |
| **developer.wordpress.org/news** | WordPress DB (blog) | `post` | Direct editing | Pitches/issues in `WordPress/developer-blog-content` | Developer Blog editorial group | Media library | — | — |
| **learn.wordpress.org** | WordPress DB (Sensei courses/lessons, tutorials, lesson plans) | Custom CPTs | Direct editing; legacy lesson plans were imported from `wptrainingteam.github.io/manifest.json` (`wporg-learn` `class-markdown-import.php`, cron 15 min) | Issues in `WordPress/Learn` | Training team faculty | Media library / WordPress.tv | Legacy only | Some localized content |
| **make.wordpress.org/*/handbook** (most) | WordPress DB on each P2 | `handbook` CPT (`post_parent`) via the `handbook` plugin | Direct editing | Slack / P2 comments; team-specific | Team members with the editor role | Media library | — | — |
| **make.wordpress.org/hosting/handbook** | `WordPress/hosting-handbook` `main` | `handbook`, `post_parent` | `handbook` plugin importer (manifest URL set in handbook settings) | PR / issue | **2 Hosting-team reviews** before merge | Must be uploaded to the make/hosting media library before merge; copy kept in `/assets/` | `wp hosting-handbook gen-all` (`bin/command.php`), **run by hand** | — |
| **make.wordpress.org/accessibility/handbook** | `WordPress/accessibility-team-handbook` (2025-08) | same | same importer **[unverified that it is live]** | PR / issue | 2 Accessibility-team reviews | Same media library rule | `wp accessibility-team-handbook gen-all` by hand | — |
| **make.wordpress.org/test/handbook** | `WordPress/test-handbook` `trunk` (move agreed 2025-09-30) | same | same importer (content matches a 2026-10-01 commit, so it appears synced) | Issue → discuss in #core-test → PR → 2 reviews → 1-week wait | Test team | — | `bin/handbook-manifest.json` (hand) | — |
| **make.wordpress.org/docs/style-guide** | `WordPress/WordPress-Documentation-Style-Guide` `main` **[import status unverified]** | same | likely the `handbook` importer | PR | Docs team | — | Hand-edited `manifest.json` | — |
| **make.wordpress.org/handbook** (Contributor Handbook) | `WordPress/contributor-handbook` (draft, 2024-03) **[import status unverified]** | same | — | Issue commands Actions | — | — | `bin/handbook-manifest.json` | — |
| **make.wordpress.org/core/handbook**, polyglots, meta, support, training, themes, community, marketing, design, mobile, tv, performance, openverse, photos, sustainability | WordPress DB | `handbook` CPT | Direct editing | Team channels | Team editors | Media library | — | — |

The make-site rows were verified by checking each handbook landing page for importer-generated GitHub `edit/`/`commits/` links. Only hosting and cli showed them, but the make theme does not always render those links (test is synced without them), so "edited in WP" for the remaining make handbooks is a strong inference, not proof.

---

## Shared machinery (read this first)

**`wporg-markdown` plugin** (`wordpress.org/public_html/wp-content/plugins/wporg-markdown/`, mirrored at https://github.com/WordPress/wordpress.org):

- It imports Markdown from a remote URL as WordPress pages.
- It reads a **manifest**: a JSON object keyed by permalink path, with `slug`, `markdown_source`, `parent` (the key of the parent) and optional `title` and `order`.
- Hierarchy is `post_parent`, resolved from `parent` keys. `order` maps to `menu_order`.
- It stores an ETag per post (`wporg_markdown_etag`) to skip unchanged files.
- It creates and updates, but **does not trash pages removed from the manifest**. The handbook importer only labels them "Not Imported" in wp-admin.
- Its `Editor` class swaps "Edit" for an "Edit on GitHub" link.
- Subclasses hook `wporg_markdown_before_transform` / `after_transform` for per-site rewrites (link rewriting, callouts, MDX stripping).

**DevHub importers** (`WordPress/wporg-developer`, `source/wp-content/themes/wporg-developer-2023/inc/`):

- `DevHub_Docs_Importer` (`import-docs.php`) runs on `15_minutes` cron by default.
- Subclasses and their manifest URLs:
  - `import-block-editor.php` → `WordPress/gutenberg/trunk/docs/manifest.json`
  - `import-advanced-admin.php` → `WordPress/Advanced-administration-handbook/main/bin/handbook-manifest.json`
  - `import-coding-standards.php` → `WordPress-Coding-Standards/docs/master/manifest.json` (repo renamed to `WordPress/wpcs-docs`)
  - `rest-api.php` → `WP-API/docs/master/bin/manifest.json`
  - `import-scf.php` → `WordPress/secure-custom-fields/trunk/docs/bin/manifest.json`
  - `import-playground.php` → `WordPress/wordpress-playground/trunk/packages/docs/site/manifest.json`
  - `cli.php` → `wp-cli/handbook/main/bin/commands-manifest.json` (`twicedaily`)
- Other handbook CPTs (`apis`, `plugin`, `theme`) are plain `handbook` plugin CPTs, edited in WP. `Devhub_Handbooks` creates a `handbook_editor` role.
- The local dev env runs `wp cron-concurrent run --filter=import_manifest` to pull all manifests.

**`handbook` plugin importer** (`plugins/handbook/inc/importer.php`, `WPorg_Handbook_Importer`):

- Added 2021-03-05: "Handbooks: Add ability to import handbook content from a remote source."
- Each handbook's config has `manifest` and `cron_interval` (default `15_minutes`), set in the handbook settings, i.e. the DB, not code. That is why `gh search` finds no hosting or test manifest URLs in meta code.
- It assigns imported posts to the `wordpressdotorg` user.
- This is the mechanism any make-site handbook (and in principle any site running the `handbook` plugin) can use to become GitHub-backed **without new code**.

**Bespoke:**

- `plugins/wporg-cli/inc/class-markdown-import.php` (make/cli handbook, 15 min).
- `plugins/wporg-learn/inc/class-markdown-import.php` (legacy lesson plans from `wptrainingteam.github.io/manifest.json`).

**Markdown *output*:** since 2026-03-03, "most WordPress.org sites" serve Markdown with `Accept: text/markdown` or `?output_format=md`, using Dennis Snell's html-to-md (Dion Hulse, https://make.wordpress.org/meta/2026/03/03/markdown-now-available-on-wordpress-org/). This is HTML→MD on the fly, not a source-of-truth change. It is handy for exporting HelpHub articles (it is how the changelog examples below were pulled).

---

## Per-site notes

### 1. wordpress.org/documentation (HelpHub, end-user docs)

- **URL:** https://wordpress.org/documentation/ (formerly wordpress.org/support/, renamed with the 2023 redesign: "New look, new site, new HelpHub", https://make.wordpress.org/docs/2023/01/24/new-look-new-site-new-helphub/).
- **Code:**
  - Theme and dev env: https://github.com/WordPress/wporg-documentation-2022 (README: "formerly WordPress.org/support, also called HelpHub").
  - The `support-helphub` plugin lives in meta SVN at `wordpress.org/public_html/wp-content/plugins/support-helphub/`. The repo pulls it, `wporg-support-2024` and `pub` via Composer SVN.
  - The old `WordPress/HelpHub` GitHub repo (2016) is **archived**.
- **Source of truth:** the WordPress database. Articles are written directly in the block editor. Since 6.9 the team drafts in WP rather than Google Docs (see the Dec 2025 proposal below).
- **Content model** (`inc/helphub-post-types/classes/class-helphub-post-types.php`):
  - `helphub_article` (rewrite `article`, `hierarchical => false`, supports page-attributes, revisions and comments).
  - `helphub_version` (rewrite `wordpress-version`) with the `helphub_major_release` taxonomy.
  - `post`.
  - Taxonomies: `category` (shared by posts and articles), plus `helphub_persona` and `helphub_experience` (seen in the dev-env WXR data).
  - Front-page "category blocks" are widgets keyed to category IDs and nav menus (`env/setup.sh`).
  - **There is no page-tree hierarchy.** Articles are flat under `/documentation/article/<slug>/`, and grouping comes from categories and menus. This matters for any GitHub migration: the manifest would need to encode categories and menus, not just `parent`.
- **Roles** (`support-helphub`):
  - `helphub_editor` ("HelpHub Editor"): a clone of `editor` caps, with the Themes screen hidden (`helphub-customroles`).
  - `helphub_manager` ("HelpHub Manager"): editor caps plus `edit_theme_options` and `manage_helphub` (`helphub-manager`). Managers can assign HelpHub roles from the bbPress profile screen (`/support/users/USERNAME`). This was introduced in meta #3918.
  - Meta #5235 ("Add 'HelpHub Contributor' role for on-boarding users") is still open per search results **[unverified current status]**.
  - On Rosetta sites, Polyglots Global Mentors grant the first locale HelpHub admin (https://make.wordpress.org/docs/handbook/helphub/translating-helphub/).
- **How someone gets edit access:**
  - The docs handbook "Editing articles" page (https://make.wordpress.org/docs/handbook/helphub/migrating-articles/) says to request write access by DMing your WordPress.org username and email to @atachibana on Slack, or to ping @Kenshino or @atachibana in #docs.
  - In practice, access is granted by a HelpHub Manager after some track record.
  - Per the 2026-04-21 post, contributors without access "comment with the markdown or a link to the draft" on the issue, and someone with access applies it.
- **Issue tracker and triage:** https://github.com/WordPress/Documentation-Issue-Tracker. It hosts no docs and covers HelpHub, DevHub and the docs handbook.
  - **Issue templates:** `doc-issue-fix`, `new-doc`, `helphub-feedback-reports` (fed from the on-site feedback form), `new-release-enduser-issue`, and good-first-issue templates for ALT attributes, headings, **screenshots** and videos.
  - **Labels:** project labels (`user documentation (HelpHub)`, `developer documentation (DevHub)`, `advanced administration`, `plugins`, `themes`, `APIs`, …), version labels (`5.6` … `6.8`), `[Block] X` labels, `needs screenshots` / `has-screenshots`, `HelpHub feedback`, `migration from Codex`, and status labels.
  - **Automation** (`.github/workflows/`): `label-when-assigned` (→ In progress), `actions-when-commented` (`/assign`, `/review`), `label-when-closed` (→ Done), `add-to-project`, and `notify-team-on-label` (pings the project's reps).
  - **Project boards:** label→project, e.g. "End-user documentation" (projects/90) and per-release "WP 6.x Documentation" boards (https://make.wordpress.org/docs/handbook/github-repository-and-projects/documentation-issue-tracker/).
  - **Workflow:** comment to claim → maintainer assigns (In progress) → `/review` → reviewer asks for fixes or invites you to update the doc → Done.
  - **2026 overhaul:** ~800 issues triaged and 200 closed. Open counts: HelpHub 358, Themes 146, DevHub 101, Advanced Admin 33 (Estela Rueda, https://make.wordpress.org/docs/2026/04/21/wordpress-documentation-team-closes-200-issues-and-needs-your-help/).
- **Changelog convention:** each article ends with a `## Changelog` heading listing dated bullets, newest first, often with props. It is maintained by hand. Examples from the live Markdown output:
  ```
  ## Changelog
  * Updated 2026-09-14 (props @karthickmurugan @awetz583)
      - Added Zoom out
  * Updated 2026-08-19
      - Updated content and screenshots for 7.1
  ```
  Older articles use a bold "**Changelog**" paragraph and bare dates (`* 2023-03-28 - Updated images and videos for 6.2`). The release-issue template checklist ends with "Update the changelog at the end of the article". Javier Casares's 2023 GitHub proposal kept this convention: "each document has an H1 title and a final H2 'Changelog' section".
- **Screenshot updates per release:**
  - For each release, the team opens one issue per affected article from `new-release-enduser-issue.md`. The issue lists the Gutenberg PRs to document, plus a checklist: screenshots current, videos current, ALT text, sentence-case headings, convert reusable blocks, update changelog.
  - Directions: on a fresh English install (Playground or InstaWP), default theme, no plugins, capture "the same page area as the existing one", and **upload new screenshots as a comment on the issue**. Someone with HelpHub access then uploads them to the media library and swaps them in.
  - Images live at `wordpress.org/documentation/files/YYYY/MM/…`. Guidance: https://make.wordpress.org/docs/handbook/get-involved/getting-started-at-a-contributor-day/good-first-issues/#updating-screenshots and a WordPress.tv video.
- **Versions:** there is no per-version doc. `helphub_version` holds release pages, and articles track changes via the changelog.
- **i18n:** separate HelpHub instances on Rosetta sites (`LOCALE.wordpress.org/support`), maintained by locale teams in WP. The `helphub-codex-languages` module handles Codex language links.
- **Pain points (from posts):**
  - review bottlenecks (multi-week waits)
  - backlog, and articles updated out of release order (6.4→6.6→6.5)
  - the screenshot hand-off from issue comment to media library
  - access gating
  - 358 open HelpHub issues (2026-04)
  - most original HelpHub contributors inactive (2023-02 post)

### 2. developer.wordpress.org/block-editor (brief; covered in depth elsewhere)

- **Source:** `WordPress/gutenberg` `trunk` `docs/`.
- **Manifest:** `docs/manifest.json`, generated from `docs/toc.json` by `npm run docs:gen` (part of `docs:build`, workspace `@wordpress/docs-tools`). CI checks docs are up to date.
- **Import:** pulled by `import-block-editor.php` on cron, which rewrites relative links to `/block-editor/...` and relative images to `raw.githubusercontent.com`. Uses the `single-handbook-block-editor.html` template.
- **Contributions:** Gutenberg PRs, merged by Gutenberg committers.
- Not versioned, not translated.

### 3. developer.wordpress.org/advanced-administration (closest precedent for HelpHub)

**History:**
- **Aug 2022:** the Docs team approached the Hosting team. Meta ticket #6411 ("Advanced Administration – New DevHub Handbook") was opened (July 2022 per the wp-meta list).
  - Per search snippets, the ticket initially said the content would be maintained from the dashboard. A later comment says it should be generated from its own GitHub repo, with issues in the Docs tracker. **[Trac 403; not read directly]**
- **2022-08-13:** repo created. First commits by Javier Casares on 2022-08-16.
- **2022-09-07:** announcement post by Javier Casares on make/hosting (https://make.wordpress.org/hosting/2022/09/07/wordpress-advanced-administration-handbook/). Leads were @JavierCasares, @lucp and @milana_cap. One issue per page "to be copied from their origin" (Codex/HelpHub). Two-level structure (category → pages).
- **2023-01-15:** status post. 63 pages in 10 sections, 51 to be moved from Support/Codex/APIs (https://make.wordpress.org/hosting/2023/01/15/advanced-administration-handbook-status-2023-01-15/).
- **2023-03-28:** Dion Hulse (meta) committed "Changes needed for WordPress.org handbook import (#190)" to the repo:
  - fixed the branch and repo names in the manifest
  - renamed slug `feed`→`feeds`
  - removed `parent: handbook`
  - set homepage `order: -1` so it tops the menu
- **Go-live:** probably late March–April 2023, inferred from that commit. **[launch post not found]**
- **Since then:** manifest edits by hand (2023-04 "Manifest with ordered pages", 2023-09 "added to manifest", 2025-07 Mail section, 2025-12 Application Passwords). The repo is active in 2026 (Multisite rewrite, FileZilla, debugging, PHPUnit/Xdebug), with PRs from several contributors.

**Mechanics:**
- **Repo:** https://github.com/WordPress/Advanced-administration-handbook, `main`, 80 `.md` files, folders mirror URL sections, `index.md` per section, `assets/` (548 KB).
- **`bin/handbook-manifest.json`:** 75 entries with `title`, `slug`, `markdown_source` (a GitHub `blob` URL), `parent` and `order`. **Hand-maintained**; there is no generator script.
- **No `.github/` directory**, so there is no CI (not even lint). There is a stray `.obsidian/` folder, suggesting a maintainer edits in Obsidian.
- Docs-team handbook: "Updating the page in the handbook is done by merging the PR" (https://make.wordpress.org/docs/handbook/get-involved/team-roles/project-based/developer-roles/).
- **Contributions:** PRs; issues in the Documentation-Issue-Tracker with the `advanced administration` label (33 open as of 2026-04); project board orgs/WordPress/projects/47.
- **Images (measured):**

  | Host | Count |
  |---|---|
  | `wordpress.org/documentation/files/…` (HelpHub media library) | 31 |
  | `user-images.githubusercontent.com` (GitHub issue/PR attachments) | 27 |
  | `i0/i1/i2.wp.com/wordpress.org` | 10 |
  | `raw.githubusercontent.com/WordPress/Advanced-administration-handbook/main/assets/` | 5 |
  | `codex.wordpress.org/images` | 1 |

  Images are therefore not version-controlled in practice, and some live on a different site's media library.
- **Lessons and pain points** (inferred from history, no retrospective post found):
  - The manifest is a hand-edited single point of failure. The first import required meta to fix branch, repo, slug and parent mistakes.
  - There is no CI to catch manifest drift or broken links.
  - Image hosting is ad hoc.
  - Deletions and moves require manual DevHub cleanup.
  - It still works with a small group of maintainers and stays active, which is the main positive precedent.

### 4. developer.wordpress.org/playground

- **Source:** `WordPress/wordpress-playground` `trunk` `packages/docs/site/docs/` (English) and `packages/docs/site/i18n/` (translations, 220+ pages in pt-BR, ja, es, fr, gu, bn, tl, …).
- **Two outputs from one source:**
  1. **Docusaurus site:** built by the `deploy-website.yml` workflow and published to GitHub Pages at `wordpress.github.io/wordpress-playground/`. It still serves translations. English pages are replaced at build time with redirect stubs to developer.wordpress.org/playground (`plugins/redirect-docs-to-developer-wordpress-org.js`).
  2. **DevHub handbook:** `import-playground.php` (wporg-developer, added 2026-07-15, #569; images #572 and Blueprint steps reference #574 in Aug 2026).
     - Pulls the **committed** `packages/docs/site/manifest.json` (88 entries).
     - Transforms MDX (`transform_mdx`), converts callouts, rewrites root-relative links and images, adds "Run Blueprint" links and `[playground_php_snippet]`.
     - **Downloads images into the WP media library** with an ETag bump.
     - Adds "Also available in:" links from `translation-availability.json`.
- **Manifest:**
  - First hand-written (#3267, 2026-07-15).
  - Since **PR #4332 (2026-09-30)**, generated by a Docusaurus plugin (`plugins/generate-handbook-manifest.js`) in `allContentLoaded`/`postBuild` from the resolved doc titles and slugs plus the `sidebars.js` tree and order.
    - Drafts, unlisted and `orphan: true` pages are excluded.
    - **The build fails if an active page is missing from the sidebar.**
    - It emits absolute raw GitHub URLs and is deployed to `https://wordpress.github.io/wordpress-playground/manifest.json`.
  - The committed manifest is a "compatibility snapshot" until the importer URL is switched (pending as of this writing **[check importer URL]**).
  - Two Markdown references (Blueprint steps, API client) are generated by scripts in `site/bin/` (PR #4337, 2026-09-17).
- **Announcement:** Fellyph Cintra, "Migrating WordPress Playground Documentation to WordPress.org", 2026-04-07 (https://make.wordpress.org/playground/2026/04/07/migrating-wordpress-playground-documentation-to-wordpress-org/).
  - Phases: English → i18n → "Ask AI" (Kapa.ai).
  - **Pain points in comments:**
    - The importer handles Docusaurus front matter poorly (also hit by the Contribution Pathways handbook, per a commenter).
    - Callouts, MDX fragments and SEO metadata need work.
    - The i18n redirect rules are unresolved.
    - One commenter argued WordPress isn't set up for technical docs.
- **Takeaway:** this is the most sophisticated pattern. The manifest is derived from an existing nav definition (the sidebar) and published as a build artifact, not hand-kept.

### 5. developer.wordpress.org/cli and make.wordpress.org/cli/handbook

- **Source:** https://github.com/wp-cli/handbook `main`. Long-form `.md` files under `guides/`, `how-to/`, `references/`, `contributions/`. Generated `commands/` pages come from WP-CLI docblocks.
- **Two importers:**
  - developer.wordpress.org/cli/commands: `wporg-developer` `inc/cli.php`, `twicedaily`, `bin/commands-manifest.json`, `command` CPT.
  - make.wordpress.org/cli/handbook: the `wporg-cli` plugin (`class-markdown-import.php`), every 15 min, `bin/handbook-manifest.json`. Live pages show GitHub edit/commits links (verified).
- **`bin/`:** `Handbook_Command.php` (`wp handbook gen-all`, `gen-commands-manifest`, `gen-hb-manifest`, `update-command-history`), `install_packages.sh`, `templates/`, `command-history.json`.
  - `gen-hb-manifest` walks the repo for `.md` (skipping `bin`, `commands`, `.github`, `vendor`, README).
  - It derives the title from the first `# H1`, `parent` from the directory name, and `slug` from the filename (`index` → `handbook`).
  - It emits a GitHub `blob` URL and sorts keys.
- **GitHub Actions:**
  - `regenerate-manifest.yml`: on push to `main` and manual dispatch. Runs `wp handbook gen-hb-manifest` and opens or updates a bot PR `update-handbook-manifest`, labelled `scope:distribution`, reviewer @swissspidy.
  - `regenerate-handbook.yml`: manual or `repository_dispatch: regenerate-handbook` from wp-cli/wp-cli on release. Runs `gen-all` against the nightly phar with `--stable-phar` and opens a bot PR.
  - `code-quality.yml`.
- **Versioning:** `command-history.json` drives "Available since WP-CLI X.Y.Z" and "Options added later".
- **Note:** the action still opens a PR that a human merges, so the manifest is reviewed, not auto-committed.

### 6. developer.wordpress.org/rest-api

- **Source:** https://github.com/WP-API/docs `master` ("The content for developer.wordpress.org/rest-api"). Last push 2025-06-04.
- **Manifest:** `bin/manifest.json`, generated by `bin/generate-manifest.php` (globs `*.md` three levels deep; key = path, parent = dirname). No GitHub Actions, so it is run by hand.
- **Endpoint reference:** generated from templates (`bin/regenerate.php`, `bin/templates/endpoint.md`). `bin/parse-wxr.php` is the original WXR→MD migration script.
- **Import:** `inc/rest-api.php` / `import-docs.php`. Live pages show "Edit on GitHub" (verified).

### 7. developer.wordpress.org/coding-standards

- **Source:** https://github.com/WordPress/wpcs-docs `master`. The importer URL still references `WordPress-Coding-Standards/docs`, which redirects. Live pages link to `WordPress/wpcs-docs` edit URLs (verified).
- **Manifest:** `manifest.json` at the root, **hand-edited**. README: "When creating new files, these must be added to the manifest.json … After deletion and sync with DevHub, the page also needs to be manually deleted from DevHub."
- **History:** `changelog.md` records "2018-01-14 Initial import from https://make.wordpress.org/core/handbook/best-practices/". This is a precedent for moving a WP-edited handbook to GitHub.
- **CI:** `qa.yml` (`typos`) only.

### 8. developer.wordpress.org/secure-custom-fields (not in the original list; found in the importer directory)

- **Source:** https://github.com/WordPress/secure-custom-fields `trunk` `docs/`.
- **Manifest:** `docs/bin/manifest.json`, generated by `docs/bin/generate-manifest.php` via `composer run docs:manifest`.
- **CI:** `.github/workflows/docs-manifest.yml` runs on PRs touching `docs/**`. It regenerates the manifest and **fails if it differs** ("Please run 'composer run docs:manifest' and commit"). This is a lightweight, robust pattern.
- **Import:** `import-scf.php` (2025-02-20; CPT renamed to `scf-handbook` because of the 20-char post-type limit).

### 9. developer.wordpress.org/plugins, /themes, /apis

- **Edited in WP** (verified):
  - `Devhub_Handbooks::filter_handbook_post_types` registers `apis`, `plugin` and `theme` as regular handbook CPTs.
  - There is no importer.
  - Live pages show no GitHub edit links.
  - The docs-team roles page says "Updating the page in the handbook is usually done by one of the project reps or active contributors who have access to the dashboard."
  - Issues go in the Documentation-Issue-Tracker (`plugins`, `themes`, `APIs` labels).
- **Editors:** the `handbook_editor` role (meta #621) can edit handbooks only. Meta #5220 (per-handbook editor permissions) is open per search results **[unverified]**.
- **GitHub mirrors exist but are not the source:**
  - https://github.com/WordPress/developer-plugins-handbook was created 2023-11-12 by Javier Casares as a Markdown copy with `manifest/handbook-manifest.json`. It still gets PRs (e.g. #76 "Add GIF as a supported format for plugin banners", merged 2026-09-23).
  - The live page https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/ does **not** contain that change, so the repo has diverged from the live handbook. This is a cautionary example: a mirror nobody imports.
  - Same pattern: https://github.com/WordPress/plugins-handbook (Plugins *team* handbook, make.wordpress.org/plugins/handbook). Created the same day, with no import evidence.
- **No theme-handbook repo** was found in the WordPress org.

### 10. developer.wordpress.org/news

- A WordPress blog (`post` CPT), edited in WP.
- Pitches, issues and editorial planning happen in https://github.com/WordPress/developer-blog-content. Monthly meeting in #core-dev-blog.

### 11. learn.wordpress.org

- Edited in WP: Sensei courses and lessons, tutorials, lesson plans, workshops.
- Code and content issues are in https://github.com/WordPress/Learn ("canonical source for the code and content behind learn.WordPress.org"); content is planned via issues.
- **Legacy:** `wporg-learn` once imported `lesson-plan` posts from `https://wptrainingteam.github.io/manifest.json` (the cron hook is now commented out, and a filter remains for previously imported plans). This is the only non-handbook use of the manifest importer, and it was abandoned in favour of WP editing.

### 12. make.wordpress.org/*/handbook

- **Default:** the `handbook` plugin on each P2, `handbook` CPT with `post_parent` hierarchy, edited in wp-admin by team editors. This covers core, polyglots, meta, support, training, themes, community, marketing, design, mobile, tv, performance, openverse, photos, sustainability and docs. The landing pages show no GitHub source links.
- **make.wordpress.org/core/handbook is edited in WP**, not imported. Its coding-standards section was moved *out* to wpcs-docs in 2018.
- **GitHub-backed via the `handbook` plugin's importer** (manifest URL configured in handbook settings):
  - **Hosting:** https://github.com/WordPress/hosting-handbook (2020-05).
    - Verified: the live page links to `github.com/wordpress/hosting-handbook/edit/main/index.md`.
    - CONTRIBUTING: PRs need **two Hosting-team reviews**.
    - Manifest is regenerated **manually** with `wp hosting-handbook gen-all` (a WP-CLI command in `bin/command.php`).
    - "Assets such as images are not automatically imported … upload the assets to the … media library before merge, and link to the uploaded media directly."
  - **Accessibility:** https://github.com/WordPress/accessibility-team-handbook (2025-08). CONTRIBUTING is a copy of Hosting's (two reviews, `wp accessibility-team-handbook gen-all`, same media rule). **[live import not verified]**
  - **Test:** https://github.com/WordPress/test-handbook. The move was agreed in "The Test Handbook overhaul" (SirLouen, 2025-09-30, https://make.wordpress.org/test/2025/09/30/the-test-handbook-overhaul/).
    - Lesson recorded in that post: a sync attempt 2–3 years earlier "stalled because the docs had partly changed and not all were mirrored". The mirror must match the live handbook before switching.
    - Process: issue → discuss in #core-test → PR → ≥2 reviews → merged after one week.
    - The live page content matches a 2026-10-01 commit, so it appears synced.
  - **Docs Style Guide:** https://github.com/WordPress/WordPress-Documentation-Style-Guide (2020 Google Season of Docs) with a hand-edited `manifest.json`. **[import status unverified]**
  - **Contributor Handbook:** https://github.com/WordPress/contributor-handbook ("Draft for the WordPress.org Contributor Handbook", 2024-03) with `bin/handbook-manifest.json` and issue-command Actions. **[import status unverified]**
- **make.wordpress.org/cli/handbook:** see §5 (bespoke `wporg-cli` importer).

### 13. DocsPress

- https://github.com/Automattic/docspress (created 2026-07-09, "Publish Markdown documentation from GitHub to native WordPress Pages and Gutenberg blocks", homepage docs.press). It ships agent skills (e.g. `docspress-install`).
- No reference to DocsPress was found in any WordPress-org repo (`gh search code docspress --owner WordPress` returned nothing) or on make.wordpress.org.
- **Not used or proposed for WordPress.org** as of 2026-10-11.

---

## Prior public discussion of moving HelpHub to GitHub

Chronological. **Short answer: yes, the docs team proposed essentially this in 2023. It got a repo and a manifest format but stalled before any content moved, and the team's 2025–2026 direction has been to streamline editing *inside* WordPress instead.**

1. **2015-01: HelpHub spec** (https://make.wordpress.org/meta/2015/01/13/help-hub-spec/). HelpHub was conceived as a WP-native Codex replacement, and the `WordPress/HelpHub` GitHub repo (2016) held the *plugin code*, not content. It is now archived.
2. **2023-02-07: "Future plans for HelpHub"** (Estela Rueda, https://make.wordpress.org/docs/2023/02/07/future-plans-for-helphub/). Post-relaunch to-dos: changelog, inventory board, Polyglots site-map work, and the idea of a GitHub issue tracker per Rosetta site. No Markdown or GitHub-content plan.
3. **2023-09-01:** `WordPress/documentation-end-user` repo created (https://github.com/WordPress/documentation-end-user).
   - Language folders `en de es fr it ja pt ru sr hi bn`, each with only `index.md` and `assets/`.
   - `manifest/documentation-manifest-<lang>.json` files, each with a single `index` entry (`markdown_source` → `blob/trunk/<lang>/index.md`).
   - CONTRIBUTING covers only adding a language. README: "At this moment, adding languages is not allowed due technical challenges."
   - Last commits 2024-02-16 (Jonathan Desrosiers / Javier Casares removing the CoC file). **No article content was ever migrated.**
4. **2023-09-06: "Proposal: Documentation translation / localization"** (Javier Casares, make/project, https://make.wordpress.org/project/2023/09/06/documentation-translation-localization/). This is the most directly relevant precedent. Key points:
   - Foundational docs move to GitHub, one repo per documentation segment (end-user, advanced admin, developer), with ISO-code language folders.
   - Markdown files editable in GitHub's web UI; each doc has an H1 and a final H2 "Changelog".
   - Folder structure mirrors URLs (`index.md`).
   - A **manifest** lists files, slugs, hierarchy, menu priority and language IDs. Content "is automatically converted from Markdown to HTML or WordPress blocks". The manifest links language versions together.
   - Roles: Repository Maintainers (control publication and the GitHub→WP sync config), General Translation Editors per language, Translators. Not GlotPress.
   - **Comments:**
     - Felipe Santos worried PRs burden non-technical translators and asked why a manual changelog is needed with Git.
     - Jon (Kenshino) said issues can be converted to PRs by the docs team.
     - Javier said the changelog is reader-facing, not a diff.
     - Alex Kirk asked how to detect stale translations and suggested GlotPress segmenting or MT+edit.
   - No formal Meta-team response and no recorded decision.
5. **2023-09-25: "End-user docs repo – workflows and settings"** (Milana Cap, https://make.wordpress.org/docs/2023/09/25/end-user-docs-repo-workflows-and-settings/).
   - Announces that the Docs and Polyglots teams are "moving complete end-user documentation (HelpHub)" into `WordPress/documentation-end-user`. Existing docs move first; then translation, new English docs and updates all happen via PRs.
   - Defines personas: first-time and experienced contributors, repo maintainer, issues coordinator, reviewers, translator, translation editor.
   - Covers issue life cycles (including "updating screenshots") and one-problem user-story issues.
   - Status: planning. It does not specify how sync to wordpress.org would work.
6. **2023-11 → 2023-12:** Javier Casares creates `WordPress/developer-plugins-handbook` and `WordPress/plugins-handbook`, Markdown copies with manifests in the same `manifest/` layout as documentation-end-user. Neither is imported (see §9). This was presumably part of the same multi-repo plan **[inferred]**.
7. **2025-12-02: "Proposal to change the user documentation workflow"** (Estela Rueda, https://make.wordpress.org/docs/2025/12/02/proposal-to-change-the-user-documentation-workflow/).
   - Problem: a 13-column GitHub project template, Google Docs drafts, and multi-week waits for first and second reviews.
   - For 6.9, articles were written **directly in WordPress**, scheduled for release day, and reviewed *after* publication. GitHub is used only for tracking.
   - Recommends skipping most pre-release review, small per-release writing teams, and a simpler board.
   - Comments: Andrea Roenning suggested people without edit access propose improvements via the Documentation Issue Tracker; Steven Lin suggested publishing at Beta/RC; annezazu suggested tiered review (new contributors reviewed, experienced not).
   - **No mention of GitHub or Markdown as source of truth.**
8. **2026-03-03:** Markdown *output* on WordPress.org (Dion Hulse, meta). Aimed at AI agents; not a source-of-truth change.
9. **2026-04-07:** Playground docs migration to the DevHub handbook (Fellyph Cintra). Shows the meta and handbook side is actively investing in GitHub→handbook imports in 2026 (new importer features: MDX transform, image import, translation links).
10. **2026-04-21:** Docs team issue-tracker overhaul (Estela Rueda). 358 open HelpHub issues. Contributors without access are asked to paste Markdown drafts into issues, which is a de facto GitHub→WP hand-copy workflow. No migration plan mentioned.

**Implications for this project:**
- The idea is not new. Javier Casares and Milana Cap (Docs team) proposed it publicly in Sept 2023, including the manifest, changelog and i18n folder design, and it stalled for "technical challenges" (unspecified) and lack of migration tooling. **[the reason for the stall was not found in public posts]**
- The current Docs-team leadership (Estela Rueda) is optimizing the WP-native workflow. Any new proposal should engage them directly and explain what is different this time:
  - automated migration of 1,000+ HelpHub articles (not hand-copying)
  - a generated manifest
  - image handling
  - category and menu mapping for a flat, taxonomy-organized post type
  - a plan for Rosetta translations
- The proven technical path is the existing `wporg-markdown`-based importers. The DevHub importer classes and the `handbook` plugin's manifest setting already work for Advanced Administration, Hosting and Test. HelpHub, however, is `helphub_article` (non-hierarchical, taxonomy-driven), not a `handbook` CPT, so it would need either a custom importer subclass or a content-model change. **[needs meta-team confirmation]**
- **Lessons from existing GitHub-backed handbooks:**
  - Generate the manifest in CI (WP-CLI, SCF, Playground), not by hand (AAH, wpcs).
  - Solve images up front (the Playground importer is the only one that imports them).
  - Plan for deletions and redirects (the importer doesn't trash removed pages).
  - Do not create a GitHub mirror without switching the importer: developer-plugins-handbook and the 2022-era Test handbook attempt both diverged from the live site.
