# Markdown conventions (draft, 2026-10-07)

Target: the `wporg-markdown` Importer used for the Block Editor handbook. Source in
`notes/reference/wporg-markdown/`. Everything below is derived from reading that code and the
Gutenberg `docs/` tree, not from memory.

## What the importer actually does

| Step | Behaviour | Consequence for us |
|------|-----------|--------------------|
| Fetch | Reads `manifest.json` from raw.githubusercontent on a cron, with ETag dedupe | Merged PRs go live without a deploy |
| Frontmatter | Stripped with `^---(.+)---` (ungreedy) | Frontmatter is allowed but ignored |
| Title | First `# H1` line becomes `post_title`; otherwise manifest `title` | Every file starts with `# Title` |
| Convert | Jetpack `WPCom_GHF_Markdown_Parser` (GitHub-flavored) | Fenced code, tables, raw HTML pass through. Markdown inside HTML blocks is **not** parsed |
| Sanitize | `wp_filter_post_kses` | `<iframe>` stripped unless the handbook subclass allows it. `<video>`, `<img>`, `<div class>` are allowed |
| Excerpt | First line of text | First paragraph should be a real summary sentence |
| Hierarchy | `parent` + `order` from manifest set `post_parent` / `menu_order` | Hierarchical post type. HelpHub uses categories, so a HelpHub subclass must map parents to terms |
| Links | Handbook subclass rewrites relative `.md` links to permalinks in `wporg_markdown_before_transform` | We can use relative links in Markdown |

Gutenberg's own conventions (observed in `docs/`): `/docs/path/file.md#anchor` links, `README.md` as folder
index, images as absolute `developer.wordpress.org/files/...` URLs, callouts as raw HTML
`<div class="callout callout-info|callout-tip|callout-warning|callout-alert">` with `<p>` inside,
YouTube as raw `<iframe>` (allowed by their subclass), `{% codetabs %}` for tabbed code.

## Our conventions

- **File layout**: `docs/<top-category>/<sub-category>/<slug>.md`, `README.md` per folder as index.
- **Title**: `# Title` first line. No other H1 in body.
- **Frontmatter**: minimal, flat: `title`, `slug`, `original_url`, `wp_id`, `categories`, `date`, `modified`,
  `migration` (converter warnings, to be deleted once reviewed).
- **Headings**: h2/h3 drive the TOC. Anchor ids follow WordPress `sanitize_title` of the heading text,
  with `-2`, `-3` suffixes for duplicates, because existing `#anchor` links depend on that.
- **Callouts**: GitHub-style alerts `> [!NOTE]` / `[!TIP]` / `[!WARNING]` / `[!CAUTION]` (decided
  2026-10-07, to render well on GitHub). The HelpHub importer subclass needs a small
  `wporg_markdown_before_transform` filter to turn these into notice markup. Converter can still emit the
  Gutenberg HTML style with `--callout-style gutenberg`.
- **Links**: relative Markdown links between files. Links off-site stay absolute.
- **Images**: relative paths into `docs/assets/images/YYYY/MM/<file>`, mirroring the original
  `/documentation/files/` path so unchanged images can be mapped back to their existing attachment URL on
  import. Alt text preserved. Caption as italic line under the image.
- **Video**: VideoPress / YouTube as a bare URL on its own line (auto-embed). Self-hosted `<video>` kept as
  HTML with a local `src`.
- **Tables**: GFM tables; complex tables (rowspan etc.) stay as HTML.
- **Code**: fenced, with language hint.
- **Manifest**: `docs/manifest.json` in importer format, generated from the folder tree by a script, never
  hand-edited.

## Decisions so far (2026-10-07)

- Publish via GitHub + wporg-markdown importer, like the Block Editor handbook.
- Optimise for rendering on GitHub: plain Markdown, GFM alerts, relative links, relative images.
- Keep URLs flat (`/article/<slug>/`) and map folders to categories in a HelpHub importer subclass.
- Astro Starlight is a disposable preview renderer in `site/`; nothing framework-specific goes into `docs/`.
- Changelog sections stay in the body for now; likely dropped in favour of git history later.
- "Was this article helpful?" is out of scope here; it will be a wordpress.org theme feature (or an
  "Edit on GitHub" link).
- Media: in-repo copies under docs/assets for now; long-term home still open.

## Open design questions for merge-back

1. URL scheme. HelpHub articles live at `/documentation/article/<slug>/` (flat) with categories. The
   importer wants a hierarchy. Options: (a) HelpHub importer subclass that ignores `parent` for the post
   and assigns categories instead, keeping URLs unchanged (no redirects needed); (b) switch to
   hierarchical URLs and add 321 redirects.
2. Blocks vs classic HTML. The importer saves classic HTML; HelpHub content today is block HTML. The
   HelpHub theme may style `.wp-block-*` classes. Either accept classic HTML output, or use the
   `WordPress/php-toolkit` Markdown-to-blocks component in the subclass.
3. Image hosting. Keep images in the repo (reviewable in PRs, importer sideloads like Playground does) or
   keep pointing at the wordpress.org media library (zero work, but screenshots can't be updated via PR).
4. Changelog sections. Hand-written in 213 articles today. Keep in body, or move to git history?
5. "Was this article helpful?" has no static/GitHub equivalent. Replace with "Edit on GitHub" / issue link?
