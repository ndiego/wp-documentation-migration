# Prior art: automated documentation screenshots and video

Produced 2026-10-09 by a research agent for `../proposal.md`. **[V]** = verified in a primary source (repo file,
README, release notes, official docs); **[I]** = inferred or from secondary sources.

## 1. Detailed examples

### GitLab: RSpec/Capybara "screenshot generators" [V]
- Screenshot specs live in `spec/docs_screenshots/*_docs.rb` and use `DocsScreenshotHelpers`
  (https://docs.gitlab.com/development/documentation/styleguide/,
  https://gitlab.com/gitlab-org/gitlab/-/raw/master/spec/support/helpers/docs_screenshot_helpers.rb).
- Each RSpec `it` description *is* the output path relative to `doc/`:
  ```ruby
  it 'user/packages/container_registry/img/expiration_policy_form' do
    visit project_settings_ci_cd_path(project)
    screenshot_area = find('#js-registry-policies')
    expect(screenshot_area).to have_content 'Expiration interval'
    set_crop_data(screenshot_area, 20)
  end
  ```
- Needs a local GitLab Development Kit. Data from test factories. Window fixed at 1366×1024.
- An `after` hook saves, then crops with MiniMagick to the element's bounding rect plus padding.
  `scripts/docs_screenshots.rb` finds changed PNGs via git, compresses with pngquant, renames to
  `name_v<milestone>.png`. Style guide: ≤1000 px wide, ≤500 px tall, PNG, ≤100 KB, `img/` next to the `.md`.
- Annotations not automated (manual rule: `#EE2604`, 3 pt).
- Regeneration manual, not in CI.
- Outcome: tooling from 2020; only **two** generator files exist today. Issue #14146 (2015, closed 2025) framed the
  staleness problem. **Lesson [I]:** worked, but writers did not adopt it (dev environment + Ruby skills, no CI run).

### TYPO3: `t3docs-screenshots` (declarative JSON, CMS, LTS cadence) [V]
Closest analogue: a CMS docs team regenerating screenshots per major release.
- https://github.com/TYPO3-Documentation/t3docs-screenshots: DDEV project with pre-seeded TYPO3 suites; browser
  driven by Codeception actions. 2021 announcement: "Maintaining screenshots is hard"; ~850 images stale per LTS.
- Each manual has a `screenshots.json`, keyed by suite, entries are lists of actions:
  ```json
  {"suites": {"ExtensionBuilder": {"screenshots": [[
    {"action": "see", "text": "Extension Builder"},
    {"action": "click", "link": "Extension Builder"},
    {"action": "makeScreenshotOfFullPage", "fileName": "ExtensionBuilderFullPage"}
  ]]}}}
  ```
  Product-specific actions: `openPageTreePath`, `makeScreenshotOfRecord`, `makeScreenshotOfField`, `cropScreenshot`.
- Annotations by DOM-drawing actions before capture: `drawBox`, `drawArrow`, `drawBadge`, `clearDrawings`.
- Output to `Images/AutomaticScreenshots`; the runner also writes an RST include snippet per image.
- Review step: shots go to `actual/`, a "screenshots manager" UI compares with originals, a human approves.
- Outcome: 2022 budget proposal to move into Core CI because core changes broke the tool
  (https://talk.typo3.org/t/integrate-the-automatic-screenshot-tool-closely-into-the-typo3-core/4406). Repo
  **archived August 2022**. **Lesson [I]:** a standalone tool outside the product's CI rots; bus factor.

### Django: Selenium screenshot cases (in progress) [V, forum]
- Ticket #35380, PR django#19514, still draft mid-2025. Reuses the Selenium suite:
  `./runtests.py --selenium=… --screenshots`, `@screenshot_cases(["desktop_size","dark",…])`, writes into docs
  `_images` folders under predictable names.
- Problems: OS dark mode leaked in; native `<select>` dropdowns don't render; cropping needed; debate over where
  fixture apps live; suggestion to regenerate only at major releases.

### Zulip: data-seeded Puppeteer captures [V]
- `tools/screenshots/` with `generate-integration-docs-screenshot` and `generate-user-messages-screenshot`.
- Content declared as **JSON data** (channel, topic, users, messages, reactions, fixed dates); script seeds the
  server then captures. `deviceScaleFactor: 2` at 1280×1024, clipped to the message box plus ~5 px padding.
- Lesson: keep seeded data declarative and separate from capture logic; pin timestamps.

### GitHub Docs: manual, but with a precise spec [V]
https://docs.github.com/en/contributing/writing-for-github-docs/creating-screenshots: 750–1000 px wide, 144 dpi
(2x), PNG, ≤250 KB, no GIFs, light theme. Highlights via Snagit, stroke `#BC4C00`, 4 px radius, gap about equal to
stroke. Usernames/avatars replaced with @octocat via DevTools. Images versioned by Liquid conditionals; when
replacing, keep the filename. No automation mentioned.

### Microsoft Learn, Grafana, Sourcegraph, Tailscale, Shopify, Stripe, Atlassian, HashiCorp, MDN, Home Assistant, Obsidian, Notion, Linear
No public automated docs-screenshot pipeline found for any of these [I: absence of public evidence only]. Jenkins
(GSoC 2024 idea, a YAML DSL "understandable by documentation writers") and XWiki GSoC pages are proposals only.

## 2. WordPress-ecosystem prior art

- **Make WordPress Docs guidance [V].**
  https://make.wordpress.org/docs/handbook/get-involved/onboarding-sessions/updating-and-creating-new-screenshots/
  (2024-03-07): "Fresh WordPress install, the default theme and no additional plugins"; Playground or InstaWP
  suggested; use a tool with annotation abilities; when replacing, "cover the same area" and keep "the same
  annotation"; capture "enough of the surroundings"; consider video→GIF for complex flows; uploads go into GitHub
  issue comments. Good-first-issues page adds: site must be in English. **No rule on dimensions, format, DPR,
  browser chrome or annotation colour.** The style guide has no images section.
- **Current process [V].** Documentation-Issue-Tracker has 94 issues with "screenshots" in the title (87 closed),
  e.g. #2503 "[HelpHub][7.1]: Update Layout Settings Page screenshots", linking the Gutenberg PRs that changed the UI.
- **Playground team, `doc-screenshots` agent skill [V].** PR #4124 (merged 2026-07-31), `.agents/skills/doc-screenshots/`.
  Capture at 1440×900, `deviceScaleFactor: 2`; bounding boxes from `locator.boundingBox()` ("Never eyeball
  coordinates"); welcome guides dismissed with an Escape loop. `annotate.py` (Pillow) renders from JSON: `outlines`,
  `arrows`, numbered `cards`, `dim`, optional fake `chrome_bar`; WEBP output. House style: orange `#e8590c` arrows
  with white halos, WordPress-blue `#3858e9` outlines and cards, `#f6f7f7` canvas with 36 px margins. Quality gate:
  legibility at ~860 px and 343 px. **Gap:** capture steps are not committed as reproducible specs.
- **Playground, other [V].** `vanilla-wordpress-screenshot.spec.ts` is skipped unless `REGENERATE_SCREENSHOTS=1`.
  WordPress/blueprints `screenshots.yml` runs `scripts/screenshot-blueprints.ts` on PRs touching a blueprint:
  opens `playground.wordpress.net/?mode=seamless&blueprint-url=…`, `reducedMotion: 'reduce'`, waits for the progress
  bar (5-minute timeout), captures desktop 1920×1080 @1x plus mobile 390×844 @2x JPG, commits only on git changes.
  Long timeouts show hosted-Playground boot is the flakiness source [I]. Playwright E2E guide and programmatic
  `runCLI` are the supported no-Docker path.
- **Simple History plugin [V]** (blog, 2026-05-20): Playground CLI with `--mount` and a blueprint installing a
  mu-plugin (silences notices, remaps avatars); `events.php` seeds curated data, backdated in the DB; one Playwright
  spec per shot, 1600×1130 @2x PNG; `npm run screenshot` boots, captures, tears down. Problems: hover states sticking
  (park cursor, dispatch `mouseleave`), seed order reversed, missing data keys crashing the React UI.
- **Others.** bph/playground-for-screenshots (2025 PoC, Express + Playwright, fixed 20 s waits). Playground issue
  #1254 proposed docs on preparing sites for screenshots/video (manual). **Gutenberg:** only `page.screenshot` usage
  is Storybook visual tests; no docs/release-image tooling found [V]; release videos presumably hand-recorded [I].
  No automated pipeline found for WooCommerce, WordPress.com, Learn WordPress, Jetpack, Yoast or Kinsta.

## 3. Open-source tools

- **shot-scraper** (simonw, ~2.6k stars, v1.12 2026-09) [V]. YAML `multi` shots: `url`, `output`, `width`, `height`,
  `selector(s)`, `padding`, `javascript`, `wait`, `wait_for`, `server`/`sh`/`python` setup hooks; flags `--retina`,
  `--fail`, `--no-clobber`, `-o`. **v1.10 (2026-06) added `shot-scraper video`**: YAML storyboards `scenes:` → `do:`
  actions (`click`, `type`, `fill`, `press`, `scroll`, `pause`, `wait_for`, `screenshot`) plus `cursor: true`; WebM,
  MP4 via ffmpeg. GitHub Actions template caches Playwright, runs oxipng, commits. Closest match to our schema; limits:
  thin actions, no login/seeding concept, no annotations, Python.
- **Doc Detective** (136 stars, active) [V]. Inline Markdown steps (`<!-- step goTo: … -->`, `<!-- step screenshot:
  reference.png -->`). Screenshot schema: `path`, `crop` (selector/text/ARIA/test ID + padding), **`maxVariation`**
  (default 0.05), **`overwrite: "true"|"false"|"aboveVariation"`** (default aboveVariation). Best staleness model
  found. `record`/`stopRecord` for mp4/webm/gif. Runtime is WebdriverIO.
- **Playwright** (1.65 in development) [V]. `page.screenshot` options: `style`/`stylePath` (pierces shadow DOM and
  inner frames), `mask`/`maskColor`, `animations: "disabled"`, `caret: "hide"`, `scale`, `clip`; `toHaveScreenshot`.
  **`page.screencast` (since 1.59):** `start({path, size, fps})`, `showChapter(title, {description})`,
  `showOverlay(html)`, `showActions({cursor, position, style})`.
- **VHS** (charmbracelet, 21k stars) [V]. `.tape` DSL: `Output`, `Set`, `Type`, `Enter`, `Sleep`, `Wait+Screen /re/`,
  `Hide`/`Show`, `Screenshot`; CI action; golden outputs. Good model for a video format.
- Others: Remotion (React-composed video, optional later), capture-website/pageres (single URL), puppeteer-screen-
  recorder (superseded), terminalizer/Kap (less relevant), sharp (Node post-processing/WebP), Chromatic/Storybook
  (component regression only), hosted APIs (unsuitable), `@wordpress/e2e-test-utils-playwright` (natural helper layer).

## 4. Annotation approaches compared
1. **Draw on the DOM before capture** (TYPO3 draw actions, Playwright `style`, screencast overlays): positions follow
   real elements, survive layout changes, reusable in video; risk of disturbing layout, mitigate with fixed overlay layer.
2. **Post-process from captured coordinates** (Playground `annotate.py`, GitLab MiniMagick): raw capture stays clean,
   framing consistent; only maintainable if boxes come from locators at capture time.
3. **Manual tools** (Snagit, Nimbus): GitHub and Make Docs today; redone by hand every release.

Recommendation [I]: declare annotations against locators; render box/badge/blur as injected overlays; sharp post-step
only for framing, padding, encoding.

## 5. Staleness detection seen in the wild
Version in filename (GitLab); pixel diff vs previous run (Doc Detective, TYPO3 manager, Playwright
`toHaveScreenshot`, VHS goldens); commit only on git diff (Blueprints, shot-scraper); human tracking issue per release
(WordPress Docs today). No team found using frontmatter/alt-text "verified with version X" metadata; easy addition.

## 6. Design lessons
1. Writers must author shots without a dev environment (Playground CLI + YAML, `npx` one-liner).
2. Run in CI on a schedule and on each WordPress release/RC; commit only what changed; PR with before/after.
3. Seed declaratively and deterministically (pinned WP, en_US, default theme, no plugins; JSON/PHP fixtures;
   mu-plugin removing notices; fixed dates, avatars, usernames; reducedMotion, animations disabled, caret hidden,
   parked cursor).
4. Name outputs after the doc they serve; keep filenames stable; versions in a sidecar manifest.
5. Any change above a threshold needs human review; a changed image signals the text may need updating.
6. Anchor annotations to locators; keep house style in code; reuse Playground's colours.
7. Define one fixed output spec (≤1440 CSS px, DPR 2, element crops with padding, PNG/WebP, ≤~250 KB, no browser
   chrome, light theme), then optimise.
8. Explicit readiness-based waits; handle welcome guides once in shared helpers.
9. One action language for shots and videos (screencast `showChapter`/`showActions` for narration).
10. Fewer, cropped shots; "same area as before" reduces churn.

## 7. Adopt or reinvent
**Adopt:** Playwright (style, mask, animations, toHaveScreenshot, screencast), Playground CLI + Blueprints,
`@wordpress/e2e-test-utils-playwright`, sharp, ffmpeg, oxipng/pngquant, Playground's annotation style (talk to its author).
**Borrow the schema:** shot-scraper YAML and storyboards; Doc Detective `maxVariation`/`overwrite`; TYPO3 suite+actions
JSON and draw actions; VHS `Hide`/`Show`, `Wait+Screen`.
**Build:** WordPress-specific actions; shot↔doc manifest with version metadata; CI before/after PR workflow.
**Skip:** pageres, capture-website, puppeteer-screen-recorder, hosted capture APIs; Remotion optional later.

## 8. Unresolved
Whether the Docs team has discussed automation on make.wordpress.org/docs (none found); outcome of TYPO3's funding
request; how widely the WP e2e utils are used outside Gutenberg; exact Playground CLI flags for locale and login.
