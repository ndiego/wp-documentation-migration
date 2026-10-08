# Starlight preview site (disposable)

A throwaway renderer for the documentation trees, built so WordPress contributors can compare the
current and the proposed structure and approve the change. Everything framework-specific lives in
this folder; `docs/` stays plain, portable Markdown (GitHub + the wporg-markdown importer read the
same files). Nothing here writes to `docs/` or `build/`.

| Route | Source | What |
|---|---|---|
| `/` | `src/pages/index.astro` | Landing page: what this is, buttons into both trees and the compare page |
| `/current/...` | `../build/before` | The old category tree (same articles, old layout, own `manifest.json`) |
| `/proposed/...` | `../docs` | The new hierarchical tree |
| `/compare/` | `src/pages/compare/index.astro` | Metrics, both trees side by side, "find your article", what changed |
| `/compare/decisions/` | `src/pages/compare/decisions.astro` | `../data/structure-review.md`, rendered at build time |
| `/assets/...` | `../docs/assets` | Images/videos, shared by both trees |

Pinned: `astro@7.3.6`, `@astrojs/starlight@0.42.5`, `@astrojs/markdown-remark@7.3.2` (see
`notes/framework-options.md`; Starlight 0.x minors break things, so bump on purpose).

## Run

```sh
../scripts/build_all.sh   # (repo root) regenerate build/before, docs/, data/restructure-map.json, metrics
cd site
npm install
npm run dev          # http://localhost:4321  (Astro 7 daemonises it: `npx astro dev stop|status|logs`)
npm run build        # -> dist/, 712 pages (348 current + 360 proposed + landing/compare/decisions/404), ~4-10 s
npm run preview      # serve dist/ (videos/images included via the dist/assets symlink)
npm run check-links  # internal link + #anchor check over dist/ (run after build), per tree
npm run build:publish  # build with a real copy of the images in dist/assets (for Spacefast)
```

`build/before` is gitignored, so a fresh checkout needs `scripts/build_all.sh` before the site builds.
To regenerate everything after changing `data/structure.yaml` or the converter: `scripts/build_all.sh`,
then `npm run build:publish` (and restart `npm run dev`: sidebars and the compare data are read at
config/build time).

## Dual tree: how it works

- **One collection, two roots.** Starlight renders exactly one `docs` collection, and two `glob()`
  loaders cannot share a collection (each deletes the entries it did not load). So
  `src/content.config.ts` uses one glob loader with `base: '..'` (repo root) and the patterns
  `docs/**/*.md` + `build/before/**/*.md`; `generateId` (`idFromRepoPath` in `lib/trees.mjs`) prefixes
  ids with the tree: `docs/overview/README.md` -> `proposed/overview`,
  `build/before/customization/x.md` -> `current/customization/x`. `lib/trees.mjs` `TREES` is the one
  place that defines both trees (folder, prefix, labels, GitHub source URL).
- **Sidebars.** `lib/sidebar.mjs` builds one top-level group per tree from that tree's
  `manifest.json`. `src/routeData.ts` (Starlight `routeMiddleware`) replaces the sidebar on every
  page with the entries of the page's own tree, recomputes prev/next from it (so pagination never
  crosses trees), sets the edit link and suffixes `<title>` with "(Current)"/"(Proposed)". Pages
  outside both trees get no sidebar.
- **Which tree am I in.** `src/components/SiteTitle.astro` adds a Current/Proposed pill next to the
  site title; `src/components/Banner.astro` shows a coloured bar (orange = current, blue = proposed)
  on every tree page with a one-click switch to the same page in the other tree and a link to the
  compare page (pre-filled with the article's slug). The switch target comes from
  `lib/structure-data.mjs` `counterpartOf()`: articles via `data/restructure-map.json` (slug ->
  before/after path); section pages go to the deepest section of the other tree holding more than
  half of their articles (top-level sections only to a top-level section); root pages to the same path.
- **Edit link** (`src/components/EditLink.astro` + `routeData.ts`): proposed -> "Edit on GitHub"
  (`.../edit/restructure/docs/<path>`); current -> read-only "View source (before-restructure tag)"
  (`.../blob/before-restructure/docs/<old path>`; the tag has exactly the build/before file list).
- **Search.** Both trees are in one Pagefind index; `PageTitle.astro` sets the Pagefind result
  title to "<title> (Current|Proposed)".

## Compare page

`/compare/` is a custom page using `<StarlightPage>` (same header/theme, no sidebar). All numbers
come from `../data/structure-metrics.json`, `../data/restructure-map.json` and the two manifests at
build time (`lib/compare.mjs`); they are read with `fs` rather than imported, so Vite needs no
`fs.allow` changes for files outside `site/`.

- Headline metrics table with footnoted definitions (from the metrics file's `definitions`, also as
  link tooltips).
- Both trees side by side as nested `<details>` (current left, proposed right, stacked on phones),
  each node linking into its route, sections with descendant article counts; expand/collapse all.
- "Find your article": the 321 map rows are embedded as JSON in the page; plain JS filters by
  title/slug and shows old section chain -> new section chain with links into both trees. `?q=`
  pre-fills the search (the banner's "Compare locations" uses it).
- What changed: top-level moves, misfiled articles fixed, articles that became section overviews,
  the formerly Uncategorized articles, removed "Go back to…" lines (count by old section).
- `/compare/decisions/`: `data/structure-review.md` rendered with `createMarkdownProcessor` and the
  same H1-strip, alerts and WordPress heading-id plugins; article slugs and folder paths in inline
  code become links into the proposed tree.

## How the trees are wired in

- **Content collection** (`src/content.config.ts`): Starlight's `docsLoader()` is hard-wired to
  `src/content/docs` and takes no `base`, so the collection uses Astro's `glob()` loader directly
  (see "Dual tree" above). No symlink, no copy. `assets/**` is excluded in both trees.
- **README.md -> folder index**: Starlight does *not* treat `README.md` as an index (it would become
  `/customization/readme/`), and the glob loader's default id would be the frontmatter `slug`, which
  flattens every URL. `generateId` (`lib/trees.mjs`) builds ids from the path instead:
  `docs/overview/README.md` -> `/proposed/overview/`, root `docs/README.md` -> `/proposed/`.
- **Frontmatter**: the schema is extended (`z.looseObject`) with `slug`, `original_url`, `wp_id`,
  `wp_category_id`, `categories`, `date`, `modified`, `migration`, so the importer metadata validates.
- **Markdown processor**: Astro 7 defaults to Sätteri, which runs no remark/rehype plugins, so
  `astro.config.mjs` opts into `unified()` from `@astrojs/markdown-remark`.
- **`markdown.processedDirs: ['../docs', '../build/before']`**: Starlight only runs its own transforms
  (asides, heading anchor links) on files under `src/content/docs` unless told otherwise.
- **Site folder (`#site-root`)**: `lib/trees.mjs` holds the tree definitions and pure id/route helpers (no
  file paths; `content.config.ts` imports only this, since `astro sync` cannot load `astro:config/server`).
  `lib/paths.mjs` adds the absolute folders, from `#site-root` (package.json `imports`): Node, i.e.
  `astro.config.mjs` and what it imports, gets `lib/site-root.mjs` (`import.meta.url`); Vite-bundled code
  (pages, components, `routeData.ts`) gets `lib/site-root.server.mjs` through a `vite.resolve.alias`, which
  reads Astro's `root` from `astro:config/server` (a bundled `import.meta.url` would point into `dist/`).
- **Dev watcher**: `vite.server.watch.ignored` keeps the watcher (rooted at the repo, because of the glob
  base) out of `.venv`, `raw/`, `docs/assets`, `build/before/assets`, `notes/`, `data/` and `site/dist`.

## Plugins (`plugins/`)

| Plugin | What | Why |
|---|---|---|
| `remark-strip-first-h1` | Removes the first `# H1` | The importer needs it; Starlight already renders the frontmatter title |
| `remark-github-alerts` | `> [!NOTE\|TIP\|IMPORTANT\|WARNING\|CAUTION]` -> Starlight `containerDirective` (note/tip/note/caution/danger), which Starlight's own remark-asides then renders | Starlight 0.42 still only supports `:::` asides natively |
| `remark-videopress` | A paragraph that is only a `https://videopress.com/v/<id>` URL -> iframe embed + visible link | WordPress auto-embeds the bare URL; preview only |
| `remark-docs-paths` | Relative `.md` links (incl. `#anchor`) -> site routes **in the same tree** (`/current/...` or `/proposed/...`, decided by which folder the file is in); relative paths into `docs/assets` in Markdown images/links **and** raw HTML (`<video src>`, `<img src>`, `poster`, `href`) -> `/assets/...` | Done in remark (not rehype) because Astro only parses raw HTML with rehype-raw *after* user rehype plugins. Rewriting images to absolute `/assets/` also stops Astro from trying to optimise ~2.5k images |
| `rehype-wp-heading-ids` (+ `lib/sanitize-title.mjs`) | Heading ids = WordPress `sanitize_title()` with `-2`/`-3` dedupe and wporg reserved ids (JS port of `scripts/convert.py`) | Astro/Starlight use github-slugger, which breaks 68 in-content anchors (111 vs 43 missing). Astro and Starlight keep pre-set ids, so the TOC uses these too. Explicit `<a id>` lines pass through as raw HTML |

## Other site code

- `lib/docs-assets-integration.mjs`: serves `docs/assets` at `/assets` without copying 1.8 GB.
  Dev: sirv middleware (Range requests work, videos seek). Build: `dist/assets` is a symlink to
  `docs/assets`. A `public/assets` symlink was avoided on purpose: Astro copies `public/` into `dist/`.
- `lib/sidebar.mjs`: per tree, sidebar from its `manifest.json` (itself generated from the folder tree),
  sorted by `order`; a "Home" link to the tree root; group labels are the README titles; each group starts
  with its README as "Overview"; sub-groups collapsed. Root pages (`site-health`, `update-php`) and
  `Uncategorized` go in a collapsed "Other pages" group at the end. `loadTree()` is reused by the compare page.
- `src/components/PageTitle.astro`: override that adds "Last updated <modified>" (parsed as UTC) and a
  "View on wordpress.org" link (`original_url`).
- `editLink.baseUrl` only switches Starlight's edit link on; the real URLs are set per tree in `src/routeData.ts`.
- `src/styles/custom.css`: wp.org blue accent (#3858e9). Pagefind search is on (Starlight default).
- `scripts/check-links.mjs`: checks `<a href>`, `<img/video/source src>` and `poster` in the content
  area of every built page (`--all` includes sidebar/header), `--json file` dumps problems. Stats are
  also printed per tree (current / proposed / other); a content link from one tree into the other is a
  `cross-tree` problem, and every banner switch link (`[data-tree-switch]`) must resolve.
  `PREVIEW_BASELINE=links,ids npm run build` disables the link rewrite / WP ids to measure them.

## Known limitations

- Remaining link-check failures are content issues; they match `data/link-check.json` and are the same
  in both trees (22 missing files, 42 missing anchors each).
- Pagefind returns both copies of an article (titles say which tree); there is no tree filter in the UI.
- `dist/assets` is a symlink: deploy hosts that don't follow symlinks need a real copy (or a CDN).
- Some image files are named `.img` (external downloads); served without a proper content type,
  browsers sniff them.
- Build warnings that are harmless: no `i18n` collection, no custom 404 entry, sitemap skipped (no `site`).
- Markdown inside raw HTML blocks isn't parsed (same as GitHub and the importer).
- Live reload on edits under `../docs` was not tested; edits to either `manifest.json` need a restart (sidebar is
  built at config time).

## Swapping the renderer later

Delete `site/`. Nothing in `docs/` or `build/` depends on it.
