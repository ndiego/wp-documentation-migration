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
scripts/    fetch + convert tooling
notes/      investigation write-ups (content audit, site structure, framework options)
docs/       generated Markdown: docs/<top>/<sub>/<slug>.md + README.md per folder, docs/manifest.json
docs/assets/ images (and posters) mirrored from /documentation/files/YYYY/MM/ + images-manifest.json.
            Videos are gitignored (1.3 GB); <video src> points at the wordpress.org originals for now.
data/       machine-readable reports: redirects, convert report, link check, download report
.venv/      Python venv (bs4, markdownify) used by scripts/convert.py: `.venv/bin/python -I scripts/convert.py`
```

## Regenerating

Order matters: `python3 -I scripts/download_assets.py`, then `.venv/bin/python -I scripts/convert.py`, then
download again (the downloader records external asset types that the converter uses for file extensions).
`convert.py` rebuilds everything under docs/ except docs/assets/.

## Status

- [x] Framework comparison (notes/framework-options.md)
- [x] Live-site structure notes (notes/site-structure.md)
- [x] REST API discovered and all raw JSON pulled (2026-10-07)
- [x] Markdown conventions drafted (notes/markdown-conventions.md)
- [x] Content audit (notes/content-audit.md, notes/audit-stats.json)
- [x] HTML → Markdown converter (scripts/convert.py) — 321 articles + 2 pages → docs/, 246 clean / 75 with warnings (notes/converter-notes.md)
- [x] docs/manifest.json (importer format) and docs/assets/images-manifest.json (2,556 assets)
- [x] Asset download (scripts/download_assets.py) — 2,533 fetched, ~1.8 GB; 23 unreachable, see notes/missing-assets.md
- [ ] Decide open questions in notes/markdown-conventions.md
- [ ] Starlight preview site in site/ — in progress
- [ ] HelpHub importer subclass (merge-back)
