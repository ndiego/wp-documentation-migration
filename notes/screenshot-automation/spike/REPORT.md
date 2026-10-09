# Spike: headless WordPress Playground + Playwright docs screenshots

**Verdict: yes.** On this Mac (macOS 27.0.1, arm64, Node 24.21.0, npm 11.19.0), `@wp-playground/cli server` boots WordPress 7.1.3 from a blueprint in about 4 s (about 6.3 s when it also has to download WordPress). A plain Node + Playwright script captures 2x block-editor screenshots in about 5 s total, and every PNG was **byte-identical** across 3 runs, including a run after a full server restart. Time spent: about 75 min.

Spike directory: `notes/screenshot-automation/spike/`

## Versions
| Package | Version |
|---|---|
| @wp-playground/cli | 3.1.57 |
| @playwright/test | 1.64.0 (Chrome Headless Shell 156.0.8078.4) |
| @wordpress/e2e-test-utils-playwright | 3.0.0 (works standalone, see below) |
| pngjs / pixelmatch | 7.0.0 / 8.0.0 |
| WordPress | 7.1.3 (latest stable per api.wordpress.org), PHP 8.3, SQLite |
| Default theme | twentytwentyfive (`WP_DEFAULT_THEME`) |

Install: `npm i -D @wp-playground/cli @playwright/test @wordpress/e2e-test-utils-playwright pngjs pixelmatch` took **18 s**. `node_modules` is **764 MB** (mostly the Playground PHP wasm builds and lighthouse, which comes in through e2e-utils). `npx playwright install chromium` took **36 s** (99 MiB, stored in `~/Library/Caches/ms-playwright`). npm warned that `fs-ext-extra-prebuilt` has an install script that was not approved; everything worked anyway.

## Commands
```bash
node gen-images.mjs                 # makes 3 placeholder JPEGs (canvas, original work, no licence issues)
./start-server.sh                   # wraps the command below and measures time to first response
#   ./node_modules/.bin/wp-playground-cli server --blueprint=blueprint.json \
#       --blueprint-may-read-adjacent-files --port=9400
node capture.mjs out/run1           # screenshots + report.json (timings, diagnostics)
node capture.mjs out/run2
node compare.mjs out/run1 out/run2  # sha256 + pixelmatch(threshold 0), writes diff PNGs
node video.mjs && node video-frame.mjs   # optional .webm, plus a frame extracted for review
BLUEPRINT=blueprint-nightly.json ./start-server.sh   # trunk/nightly variant
```
- `--blueprint-may-read-adjacent-files` is required for `{"resource":"bundled"}` (local images and the WXR).
- **State is ephemeral** in `server` mode. Each boot builds a fresh VFS in `$TMPDIR/node-playground-cli-site-<pid>-*`. I proved this with a test post (`marker.mjs create`, then restart, then `check` returned 0). The `start` subcommand does keep sites, and `--reset` wipes them. The CLI does write a **WordPress zip cache to `~/.wordpress-playground/`** (`7.1.3.zip`, `trunk.zip`, `6.9.10.zip`). That is the only thing it writes outside the project.

## Blueprint (`blueprint.json`)
Steps: `login`, then `setSiteOptions` (title "Demo Site", tagline, UTC, pretty permalinks), then `runPHP switch_theme(WP_DEFAULT_THEME)`, then `runPHP update_user_meta(1, $wpdb->get_blog_prefix().'persisted_preferences', [...])`. The preferences set are `core/edit-post.welcomeGuide=false`, `fullscreenMode=true`, `core.welcomeGuide=false`, `enableChoosePatternModal=false` and the edit-site guides. After that come `mkdir` and 3× `writeFile` (bundled JPEGs), then `runPHP media_handle_sideload` ×3 (with alt text), then a post with paragraph/image/heading and an "About Us" page, then `importWxr` (bundled `assets/demo.wxr`, 1 post). All of it worked on the first try. REST confirmed 3 media items, posts "Planning Your First Hiking Trip" and "Imported via WXR…", page "About Us", name and description set. **No welcome guide and no modal appeared**: `update_user_meta` on `wp_persisted_preferences` during the blueprint is enough, so the REST preferences call was not needed. The full JSON is in the file. It is long only because the PHP is inlined; a real toolkit would put that PHP in bundled files.

## Auth (step 4a)
**No login code was needed.** The blueprint `login` step makes Playground auto-login **any** HTTP client on its first request. The response sets `wordpress_logged_in_*` plus `playground_auto_login_already_happened=1` and returns a 302 to the same URL. Playwright's fresh context lands in wp-admin already logged in. The script keeps a fallback that posts the `#loginform` (admin/password), but it never ran. Side effect: a cookieless `curl` always gets a 302, so health checks must accept 302 or keep a cookie jar.

## Capture script (`capture.mjs`), key parts
```js
const context = await browser.newContext({ baseURL, viewport:{width:1440,height:900}, deviceScaleFactor:2,
  reducedMotion:'reduce', colorScheme:'light', locale:'en-US', timezoneId:'UTC' });
const editor = new Editor({ page });            // from @wordpress/e2e-test-utils-playwright, no fixtures needed
await editor.insertBlock({ name:'core/image' }); // editor.canvas = frameLocator('[name="editor-canvas"]')
const settle = async () => { await page.mouse.move(1439,899);   // NOT (0,0): that hovers the admin-bar W menu
  await page.evaluate(()=>document.fonts.ready); await editor.canvas.locator('body').evaluate(()=>document.fonts.ready);
  await page.waitForLoadState('networkidle').catch(()=>{}); await page.waitForTimeout(300); };
const SO = { animations:'disabled', caret:'hide', scale:'device' };
await toolbar.screenshot({ path, ...SO });                         // element crop
await page.evaluate(() => wp.data.dispatch('core/edit-post').openGeneralSidebar('edit-post/block'));
await page.getByRole('button',{name:/block inserter/i}).click(); await page.getByRole('searchbox',{name:/search/i}).fill('image');
// annotation: inject a class, outline the button, then clip around the toolbar with 32px padding
await page.addStyleTag({ content: `.docs-highlight{outline:2px solid #d63638!important;outline-offset:3px!important;box-shadow:0 0 0 6px rgba(214,54,56,.12)!important}` });
await replace.evaluate(el => el.classList.add('docs-highlight'));
await page.screenshot({ ...SO, clip:{ x:tb.x-32, y:tb.y-32, width:tb.width+64, height:tb.height+64+120 } });
await page.screenshot({ ...SO, mask:[editor.canvas.locator('[data-type="core/image"] img')], maskColor:'#dcdcde' });
```
For the "Replace" button to exist, the image needs a real attachment. The script sets `{id,url,alt}` on the block through `wp.data` `updateBlockAttributes`, using the seeded media item that `wp.apiFetch` returns.

## Timings
| Step | Time |
|---|---|
| npm install (5 packages) | 18 s |
| Playwright Chromium download | 36 s |
| Playground boot, WP zip already cached (7.1.3 and trunk, ~8 runs) | 3.8–4.3 s to first response |
| Playground boot, WP not cached (6.9.10 downloaded) | 6.3 s |
| Chromium launch | ~60 ms |
| First load of post-new.php (auto-login redirect, editor JS) | ~1.0 s |
| Editor ready / insert block / open inserter | ~125 / ~105 / ~115–145 ms |
| Per screenshot: full 2880×1800 | 61–98 ms |
| Per screenshot: element crop | 35–81 ms |
| Settle per shot (fonts, networkidle, 300 ms fixed wait), not included in the shot times | ~0.3–0.8 s |
| **Total capture run (9 PNGs)** | **4.85–5.32 s** |
| Video script (scripted part) | 6.9 s, giving a 9.9 s webm |

"Cold" here means the server's cold boot. I did not clear `~/.wordpress-playground` (it is outside the spike dir), so the first-ever cold start that also downloads the CLI isn't measured. The uncached 6.9 boot is the closest stand-in.

## Screenshots (run1; run2/run3 are identical)
All are under `…/spike/out/run1/`:
- `01-editor-image-placeholder.png` (2880×1800): crisp 2x, Manrope theme font renders correctly, no modal or notices. The floating block toolbar covers the line above the block, which is normal WP behaviour.
- `02-block-toolbar.png` (826×96): a clean element crop, good for inline docs.
- `03-block-settings-sidebar.png` (560×1540): clean. The panel's empty lower half is included; the crop should be tightened to the content.
- `04-inserter-search-image.png` (2880×1800): good, with 7 block results. **The patterns section below the results had not loaded yet** (the video shows it appears later). That is a hidden timing dependency.
- `04b-inserter-panel.png` (700×1540): good panel crop, same pattern caveat.
- `05-editor-with-image.png` (2880×1800): the seeded media image loads and the sidebar shows filename and alt text. It looks like real docs.
- `06-annotated-replace.png` (1058×460): the 2px red outline plus halo around "Replace" looks good. A 120 px bottom extension was used to show some context.
- `07-mask-and-caret-hidden.png` (2880×1800): the image is masked in grey, the title was typed and the caret is hidden. The sidebar reads "Last edited a second ago", which is **time-dependent text** that can break determinism.
- `07b-caret-visible.png`: `caret:'initial'`, used for contrast. It still matched byte-for-byte across runs.
- Video: `…/spike/out/video/insert-image-block.webm` (1440×900, 9.9 s, ~1 MB VP8) and frame `out/video/frame-near-end.png`. Usable for a rough preview only: it is fixed at 1x, compressed with visible softness, has no cursor overlay, and recording starts at context creation (blank or loading frames at the start). Docs-quality video would need CDP screencast or ffmpeg post-processing.

General judgment: crisp 2x, correct system and UI fonts, no welcome modal, no update nags, no SQLite notices. One surprise: **the admin bar is visible in the WP 7.1 post editor even though `is-fullscreen-mode` is on** (the fullscreen preference is true; the class is present). This appears to be how 7.x looks now, not something the spike broke, but someone should confirm that docs want it. Hiding it with CSS is easy.

## Determinism
`compare.mjs` (sha256 plus pixelmatch at threshold 0):
- run1 vs run2 (same server): **9/9 byte-identical, 0 diff pixels**.
- run1 vs run3 (server killed and re-booted from the blueprint): **9/9 byte-identical**.
- run1 (7.1.3) vs nightly (7.2-alpha trunk): all 9 differ (470–22k pixels; for example the toolbar icons changed, see `out/nightly/diff/02-block-toolbar.png`). This shows diffing can flag UI drift between WP versions.

## What failed, and the workarounds
1. **`--wp=<x>` is ignored when the blueprint has `preferredVersions`.** The CLI banner prints the flag value, but the blueprint value wins. I read the CLI source: `getEffectiveBlueprint` spreads `...blueprint.preferredVersions` after the CLI args. Worse, with no `preferredVersions` at all, `--wp=7.0`, `6.8`, `nightly`, `beta` and even a zip URL **all resolved to 7.1.3** (CLI 3.1.57, v2 code path). That is either a bug or a quirk. **Workaround:** set the version in the blueprint (`preferredVersions.wp`). `"nightly"` gave 7.2-alpha trunk (from the GitHub master zip, cached as `trunk.zip`), and `"6.9"` gave 6.9.10. Both worked, and capture ran fine on nightly. I did not test `beta` through the blueprint.
2. **The server died when launched through some wrappers.** It was killed whenever the harness ended a shell or when it ran in the agent's backgrounded tasks (exit 144 / signal). That is an environment problem, not Playground. **Workaround:** `start-server.sh` (`nohup` + PID check + curl polling). A real toolkit should start and stop the server from Node itself, or use Playwright's `webServer` config.
3. The first boot-wait loop waited for HTTP 200 on `/wp-login.php` and never saw it, because of the auto-login 302 described above. It now accepts 302.
4. `page.mouse.move(0,0)` to "park" the cursor opened the admin-bar WordPress menu, which then appeared in the screenshot and blocked clicks. The cursor is now parked in the bottom-right corner.
5. The toolbar of a first block floats over the post title. Adding a paragraph first makes the composition cleaner.

## What this means for a full toolkit
**Proven:** reproducible, fast (about 4 s boot, about 70 ms per shot), no Docker, no MySQL. Auth is free. Blueprint seeding (options, theme, prefs, media, WXR) is enough for docs scenes. e2e-utils `Editor` works without the test runner.

**Risks and work still needed:**
- **Version pinning:** don't trust the `--wp` flag. Generate or override blueprints per WP version, and add a check that reads `version-x-y-z` from the body class to confirm which version actually booted. File an upstream issue for the CLI resolver behaviour.
- **Readiness and "settled" detection** is the main source of future flakiness. Lazy pattern loading, popover positioning, image decode, fonts, and "Last edited a second ago" text all need handling. Plan a per-scene `waitFor` vocabulary plus a fixed-time freeze (`page.clock.install()` and setting the post's modified date) rather than ad-hoc timeouts.
- **Determinism is only proven on one machine.** Expect differences across macOS versions, Chromium updates and Linux CI (font hinting and the system UI font, since the editor chrome uses `-apple-system`). Pin the Playwright version, generate on one platform (or in a Linux container with bundled fonts), and use a small pixel threshold instead of exact bytes.
- **Scene authoring model:** each screenshot is "seed state, drive UI, choose crop, annotate". Expect a DSL or config (YAML/JS) for scenes, a reusable crop and padding helper, consistent annotation styles (outline, numbered callouts, arrows), and an element-based crop that trims empty sidebar space.
- **UI drift across WP releases:** selectors like `.block-editor-block-toolbar` and `.interface-complementary-area`, and button names, change. Prefer role/name locators and `wp.data` actions, and run a nightly job against trunk with pixel diffs (shown working here) to catch changes early.
- **Content and assets:** upload paths include the date (`/2026/10/`), and media IDs depend on step order. Neither is visible in these shots, but alt text and filenames do show. Use original or CC0 assets kept in the repo. Placeholders are fine for UI shots; real-looking photos need a licensing record.
- **Admin bar, locales, dark mode, RTL:** these are context options plus blueprint `setSiteLanguage`. They should be cheap to add but are untested.
- **Video** needs its own pipeline (2x, cursor highlight, trimming). Playwright `recordVideo` alone is not docs-grade.
- **Footprint:** 764 MB `node_modules` plus a ~100 MB browser plus a ~37–65 MB zip cache per WP version. That's fine for CI with caching. e2e-utils pulls in lighthouse; we could vendor only `Editor` to slim it down.

## Files
`blueprint.json` (pinned 7.1.3), `blueprint-nightly.json`, `blueprint-wp69.json`, `blueprint-nowp.json` (used to show the `--wp` flag bug), `assets/` (3 JPEGs plus `demo.wxr`), `gen-images.mjs`, `start-server.sh`, `capture.mjs`, `compare.mjs`, `marker.mjs` (persistence test), `probe.mjs` (prefs, theme and version probe), `video.mjs`, `video-frame.mjs`, `out/run1..3`, `out/nightly` (with `diff/`), `out/video/`. The server is stopped; restart it with `./start-server.sh`.
