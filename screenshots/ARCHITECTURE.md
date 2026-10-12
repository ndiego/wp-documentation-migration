# Architecture

Phase 1 of the toolkit proposed in `../notes/screenshot-automation/proposal.md`. This file is the contract
between the pieces; keep it current when the pieces change.

## Two layers

```
screenshots/                      the PROJECT: this repo's shots, blueprint, content and config
  shots.config.js                 project config consumed by the engine
  blueprint/                      Playground blueprint + mu-plugin + demo content pack (see blueprint/README.md)
  shots/                          YAML shot specs, mirrored to the docs tree
  (engine)                        the ENGINE lives in ../toolkit/wp-shots, npm package `wp-shots`, consumed as a path dependency
```

The engine knows nothing about this repository. It receives a config object (directories, blueprint path,
WordPress version, style tokens) and does the rest. It lives in `../toolkit/wp-shots` (see `../toolkit/README.md` for the boundary rules). Publishing it from its own
repository is a move, not a rewrite; the project would then depend on `wp-shots` from npm instead of the path.

Rules that keep that true:

- Nothing under `toolkit/wp-shots/` imports from outside it, reads `../docs`, or assumes article slugs look like ours.
- Project-specific facts (output dir, docs dir, manifest path, blueprint path, versions, viewports, style tokens)
  come from `shots.config.js`.
- Project-specific content keys (`{{media.harbor}}`) are resolved against the running site by slug, not against
  files in this repo.

## Engine (`../toolkit/wp-shots/src/`)

| Module | Responsibility |
|---|---|
| `cli.js` | `wp-shots run|check|update|lint|snippet|dev|doctor|list|vocab`, argument parsing, exit codes |
| `config.js` | Load `shots.config.js`, apply defaults, resolve paths |
| `spec.js` | Load and validate YAML specs; expand defaults; compute spec hashes |
| `env/playground.js` | Start/stop `@wp-playground/cli server` from a blueprint, wait for readiness, assert booted WordPress and PHP versions |
| `browser.js` | Launch Chromium with the deterministic context options; build `Admin`, `Editor`, `PageUtils`, `RequestUtils` from `@wordpress/e2e-test-utils-playwright` |
| `site.js` | REST lookups for `{{media.*}}` / `{{post.*}}` / `{{page.*}}` templating; cleanup of content a shot created |
| `scenes.js` | `new-post`, `new-page`, `post:<slug>`, `page:<slug>`, `admin:<path>`, `site-editor[:<route>]`, `front[:<path>]` |
| `actions.js` | The step vocabulary; each verb is a function `(ctx, arg) => Promise<void>` |
| `locators.js` | Semantic locator keys (`button:`, `control:`, `menuitem:`, `tab:`, `text:`, `role:`, `selector:`) to Playwright locators, searching page and canvas |
| `targets.js` | Named capture targets to locators (`block-toolbar`, `inspector`, `inserter`, ...) in one registry |
| `capture.js` | Settle, compute clip from target + include + pad, inject annotations, screenshot, hand off to `image.js` |
| `annotate.js` | Overlay layer drawn in the top document from bounding boxes: `outline`, `badge`, `dim` |
| `image.js` | sharp: frame presets, WebP/PNG encode, decode for compare; pixel compare via pixelmatch |
| `manifest.js` | Read/write the output manifest; only touch entries whose pixels changed |
| `lint.js` | Spec/alt/orphan/reference checks against the docs tree; `--fix` for alt text |
| `report.js` | HTML before/after/diff report for `check`; `update` applies the staged images and manifest entries |
| `style.js` | Default style tokens (overridable from config) |
| `runner.js` | Orchestrates: boot once, group shots by suite and article, run scenes and steps, capture, write, manifest |

Plain ESM JavaScript with JSDoc types. No build step, so a contributor can read the file that runs.

## Shot spec

```yaml
article: image-block             # required; output folder name. Must exist in docs manifest when lint runs.
suite: default                   # optional; blueprint suite (blueprint/suites/<name>/blueprint.json), default "default"
defaults:                        # optional; merged into every shot
  scene: new-post
  viewport: desktop
shots:
  - id: toolbar-replace          # required; file name. [a-z0-9-]+
    alt: ...                     # required; the Markdown alt text
    caption: ...                 # optional; italic caption line under the image
    scene: new-post              # see scenes
    viewport: desktop            # desktop | narrow | mobile | {width, height}
    isolated: false              # true = this shot needs a fresh Playground boot afterwards (it mutated the site)
    steps: [ ... ]               # list of verbs; string or single-key object
    capture:
      target: block-toolbar      # named target or selector; default "editor"/"admin-screen"/"front" per scene
      include: [selected-block]  # optional; extend clip to cover these targets too
      pad: 16                    # CSS px; default from style
      fit: content               # optional; clip a tall target's bottom to its last visible child
      frame: plain               # plain | card
      annotate:
        - outline: { button: Replace }
        - badge: { label: 1, control: Alternative text }
        - dim: { target: inspector }
      mask: [ { selector: ".some-dynamic" } ]
    kind: image                  # image (default) | clip (phase 5, parsed and skipped with a warning for now)
    script: ./custom.js          # optional escape hatch; default export (ctx) => Promise<void>, replaces steps
```

Templating in any string value: `{{media.<slug>}}` (attachment ID), `{{media.<slug>.url}}` (source URL),
`{{post.<slug>}}` / `{{page.<slug>}}` (ID), `{{post.<slug>.url}}`, `{{site.url}}`.

## Step verbs (phase 1)

| Verb | Argument | Notes |
|---|---|---|
| `insertBlock` | `core/image` or `{name, attributes, innerBlocks}` | Via `wp.data`, like Gutenberg's tests; the new block becomes selected |
| `selectBlock` | `core/image` or `{name, nth}` | Selects the nth block of that type in the canvas |
| `setContent` | block HTML string | Replaces the whole post content |
| `openInserter` | none | Opens the main block inserter |
| `searchInserter` | search term | Opens the inserter, types the term and waits for the debounced results (and the patterns section) |
| `openInspector` | `content`, `settings` or `styles` (default `settings`) | Opens the Block sidebar on that tab. `content` exists only for blocks with content controls (Image alt text lives there) |
| `openDocumentSidebar` | none | Opens the Post/Page tab of the sidebar |
| `openPanel` | panel name | Expands a collapsed sidebar panel by its button name |
| `openBlockMenu` | none | Opens the block toolbar's Options (⋮) menu |
| `openToolbarDropdown` | button name | Opens a toolbar dropdown, e.g. `Align` |
| `openListView` | none | |
| `openOptionsMenu` | none | The editor's top-right ⋮ menu |
| `click` / `hover` | locator key | |
| `type` | `text` or `{text, pace}` | `page.keyboard.type`; pace `human` adds delay |
| `fill` | `{ <locator key>, value }` | |
| `select` | `{ <locator key>, option }` | Native `<select>` |
| `press` | key chord | `Enter`, `Escape`, `primary+k` (via PageUtils) |
| `wait` | `{ for: <target or locator key>, state?: visible|hidden|attached }` or ms number | |
| `setViewport` | viewport name or `{width, height}` | |
| `setPreference` | `{ scope, key, value }` | `core`, `core/edit-post`, `core/edit-site` |
| `scrollTo` | locator key | `scrollIntoViewIfNeeded` |
| `evaluate` | JS source string | Escape hatch; runs in the page |

Locator keys: `{ button: "Replace" }`, `{ control: "Alternative text" }` (textbox/combobox/checkbox/spinbutton by
label), `{ menuitem: "Edit as HTML" }`, `{ tab: "Styles" }`, `{ text: "Settings" }`, `{ role: "searchbox", name: "Search" }`,
`{ selector: ".css" }`, `{ block: "core/image" }`. Names match the whole accessible name (`exact: true` by default;
set `exact: false` for a substring). The page document and the editor canvas frame are both polled until one has a
match, unless `in: canvas` / `in: page` is given; `within: <target>` scopes the search. Unknown keys, verbs, scenes
and targets are rejected at spec-load time with a "did you mean" suggestion, so `lint` catches them in CI.

## Named targets (phase 1)

`editor`, `canvas`, `selected-block`, `block-toolbar`, `inspector`, `inspector-panel:<name>`, `document-sidebar`,
`inserter`, `list-view`, `top-bar`, `options-menu`, `popover`, `modal`, `site-editor-sidebar`, `site-editor-canvas`,
`admin-content`, `admin-screen`, `admin-menu`, `front`. Anything else is treated as a CSS selector.

## Output

- `docs/assets/screenshots/<article>/<id>.webp`. WebP is lossless when the result fits `style.webp.maxBytes`
  (300 KB by default; UI crops land at 10–50 KB) and lossy at `style.webp.quality` (90) above it, because
  lossless WebP of a photo-heavy 2x editor shot is larger than PNG (1.2 MB vs 0.6 MB; lossy q90 is ~0.38 MB).
  Both encodings are deterministic. The manifest records `encoding` per image, so lossless ones can be converted
  to PNG later without loss. `format: png` in config switches everything to PNG.
- `docs/assets/screenshots/manifest.json`: `{ "version": 1, "shots": { "<article>/<id>": { file, article, alt,
  caption, suite, kind, wordpress, php, theme, specHash, blueprintHash, playwright, chromium, platform,
  canonical, capturedAt, width, height, bytes, encoding, pixelHash } } }`, keys sorted. An entry only changes
  when the image's pixels change, its spec metadata changes, or a field is missing.
- Images are compared pixel-for-pixel against the committed file before writing; identical pixels mean the file is
  left untouched so git shows no churn.

## Environment contract (`blueprint/`)

See `blueprint/README.md`. The engine only needs: a blueprint path, the port, the admin credentials
(`admin` / `password`), and that the blueprint's `login` step is present so the browser arrives authenticated.
Content keys are resolved by slug through the REST API, so the demo content pack may be replaced wholesale as long
as the slugs listed in `blueprint/README.md` keep existing.
