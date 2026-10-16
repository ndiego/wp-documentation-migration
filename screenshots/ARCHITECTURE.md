# Architecture (project side)

Phase 1 of the toolkit proposed in `../notes/screenshot-automation/proposal.md`. The engine's architecture, module
map, spec format, step verbs and named targets are documented with the engine in
`../toolkit/packages/screenshots/ARCHITECTURE.md`. This file covers only what this repository owns.

## Two layers

```
screenshots/                      the PROJECT: this repo's shots, blueprint, content and config
  shots.config.js                 project config consumed by the engine
  blueprint/                      Playground blueprint + mu-plugin + demo content pack (see blueprint/README.md)
  shots/                          YAML shot specs, mirrored to the docs tree
../toolkit/packages/screenshots/  the ENGINE: @wporg-docs/screenshots, from the documentation-toolkit submodule
                                  pinned at a tag, consumed as the path dependency file:../toolkit/packages/screenshots
```

The engine knows nothing about this repository. It receives a config object (directories, blueprint path,
WordPress version, style tokens) and does the rest. Once the package is on npm, this project depends on it from
npm instead of the path.

Rules that keep that true:

- Nothing in the engine imports from outside it, reads `../docs`, or assumes article slugs look like ours.
- Project-specific facts (output dir, docs dir, manifest path, blueprint path, versions, viewports, style tokens)
  come from `shots.config.js`.
- Project-specific content keys (`{{media.harbor}}`) are resolved against the running site by slug, not against
  files in this repo.

## Environment contract (`blueprint/`)

See `blueprint/README.md`. The engine only needs: a blueprint path, the port, the admin credentials
(`admin` / `password`), and that the blueprint's `login` step is present so the browser arrives authenticated.
Content keys are resolved by slug through the REST API, so the demo content pack may be replaced wholesale as long
as the slugs listed in `blueprint/README.md` keep existing. The mu-plugin adds `wp_screenshots` to `GET /wp-json/`
so the engine can assert the booted versions.

## Output

- `docs/assets/screenshots/<article>/<id>.webp`, lossless under 300 KB and lossy quality 90 above, as the engine
  decides; the manifest records the encoding.
- `docs/assets/screenshots/manifest.json`, written by the engine (format in its ARCHITECTURE.md).

## CI

`.github/workflows/screenshots.yml` lints on pull requests and performs the canonical render (inside the pinned
Playwright image, `WP_SCREENSHOTS_CANONICAL=1`) on demand and weekly. Lint installs the engine at the toolkit root
(`npm ci` in `toolkit/`) and the project in `screenshots/`.
