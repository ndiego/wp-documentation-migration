# Documentation screenshots

Reproducible screenshots for the WordPress documentation. A YAML file per article says what to show; the
toolkit boots WordPress Playground from a committed blueprint (pinned WordPress and PHP, the default theme, an
approved demo site), drives the UI with Playwright, and writes the images into `docs/assets/screenshots/`.
When a WordPress release changes the UI, regenerate and review the diff instead of retaking by hand.

Background: `../notes/screenshot-automation/proposal.md`. Design contract: `ARCHITECTURE.md`.

## Setup

Requirements: Node 22.19+ (24 recommended), about 1 GB of disk for dependencies and the browser. No Docker,
no database, no local WordPress.

The engine (`wp-shots`) comes from the `toolkit/` git submodule
([ndiego/documentation-toolkit](https://github.com/ndiego/documentation-toolkit), pinned at a tag), consumed as
the path dependency `file:../toolkit/wp-shots`.

```sh
git submodule update --init   # once per clone: fetches toolkit/ at the pinned tag
cd toolkit/wp-shots && npm ci && cd ../..
cd screenshots
npm install            # links the engine and downloads Chromium for Playwright
npm run shots -- doctor
```

To work on the engine itself, edit it in the documentation-toolkit repo, tag a release there, then check out
the new tag inside `toolkit/` here and commit the submodule pointer.

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

`run` only writes an image when its pixels changed, so a repeat run against the same WordPress version leaves
git clean. Failures save the page state to `.wp-shots/failures/`.

## Writing a shot

Specs live in `shots/` mirrored to the docs tree, one file per article. The file name does not matter; the
`article` key must be the article's slug from `docs/manifest.json`, and the output goes to
`docs/assets/screenshots/<article>/<shot id>.webp`.

```yaml
article: image-block
defaults:
  scene: new-post
  steps:
    - insertBlock: { name: core/paragraph, attributes: { content: Some lead text. } }
shots:
  - id: toolbar-replace
    alt: The Image block toolbar with the Replace button highlighted.
    steps:
      - insertBlock:
          name: core/image
          attributes: { id: "{{media.hero}}", url: "{{media.hero.url}}", alt: "{{media.hero.alt}}" }
    capture:
      target: block-toolbar
      pad: 24
      annotate:
        - outline: { button: Replace, within: block-toolbar }
```

- **Scenes** start from a known place: `new-post`, `new-page`, `post:<slug>`, `page:<slug>`,
  `admin:plugins.php`, `site-editor`, `site-editor:styles`, `site-editor:template:<theme>//<slug>`, `front`,
  `front:/about/`.
- **Steps** are verbs: `insertBlock`, `selectBlock`, `searchInserter`, `openInspector: content|settings|styles`,
  `openPanel`, `openBlockMenu`, `openToolbarDropdown`, `openListView`, `openOptionsMenu`, `click`, `hover`,
  `type`, `fill`, `select`, `press`, `wait`, `setViewport`, `setPreference`, `scrollTo`, `evaluate`.
  Elements are named the way a reader would: `{ button: Replace }`, `{ control: Alternative text }`,
  `{ menuitem: Edit as HTML }`, `{ tab: Styles }`, `{ text: Settings }`, `{ selector: .css }`.
- **Capture targets** are named regions kept in one registry (`toolkit/wp-shots/src/targets.js`): `editor`,
  `selected-block`, `block-toolbar`, `inspector`, `inspector-panel:<name>`, `inserter`, `list-view`, `top-bar`,
  `popover`, `modal`, `admin-content`, `admin-screen`, `front`, or any selector. `include:` widens the crop,
  `pad:` adds space, `fit: content` trims a tall panel, `frame: card` puts a full-editor shot on a card.
- **Annotations** anchor to elements, never pixels: `outline`, numbered `badge`, `dim`.
- **Templating**: `{{media.<slug>}}`, `{{media.<slug>.url}}`, `{{media.<slug>.alt}}`, `{{post.<slug>}}`,
  `{{page.<slug>}}` resolve against the demo site by slug. The available slugs are the contract in
  `blueprint/README.md`.
- **Alt text** lives in the spec and is the source of truth; `lint --fix` copies it into the Markdown.
- **`defaults.steps`** run before every shot that uses the default scene. A shot that sets another `scene`
  (an admin screen, the front end) does not inherit them.
- **Names match exactly** (`button: Replace` is the whole accessible name, case-sensitive). Add
  `exact: false` for a substring match, for example `{ link: Activate, exact: false }` when the link's
  accessible name is "Activate Akismet".
- **Typos fail fast.** Unknown keys, verbs, scenes, targets and locator keys are rejected when the spec loads
  (with a "did you mean"), so `lint` catches them in CI before anything boots.
- For anything the vocabulary cannot express, `script: ./file.js` replaces `steps` with a function that receives
  `{ page, editor, admin, pageUtils, site, style }`.

Authoring loop: `npm run shots -- dev --article x --shot y` opens a visible browser, runs the scene and steps,
and pauses in the Playwright Inspector, whose "Pick locator" tool shows the role and name to use.

## Determinism and the canonical render

Every run uses a 1440×900 viewport at 2x, light scheme, en-US, UTC, reduced motion, animations disabled,
caret hidden and the pointer parked, against the same pinned WordPress, PHP, theme and demo content. On one
machine, repeat runs are byte-identical.

Fonts differ between macOS and Linux, so local renders are previews. The canonical render runs inside the
pinned Playwright Docker image, locally with `--docker` (needs Docker Desktop) or in CI. The manifest marks each
image `canonical: true|false`. `--docker` shares the host's `~/.wordpress-playground` download cache with the
container, so after the first fetch of a WordPress version a render needs no network for WordPress itself.

## Output

- `docs/assets/screenshots/<article>/<id>.webp`, 2x. Lossless WebP when under 300 KB, lossy quality 90 above
  that (full-editor shots with photos). The manifest records which.
- `docs/assets/screenshots/manifest.json`: per image, the alt text, article, WordPress/PHP/theme versions,
  spec and blueprint hashes, Playwright and Chromium versions, platform, canonical flag and pixel hash.

## Layout

```
screenshots/
  shots.config.js      paths, pinned versions, style overrides
  shots/               YAML specs, mirrored to the docs tree
  blueprint/           Playground blueprint, mu-plugin, demo content pack (contract in blueprint/README.md)
  toolkit/wp-shots/              the `wp-shots` package; knows nothing about this repo (see ARCHITECTURE.md)
  .wp-shots/           logs, failures, check staging, reports (gitignored)
```

## Regeneration at a WordPress release

1. Bump `preferredVersions.wp` in `blueprint/blueprint.json` and `wordpress.version` in `shots.config.js`
   (and `@wordpress/e2e-test-utils-playwright` in `toolkit/wp-shots/package.json` if the editor changed a lot).
2. `npm run shots -- check --docker` (or let the CI workflow do it) and open `.wp-shots/report/index.html`.
3. Review the before/after pairs; a changed image is also a prompt to re-read the article text.
4. `npm run shots -- update` copies the staged images and their manifest entries into place; open a PR. Do not
   follow it with a plain `run`: a local render would overwrite the canonical images with macOS previews.
