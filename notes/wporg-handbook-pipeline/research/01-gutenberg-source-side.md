# Block Editor Handbook: the source side (WordPress/gutenberg)

How the Block Editor Handbook (https://developer.wordpress.org/block-editor/) is written, generated and checked in the `WordPress/gutenberg` repository, before the developer.wordpress.org importer reads it. The importer itself is covered in a separate report.

- **Commit inspected:** `9af2d4154e6399e4bc0fbb1b318d02e09c0742cc` (trunk, 2026-10-11 22:12 +1100, "Tests: Scope Classic block media checkbox locator (#84524)").
- **Method:** a sparse, shallow clone of trunk. I ran the manifest generator against the clone myself, from a separate directory with only `change-case@4` and `glob@13` installed, and diffed its output against the committed `docs/manifest.json` (see 1.6). Issue and PR data comes from `gh` on 2026-10-11.
- **Path change to know about:** the docs tooling no longer lives in `docs/tool/` or `bin/api-docs/`. PR #78870 (2026-06-02, "Tools: migrate docs/tool into tools/docs workspace") moved it into the npm workspace **`tools/docs/`** (`@wordpress/docs-tools`, private). Older issues, PRs and blog posts still mention `docs/tool/manifest.js` and `bin/api-docs/*` or `tools/api-docs/*`.

---

## 1. The manifest

### 1.1 The pipeline at a glance

```
docs/toc.json  (hand-edited tree of file paths, plus 3 expansion tokens)
     │
     │  npm run docs:gen  →  node tools/docs/gen-manifest.cjs
     │                       (uses tools/docs/manifest.cjs)
     ▼
docs/manifest.json  (flat array of {title, slug, markdown_source, parent}; committed)
     │
     │  developer.wordpress.org importer fetches
     │  https://raw.githubusercontent.com/WordPress/gutenberg/trunk/docs/manifest.json
     ▼
handbook pages (one per manifest entry, keyed by slug)
```

The scripts in the root `package.json` (lines 136–143):

```json
"docs:build": "npm run docs:components && npm run docs:gen && npm run docs:blocks && npm run docs:blocks-detail && npm run docs:api-ref && npm run docs:theme-ref",
"docs:gen": "npm run --workspace @wordpress/docs-tools docs:gen --",
```

The same scripts in `tools/docs/package.json`:

| npm script | file | output |
|---|---|---|
| `docs:gen` | `gen-manifest.cjs` + `manifest.cjs` | `docs/manifest.json` |
| `docs:components` | `gen-components-docs/index.mjs` | `packages/components/src/**/README.md` (only components with a `docs-manifest.json`) |
| `docs:blocks` | `gen-block-lib-list.js` | `docs/reference-guides/core-blocks/README.md` (summary list) |
| `docs:blocks-detail` | `generate-block-docs.mjs` | `packages/block-library/src/*/README.md` + `docs/reference-guides/core-blocks/category-*.md` |
| `docs:api-ref` | `update-api-docs.js` (runs `@wordpress/docgen`) | token sections in `packages/*/README.md` and `docs/reference-guides/data/data-core*.md` |
| `docs:theme-ref` | `gen-theme-reference.mjs` | `docs/reference-guides/theme-json-reference/theme-json-living.md` |
| `docs:check-api-docs-unstaged` | `are-api-docs-unstaged.js` | none (exits 1 if token docs are dirty) |

Note on ordering: `docs:gen` runs **before** `docs:blocks` and `docs:blocks-detail`. If a brand-new block's README does not exist yet, one `docs:build` run will not add it to the manifest. It only gets added on the next run, or when lint-staged runs `docs:gen` because a `README.md` changed. This is my inference from the script order; I did not test it.

### 1.2 `gen-manifest.cjs` (the whole file)

`tools/docs/gen-manifest.cjs`:

```js
const tocFileInput = path.resolve( __dirname, '../../docs/toc.json' );
const manifestOutput = path.resolve( __dirname, '../../docs/manifest.json' );

fs.writeFileSync(
	manifestOutput,
	JSON.stringify( getRootManifest( tocFileInput ), undefined, '\t' ).concat( '\n' )
);
```

### 1.3 `docs/toc.json`

`docs/toc.json` is a hand-edited nested array. Each element is a one-key object. The key is a repo-root-relative path to a Markdown file. The value is either:

- an array of child objects in the same shape (`[]` for a leaf page), or
- one of three **expansion tokens**: `"{{components}}"`, `"{{blocks}}"` or `"{{packages}}"`.

```json
[
	{ "docs/README.md": [] },
	{
		"docs/getting-started/README.md": [
			{
				"docs/getting-started/devenv/README.md": [
					{ "docs/getting-started/devenv/nodejs-development-environment.md": [] },
	...
			{ "docs/reference-guides/core-blocks/README.md": "{{blocks}}" },      // line 198
	...
			{ "packages/components/README.md": "{{components}}" },               // line 301
			{ "docs/reference-guides/packages.md": "{{packages}}" },             // line 302
```

At this commit the TOC has 183 entries. Only one of them points outside `docs/`: `packages/components/README.md`. The three tokens add 361 more pages.

### 1.4 How a TOC entry becomes a manifest entry

From `tools/docs/manifest.cjs`, `generateRootManifestFromTOCItems()` (lines 168–243):

```js
let slug = fileNameFragments[ fileNameFragments.length - 1 ].replace( '.md', '' );
if ( 'readme' === slug.toLowerCase() ) {
	slug = fileNameFragments[ fileNameFragments.length - 2 ];
	// Special case - the root 'docs' readme needs the 'handbook' slug.
	if ( parent === null && 'docs' === slug ) {
		slug = 'handbook';
	}
}
let title = pascalCase( slug );
const markdownSource = fs.readFileSync( join( ROOT_DIR, fileName ), 'utf8' );
const titleMarkdown = markdownSource.match( /^#\s(.+)$/m );
if ( titleMarkdown ) {
	title = titleMarkdown[ 1 ];
}
pageItems.push( {
	title,
	slug,
	markdown_source: `${ baseRepoUrl }\/${ fileName }`,   // baseRepoUrl = '..'
	parent,
} );
```

The rules:

- **slug** is the file's basename without `.md`. For `README.md` it is the parent directory name instead. Slugs are **flat**: the slug does not include the path, so it must be unique across the whole handbook.
- **title** is the first `# H1` line in the file. If the file has no H1, it falls back to `pascalCase(slug)`.
- **parent** is the slug of the TOC parent, or `null` at the top level.
- **The handbook root is `docs/README.md`.** It gets the slug `handbook` from the special case above, has `parent: null`, and has the title "Block Editor Handbook". Five other top-level entries also have `parent: null`: `getting-started`, `how-to-guides`, `reference-guides`, `explanations` and `contributors`. They are siblings of `handbook`, not its children. Mapping `handbook` to the URL `/block-editor/` is done on the .org side; nothing in this repo encodes it.
- **Duplicate slugs** stop the build (lines 220–240). The generator throws `Duplicate slugs found in the TOC: …` and links to issue #61206 / PR #61332. Before that check existed, two files with the same basename in different folders silently overwrote each other on .org (#61206, and earlier #37505).

### 1.5 Entry schema and `markdown_source` format

Every manifest entry has exactly four keys: `title`, `slug`, `markdown_source` and `parent`. There is **no `order` field**. Order is implied by the array order, which follows the depth-first TOC order. There is no frontmatter and no per-page metadata of any other kind.

```json
{
	"title": "Block Editor Handbook",
	"slug": "handbook",
	"markdown_source": "../docs/README.md",
	"parent": null
},
{
	"title": "Block Development Environment",
	"slug": "devenv",
	"markdown_source": "../docs/getting-started/devenv/README.md",
	"parent": "getting-started"
}
```

**`markdown_source` is not a raw.githubusercontent.com URL.** It is a path relative to the manifest's own location: `"../docs/..."` or `"../packages/..."`. This contradicts the brief's assumption. The importer turns it into an absolute URL by resolving it against the manifest URL. The importer fetches `https://raw.githubusercontent.com/WordPress/gutenberg/trunk/docs/manifest.json` (confirmed in `wporg-developer/.../inc/import-block-editor.php` line 8), so `../docs/x.md` resolves to `https://raw.githubusercontent.com/WordPress/gutenberg/trunk/docs/x.md`. The resolution code is on the .org side, which the other report covers.

How the three tokens expand (`manifest.cjs`):

| Token | Source of pages | slug | parent | title |
|---|---|---|---|---|
| `{{components}}` | glob `packages/components/src/*/**/README.md`, minus 6 private components (lines 18–30) | name of the folder containing the README, e.g. `button` | `components` | `pascalCase(slug)` (**not** the H1) |
| `{{blocks}}` | `docs/reference-guides/core-blocks/category-*.md`, plus each `packages/block-library/src/*/block.json` whose folder has a `README.md` | `core-blocks-{category}` for category pages; `core-block-{dir}` for block pages | `core-blocks` for category pages; `core-blocks-{block.json category}` for block pages | category pages: first H1; block pages: `block.json` `title` |
| `{{packages}}` | every `packages/*/package.json` without `"private": true` | `packages-{folder}` | `packages` | `package.json` `name`, e.g. `@wordpress/dom-ready` |

For packages, the generator also appends `packages/{pkg}/docs/toc.json` if that file exists. That file is already in **manifest format**: a hand-written array of `{title, slug, markdown_source, parent}` entries. Only `create-block` and `style-engine` use it today.

### 1.6 Confirmed by running the generator

Running a path-patched copy of `manifest.cjs` against `docs/toc.json` produced output **byte-identical** to the committed `docs/manifest.json` (3,308 lines, `diff` showed no differences). What the manifest contains at this commit:

| Measure | Value |
|---|---|
| Manifest entries | **551** |
| Sources under `docs/` | 189 (of 194 `.md` files in `docs/`) |
| `packages/components/src/**/README.md` | 124 |
| `packages/block-library/src/*/README.md` (per-block pages) | 116 |
| Package READMEs (`packages-*`) | 119, plus 2 from package `docs/toc.json` files, plus `packages/components/README.md` |
| Largest parents | `components` 124, `packages` 119, `core-blocks-theme` 51, `core-blocks-design` 24 |
| Orphan `.md` files in `docs/` (not in the manifest, so not published) | `docs/contributors/code/back-merging-to-wp-core.md`, `docs/contributors/code/build-system-function-prefixing.md`, `docs/contributors/documentation/how-to-guide-template.md`, `docs/how-to-guides/eslint-v10-migration.md`, `docs/private-apis.md` |

**Published URLs.** The URL is built from the chain of parent slugs, not from the file path. You can see this in the absolute URLs that `generate-block-docs.mjs` hardcodes (line 444):
`https://developer.wordpress.org/block-editor/reference-guides/core-blocks/core-blocks-${category}/core-block-${slug}/`

---

## 2. Auto-generated docs

### 2.1 What is generated

| Output | Generator (`tools/docs/…`) | Input | Mechanism |
|---|---|---|---|
| API sections of **53** `packages/*/README.md` | `update-api-docs.js` → `@wordpress/docgen` bin | JSDoc/TSDoc of `src/index.*`, or the file named in the token | Replaces content between `<!-- START TOKEN(Autogenerated API docs) -->` and `<!-- END TOKEN(...) -->`. Symbols matching `/unstable\|experimental/i` are ignored. Runs `npm run format` on the result. |
| **16** data store references `docs/reference-guides/data/data-core*.md` | same script | store selectors/actions source, e.g. `<!-- START TOKEN(Autogenerated selectors\|../../../packages/notices/src/store/selectors.ts) -->` | token replacement |
| `docs/reference-guides/core-blocks/README.md` (summary of every core block) | `gen-block-lib-list.js` | `packages/block-library/src/*/block.json` | `<!-- START TOKEN Autogenerated - DO NOT EDIT -->` … `END` |
| **116** per-block pages `packages/block-library/src/{block}/README.md` + 7 `category-*.md` | `generate-block-docs.mjs` (1,065 lines; PR #77612, merged 2026-06-07 after a first attempt #77350 was reverted in #77590) | `block.json` + test fixtures | `<!-- START TOKEN(Autogenerated block API docs) -->`. Hand-written prose outside the tokens is kept. Creates the file if it is missing. Also maintains a `<!-- START TOKEN(Deprecated blocks) -->` section in the core-blocks README. |
| `docs/reference-guides/theme-json-reference/theme-json-living.md` | `gen-theme-reference.mjs` | `schemas/json/theme.json` (JSON Schema, `$ref`s resolved) | `START TOKEN Autogenerated - DO NOT EDIT` |
| **14** component READMEs (of 129) | `gen-components-docs/index.mjs` (`react-docgen-typescript`) | `packages/components/src/**/docs-manifest.json` + TS types/TSDoc + Storybook tags | Writes the whole file. The header is `<!-- This file is generated automatically and cannot be edited directly. Make edits via TypeScript types and TSDocs. -->` |
| `docs/manifest.json` | `gen-manifest.cjs` | `docs/toc.json` + globs | full rewrite |

Across the 551 published pages, 193 contain at least one `<!-- START TOKEN` block (215 blocks in total).

**Important for migration:** many of these generated pages contain **hardcoded absolute `https://developer.wordpress.org/block-editor/...` links**. `generate-block-docs.mjs` constants `ATTRIBUTES_REF` and others (lines 50–65, 299, 444, 456, 673–807) and the root `docs/README.md` both do this. Counting every published page, there are 3,722 such absolute links in 200 files. If URLs change in a migration, these must be rewritten in the **generators**, not only in the Markdown.

### 2.2 How CI makes sure generated docs are up to date

There are two layers.

**1. Pre-commit (local, can be skipped).** `lint-staged.config.cjs`:

```js
'{docs/toc.json,tools/docs/*.cjs,packages/{*/README.md,components/src/*/**/README.md,block-library/src/*/README.md}}':
	[ 'npm run docs:gen' ],
'packages/**/*.{cjs,cts,js,jsx,mjs,mts,ts,tsx,json}': [
	'npm run docs:api-ref',
	'npm run docs:blocks',
	'npm run docs:blocks-detail',
	'npm run docs:theme-ref',
	'npm run docs:check-api-docs-unstaged',
],
```

`are-api-docs-unstaged.js` fails the commit if any unstaged `.md` file contains `<!-- START TOKEN`. Its message is "Some API docs may be out of date … build and stage them with npm run docs:build or continue with --no-verify."

**2. CI: the authoritative check.** In `.github/workflows/static-checks.yml`, job `check` (runs on every `pull_request` and on pushes to `trunk`, `release/*` and `wp/*`), step **"Check local changes"** (line 148) runs `npm run other:check-local-changes`. The root `package.json` line 173 defines a pre-hook for it:

```json
"preother:check-local-changes": "npm run docs:build && npm run --workspace @wordpress/theme build",
```

So CI regenerates **all** docs, then `tools/validation/check-local-changes.cjs` runs `git diff -U0` and exits 1 if there is any diff (it ignores optional-only `package-lock.json` noise). The failure message:

```
There are local changes after running one or more of the following commands:
- npm install
- npm run lint:js:prune-suppressions
- npm run lint:css:update-suppressions
- npm run docs:build
- npm run --workspace @wordpress/theme build
Run these commands in your local environment and commit the resulting changes to resolve the issue.
```

The contributor guide states the same consequence (`docs/contributors/documentation/README.md` line 65): if you forget `npm run docs:build`, "your PR will fail the static analysis check since the `manifest.json` file is an uncommitted local change". The same CI path also catches a duplicate slug, because `docs:gen` throws.

**Not enforced in CI:**

- **Markdown lint.** `lint:md:docs` (`wp-scripts lint-md-docs`) exists, but no workflow or lint-staged entry runs it. The config is `.markdownlint.json`, which extends `packages/scripts/config/.markdownlint.json` (ATX headings, 4-space list indent, MD013 effectively off) and sets `"MD033": false` so inline HTML is allowed.
- **Link checking.** No link checker runs. Broken links are found by hand (see section 6).

---

## 3. Authoring conventions

The main source is `docs/contributors/documentation/README.md` (246 lines). Its neighbours are `copy-guide.md` (voice and copy rules) and `how-to-guide-template.md` (template; not in the manifest). `AGENTS.md` lines 39–54 repeats the no-hard-wrap rule and points to the guide.

### 3.1 Adding a page (guide lines 55–65)

1. Create a lower-case, dash-separated `.md` file in `docs/`.
2. Use exactly one `h1` ("All documents require one and only `h1` tag"). The H1 becomes the manifest title. On .org it is rendered as the page title, so anchors that point to the H1 do not resolve (PR #82878).
3. Add the file to `docs/toc.json`.
4. Run `npm run docs:build`.
5. Commit `manifest.json` together with the page.

For a package, put extra pages in `packages/{pkg}/docs/` and list them in `packages/{pkg}/docs/toc.json` with `parent: "packages-{pkg}"` (guide lines 67–84).

Updating an existing page needs only a PR with the `[Type] Developer Documentation` label (guide lines 45–53).

### 3.2 Links (guide lines 86–108)

> To create links that work in all contexts, you must use absolute path links without the `https://github.com/WordPress/gutenberg` prefix … `/docs/*.md`, `/packages/*/README.md`, `/packages/components/src/**/README.md` … Use the full directory and filename from the Gutenberg repository, not the published path … the `readme.md` portion is dropped in the handbook but should be included in the links.

So the convention is **repo-root-absolute file paths**, which the importer rewrites into handbook URLs. The three contexts the guide names are GitHub, npm and the handbook. Known exceptions:

- **Links inside callouts are not transformed.** You must use an HTML `<a href="https://developer.wordpress.org/block-editor/...">` with the final handbook URL (lines 106–108 and 165–171). Issue #50125 documented this.
- **Root-absolute links break on npmjs.com** (#36426, open). A link like `/packages/scripts` resolves against the package directory on npm.
- **Links to files that are not in the manifest 404 on .org.** PR #83449 had to change them to full `https://github.com/WordPress/gutenberg/blob/HEAD/...` URLs.

What the 551 published pages actually use (regex tally, approximate):

| Link style | Occurrences | Files |
|---|---|---|
| Root-absolute `](/docs/…)` or `](/packages/…)` (the convention) | 661 | 143 |
| Relative `./` or `../` | 13 | 10 |
| Bare relative `foo.md` | 1 | 1 |
| Absolute `https://developer.wordpress.org/block-editor…` | 3,722 | 200 (mostly generated block pages) |
| Absolute `https://github.com/WordPress/gutenberg/(blob\|tree)/…` | 678 | 266 (mostly package README footers) |
| Same-page anchors `](#…)` | 180 | 42 |

**Anchors are a hazard.** Heading ids on .org are made by a different slugifier from GitHub's. For example, "Node.js development tools" becomes `#node-js-development-tools` on .org but `#nodejs-development-tools` on GitHub (PR #82878). PR #83545 (2026-09) fixed a batch of stale anchors.

### 3.3 Images (guide lines 200–220)

> Images displayed in the Block Editor Handbook must be hosted in the developer.wordpress.org Media Library, not linked from GitHub … URLs starting with `https://raw.githubusercontent.com` are subject to rate limiting … `https://developer.wordpress.org/files/2026/06/your-image.png`

Uploading needs developer.wordpress.org Media Library permissions; the guide says to ask in #docs. SVG cannot be uploaded, so use a PNG unless the SVG is meant to be downloaded. This rule was added after issue #79521 (2026-06).

Image hosts referenced in published pages (count of `![](…)` / `<img>` sources, which includes some inside code samples):

| Host | Count |
|---|---|
| `developer.wordpress.org` (mostly `/files/`) | 114 |
| `s.w.org` (mostly the "Code is Poetry" footer in package READMEs) | 109 |
| `wordpress.org` | 48 |
| `make.wordpress.org` | 34 |
| `user-images.githubusercontent.com` / `github.com/.../assets` | 12 (7 files) |
| `cldup.com` | 7 |
| `raw.githubusercontent.com` | 5 (2 files) |

No image uses a relative path. Images do not live in the repo; `docs/assets/` exists but published pages do not reference it via relative paths.

### 3.4 Code blocks and `codetabs` (guide lines 110–133)

- Use fenced code blocks with a language: ` ```js `, ` ```php `, ` ```json `, ` ```html `, ` ```css `, ` ```bash `. The importer maps `class="css"` to `language-css` (importer side).
- The `codetabs` toggle is Gutenberg-specific syntax that the .org importer parses:

  ````md
  {% codetabs %}
  {% JSX %}
  ```js
  // JSX code here
  ```
  {% Plain %}
  ```js
  // Plain code here
  ```
  {% end %}
  ````

  The first tab is the default. JSX is preferred. It is effectively deprecated in practice: only **one** published page still uses it (`docs/how-to-guides/themes/global-settings-and-styles.md`, 10 markers).

### 3.5 Callouts (guide lines 135–171)

Raw HTML is used instead of shortcodes so the pages render on GitHub and npm too:

```html
<div class="callout callout-info">This is an **info** callout.</div>
```

The documented levels are `info`, `tip`, `alert` and `warning`. In use across `docs/` and package READMEs: `info` 60, `alert` 30, `tip` 20, `warning` 16, an undocumented `note` 1, and one `<p class="callout callout-alert">`. Component READMEs generated by `gen-components-docs` emit `<p class="callout callout-info">`. Across published pages there are 176 callouts in 101 files. Markdown inside the div is processed by the .org renderer (the guide's own examples rely on `**bold**`), but links inside a callout are not rewritten.

### 3.6 Video and embeds (guide lines 222–240)

Videos must be unlisted uploads on the WordPress YouTube channel (ask in #marketing) and embedded with a raw `<iframe width="960" height="540" src="https://www.youtube.com/embed/…" …>` at 16:9. Four iframes appear in three published pages. `<details>` is used 18 times in 7 files.

### 3.7 Other conventions

- **Frontmatter:** none. No published page starts with `---`, and the manifest has no metadata fields. Issue #45669 proposed frontmatter or a `__meta` key for redirects; nothing was built.
- **H1:** exactly one per page. Every page meets this except `packages/project-management-automation/README.md`.
- **HTML pass-through:** `MD033` is disabled, so inline HTML is allowed (callouts, iframes, `<details>`, `<br />`, `<p align="center"><img …>`). There are 871 HTML comments in 229 files. Most are generator tokens, which must be preserved and should never be hand-edited. `<!-- wp:… -->` appears 229 times in 133 files, almost always inside fenced code samples showing block markup, not as live content.
- **Line wrapping:** never hard-wrap prose (lines 173–181). Format Markdown with Prettier (lines 183–198).
- **"Edit on GitHub" / "Last updated":** nothing on the source side. The edit link is built by the importer from `markdown_source` (raw → `github.com/.../edit/`). Issue #57630 (2024-01) reported empty "Improve it on GitHub" links, which was an importer-side bug. The repo has no last-updated metadata; it would have to come from git or the importer.

---

## 4. Review, ownership and release timing

| Item | Finding |
|---|---|
| CODEOWNERS (`.github/CODEOWNERS` lines 1–3) | `/docs` → `@juanmaguitar @fabiankaegy`; `/packages/interactivity/docs` → `@juanmaguitar`. Related paths: `/packages/block-library` → `@fabiankaegy`; `/tools` (including `tools/docs`) → `@manzoorwanijk`; `/packages/components` → `@WordPress/gutenberg-components`. Package READMEs are owned by each package's owners, not by docs owners. |
| Label | `[Type] Developer Documentation` ("Documentation for developers"). `Needs User Documentation` is for end-user docs. `.github/workflows/enforce-pr-labels.yml` requires **exactly one** `[Type] …` label on every PR, so a docs PR that also changes code still carries just one type label. |
| Auto-labeling | `.github/labeler.yml` labels by package (`[Package] X`, `[Tool] Docgen`). No rule labels `docs/**`. |
| Docs with code? | Both happen. Of the last 100 merged `[Type] Developer Documentation` PRs, 58 changed only `docs/` or `.md` files and 42 also changed other files. Generated READMEs, block pages and theme.json docs change automatically in code PRs because CI forces regeneration. |
| Open docs issues | 71 open issues labelled `[Type] Developer Documentation` (2026-10-11). |
| Project board | **Unverified.** `gh project list` needs the `read:project` scope, which the token lacks. |
| Publish timing | The handbook is **built from trunk, not tied to releases.** The guide (line 26) says "An automated job publishes the docs every 15 minutes". The importer reads `.../gutenberg/trunk/docs/manifest.json` (wporg-developer `import-block-editor.php` line 8), and generated source links hardcode `tree/trunk`. The importer also has a filter that rewrites `/wp/{WP_CORE_STABLE_BRANCH}/` edit links to `/trunk/` (lines 381–389), which suggests a branch-based import was planned or used at some point. That is for the importer report to verify. |
| Version skew | Because docs publish from trunk, the handbook documents unreleased features. This is a long-standing complaint: #6514 (2018, closed), #44430 (open, versioned docs request), #78376 (open, "since" versions in generated API docs), and #56499 (theme.json docs duplicated with the Theme Handbook). |

---

## 5. Redirects and renames

- **The gutenberg repo has no redirect list.** The manifest schema has no `redirect_from` or similar field. When a page is renamed or moved, the slug or parent changes, which makes a new URL; the old URL 404s unless someone adds a redirect on the .org side.
- **Current process (manual, cross-repo):** after the Gutenberg PR merges, someone opens a PR against `WordPress/wporg-developer` that adds an `'old/path' => 'new/path'` entry to the `redirects()` array in `source/wp-content/themes/wporg-developer-2023/inc/import-block-editor.php`. Examples:
  - wporg-developer PR #274, for Gutenberg #54120 (glossary move).
  - wporg-developer PR #487, which added the "After handbook restructuring, January 2023" and "December 2023" groups.
  - Gutenberg PR #74974 (2026-02, renaming the Interactivity API "API Reference" to "Directives and Store"), where a comment notes: "Once is merged we need to add a redirection in the Block Editor Handbook like in here [wporg-developer#487]".
- **Open proposal:** issue #45669 (2023, open, `Needs Dev`) proposes `redirect_from` in `toc.json`/`manifest.json` or frontmatter, paired with Meta Trac #6407. A maintainer called the current process "very pedestrian"; the issue has stalled.
- **The flat-slug collision trap:** #61206 (fixed by #61332). Moving a file can create a slug that collides with another page. Before the check existed, one page silently overwrote the other on .org.

---

## 6. Known pain points (from issues and PRs)

| Theme | Evidence | Status |
|---|---|---|
| **Broken links after publish** (anchors, unpublished targets, callout links) | #29662 (fix broken links, 2021), #49469 (dead link), #57630 (empty edit links), #83545 (stale anchors, 2026-09), #82878 (self-anchor to H1, 2026-09), #83449 (links to a non-manifest guide 404ed; rewritten to GitHub URLs) | Recurring; no automated link check in CI |
| **Link convention conflicts across contexts** (GitHub, npm, handbook) | #36426: root-relative links 404 on npm. Callout links need hardcoded handbook URLs (#50125). | #36426 open |
| **Images on GitHub get rate-limited** | #79521 (2026-06). The guide now requires the developer.wordpress.org Media Library, which needs special permissions to upload. | Policy added; 17 GitHub-hosted images remain in published pages |
| **Renames need manual redirects in another repo** | #45669, Meta Trac #6407, wporg-developer #274/#487, PR #74974 | Open |
| **Slug collisions** | #61206, #37505, #15526 (duplicate pages, 2019) | Mitigated by the build-time check |
| **Sync staleness** | #3938 ("Handbook is not synced", 2017–2021), #6514 | No recent source-side reports. The 15-minute cron is .org side. |
| **Docs ahead of shipped WordPress** (trunk publishing) | #6514, #44430, #78376; comments on the make/core proposal for block.json docs (May 2026) | Open; no versioning |
| **Generated-docs churn and tooling** | #61036 (improve the JS API docs tool, open). Block-page generator reverted once (#77590) for lack of consensus, then relanded (#77612). #78998 (open): make the generator reusable for third-party blocks. | Active area |
| **Navigation order** | #14794: next/prev links did not follow sidebar order (2019) | Closed (historical) |

The search queries I ran: "developer.wordpress.org handbook", "manifest.json handbook", "handbook not updating", "docs sync handbook", "handbook broken links", "handbook redirect", "block editor handbook 404", "handbook images github raw", "callout links handbook".

---

## 7. Three representative pages

### 7.1 Hand-written guide: `docs/how-to-guides/format-api.md`

Manifest entry: slug `format-api`, parent `how-to-guides`. It shows one H1, a Media Library image, the root-absolute link convention, and a fenced `js` block.

```md
# Formatting Toolbar API

## Overview

The Format API makes it possible for developers to add custom buttons to the formatting toolbar ...

![Format API Toolbar animated example](https://developer.wordpress.org/files/2021/12/format-api-example.gif)
...
This guide assumes you are already familiar with WordPress plugins and loading JavaScript with them, see the [Plugin Handbook](https://developer.wordpress.org/plugins/) or [JavaScript Tutorial](/docs/getting-started/fundamentals/javascript-in-the-block-editor.md) to brush up.
...
```js
import { registerFormatType } from '@wordpress/rich-text';

registerFormatType( 'my-custom-format/sample-output', {
	title: 'Sample output',
	tagName: 'samp',
	className: null,
} );
```
...
-   RichText: [`registerFormatType`](/packages/rich-text/README.md#registerformattype)
```

### 7.2 Auto-generated reference: `packages/block-library/src/paragraph/README.md`

Manifest entry: slug `core-block-paragraph`, parent `core-blocks-text`, title "Paragraph" (from `block.json`). It is generated by `generate-block-docs.mjs`. Everything between the tokens is regenerated, and its links are hardcoded absolute handbook URLs.

```md
# Paragraph

<!-- START TOKEN(Autogenerated block API docs) -->
Start with the basic building block of all narrative.

- **Name:** `core/paragraph`
- **Category:** [text](https://developer.wordpress.org/block-editor/reference-guides/core-blocks/core-blocks-text/)
- **API Version:** [3](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-api-versions/)
- **Block Type:** [Hybrid](https://developer.wordpress.org/block-editor/getting-started/fundamentals/static-dynamic-rendering/) (static save + server enhancements)

## Attributes

| Attribute | [Type](…/block-attributes/#type-validation) | [Default](…/block-attributes/#default-value) | Description |
|-----------|------|---------|-------------|
| `content` | `rich-text` | — | [Source](…#value-source): `rich-text`. [Selector](…#value-source): `p`. [Role](…#role): `content` |
| `dropCap` | `boolean` | `false` | — |
...
## Source

- [block.json](https://github.com/WordPress/gutenberg/tree/trunk/packages/block-library/src/paragraph/block.json) ([reference](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/))

<!-- END TOKEN(Autogenerated block API docs) -->
```

Other generated pages have the same shape. For example, `docs/reference-guides/data/data-core-notices.md` uses `<!-- START TOKEN(Autogenerated selectors|../../../packages/notices/src/store/selectors.ts) -->`, and `theme-json-living.md` uses `<!-- START TOKEN Autogenerated - DO NOT EDIT -->` below a hand-written intro.

### 7.3 Package README: `packages/dom-ready/README.md`

Manifest entry: slug `packages-dom-ready`, parent `packages`, title `@wordpress/dom-ready`. It mixes hand-written content with a docgen API section, a GitHub `tree/HEAD` link, and the standard footer with an `s.w.org` image in raw HTML. The same file is published on npm.

```md
# DOM Ready

Execute callback after the DOM is loaded.

## Installation
...
## API

<!-- START TOKEN(Autogenerated API docs) -->

### default

Specify a function to execute when the DOM is fully loaded.

_Usage_

```js
import domReady from '@wordpress/dom-ready';
...
```

_Parameters_

- _callback_ `VoidFunction`: A function to execute after the DOM is ready.

<!-- END TOKEN(Autogenerated API docs) -->
...
To find out more about contributing to this package or Gutenberg as a whole, please read the project's main [contributor guide](https://github.com/WordPress/gutenberg/tree/HEAD/CONTRIBUTING.md).

<br /><br /><p align="center"><img src="https://s.w.org/style/images/codeispoetry.png?1" alt="Code is Poetry." /></p>
```

---

## 8. What this means for a migration

1. **The manifest is the whole contract with the importer.** It is four fields, and URL hierarchy comes only from `parent`. Any new system needs slug uniqueness, title-from-H1, and the three expansion tokens, or must replace them.
2. **About two thirds of pages (362 of 551) live outside `docs/`**, in package and component and block folders. Their content comes from code (JSDoc, `block.json`, TS types, JSON Schema). Moving the docs elsewhere means either keeping these generators in the gutenberg repo or syncing their output.
3. **Hardcoded `developer.wordpress.org/block-editor/...` URLs** appear in generators and about 200 pages. Any URL change needs generator edits and redirects.
4. **Redirects are the biggest process gap.** They live only in `wporg-developer` and are added by hand.
5. **Rendering quirks the new system must support** (or convert): `{% codetabs %}` (one page), `callout callout-*` divs and p elements whose links are not rewritten, root-absolute `/docs/...md` link rewriting, anchor slug rules, and token HTML comments.

## Unverified or out of scope

- How the importer resolves `../` `markdown_source` paths and rewrites links (importer report).
- Whether the 15-minute schedule is still accurate. The guide says so; the cron lives on .org.
- The GitHub Projects board for docs (missing token scope).
- My claim that a newly added block README needs a second `docs:build` run to reach the manifest. This is inferred from script order and not tested.
