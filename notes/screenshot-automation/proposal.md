# Proposal: automated screenshots (and short clips) for the WordPress documentation

Drafted 2026-10-09. Status: proposal, nothing built yet beyond a proof of concept.

Supporting material in this folder:

- `research/01-audit-of-current-screenshots.md`: what the 2,309 images and 200 videos in `docs/` actually show.
- `research/02-prior-art.md`: how GitLab, TYPO3, Django, Zulip, GitHub, the Playground team and others do this.
- `research/03-playground-and-playwright.md`: the current state of Playground CLI, Blueprints, the Gutenberg
  Playwright utilities, and Playwright screenshot and screencast APIs, verified by running them.
- `spike/`: a working proof of concept (Playground booted from a blueprint, Playwright capturing the editor).
  `spike/REPORT.md` has the details; `spike/out/run1/` has the nine captured images.

## 1. Summary

Build a small, declarative screenshot toolkit that lives in this repo, boots WordPress Playground from a
committed blueprint plus an approved demo-content pack, and uses Playwright with the Gutenberg e2e utilities to
capture every screenshot in the docs from a YAML "shot" definition. One command regenerates a page, a section
or everything. A canonical render runs in a Docker image so output is pixel-stable across machines, which is what
makes "regenerate everything at each WordPress release candidate and review only what changed" possible.

Recommendation in one line: **Playground CLI + Blueprint v1 + `@playwright/test` + `@wordpress/e2e-test-utils-playwright`,
driven by YAML shot specs mirrored to the docs tree, output to `docs/assets/screenshots/<article-slug>/<shot-id>.png`,
canonical renders in the Playwright Docker image, regenerated at every core RC1 via CI.**

Why this is realistic now and was not two years ago:

- Playground CLI boots a full WordPress headlessly from Node in about 9 seconds with no Docker. No contributor needs
  a local WordPress.
- The Gutenberg team's Playwright utilities (`createNewPost`, `insertBlock`, `openDocumentSettingsSidebar`,
  `visitSiteEditor`, `requestUtils.uploadMedia`, and so on) are published and work standalone. They absorb most of
  the UI drift between releases, because Gutenberg has to keep them working for its own tests.
- Playwright 1.59+ has a `page.screencast` API with an animated cursor, action labels and chapter cards. Short
  clips become the same spec format as screenshots.
- The Playground team merged a `doc-screenshots` agent skill in July 2026 with a fixed house style (1440×900 at 2x,
  WordPress-blue outlines, orange arrows). We can adopt that style and talk to them rather than invent one.

The proof of concept in `spike/` confirms the core loop on a Mac: Playground boots WordPress 7.1.3 from a blueprint in
about 4 s, a plain Node script captures nine 2x screenshots of the Image block (placeholder, toolbar crop, settings
panel, inserter search, highlighted Replace button, masked image) in about 5 s, and all nine files were byte-identical
across three runs including one after a server restart. The same captures against nightly 7.2 differ in every image,
so a pixel diff does detect UI drift between versions.

The two things that killed previous attempts elsewhere (GitLab, TYPO3) were requiring a developer environment to
author a shot, and not running in CI. The design below is built around avoiding both.

## 2. The problem, in numbers

From `research/01-audit-of-current-screenshots.md` (working tree, 2026-10-09):

| Fact | Value |
|---|---|
| Image references / files | 2,309 refs in 263 articles (100 of 363 `.md` files have none) |
| Concentration | 85% in Editing & design; the 130 block pages hold 1,526; the 36 embed pages alone hold 510 |
| Shape | Over half are tight crops of one UI element (toolbar strip, sidebar panel), not full screens |
| Pixel density | Roughly 55–60% are 2x Mac captures, 40% are 1x, mixed on the same page |
| Hand annotations | About 43% carry red boxes or arrows, in at least three different tools' styles |
| Staleness | About 10–15% show pre-6.0 UI; another 30–35% are 6.0–6.4 era; roughly half would need retaking |
| Alt text | 75% descriptive, 10% empty, 5% generic ("image", "Before") |
| Videos | 200 self-hosted clips in 86 articles, median 23 s; about 125 are 30 s or shorter single interactions |
| Licensing | At least one iStock-watermarked stock image is in the docs today |

The docs team currently handles this with per-release GitHub issues such as "[HelpHub][7.1]: Update Layout
Settings Page screenshots" (94 such issues in the Documentation-Issue-Tracker, 87 closed). Each one is a human
re-creating a state, capturing, annotating by hand, and uploading. The Make Docs handbook's screenshot guidance
says "fresh install, default theme, no plugins, English" and suggests Playground, but publishes no rule on
dimensions, DPR, format or annotation colour. There is no codified spec; this toolkit would be the first.

## 3. Design principles

Drawn from the prior-art survey, each one maps to a failure someone else already had.

1. **Writers author shots in YAML, not code.** GitLab's RSpec-based generator ended up with two spec files in five
   years because it needed a dev kit and Ruby. Every common shot must be expressible without writing Playwright.
   A `script:` escape hatch exists for the long tail.
2. **One command from a clean clone.** `npm install`, `npx playwright install chromium`, `npm run shots`. Playground
   makes this possible without Docker or a database.
3. **Runs in CI, on a schedule and on every core RC.** TYPO3's tool was archived after their own post-mortem said a
   tool outside the product's CI rots silently.
4. **Deterministic by construction.** Pinned WordPress, PHP, Gutenberg (if any), npm lockfile, Playwright image tag,
   frozen clock, fixed viewport and DPR, reduced motion, animations disabled, caret hidden, committed demo content with
   no runtime network dependency. Determinism is what turns "regenerate all" into "review the diff".
5. **Annotations anchor to locators, never pixels.** Highlight boxes and numbered badges are declared against the
   same selectors the shot uses, drawn into the DOM before capture, so they survive layout changes and reuse in video.
6. **Stable filenames keyed by article slug and shot id.** Versions go in a sidecar manifest, not the filename, so a
   regeneration never touches the Markdown.
7. **Change above a threshold means a human looks.** Playwright's `toHaveScreenshot` or pixelmatch against the
   committed image; a changed screenshot is also the signal that the article text may need a review.
8. **Fewer, better shots.** The overhaul is the moment to stop reproducing the 2,309 we have. The audit suggests the
   embed section alone collapses from 510 images to one parameterised template.

## 4. The system

### 4.1 Where it lives

Recommendation: **inside this repo**, as a self-contained workspace folder, with the engine written so it can be
extracted into its own package later.

```
screenshots/
  package.json              # own deps: @wp-playground/cli, @playwright/test, @wordpress/e2e-test-utils-playwright, sharp, pixelmatch
  README.md                 # the "clone and run" guide
  playwright.config.ts
  blueprint/
    blueprint.json          # Blueprint v1: pinned versions, TT5 active, options, mu-plugin, content pack import
    mu-plugin/docs-demo.php # kill nags/notices, freeze clock, local avatars, oEmbed fixtures, disable animations
    content/                # the approved demo site: WXR, media files, patterns, templates, users, comments
    content/LICENSES.md     # source URL + license per photo
  suites/                   # alternative blueprints: classic (TT1 + Classic Editor + Classic Widgets), per default theme
  shots/                    # YAML shot specs, one file per article, mirrored to the docs tree
    editing-and-design/block-editor/blocks/media-blocks/image-block.yaml
    using-wordpress/administration-screens/plugins/manage-plugins.yaml
    ...
  src/
    cli.ts                  # shots run | check | update | lint | snippet | dev | doctor
    env/                    # start/stop Playground (or wp-env), snapshot cache
    scenes/                 # new-post, post:<slug>, site-editor:<route>, admin:<path>, front:<path>
    actions/                # the YAML verb vocabulary, implemented on top of the WP e2e utils
    targets/                # the named-target registry: block-toolbar, inspector, inserter, list-view, ...
    capture/                # crop, pad, annotate, frame, encode, optimise
    diff/                   # pixel compare + HTML report
    manifest.ts             # writes docs/assets/screenshots/manifest.json
docs/assets/screenshots/
  <article-slug>/<shot-id>.png
  manifest.json             # generated: per shot -> file, alt, caption, article, WP/GB versions, hashes, captured_at
```

Reasons for in-repo rather than a separate repo:

- During the overhaul, a shot, its image and the Markdown that uses it change together. One PR, one review.
- The preview site in `site/` can show "regenerated for 7.2" and "stale" badges straight from the manifest.
- CI on the docs repo is where an RC-triggered regeneration PR naturally lands.
- Gutenberg keeps its handbook, tests and tooling in one repo and that is the model this repo already follows.

The alternative, a standalone `wp-docs-shots` package consumed by this repo, becomes the right move once a second
consumer exists (Learn WordPress, the Playground handbook, plugin authors wanting `.wordpress-org/screenshot-N.png`).
Keeping the engine free of any knowledge of this repo's layout (it takes a shots dir, an output dir, and a blueprint)
makes that extraction a move, not a rewrite.

Shot specs live in `screenshots/shots/` mirrored to the docs path rather than next to the Markdown because
`scripts/convert.py` currently regenerates everything under `docs/` except `docs/assets/`. Once the docs become
hand-maintained after the overhaul, moving the YAML next to the article is a mechanical change.

### 4.2 Environment: Playground plus an approved demo site

- `@wp-playground/cli server --wp=<pinned> --php=8.3 --blueprint=blueprint/blueprint.json --blueprint-may-read-adjacent-files --port=9400`.
  Verified: a plain boot takes about 9 s; nightly plus a Gutenberg zip 12–19 s; a full content import with media
  about 45 s. `build-snapshot` produces a zip of the provisioned site that later runs can boot from, so the content
  import happens once per content-pack change, not per run. Cache that snapshot in CI keyed by the blueprint hash.
- **Blueprint v1**, with `preferredVersions` set explicitly. Two verified gotchas: an omitted PHP version silently
  picks the newest, and in the spike the `--wp` flag lost to the blueprint, with `--wp=7.0`, `nightly`, `beta` and a
  zip URL all still booting 7.1.3 when the blueprint had no `preferredVersions` (likely a CLI bug worth reporting).
  Setting `preferredVersions.wp` in the blueprint worked (`nightly` gave 7.2-alpha, `6.9` gave 6.9.10). So the
  toolkit generates one blueprint per target version and asserts the booted version before capturing. v2 exists in
  the schema but has no stability announcement; do not build on it yet.
- **No Gutenberg plugin by default.** HelpHub documents core. A scheduled job against `--wp=nightly` (and optionally
  the Gutenberg RC zip from GitHub releases) acts as early warning, nothing more.
- **Default theme pinned to the current default** (Twenty Twenty-Five as of 7.1; re-check at 7.2 Beta 1 on Oct 20).
- **The mu-plugin** installed by the blueprint does what every prior-art project ended up needing: hide update nags,
  admin notices and the SQLite integration notice; return local avatars instead of Gravatar; freeze `current_time`
  and the editor's relative times to a fixed date so "3 minutes ago" is stable; disable CSS transitions; and answer
  `pre_oembed_result` with committed fixture HTML for the embed providers so embed shots are deterministic and work
  offline. Playwright's `page.route` additionally serves a static poster for third-party iframes.
- **The content pack** is the "approved, professional demo". It is a fictional small site (name to be chosen; it must
  not imitate a real organisation), with:
  - 8–12 posts with featured images, categories, tags, spread-out dates, a few with revisions; a Sample Page,
    an About page and a Contact page built from Twenty Twenty-Five patterns; one post with every core block.
  - 15–25 CC0 photos from the WordPress Photo Directory, bundled locally, each recorded in `LICENSES.md`.
    A short MP3, a short MP4, a PDF, a site logo and icon.
  - Admin plus two or three named authors with bios; a threaded comment set including pending and spam items;
    a navigation menu with a submenu; a couple of synced patterns; a modified template and template part for the
    "reset" shots; custom global styles.
  - Site title, tagline, pretty permalinks, UTC timezone, English.
  - Imported via `bundled` resources and `runPHP`, not via `importWxr` with network fetches, so no run-time network.
  The Theme Unit Test data is useful for edge cases but looks like test fixtures and has no license file; do not use
  it for docs imagery.
- **Suites** for things that cannot share a site: Classic WordPress (Twenty Twenty-One, Classic Editor, Classic
  Widgets), one per classic default theme for the theme pages, a "broken plugin" suite for recovery mode. A shot
  names its suite; the runner boots suites lazily.
- **wp-env fallback**: the Gutenberg utilities default to wp-env's URL and credentials, so supporting Docker-based
  wp-env is a matter of `WP_BASE_URL`. Worth keeping as an escape hatch for anything Playground cannot do; not the
  primary path.

### 4.3 Shot specs

One YAML file per article. The spec is the source of truth for the image, its alt text and its caption.

```yaml
# screenshots/shots/editing-and-design/block-editor/blocks/media-blocks/image-block.yaml
article: image-block                  # docs/manifest.json slug; output goes to docs/assets/screenshots/image-block/
defaults:
  scene: new-post                     # fresh post, welcome guide off, fullscreen off, TT5
  viewport: desktop                   # 1440x900 @2x; also: narrow (1024x768), mobile (390x844)

shots:
  - id: inserter-search
    alt: The block inserter with "image" typed in the search field, showing the Image block as the first result.
    steps:
      - openInserter
      - type: image
    capture:
      target: inserter
      pad: 16

  - id: placeholder
    alt: The empty Image block with Upload, Media Library and Insert from URL buttons.
    steps:
      - insertBlock: core/image
    capture:
      target: selected-block
      pad: 24

  - id: toolbar-replace
    alt: The Image block toolbar with the Replace button highlighted.
    steps:
      - insertBlock: { name: core/image, attributes: { id: "{{media.harbor}}", url: "{{media.harbor.url}}" } }
      - selectBlock: core/image
    capture:
      target: block-toolbar
      include: selected-block         # extend the crop to show the block underneath for context
      pad: 16
      annotate:
        - outline: { button: Replace }

  - id: settings-panel
    alt: The Image block Settings tab with Alternative text, Aspect ratio, Resolution and Dimensions controls.
    steps:
      - insertBlock: { name: core/image, attributes: { id: "{{media.harbor}}", url: "{{media.harbor.url}}" } }
      - selectBlock: core/image
      - openInspector: settings
    capture:
      target: inspector
      annotate:
        - badge: { label: 1, control: Alternative text }
        - badge: { label: 2, control: Aspect ratio }

  - id: insert-from-url
    kind: clip                        # phase 5; same vocabulary, recorded with page.screencast
    alt: Inserting an image from a URL into the Image block.
    steps:
      - insertBlock: core/image
      - click: { button: Insert from URL }
      - type: { text: "{{media.harbor.url}}", pace: human }
      - press: Enter
      - wait: { for: selected-block, state: image-loaded }
    capture:
      target: editor
      duration-max: 15
```

Templating (`{{media.harbor}}`) resolves against the content pack's manifest so specs never hard-code IDs.

Admin and Site Editor shots use the same shape with different scenes:

```yaml
article: manage-plugins
shots:
  - id: installed-plugins
    scene: admin:plugins.php
    alt: The Plugins screen listing active and inactive plugins with the Bulk actions menu.
    capture: { target: admin-content, pad: 0 }

  - id: bulk-actions-open
    scene: admin:plugins.php
    steps:
      - select: { label: Bulk actions, option: Deactivate }
    capture: { target: "#bulk-action-selector-top", pad: 24, annotate: [ { outline: self } ] }
```

```yaml
article: styles-overview
shots:
  - id: typography-panel
    scene: site-editor:styles
    steps:
      - click: { button: Typography }
    capture: { target: site-editor-sidebar }
```

Everything a writer needs is in that vocabulary. The escape hatch:

```yaml
  - id: drag-reorder
    script: ./image-block.drag-reorder.ts   # export default async ({ page, editor, admin, requestUtils, capture }) => { ... }
```

### 4.4 The vocabulary

Scenes (the starting state):

| Scene | Starts at |
|---|---|
| `new-post`, `new-page` | Fresh editor, guides dismissed |
| `post:<slug>`, `page:<slug>` | An existing content-pack item in the editor |
| `site-editor:<route>` | Templates, template parts, patterns, navigation, pages, `styles`, `styles/typography`, a specific template |
| `admin:<path>` | Any wp-admin screen |
| `front:<path>` | The front end, optionally at `viewport: mobile` |
| `customizer:<panel>` | Classic suite only |

Actions, implemented on the Gutenberg utilities so they track UI changes upstream:

`insertBlock`, `selectBlock`, `setContent`, `openInserter`, `openInspector: settings|styles`, `openPanel`,
`openBlockMenu`, `openToolbarDropdown`, `openListView`, `openOptionsMenu`, `openPreferences`, `openCommandPalette`,
`click`, `hover`, `type`, `fill`, `select`, `press`, `scrollTo`, `wait`, `setViewport`, `setPreference`.
`click`/`hover`/`outline`/`badge` accept semantic locator keys (`button:`, `control:`, `menuitem:`, `tab:`, `text:`,
`role:`), which become ARIA-based Playwright locators, with raw `selector:` as a last resort.

Named capture targets, held in one registry so a UI change is fixed in one place:

`editor` (full editor), `canvas`, `selected-block`, `block-toolbar`, `inspector`, `inspector-panel:<name>`,
`document-sidebar`, `inserter`, `list-view`, `top-bar`, `options-menu`, `popover` (the currently open popover),
`modal`, `site-editor-sidebar`, `site-editor-canvas`, `admin-content`, `admin-screen` (with the admin menu),
`front` (viewport), or any selector.

That set covers the audit's archetypes A through L (about 90% of today's images). The remainder is third-party UI
(Spotify's "copy link" menu, a Gmail recovery email), which should not be screenshots in our docs at all, and theme
marketing composites, which are designed graphics rather than captures.

### 4.5 House style and output spec

There is no WordPress docs screenshot spec today. This is the proposed one, borrowing GitHub's limits and the
Playground skill's constants:

| Property | Value |
|---|---|
| Viewport | 1440×900 CSS px (desktop), 1024×768 (narrow), 390×844 (mobile) |
| Scale | 2x (`deviceScaleFactor: 2`); files are retina, Markdown displays at CSS width |
| Theme / scheme | Current default theme, light colour scheme, English, UTC |
| Browser chrome | Never; element or viewport crops only |
| Crop | Named target plus `pad` (default 16 CSS px), optionally `include:` another target for context |
| Framing presets | `plain` (default, just the crop) and `card` (crop on a `#f6f7f7` canvas with 36 px margin, 8 px radius, soft shadow) for full-editor hero images |
| Annotations | Outline: 3 px `#3858e9`, 4 px radius, 4 px gap. Badge: 24 px circle `#3858e9`, white numeral. Dim: 40% white overlay outside the target. Arrows: avoided; use outline or badge instead |
| Masking | Dates, avatars and "Saved" notices are masked or frozen, never left to vary |
| Format | PNG, optimised with oxipng (lossless) and, where needed, pngquant; budget 250 KB per image. WebP is a flag if weight becomes a problem; WordPress.org serves it |
| Naming | `docs/assets/screenshots/<article-slug>/<shot-id>.png`; clips `<shot-id>.mp4` plus `<shot-id>-poster.png` |

Everything in that table is a token in one file so the team can change its mind once, and regenerate.

### 4.6 Determinism and the canonical render

wp-admin uses the system font stack, so macOS and Linux renders differ in every text pixel. Two consequences:

- The **canonical render** runs in `mcr.microsoft.com/playwright:v<pinned>-noble`, both in CI and via
  `npm run shots -- --docker` locally. Images produced any other way are previews and the manifest marks them so.
- The runner compares each new render against the committed image **by pixels, not bytes**, and keeps the old file
  when nothing visible changed. Combined with the frozen clock and reduced motion, a full regeneration against the same
  WordPress version produces an empty git diff. That is the property that keeps repository growth tied to real UI
  changes.

Playwright settings per context: `reducedMotion: 'reduce'`, `colorScheme: 'light'`, `locale: 'en-US'`,
`timezoneId: 'UTC'`, `deviceScaleFactor: 2`; per screenshot: `animations: 'disabled'`, `caret: 'hide'`, the cursor
parked off-canvas before capture (sticky hover states were a real problem for Simple History's pipeline).

Readiness is the main flakiness risk, not rendering. The spike's inserter shots caught the patterns section before
it lazy-loaded, and the sidebar showed "Last edited a second ago". Each scene and target therefore declares an explicit
readiness rule (a locator state, images decoded, no pending REST requests) rather than a fixed timeout, and the
frozen clock removes relative-time text. Two composition details the spike surfaced for the style decision: the 7.1
post editor shows the admin bar even in fullscreen mode (hide it via injected CSS, or keep it; decide once), and a
selected first block's floating toolbar covers the post title, so scenes insert a lead paragraph before the block
under discussion.

Isolation: the content pack is read-only during a run. Shots that need their own content create it (new post, new
template) and the runner deletes what they created and resets preferences and global styles between articles, which
is what Gutenberg's own global setup does. Shots that mutate the site (switch theme, break a plugin) declare
`isolated: true` and get a fresh Playground boot from the snapshot.

### 4.7 Linking shots to the docs

- Markdown stays plain: `![alt](../../../../assets/screenshots/image-block/toolbar-replace.png)`. The wporg-markdown
  importer needs nothing special, and the images map to WordPress.org media on import like any other asset.
- `shots snippet image-block` prints the Markdown lines for every shot in a spec, in order, with alt and caption.
- `shots lint` fails CI when: a spec lacks alt text; a committed image under `docs/assets/screenshots/` is referenced
  by no article; an article references an image under that folder that no spec produces; or the alt text in the
  article differs from the spec (`--fix` rewrites it). The spec is the source of truth for alt text because the
  audit found 10% of today's alt text empty and heavy copy-paste reuse.
- `docs/assets/screenshots/manifest.json` records, per shot: file, article, alt, caption, suite, WordPress version,
  Gutenberg version if any, content-pack hash, spec hash, Playwright image tag, capture time, pixel hash. The preview
  site reads it to show version badges; a release checklist reads it to find anything not regenerated.
- Legacy images under `docs/assets/images/YYYY/MM/` remain untouched and are retired article by article as the
  overhaul rewrites each page.

### 4.8 Regeneration workflow and CI

Commands:

| Command | What it does |
|---|---|
| `shots run [--article x] [--section y] [--suite z] [--docker]` | Boot (or reuse) the environment, render the selected shots, write only pixel-changed files, update the manifest |
| `shots check` | Render to a temp dir, pixel-diff against committed images, write an HTML report (before, after, diff, per shot), exit non-zero above the threshold |
| `shots update` | Accept the results of the last `check` |
| `shots lint` | The checks in 4.7 |
| `shots dev [--article x]` | Start the demo site headed, log in, open the scene, and print the resolved locator for whatever you click, for authoring |
| `shots doctor` | Verify Node, Playwright browsers, Docker (optional), ports, blueprint validity, content-pack licenses |

CI:

1. **Pull requests** that touch `screenshots/**` render the affected articles in Docker and attach the diff report as
   an artifact and a PR comment with before/after thumbnails. `shots lint` runs on every PR.
2. **Scheduled** (weekly, or on each Gutenberg RC) `shots check` against `--wp=nightly`, opening or updating a single
   tracking issue listing changed shots. Early warning only; nothing is committed.
3. **Release**: when core publishes RC1 (for 7.2, late November 2026), a workflow dispatch runs a full `shots run`
   against that RC, opens a PR with the diff report split by section, and the docs team reviews and merges before GA.
   Each changed image is a prompt to re-read the surrounding text.

Throughput: the proof of concept measured 35–100 ms per capture plus 0.3–0.8 s of settling per shot after boot. A thousand shots is under an hour serially and
minutes when CI shards by section with one Playground per shard.

### 4.9 Short clips (later phase)

The same YAML with `kind: clip`, run through `page.screencast` with `showActions({ cursor: 'pointer' })` and
optional `showChapter` cards, typed with human pacing, 5–20 s, no audio. Output webm, converted with ffmpeg (in the
Docker image) to H.264 MP4 plus a poster PNG, embedded as `<video>` like the current docs (the importer strips
iframes but allows `<video>`). The audit found about 125 current videos are single interactions under 30 s; those are
the candidates. The 25 clips over a minute should become step sequences of stills.

## 5. How this intersects the docs overhaul

- **Plan shots per page, not per existing image.** For a block page the recipe is: inserter, placeholder, toolbar
  (plus one or two dropdowns), each inspector panel that matters, front-end result. Five to nine shots instead of
  today's median eight to twenty-one, most of them crops.
- **Embeds**: one parameterised spec (`placeholder`, `pasted-url`, `preview`, `toolbar`) rendered per provider from
  oEmbed fixtures, and most provider pages can share the generic shots. This alone retires roughly 500 images.
- **Classic WordPress** section: served by the classic suite, lower priority, and the per-theme pages may keep their
  existing theme screenshots since those are designed graphics.
- **Third-party UI** (how to copy a link in Spotify): replace with a sentence.
- **Alt text and captions** are written once in the spec by the author rewriting the page, so the overhaul fixes
  the 10% empty alt text as a side effect.

## 6. Roadmap

| Phase | Scope | Exit criterion |
|---|---|---|
| 0 (done) | Research, prior art, audit, proof of concept | This document and `spike/` |
| 1 | Engine MVP: blueprint, minimal content pack, scenes `new-post`/`admin`/`site-editor`/`front`, ten actions, target registry, crop/pad/outline/badge, manifest, lint, Docker canonical run, README | `npm run shots -- --article image-block` produces the full Image block page's images from a clean clone |
| 2 | House style sign-off and the approved content pack (site identity, photos with license manifest, posts, pages, users, comments, menus, patterns); write the "screenshot spec" page for the handbook | Team-approved demo site; style tokens frozen |
| 3 | Block reference coverage as pages are rewritten; embed fixtures; parameterised embed spec | Block section fully regenerable |
| 4 | Admin screens, Site Editor, classic suite; CI: PR diff reports, nightly early warning, RC1 regeneration workflow | 7.2 RC1 regeneration runs end to end |
| 5 | Clips via screencast; ffmpeg pipeline; replace short videos | First ten clips merged |
| 6 | Extract the engine as a standalone package; propose to the Playground and Docs teams | Second consumer onboarded |

Phase 1 is roughly two to three weeks of focused work for one engineer. Phases 3 and 4 are paced by the content
overhaul rather than by engineering.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Locators drift between releases | Build on `@wordpress/e2e-test-utils-playwright`, use ARIA-based locators, keep named targets in one registry; the nightly check surfaces breakage weeks before RC |
| The e2e utilities track Gutenberg trunk and may not match an older pinned core | Pin the utility version alongside the WordPress version in the lockfile; upgrade both at RC1 |
| Playground differs from a typical host (SQLite, no cron, no mail) | Irrelevant for UI shots; Site Health and a few Tools screens use the wp-env fallback or are documented as such |
| Font and anti-aliasing differences across machines | Canonical render only in the pinned Playwright Docker image; local renders are previews |
| Repository growth | Pixel-compare before writing, lossless optimisation, 250 KB budget, far fewer shots; Git LFS is the fallback if `docs/assets/screenshots/` passes a few hundred MB |
| Review fatigue on a full regeneration | Per-section PRs, perceptual thresholds, an HTML report with before/after/diff, and the early-warning job spreading surprises over the cycle |
| Content licensing | Photo Directory CC0 only, recorded per file in `LICENSES.md`, checked by `shots doctor` |
| Writers do not adopt it | YAML authoring, `shots dev` for discovering locators, the snippet generator, and CI doing the canonical work; measured by the share of new pages with specs |
| Network-restricted environments | No run-time network: bundled content, oEmbed fixtures, the `wp-cli` blueprint step avoided (it fetches from playground.wordpress.net, which was blocked on this network) |
| A new default theme in 7.2 | Theme is one blueprint line; the content pack uses patterns, so re-rendering is the plan either way |

## 8. Decisions needed

1. **Placement**: in this repo under `screenshots/` (recommended) or a separate repository from day one.
2. **Framing**: `plain` crops by default with `card` for hero shots (recommended), or `card` everywhere.
3. **Format**: PNG with optimisation (recommended) or WebP.
4. **Canonical render in Docker only** (recommended), accepting that local macOS runs are previews.
5. **Demo site identity**: who designs and approves the fictional site, and whether it should be shared with the
   Playground team's demo content efforts.
6. **Scope target**: aim for roughly 800–1,000 shots across the rewritten docs rather than 2,300.
7. **Engagement**: talk to the Playground team (the `doc-screenshots` skill author) and the Docs team now, so the
   house style becomes the handbook's spec rather than this repo's.

## 9. Reference versions (verified 2026-10-09)

| Component | Version |
|---|---|
| `@wp-playground/cli` | 3.1.57 (weekly releases); Blueprint v1 schema |
| `@playwright/test` | 1.64.0; Docker `mcr.microsoft.com/playwright:v1.64.0-noble` |
| `@wordpress/e2e-test-utils-playwright` | 3.0.0 |
| WordPress | 7.1.3 stable; 7.2 Beta 1 planned Oct 20–22, final Dec 9, 2026; trunk 7.2-alpha |
| Gutenberg plugin | 24.1.0, 24.2.0-rc.1 |
| Default theme | Twenty Twenty-Five 1.5 (re-check at 7.2 Beta 1) |
| `@wordpress/env` | 11.17.0, with an experimental `--runtime=playground` |
| `wp-now` | deprecated in favour of Playground CLI |

## 10. Appendix: proof-of-concept results

Everything below comes from `spike/REPORT.md`, run 2026-10-09 on macOS arm64 with Node 24.21, `@wp-playground/cli`
3.1.57, `@playwright/test` 1.64.0 and `@wordpress/e2e-test-utils-playwright` 3.0.0, WordPress 7.1.3 on PHP 8.3 with
Twenty Twenty-Five.

| Measurement | Result |
|---|---|
| `npm install` | 18 s; `node_modules` 764 MB (Playground wasm builds plus lighthouse via the e2e utils) |
| Chromium download | 36 s, 99 MiB |
| Playground boot, zip cached | 3.8–4.3 s (6.3 s including the WordPress download) |
| First editor load | about 1 s |
| Full-page 2880×1800 screenshot | 61–98 ms |
| Element crop | 35–81 ms |
| Full run, 9 PNGs | 4.9–5.3 s |
| Determinism, same server | 9/9 byte-identical, 0 differing pixels |
| Determinism, after server restart | 9/9 byte-identical |
| 7.1.3 vs nightly 7.2-alpha | every image differs (470 to 22k pixels; toolbar icons changed) |

What worked without workarounds: the blueprint `login` step auto-logs-in any HTTP client on first request, so
Playwright's context arrived authenticated and no login code ran; `setSiteOptions`, `runPHP` for theme activation and
user preferences (welcome guides and the pattern modal off via `wp_persisted_preferences`), `media_handle_sideload`
for bundled images, and `importWxr` of a small hand-written WXR all worked first time; `new Editor({ page })` from the
Gutenberg utilities works standalone without the test runner; the canvas iframe locator and element screenshots
inside it worked; injected CSS produced the highlight outline; `mask` and `caret: 'hide'` worked.

What needed a workaround: version pinning (see 4.2); parking the cursor at (0,0) opened the admin bar menu, so it is
parked bottom-right; the first block's toolbar covered the title; health checks must accept Playground's 302.

What the spike did not cover: Linux or CI, the Docker canonical render, the Site Editor, admin screens, annotations
beyond a single outline, and video quality (Playwright's basic `recordVideo` output was 1x, compressed and cursorless;
the `page.screencast` API verified separately in `research/03-playground-and-playwright.md` is the intended path).
