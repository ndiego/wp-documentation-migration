# Documentation screenshots

Reproducible screenshots for the WordPress documentation. A YAML file per article says what to show; the engine
boots WordPress Playground from the committed blueprint (pinned WordPress and PHP, the default theme, an approved
demo site), drives the UI with Playwright, and writes the images into `docs/assets/screenshots/`. When a WordPress
release changes the UI, regenerate and review the diff instead of retaking by hand.

This directory is the **project**: `shots.config.js`, the blueprint and demo content, and the YAML specs. The
**engine** is `@wporg-docs/screenshots` from the `toolkit/` submodule
([ndiego/documentation-toolkit](https://github.com/ndiego/documentation-toolkit), pinned at a tag). The engine's
own docs cover everything that is not specific to this repo:

- `../toolkit/packages/screenshots/README.md`: commands, configuration, the spec format (scenes, steps, locator
  keys, capture targets, annotations, templating), determinism, output.
- `../toolkit/packages/screenshots/ARCHITECTURE.md`: the contract between engine and project, module map, the
  full step-verb and target tables.

Background: `../notes/screenshot-automation/proposal.md`. Project-side contract: `ARCHITECTURE.md` here.

## Setup

Requirements: Node 22.19+ (24 recommended), about 1 GB of disk for dependencies and the browser. No Docker, no
database, no local WordPress.

```sh
git submodule update --init   # once per clone: fetches toolkit/ at the pinned tag
( cd toolkit && npm ci )      # the engine's dependencies install at the toolkit root (it is an npm workspace)
cd screenshots
npm install                   # links the engine and downloads Chromium for Playwright
npm run shots -- doctor
```

To work on the engine itself, edit it in the documentation-toolkit repo, tag a release there, then check out the
new tag inside `toolkit/` here and commit the submodule pointer.

## Everyday commands

```sh
npm run shots -- run --article image-block     # render one article's shots
npm run shots -- run --section editing-and-design/block-editor/blocks   # a whole section
npm run shots -- run                            # everything
npm run shots -- check                          # render to a staging dir, diff against committed images, HTML report
npm run shots -- update                         # accept what the last check staged
npm run shots -- lint                           # specs ↔ images ↔ Markdown cross-checks (CI runs this)
npm run shots -- snippet --article image-block --from ../docs/editing-and-design/block-editor/blocks/media-blocks/image-block.md
npm run shots -- dev --article image-block --shot toolbar   # headed browser, pauses in the Playwright Inspector
npm run shots -- list
npm run shots -- vocab                          # scenes, step verbs and capture targets
```

`run` only writes an image when its pixels changed, so a repeat run against the same WordPress version leaves git
clean. Failures save the page state to `.wp-screenshots/failures/`.

## What is specific to this repo

- Specs live in `shots/` mirrored to the docs tree, one file per article. The `article` key must be the article's
  slug from `docs/manifest.json`; output goes to `docs/assets/screenshots/<article>/<shot id>.webp`.
- `{{media.<slug>}}`, `{{post.<slug>}}` and `{{page.<slug>}}` resolve against the demo site by slug. The available
  slugs are the contract in `blueprint/README.md`; a replacement demo site must keep them.
- The blueprint pins WordPress 7.1.3 and PHP 8.3 and installs the demo mu-plugin, which also exposes
  `wp_screenshots: { wordpress, php, theme, content }` on `GET /wp-json/` for the engine's version assertion.

## Determinism and the canonical render

Fonts differ between macOS and Linux, so local renders are previews. The canonical render runs inside the pinned
Playwright Docker image, locally with `--docker` (needs Docker Desktop) or in the CI workflow
(`.github/workflows/screenshots.yml`). The manifest marks each image `canonical: true|false`. Keep `dockerImage` in
`shots.config.js`, `@playwright/test` in the engine, and the CI image at the same version.

## Layout

```
screenshots/
  shots.config.js      paths, pinned versions, style overrides
  shots/               YAML specs, mirrored to the docs tree
  blueprint/           Playground blueprint, mu-plugin, demo content pack (contract in blueprint/README.md)
  .wp-screenshots/     logs, failures, check staging, reports (gitignored)
../toolkit/packages/screenshots/   the engine; knows nothing about this repo
```

## Regeneration at a WordPress release

1. Bump `preferredVersions.wp` in `blueprint/blueprint.json` and `wordpress.version` in `shots.config.js`
   (and `@wordpress/e2e-test-utils-playwright` in the engine if the editor changed a lot).
2. `npm run shots -- check --docker` (or let the CI workflow do it) and open `.wp-screenshots/report/index.html`.
3. Review the before/after pairs; a changed image is also a prompt to re-read the article text.
4. `npm run shots -- update` copies the staged images and their manifest entries into place; open a PR. Do not
   follow it with a plain `run`: a local render would overwrite the canonical images with macOS previews.
