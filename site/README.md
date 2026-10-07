# Starlight preview site (disposable)

A throwaway renderer for `../docs/`. Everything framework-specific lives in this folder;
`docs/` stays plain, portable Markdown (GitHub + the wporg-markdown importer read the same
files). Nothing here writes to `docs/`.

Pinned: `astro@7.3.6`, `@astrojs/starlight@0.42.5`, `@astrojs/markdown-remark@7.3.2` (see
`notes/framework-options.md`; Starlight 0.x minors break things, so bump on purpose).

## Run

```sh
cd site
npm install
npm run dev          # http://localhost:4321  (Astro 7 daemonises it: `npx astro dev stop|status|logs`)
npm run build        # -> dist/, ~350 pages, about 5 s
npm run preview      # serve dist/ (videos/images included via the dist/assets symlink)
npm run check-links  # internal link + #anchor check over dist/ (run after build)
```

## How docs/ is wired in

- **Content collection** (`src/content.config.ts`): Starlight's `docsLoader()` is hard-wired to
  `src/content/docs` and takes no `base`, so the collection uses Astro's `glob()` loader directly
  with `base: '../docs'`. No symlink, no copy. `docs/assets/**` is excluded.
- **README.md -> folder index**: Starlight does *not* treat `README.md` as an index (it would become
  `/customization/readme/`), and the glob loader's default id would be the frontmatter `slug`, which
  flattens every URL. `generateId` (`lib/paths.mjs`) builds ids from the path instead:
  `customization/README.md` -> `/customization/`, root `README.md` -> `/`.
- **Frontmatter**: the schema is extended (`z.looseObject`) with `slug`, `original_url`, `wp_id`,
  `wp_category_id`, `categories`, `date`, `modified`, `migration`, so the importer metadata validates.
- **Markdown processor**: Astro 7 defaults to Sätteri, which runs no remark/rehype plugins, so
  `astro.config.mjs` opts into `unified()` from `@astrojs/markdown-remark`.
- **`markdown.processedDirs: ['../docs']`**: Starlight only runs its own transforms (asides, heading
  anchor links) on files under `src/content/docs` unless told otherwise.

## Plugins (`plugins/`)

| Plugin | What | Why |
|---|---|---|
| `remark-strip-first-h1` | Removes the first `# H1` | The importer needs it; Starlight already renders the frontmatter title |
| `remark-github-alerts` | `> [!NOTE\|TIP\|IMPORTANT\|WARNING\|CAUTION]` -> Starlight `containerDirective` (note/tip/note/caution/danger), which Starlight's own remark-asides then renders | Starlight 0.42 still only supports `:::` asides natively |
| `remark-videopress` | A paragraph that is only a `https://videopress.com/v/<id>` URL -> iframe embed + visible link | WordPress auto-embeds the bare URL; preview only |
| `remark-docs-paths` | Relative `.md` links (incl. `#anchor`) -> site routes; relative paths into `docs/assets` in Markdown images/links **and** raw HTML (`<video src>`, `<img src>`, `poster`, `href`) -> `/assets/...` | Done in remark (not rehype) because Astro only parses raw HTML with rehype-raw *after* user rehype plugins. Rewriting images to absolute `/assets/` also stops Astro from trying to optimise ~2.5k images |
| `rehype-wp-heading-ids` (+ `lib/sanitize-title.mjs`) | Heading ids = WordPress `sanitize_title()` with `-2`/`-3` dedupe and wporg reserved ids (JS port of `scripts/convert.py`) | Astro/Starlight use github-slugger, which breaks 68 in-content anchors (111 vs 43 missing). Astro and Starlight keep pre-set ids, so the TOC uses these too. Explicit `<a id>` lines pass through as raw HTML |

## Other site code

- `lib/docs-assets-integration.mjs`: serves `docs/assets` at `/assets` without copying 1.8 GB.
  Dev: sirv middleware (Range requests work, videos seek). Build: `dist/assets` is a symlink to
  `docs/assets`. A `public/assets` symlink was avoided on purpose: Astro copies `public/` into `dist/`.
- `lib/sidebar.mjs`: sidebar from `docs/manifest.json` (itself generated from the folder tree), sorted by
  `order`; group labels are the README titles; each group starts with its README as "Overview";
  sub-groups collapsed. Root pages (`site-health`, `update-php`) and `Uncategorized` go in a collapsed
  "Other pages" group at the end.
- `src/components/PageTitle.astro`: override that adds "Last updated <modified>" (parsed as UTC) and a
  "View on wordpress.org" link (`original_url`).
- `editLink.baseUrl` is a placeholder (`https://github.com/OWNER/REPO/edit/trunk/site/`); the entry
  path is `../docs/...` and URL resolution normalises it to `.../trunk/docs/...`. Set the real repo in
  `astro.config.mjs`.
- `src/styles/custom.css`: wp.org blue accent (#3858e9). Pagefind search is on (Starlight default).
- `scripts/check-links.mjs`: checks `<a href>`, `<img/video/source src>` and `poster` in the content
  area of every built page (`--all` includes sidebar/header), `--json file` dumps problems.
  `PREVIEW_BASELINE=links,ids npm run build` disables the link rewrite / WP ids to measure them.

## Known limitations

- Remaining link-check failures are content issues (see below); they match `data/link-check.json`.
- `dist/assets` is a symlink: deploy hosts that don't follow symlinks need a real copy (or a CDN).
- Some image files are named `.img` (external downloads); served without a proper content type,
  browsers sniff them.
- Build warnings that are harmless: no `i18n` collection, no custom 404 entry, sitemap skipped (no `site`).
- Markdown inside raw HTML blocks isn't parsed (same as GitHub and the importer).
- Live reload on edits under `../docs` was not tested; edits to `docs/manifest.json` need a restart (sidebar is
  built at config time).

## Swapping the renderer later

Delete `site/`. Nothing in `docs/` depends on it.
