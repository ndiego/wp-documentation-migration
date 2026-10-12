# Framework options for the interim docs site

Researched 2026-10-07. Versions checked against GitHub releases and npm dist-tags on that date.

## 1. How Markdown gets into WordPress.org today

**One importer, many handbooks.** Every Markdown-backed handbook on WordPress.org uses the abstract `WordPressdotorg\Markdown\Importer` class in the `wporg-markdown` plugin ([class-importer.php](https://github.com/WordPress/wordpress.org/blob/trunk/wordpress.org/public_html/wp-content/plugins/wporg-markdown/inc/class-importer.php)). The generic handbook plugin wraps it ([handbook/inc/importer.php](https://github.com/WordPress/wordpress.org/blob/trunk/wordpress.org/public_html/wp-content/plugins/handbook/inc/importer.php)), and so does DevHub ([wporg-developer `inc/import-*.php`](https://github.com/WordPress/wporg-developer/tree/trunk/source/wp-content/themes/wporg-developer-2023/inc)). The pipeline:

1. **A manifest.json lists every page.** WP-Cron fetches it every 15 minutes. Each entry has `title`, `slug`, `markdown_source` (an absolute GitHub URL or a path relative to the repo), `parent` (the parent's slug, or `null`) and an optional `order`. If `order` is missing, the entry's position in the array becomes `menu_order`. Examples: [Gutenberg `docs/manifest.json`](https://github.com/WordPress/gutenberg/blob/trunk/docs/manifest.json), which is generated from `docs/toc.json` by `npm run docs:build`; [Advanced Administration `bin/handbook-manifest.json`](https://github.com/WordPress/Advanced-administration-handbook/blob/main/bin/handbook-manifest.json), which is keyed by path and has explicit `order`; [WP-CLI `bin/handbook-manifest.json`](https://github.com/wp-cli/handbook/tree/main/bin), which `wp handbook` generates; and [Playground `manifest.json`](https://github.com/WordPress/wordpress-playground/blob/trunk/packages/docs/site/manifest.json).
2. **Each page becomes a hierarchical post.** The importer creates one post per entry in a `*-handbook` CPT, with `post_parent` and `menu_order` taken from the manifest. It saves the source URL in post meta, which drives the "Edit on GitHub" link, and uses ETags to skip pages that haven't changed.
3. **Markdown is converted to classic HTML, not blocks.** The importer strips the YAML frontmatter (`preg_replace('#^---(.+)---#Us', '', …)`), so frontmatter is allowed but ignored. It pulls the first `# H1` out as the title, runs **Jetpack's `WPCom_GHF_Markdown_Parser`** (GitHub-flavored: fenced code, tables, autolinks), and passes the result through `wp_filter_post_kses`. The first line becomes the excerpt. Per-handbook behavior lives in the `wporg_markdown_before_transform` and `wporg_markdown_after_transform` filters.
4. **The handbooks customize it in different ways:**
   - **Block Editor Handbook** ([import-block-editor.php](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-block-editor.php)): rewrites repo links such as `/docs/foo.md` and `../docs/x/README.md` to absolute DevHub URLs, converts `~~strike~~` to `<s>`, and turns `{% codetabs %}` into tabs. Callouts are raw HTML in the form `<div class="callout callout-{info|tip|alert|warning}">`. Markdown links inside callouts are *not* transformed. Images must be uploaded to the developer.wordpress.org Media Library instead of hotlinked from GitHub ([contributor docs](https://github.com/WordPress/gutenberg/blob/trunk/docs/contributors/documentation/README.md)).
   - **Playground** ([import-playground.php](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-playground.php)) is the closest precedent for our project. Its source is a **Docusaurus MDX site with 11 locales**, and the same files are imported into developer.wordpress.org/playground. The importer strips `import` lines, swaps out custom MDX components, parses Markdown inside Docusaurus callout `<div>`s, rewrites root-relative links and image paths, and **sideloads images into the Media Library as `core/image` blocks**.
   - **Advanced Administration** ([repo](https://github.com/WordPress/Advanced-administration-handbook)) holds former HelpHub content. Its files use plain `.md` with no frontmatter, `## Heading {#custom-id}`, callouts written as plain `>` blockquotes, and images hotlinked to `wordpress.org/documentation/files/…`, which is *our* source site's media library.
   - **Theme and Plugin handbooks** are edited directly in WordPress, and GitHub only tracks issues. They aren't imported.
5. **A newer option produces blocks.** [`WordPress/php-toolkit` → Markdown](https://github.com/WordPress/php-toolkit/tree/trunk/components/Markdown) (active in September 2026) converts in both directions between Markdown with frontmatter and block markup (`MarkdownConsumer` / `MarkdownProducer`, built on league/commonmark with GFM). It emits `core/heading`, `paragraph`, `list`, `table`, `code`, `quote`, `separator` and `image`. Our merge-back sync script should be built on this, not on the legacy HTML importer.

**What this means for us.** The live HelpHub content uses `wporg/notice` blocks (`is-info-notice`, `is-tip-notice`) and a few legacy `callout callout-info` divs. Both use the same four-type vocabulary (info, tip, alert, warning) as the Gutenberg callouts, and our callout syntax should map one-to-one onto it. WordPress stores hierarchy and order in the manifest, never in frontmatter, so we should be able to *generate* a manifest from our files.

## 2. Framework comparison

Not shortlisted: **Nextra.** Its last release was 4.6.1 in December 2025, it is tied to the Next.js App Router, and commits have slowed.

| | **Astro Starlight** | **Docusaurus** | **VitePress** | **Hugo** (+ Hextra/Docsy) | **Eleventy** |
|---|---|---|---|---|---|
| Current version (Oct 2026) | 0.42.5 (Oct 1), on Astro 7.3. Pre-1.0, and minor releases break things | 3.10.2 (July). v3 line is finished; v4 is in canary | **1.6.4 stable (Aug 2025)**; 2.0 still alpha.20 | 0.167 (Sept 28), releases monthly | 3.1.6 stable; 4.0 alpha |
| Plain `.md` (no MDX needed) | Yes; MDX and Markdoc optional | Yes, but every `.md` is parsed as MDX by default, which is strict about `<`, `{` | Yes | Yes | Yes |
| Callouts | `:::note/tip/caution/danger` built in; `> [!NOTE]` with the [starlight-github-alerts](https://starlight.astro.build/resources/plugins/) plugin | `:::note/tip/info/warning/danger` built in; GitHub alerts need a remark plugin | **GitHub alerts built in**, plus `::: tip` containers | GitHub alerts through the blockquote render hook | DIY with markdown-it plugins |
| Tabs | `<Tabs>` component (MDX/Markdoc only) | `<Tabs>` (MDX) | `::: code-group` (code only) | Shortcodes | DIY |
| Images | Relative paths, optimized by Astro | Relative paths, hashed | Relative paths | Page bundles, image processing | Plugin |
| Sidebar | Autogenerated from folders, or explicit config (can be generated) | Autogenerated from folders, or `sidebars.js` | **Hand-written config** | From the section tree and `weight` | DIY |
| Search | **Pagefind built in** (static, offline) | Algolia DocSearch (external) or a local plugin | Built-in MiniSearch (local) | None in core; theme or Pagefind | None (add Pagefind) |
| Build time, ~1,300 pages | Fast (new Rust compiler in Astro 7) | Slowest; needs "Docusaurus Faster" (Rspack) | Fast | **Fastest (seconds)** | Fast |
| Effort to match the wp.org look | Low to medium: CSS custom properties plus component overrides | Medium: Infima variables plus swizzling React components | Low to medium: CSS variables plus Vue slots | Medium to high: Go templates and theme work | High: build everything yourself |
| i18n | **First-class**: folder per locale, fallback to English with a notice, UI strings in 30+ languages | First-class, but builds once per locale (slow) | Locales config, more manual | Strong multilingual support | DIY |
| Ecosystem health | Very active; Astro has 63k stars, Starlight 9.4k | Very active, Meta-backed, 66k stars; **used by WP Playground** | Active repo, but no stable release in 14 months and a small core team | Very active | Active |
| Markdown lock-in | Low if you stay in `.md` | Medium: MDX habits creep in | Low | Low, but shortcodes lock content in | Low |

Caveat for Starlight: in Astro 7, the default Markdown processor is now **Sätteri** (Rust), which does *not* run remark/rehype plugins ([Astro docs](https://docs.astro.build/en/guides/markdown-content/)). If we rely on remark plugins (GitHub alerts, link rewriting), we need to opt into the Unified processor. This is one config line, but it's worth knowing ([Astro June 2026 news](https://astro.build/blog/whats-new-june-2026/)).

## 3. Recommendation

**First choice: Astro Starlight, with content kept as plain `.md`, no MDX.** Of the options here, it is the only one that ships with all of the following:
- Pagefind search that needs no external service
- Built-in i18n with English fallback, which fits how Rosetta sites translate gradually
- Theming through CSS variables, which gets us close to the wp.org look with little effort

Pin the version, because 0.x minor releases bring breaking changes.

**Fallback: Docusaurus 3.10.** It's mature, and the Playground handbook already proves that Docusaurus source → wporg importer → developer.wordpress.org works, including i18n. Set `markdown.format: 'detect'` so `.md` files aren't parsed as MDX.

(VitePress would be the fallback for authoring comfort, since it supports GitHub alerts out of the box. But its stable release is 14 months old with 2.0 still in alpha, which makes it too risky.)

The framework choice matters less than the conventions below. If we follow them, switching frameworks only means rewriting a config file.

### Content conventions

**File layout.** Use one `content/<category>/<subcategory>/<slug>.md` file per article. Category landing pages are `index.md`.

**Frontmatter.** Keep it framework-neutral. Starlight accepts extra keys through `docsSchema({ extend })`.

```yaml
---
title: Paragraph block            # required; becomes post_title / manifest title
description: Short summary.       # becomes post_excerpt, meta description
slug: paragraph-block             # globally unique, matches the live /documentation/article/<slug>/
order: 20                         # becomes menu_order (sibling sort)
wp_id: 12345                      # original helphub_article ID, for updating instead of duplicating on merge
last_updated: 2026-05-01
redirect_from: [/documentation/article/old-slug/]
---
```

- **Keep the hierarchy out of frontmatter.** It comes from the folders. A small script generates three things from folders, `order` and `title`: (a) the Starlight `sidebar` config, (b) a wporg-style `manifest.json` with `title/slug/markdown_source/parent/order`, and (c) the sync payload. Don't use Starlight-specific `sidebar:` keys.
- **Don't put a `# H1` in the body.** Starlight renders `title`, and the wporg importers strip a leading H1 anyway. Headings start at `##`. Custom anchors use `{#id}` only where needed, the same as Advanced Administration.

**Callouts.** Use GitHub alert syntax only:

```md
> [!NOTE]      → wporg/notice is-info-notice
> [!TIP]       → is-tip-notice
> [!WARNING]   → is-warning-notice
> [!CAUTION]   → is-alert-notice
```

Reasons:
- It renders on GitHub.
- It falls back to a normal blockquote anywhere it isn't supported.
- Starlight supports it through a plugin, VitePress and Hugo support it natively, and Docusaurus supports it through a remark plugin.
- It maps one-to-one onto the four `wporg/notice` types.

Avoid `:::` directives, which are framework-specific, and `<div class="callout">`, where Markdown inside isn't parsed. Callouts must not contain headings.

**Images.**
- Mirror the source path: `assets/YYYY/MM/filename.png`. Reference images with **relative paths** and real alt text: `![Alt text](../../../assets/2024/03/foo.png)`.
- Use a plain image on its own line. Add an optional caption as an italic line right after it, which the converter maps to `figcaption`. Don't use HTML `<figure>` and don't wrap images in links.
- Relative paths work on GitHub, get optimized by Astro, and let the sync script rewrite unchanged images back to their original `https://wordpress.org/documentation/files/YYYY/MM/…` attachment, so nothing gets re-uploaded. New images are sideloaded the way the Playground importer does it.
- Keep a side file, `data/media-map.json` (path → attachment ID), instead of putting attachment IDs in the Markdown.

**Links.**
- Between articles, write root-relative links by slug: `[Users screen](/article/users-screen/)`. Live HelpHub URLs are flat (`/documentation/article/<slug>/`), so links survive category moves, and merging back is just adding a prefix.
- Configure Starlight routes to match: set the entry ID from `slug` and use the generated sidebar. Check this while scaffolding.
- Validate links in CI with `starlight-links-validator`.
- Use absolute URLs for external sites.

**Other syntax.**
- **Allowed:** GFM tables (`core/table`), fenced code blocks with a language, `---`, ordered and unordered lists, and `<kbd>`.
- **Not allowed:** MDX imports, JSX, shortcodes, and raw HTML. The only exception is `<details>`, and only if the merge script supports it.
- **No tabs.** The end-user docs don't need them, and they don't round-trip.

**Merging back.** Write a PHP or WP-CLI script around `WordPress\Markdown\MarkdownConsumer` (php-toolkit) that:
1. Converts each file into block markup.
2. Post-processes alert blockquotes into `wporg/notice` blocks.
3. Rewrites image and link prefixes.
4. Upserts each post using `wp_id`/`slug`, setting `post_parent` and `menu_order` from the manifest.

`MarkdownProducer` can do the reverse, from blocks back to Markdown, if editing ever continues in WordPress. This gives us real Gutenberg blocks, not the legacy importer's classic HTML. The legacy importer is still an option because our files would also be valid input for it: frontmatter is stripped, and the manifest is generated.
