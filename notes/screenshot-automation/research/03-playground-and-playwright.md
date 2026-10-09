# Technical foundation: Playground CLI, Blueprints, Gutenberg Playwright utilities (as of 2026-10-09)

Produced 2026-10-09 by a research agent for `../proposal.md`. The agent installed the current packages and ran the
stack on macOS: booted Playground CLI with several blueprints, imported the Theme Unit Test WXR, ran
`@wordpress/e2e-test-utils-playwright` with `@playwright/test`, captured 2x screenshots and recorded a webm with a
cursor overlay. "Verified" means it was run; "docs" means read but not run; "uncertain" is flagged.

## Current versions (verified with `npm view` and WordPress.org APIs)

| Thing | Version / date |
|---|---|
| `@wp-playground/cli` | 3.1.57 (2026-10-05). Weekly releases, every Monday. |
| `@wp-playground/blueprints` | 3.1.57. `engines`: node >=24.18, npm >=11.16. CLI docs say Node 20.18+. Tested with Node 24.21. |
| `@wordpress/e2e-test-utils-playwright` | 3.0.0 (2026-10-07). Peers: `@playwright/test >=1`, node >=22.19. |
| `@wordpress/env` | 11.17.0 (2026-10-07) |
| `@playwright/test` | 1.64.0 (2026-10-09). Docker `mcr.microsoft.com/playwright:v1.64.0-noble` exists. |
| `@wp-now/wp-now` | 0.1.75, **deprecated**: "Use @wp-playground/cli instead" |
| WordPress | 7.1.3 latest; 7.0.7 and 6.9.10 still patched; trunk `7.2-alpha-64258` |
| WordPress 7.2 | Beta 1 Oct 20–22, final **Dec 9, 2026** (make/core call for volunteers, 2026-08-12) |
| Gutenberg plugin | 24.1.0 (2026-09-30), 24.2.0-rc.1 (2026-10-07). Two-week cadence; every GitHub release has `gutenberg.zip` |
| Default theme | **Twenty Twenty-Five 1.5**; `WP_DEFAULT_THEME=twentytwentyfive` in 7.1.3 and 7.2 trunk (verified). No twentytwentysix in the theme API. Re-check at 7.2 Beta 1. |

## 1. Playground as the environment

**CLI commands (verified from `--help`):** `start` (auto-detects project, persists to
`~/.wordpress-playground/sites/<cwd-hash>/`, `--login` and `--auto-mount` on by default, `--reset` wipes);
`server` (low-level, for CI; temp storage unless mounted); `run-blueprint`; `build-snapshot --outfile=wordpress.zip`;
`php`.

**Key `server` flags (verified):** `--wp` (default latest), `--php` (8.5…5.2; default 8.3), `--blueprint`,
`--blueprint-may-read-adjacent-files`, `--mount /host:/vfs`, `--mount-before-install`, `--mount-dir`, `--auto-mount`,
`--port` (9400), `--site-url`, `--login`, `--workers`, `--verbosity`, `--define*`, `--skip-sqlite-setup`,
`--phpmyadmin`, `--intl`, `--mode` (Blueprint v2). **`--skip-wordpress-setup` no longer exists**; replaced by
`--wordpress-install-mode` (download-and-install, install-from-existing-files, …, do-not-attempt-installing).

**Pinning (verified):** `--wp=7.1.3`, `--wp=nightly` (gave 7.2-alpha-64258), `--php=8.3`. `--wp=beta` resolved to
the same nightly (no 7.2 beta exists yet; behaviour once one ships is uncertain). For a specific beta/RC a zip URL
such as `https://wordpress.org/wordpress-7.2-beta1.zip` is the safer bet (untested).

**Startup (verified, macOS, warm cache):** plain boot ~9 s; nightly + Gutenberg zip 12–19 s; Gutenberg + full
Theme Unit Test WXR import with media download (57 posts, 37 media, thumbnails) ~45 s. `build-snapshot` or a
persisted site dir avoids redoing that per run.

**Headless and CI:** pure Node + WebAssembly, no browser, no Docker. Docs recommend `server` for CI and offer a
programmatic `runCLI`. Verified headless on macOS; not run in GitHub Actions, but nothing OS-specific apart from
Windows mount-path quirks.

**Blueprints.** v1 is the stable default: `landingPage`, `preferredVersions`, `features`, `constants`, `plugins`,
`siteOptions`, `login`, `steps`, `extraLibraries`. v1 steps in the 3.1.57 schema: activatePlugin, activateTheme, cp,
defineWpConfigConsts, defineSiteUrl, enableMultisite, importWxr, importThemeStarterContent, importWordPressFiles,
installPlugin, installTheme, login, mkdir, mv, resetData, request, rm, rmdir, runPHP, runPHPWithOptions,
runWpInstallationWizard, runSql, setSiteOptions, unzip, updateUserMeta, writeFile, writeFiles, wp-cli,
setSiteLanguage. Resources: `wordpress.org/plugins`, `wordpress.org/themes` (slug only), `url`, `bundled`,
`git:directory`, `literal`, `vfs`, `zip`. **v2** (`"version": 2`) ships in the same schema with declarative keys
(`wordpressVersion`, `phpVersion`, `activeTheme`, `plugins` with `slug@version`, `media`, `content`, `fonts`,
`users`, `siteLanguage`, `additionalStepsAfterExecution`); no 2026 announcement that it is default or stable. Treat
as experimental; build on v1.

**Installing Gutenberg:** latest via `{"step":"installPlugin","pluginData":{"resource":"wordpress.org/plugins","slug":"gutenberg"}}`
(verified); specific version via `{"resource":"url","url":"https://downloads.wordpress.org/plugin/gutenberg.24.0.0.zip"}`
(verified) or the GitHub release asset `…/releases/download/v24.2.0-rc.1/gutenberg.zip`; trunk/PR builds via
Playground's `plugin-proxy.php` (depends on playground.wordpress.net; trunk variant unconfirmed).

**Demo content import:** `importWxr` with `url` or `bundled` works; with `features.networking: true` attachments are
downloaded and thumbnails generated (verified). For a deterministic site prefer `importWordPressFiles` (a snapshot
zip) or `bundled` media plus `runPHP` calling `media_handle_sideload`, avoiding network at run time.

**Gotchas found:**
1. PHP version silently follows the blueprint: with no `preferredVersions`, `PHP_VERSION` was 8.5.10 although the
   banner said 8.3. Always set `preferredVersions` and pass `--php`.
2. Networking works (verified): `wp_remote_get` to api.wordpress.org returned 200.
3. The `wp-cli` step downloads `wp-cli.phar` from playground.wordpress.net, which returned 403 on this network, so
   the step failed. Prefer `runPHP`/`setSiteOptions` or bundle wp-cli.phar.
4. Image processing works (verified): GD 2.3.3 (JPEG, PNG, WebP, AVIF, FreeType), Imagick, exif; WordPress chose
   `WP_Image_Editor_GD`; thumbnails generated.
5. Database is SQLite via the integration plugin; fine for UI shots; Site Health will differ from a typical host.
6. Persistence: `server` uses temp storage (lost on stop, cleaned after 2 days); `start` persists per directory.
7. Each new client's first request gets a 302 to the same URL while Playground sets cookies; curl needs `-L` and a
   cookie jar; Playwright is fine.
8. The "latest" build ships only TT5, TT4, TT3; nightly includes all bundled themes.
9. Not tested: cron, mail, large WXR performance. Neither matters for screenshots.

**Alternatives:** wp-env 11.17 has experimental `--runtime=playground` (Docker still default); the e2e utils default
to `WP_BASE_URL=http://localhost:8889` with admin/password (wp-env's default), so supporting both is a base-URL and
start-command switch. wp-now is deprecated. Studio and Local are GUI apps, poor for clone-and-run and CI.

**Recommendation:** Playground CLI `server` driven by a committed v1 blueprint; optional wp-env fallback behind a
small wrapper exporting `WP_BASE_URL`.

## 2. Driving the editor with Playwright

**`@wordpress/e2e-test-utils-playwright` 3.0.0 works standalone with `@playwright/test` 1.64 (verified).** Exports
`test`/`expect` fixtures (`admin`, `editor`, `pageUtils`, `requestUtils`) and classes. Reads `WP_BASE_URL`,
`WP_USERNAME`/`WP_PASSWORD` (default admin/password, matching Playground), `STORAGE_STATE_PATH`. Global setup calls
`requestUtils.setupRest()`, which logs in via wp-login.php, saves storage state and fetches a REST nonce. README
claims WP 5.6+/Gutenberg 9.2+, but it tracks Gutenberg trunk (`visitSiteEditor` has a "site-editor-v2" branch).
Pin it.

**Smoke test (verified):** global setup, `createNewPost`, two `insertBlock` calls (paragraph, image with an imported
media ID), `openDocumentSettingsSidebar`, a 2880×1800 screenshot, an element screenshot of a block inside the canvas
iframe, `visitSiteEditor` and another screenshot: 8.7 s total.

**Utility surface (from 3.0.0 types):**
- Admin: `createNewPost` (sets `core/edit-post` `welcomeGuide:false`, `fullscreenMode:false`), `editPost`,
  `visitAdminPage`, `visitSiteEditor` (sets `core/edit-site` `welcomeGuide*` false), `waitForSiteEditor`.
- Editor: `canvas` (FrameLocator for `iframe[name="editor-canvas"]`), `insertBlock`, `setContent`, `getBlocks`,
  `selectBlocks`, `showBlockToolbar`, `setIsFixedToolbar`, `openDocumentSettingsSidebar`, `clickBlockToolbarButton`,
  `clickBlockOptionsMenuItem`, `transformBlockTo`, `publishPost`, `saveDraft`, `saveSiteEditorEntities`,
  `switchToLegacyCanvas`, `setPreferences(scope, {...})`.
- RequestUtils: `createPost`, `deleteAllPosts`, `createPage`, `deleteAllPages`, `uploadMedia`, `listMedia`,
  `deleteAllMedia`, `activateTheme`, `activatePlugin`, `deactivatePlugin`, `getSiteSettings`, `updateSiteSettings`,
  `createTemplate`, `deleteAllTemplates`, `resetThemeGlobalStyles`, `createNavigationMenu`, `createComment`,
  `createUser`, `resetPreferences`, `setPreferences` (persisted via `/wp/v2/users/me` meta), `setGutenbergExperiments`,
  `rest`, `batchRest`.
- PageUtils: `pressKeys('primary+a')`, `setBrowserViewport`, `dragFiles`, `emulateNetworkConditions`.

**Gutenberg's determinism settings** (`packages/scripts/config/playwright.config.js`, `test/e2e/playwright.config.ts`):
viewport 960×700, `locale:'en-US'`, `reducedMotion:'reduce'`, `strictSelectors:true`, `workers:1`, storageState from
global setup; global setup activates a theme, deletes posts/pages/blocks, `resetPreferences()`; a test plugin disables
CSS animations. For docs add `deviceScaleFactor: 2`, `timezoneId: 'UTC'`, `colorScheme: 'light'`, fixed viewport
(1440×900 worked well), a mu-plugin disabling animations and fixing the date. Preference keys: `core/edit-post`
`welcomeGuide`, `fullscreenMode`; `core/edit-site` `welcomeGuide*`; `core` for shared ones (`fixedToolbar`,
`showListViewByDefault`, `distractionFree`, `editorMode`; `core`-scope keys not individually verified).

**Iframed canvas (verified):** one `iframe[name="editor-canvas"]`; `editor.canvas.locator(...).screenshot()` works.
For callouts spanning chrome and canvas, `page.screenshot` with a clip computed from both bounding boxes (frame
coordinates are page-relative). The `style` option applies to the main page only; inject CSS into the iframe with
`frame.addStyleTag`.

**Screenshot options:** `page.screenshot({clip, fullPage, mask, maskColor, style, animations:'disabled',
caret:'hide', scale:'css'|'device', omitBackground, type})`, same on locators. `scale:'css'` gives 1x output from a
2x context (verified); default `device` gave 2880×1800. Mask dates, avatars, "Saved" notices.

**Fonts:** wp-admin uses the system-ui stack (SF on macOS, Cantarell/DejaVu on Linux), so output differs across
OSes. Canonical captures only inside `mcr.microsoft.com/playwright:v1.64.0-noble`, locally via Docker and in CI.
Optionally override system-ui with a bundled font via `@font-face`.

**Video (verified):** Playwright 1.59+ `page.screencast`: `start({path, size, fps, quality, onFrame})`,
`showActions({cursor:'pointer'|'none', position, duration, fontSize})` (cursor added in 1.61),
`showChapter(title, {description, duration})`, `showOverlay(html)`, `stop()`. Recorded an 8.6 s 1440×900 webm with
an animated pointer, "Press Enter" action labels and a chapter card. Clearly the path for 5–20 s clips, ahead of
`recordVideo` (no cursor, test-scoped) or raw CDP screencast + ffmpeg. Output webm at CSS-pixel size; convert with
ffmpeg (not installed on this machine). Use `pressSequentially`/typing `delay` for human pacing.

## 3. Demo content
- Theme Unit Test data (WPTT/theme-test-data) imports fine but looks like fixtures ("Template: Sticky") and the repo
  has **no license file**. Edge cases only.
- WordPress Photo Directory: CC0, no attribution required, cannot claim authorship; spot-check each photo. Best source.
- Openverse: mixed licenses; filter to CC0/PDM.
- Twenty Twenty-Five: GPL-2.0+ with bundled images; patterns and style variations make professional pages;
  `importThemeStarterContent` where applicable.
- No Gutenberg "welcome demo" content set found.
- Recommendation: a small, team-approved content pack committed to the repo (WXR or blocks-in-PHP seed plus 15–25
  Photo Directory images bundled locally), imported via `bundled`, no run-time network; record source URLs.

## 4. Version strategy
- Core: ~3 majors a year; next 7.2 on Dec 9, 2026 (Beta 1 Oct 20). Minors rarely change UI. Regenerate at RC1
  (late November), publish at GA.
- Gutenberg: every two weeks; reaches core only via the major. Target core's bundled editor; run a scheduled job
  against Gutenberg RC or nightly core as early warning.
- Detecting change: `expect(page).toHaveScreenshot({maxDiffPixelRatio, threshold})` or pixelmatch against committed
  images, in a PR report. Only works with the same Docker image, DPR and content. Pin `--wp`, `--php`, Gutenberg
  version, npm lockfile, Playwright image tag; record in the manifest.

## Recommended stack
- Environment: `@wp-playground/cli@3.1.57`, `server --wp=7.1.3 --php=8.3 --port=9400 --blueprint=blueprint.json
  --blueprint-may-read-adjacent-files`; Blueprint v1 with `preferredVersions` pinned and networking off at run time;
  bundled content pack; `setSiteOptions` (blogname, timezone UTC, date format); TT5; mu-plugin via `writeFile`
  (animations off, frozen clock, nags hidden). Optionally `build-snapshot` once and boot from `importWordPressFiles`.
- Fallback: wp-env (Docker) selected via `WP_BASE_URL`.
- Driver: `@playwright/test@1.64.0` + `@wordpress/e2e-test-utils-playwright@3.0.0`, Gutenberg-style global setup;
  context 1440×900, DPR 2, reducedMotion, en-US, UTC, light; screenshots with `animations:'disabled'`, `caret:'hide'`,
  `mask`.
- Canonical rendering inside `mcr.microsoft.com/playwright:v1.64.0-noble`, locally and in GitHub Actions.
- Video: `page.screencast` with `showActions({cursor:'pointer'})` and `showChapter`, then ffmpeg to mp4.
- Regression: scheduled run against `--wp=nightly` (and Gutenberg RC) with `toHaveScreenshot` diffs; full
  regeneration at each core RC1.

**Not verified:** GitHub Actions Linux run; wp-env's playground runtime; `--wp` with an explicit beta zip; Blueprint
v2 execution; cron/mail; `core`-scope preference keys in 3.0.0; whether a new default theme lands in 7.2.
