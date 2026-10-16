# WordPress.org Documentation → Markdown migration

Goal: extract every page on https://wordpress.org/documentation/ (HelpHub) into
Markdown + local images, restructure, stand up a custom Markdown-based docs site to
iterate on, and later merge the result back into WordPress.

## Source of truth

The site exposes an open WordPress REST API at
`https://wordpress.org/documentation/wp-json/wp/v2/`. Everything is pulled from
there, not scraped from HTML.

| Endpoint             | Post type         | Count | Notes                                              |
|----------------------|-------------------|-------|----------------------------------------------------|
| `articles`           | `helphub_article` | 321   | The actual documentation articles                  |
| `wordpress-versions` | `helphub_version` | 935   | One page per WordPress release. **Out of scope for now** (auto-generated; raw JSON kept for reference) |
| `pages`              | `page`            | 7     | Front page, 4 category landing pages, site-health, update-php |
| `category`           | taxonomy          | 27    | Hierarchical, 2 levels deep                        |
| `media`              | `attachment`      | 7201  | Media library metadata (source_url, alt, caption)  |

Category tree (article counts in parentheses):

- Customization (206): Appearance 14, Block Editor 27, Default themes 28, Design blocks 13,
  Embed blocks 36, Media blocks 9, Site Editor 5, Text blocks 13, Theme blocks 51, Widget blocks 12
- Support guides (80): Dashboard 46, Media 9, Publishing 25
- Technical guides (13): Installation 4, Maintenance 6, Security 3
- WordPress overview (18): About WordPress 6, FAQs 5, Where to start 7
- Empty/legacy: DevHub, Mobile App > Post and Pages, Uncategorized (2)

## Decision: publish like the Block Editor handbook

Decided 2026-10-07. The Markdown lives in a GitHub repo and every change is a PR. WordPress.org
pulls it in with the `wporg-markdown` importer (source copied to notes/reference/wporg-markdown/),
the same pipeline that publishes the Block Editor handbook from the Gutenberg repo.

What that importer does, and therefore what our Markdown must satisfy:

- Reads a `manifest.json` (object keyed by URL path; entries have `slug`, `markdown_source`,
  `parent`, `title`, optional `order` and `meta`). Polled on a cron, so merges go live automatically.
- Strips YAML frontmatter, so frontmatter is allowed but ignored on import. Keep it minimal.
- Takes the first `# H1` line as the post title. Every file must start with one.
- Converts with Jetpack's GitHub-flavored Markdown parser (fenced code, tables, raw HTML pass-through)
  and saves classic HTML, then runs it through `wp_filter_post_kses`, which strips `<iframe>`.
  Videos therefore need to be plain URLs (auto-embedded) or links, not iframes.
- Two filters, `wporg_markdown_before_transform` / `after_transform`, are where a HelpHub-specific
  subclass can rewrite relative links and image paths.
- It imports into a hierarchical post type via `parent`. HelpHub uses `helphub_article` + categories,
  so merging back needs a small HelpHub importer subclass that maps manifest parents to categories
  (or a decision to restructure). Open question, see below.

## Layout

```
raw/        JSON dumps straight from the REST API (regenerate: python3 -I scripts/fetch_raw.py --media)
scripts/    the HelpHub pipeline: fetch + convert + assets + builds (project-specific)
convert/    wp_markdown.py, the generic facade over scripts/convert.py that other handbook conversions import
notes/      investigation write-ups (content audit, site structure, framework options)
docs/       generated Markdown: docs/<top>/<sub>/<slug>.md + README.md per folder, docs/manifest.json
docs/assets/ images (and posters) mirrored from /documentation/files/YYYY/MM/ + images-manifest.json.
            Videos are gitignored (1.3 GB); <video src> points at the wordpress.org originals for now.
data/       machine-readable reports: redirects, convert report, link check, download report
screenshots/ this repo's screenshot PROJECT (shots.config.js, blueprint, YAML shot specs); output in docs/assets/screenshots/.
            The engine is @wp-docs-toolkit/screenshots from toolkit/. See screenshots/README.md and notes/screenshot-automation/proposal.md
toolkit/    git submodule: https://github.com/ndiego/wp-docs-toolkit pinned at a tag (v0.2.0). The cross-handbook
            maintenance tooling: screenshot engine, manifest validator + CI action, style/CONVENTIONS.md, agent
            skills (a Claude Code plugin). After cloning: `git submodule update --init`. Bump by checking out a newer tag inside toolkit/
            and committing the pointer. Engine changes are made in that repo, not here.
.venv/      Python venv (bs4, markdownify) used by scripts/convert.py: `.venv/bin/python -I scripts/convert.py`
```

## Preview deployment

- GitHub: https://github.com/ndiego/wp-documentation-migration (private)
- Spacefast space: https://wp-documentation-preview.space.fast/ (private; share via `sf share link`)
  - Live (trunk): landing page, `/current/` and `/proposed/` trees, `/compare/` page
  - v1, frozen single-tree site of the original structure: https://wp-documentation-preview--v1.space.fast/
- Restructure PR (merged 2026-10-08): https://github.com/ndiego/wp-documentation-migration/pull/1
- Publish a new version: `scripts/build_all.sh && cd site && npm run build:publish && cd .. && sf publish site/dist --wait -m "<what changed>"`
  (the folder is linked to the space via .spacefast/space.json)

## Regenerating

Order matters: `.venv/bin/python -I scripts/convert.py` (a docs/ build writes docs/assets/images-manifest.json),
then `python3 -I scripts/download_assets.py`, then convert again if data/external-asset-types.json changed and
download once more (the downloader records external asset types that the converter uses for file extensions).
`scripts/build_all.sh` does exactly this.
`convert.py` rebuilds everything under docs/ except docs/assets/.

## Structure mode and before/after

The converter can lay the same raw data out two ways:

- **Category layout** (default, unchanged): `docs/<top-category>/<sub-category>/<slug>.md`.
- **Structure mode** (`--structure data/structure.yaml`): a hand-designed tree. Each section is a folder with a
  `README.md` (generated from `title` + `intro`, or the converted `index:` article), nested `children` to any
  depth, and an ordered `articles` list (order = menu order). Article frontmatter gains `position`
  (1-based among the folder's articles) and `legacy_categories` (replaces `categories`); generated READMEs have
  only `title` and `section: true`, index articles keep their normal frontmatter plus `section: true`.
  With `remove_nav_links: true` the first-paragraph "Go back to the list of Blocks" links are dropped
  (`migration.nav_link_removed: true`). A section with `classic: true` (boolean, inherited by every descendant
  section, cannot be switched off below it) marks classic-era content, i.e. the "Classic WordPress" section of the
  block-first tree: its articles and generated READMEs get `classic: true` frontmatter, its manifest entries
  `"classic": true`, its map rows `is_classic: true`. Every raw article must be placed exactly once; unknown,
  duplicate and missing slugs abort before anything is written.

```sh
scripts/build_all.sh                       # everything: assets (if missing), build/before, docs/, link checks
.venv/bin/python -I scripts/convert.py --structure data/structure.yaml --check-structure   # validate only
.venv/bin/python -I scripts/convert.py --out build/before                                 # category tree
.venv/bin/python -I scripts/convert.py --structure data/structure.yaml                    # docs/ (new tree)
.venv/bin/python -I scripts/check_links.py --docs build/before                            # check either tree
```

Outputs of structure mode, besides docs/: `data/restructure-map.json` (per article: before/after path,
section chain, depth, position, nav_link_removed, is_classic) and `data/structure-metrics.json` (before/after:
folders, depth, ordering, orphans, breadcrumb paragraphs, moves, boilerplate share, classic articles, classic articles
outside a classic section, sections mixing classic and current articles, with the structure file's classic set applied
to both trees; definitions inside the file;
computed by `scripts/structure_metrics.py`). The manifest lists, within each folder, the sub-sections first and
then the articles, with `order` counting both. Links are resolved by slug, so they follow moved files; links to
a category page point at the deepest section that holds all of that category's articles.

`--out DIR` (anywhere outside docs/) writes a complete second tree and never touches docs/: DIR gets a relative
symlink `assets -> docs/assets`, so the Markdown keeps the same `../../assets/...` paths as docs/, and
`docs/assets/images-manifest.json` is only written by docs/ builds. With `--structure --out DIR` the move map
and metrics go to `DIR/_restructure-map.json` and `DIR/_structure-metrics.json`; only docs/ builds write the
committed `data/` files. `build/` is gitignored.

## Status

- [x] Framework comparison (notes/framework-options.md)
- [x] Live-site structure notes (notes/site-structure.md)
- [x] REST API discovered and all raw JSON pulled (2026-10-07)
- [x] Markdown conventions drafted (toolkit/style/CONVENTIONS.md)
- [x] Content audit (notes/content-audit.md, notes/audit-stats.json)
- [x] HTML → Markdown converter (scripts/convert.py) — 321 articles + 2 pages → docs/, 246 clean / 75 with warnings (notes/converter-notes.md)
- [x] docs/manifest.json (importer format) and docs/assets/images-manifest.json (2,556 assets)
- [x] Asset download (scripts/download_assets.py) — 2,533 fetched, ~1.8 GB; 23 unreachable, see notes/missing-assets.md
- [ ] Decide open questions in toolkit/style/CONVENTIONS.md
- [x] Structure mode (`--structure`), before/after builds and metrics (scripts/build_all.sh)
- [ ] Starlight preview site in site/ — in progress
- [ ] HelpHub importer subclass (merge-back)
