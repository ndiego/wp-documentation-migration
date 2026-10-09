# Screenshot audit: WordPress end-user docs (Markdown migration)

Produced 2026-10-09 by a research agent for `../proposal.md`. Scanned the working tree mid-restructure:
**2,309 image refs across 363 .md files** (263 articles with images) and **200 `<video>` embeds in 86 files**.
42 images were viewed directly, spread across every section. Scripts and CSVs (`scan.py`, `classify.py`,
`image_refs.csv`, `images_per_page.csv`, `video_refs.csv`, `visual_sample.csv`) were produced in the session
scratchpad; rerun with `python3 -I scan.py <outdir>` if needed.

## 1. Distribution

| Section (2nd level) | Image refs | Pages | Pages with 0 images |
|---|---|---|---|
| editing-and-design/block-editor | **1,797** | 176 | 15 |
| ↳ blocks/ (embeds 510, theme 490, widgets 138, design 132, media 126, text 123) | 1,526 | — | — |
| ↳ working-with-blocks | 155 | — | — |
| ↳ patterns | 28 | — | — |
| editing-and-design/site-editor | 114 | 11 | 0 |
| using-wordpress/administration-screens | 110 | 42 | 9 |
| classic-wordpress/classic-default-themes | 73 | 23 | 14 |
| editing-and-design/themes | 57 | 14 | 6 |
| classic-wordpress/classic-editor | 33 | 12 | 5 |
| using-wordpress/writing-and-publishing | 33 | 21 | 10 |
| classic-wordpress/widgets-menus-and-customizer | 24 | 6 | 1 |
| using-wordpress/comments, media, maintenance, users, install | 17 / 16 / 12 / 7 / 3 | 31 | 17 |
| overview (where-to-start, faq) | 11 | 13 | 10 |

Top level: editing-and-design 1,968 refs (85%), using-wordpress 198, classic-wordpress 130, overview 11.

Images per page: 100 of 363 pages have none (mostly READMEs). Median 4 overall, 8 across pages with images
(mean 8.8). 115 pages have 10 or more; 10 pages have 20 or more; max 42.

Top 20 pages: styles-overview 42, manage-plugins 31, keyboard-shortcuts-block-editor 28,
page-post-settings-sidebar 25, embeds/mixcloud 22, image-block 21, twenty-twenty-one/README, embeds/spotify,
widgets/search, work-with-blocks 20 each, site-editor/README, file-block, list-block, soundcloud 19 each,
query-loop, cover, reddit, social-icons 18 each, template-editor, buttons-block 17 each.

The 36 embed pages carry 510 refs, 10–22 each, all following the same template.

## 2. Dimensions and quality

Dimensions read from file headers (2,287 refs resolved).

| Width | <400 | 400–599 | 600–799 | 800–1023 | 1024–1279 | 1280–1599 | 1600–1999 | 2000–2559 | 2560–2999 | ≥3000 |
|---|---|---|---|---|---|---|---|---|---|---|
| Count | 242 | **589** | 440 | 249 | 219 | 228 | 124 | 104 | 47 | 45 |

- Heights: <200 px 499; 200–399 498; 400–599 429; 600–999 511; ≥1,000 350. Median size 714×464.
- Aspect ratios: strips (≥3:1, cropped toolbar or single row) 537; wide (1.8–3:1) 676; 4:3 to 16:9 516; roughly
  square 378; tall (<0.75, sidebar panels) 180. **Over half are tight crops of a single UI element.**
- Retina vs 1x: about 55–60% of the sample are 2x Mac captures (many small crops at 2x); about 40% are 1x, mostly
  Windows captures from 2018–2022. 406 images (18%) are 1,400 px or wider. Density is inconsistent within a page.
- WordPress-resized variants: only 13 (`-1024x505`), 3 `-scaled`, 1 `@2x`.
- Browser chrome / window frames / cursors: almost none. No sampled image showed browser chrome. Cursors only in
  GIFs and videos. Partial admin bars about 5% of the time.
- Annotations: **18 of 42 sampled (about 43%)** have red boxes and/or arrows in varying styles (CleanShot, Markup,
  Skitch). Alt text mentions highlight/arrow/pointing in only 108 refs. No numbered callouts in the sample.
- GIFs (36): almost all 10–30 s "how to add block X" demos; a few interactions (undo/redo in widgets, trash,
  restore image, copy URL, Mixcloud player).

Path year is unreliable: files were replaced in place under old paths (`2019/02/view-revisions.jpg` shows the 7.0
revisions UI; `2021/07/site-editor-reset-template.jpg` shows Twenty Twenty-Five). In 150 refs the filename date is
newer than the path year; corrected, about 263 refs are 2026 captures, not 114. Filename WP-version tokens:
6.8 ×44, 7.1 ×28, 7.0 ×6, 4.9 ×18.

Visibly outdated: about 10–15% show pre-6.0 UI (2019 "Most Used" inserter, 2013-era Posts bulk-edit and
Dashboard, 5.x embed placeholders); a further 30–35% are 6.0–6.4 era (old top bar with "Update" and gear icon,
"Create Reusable block", old blue accent, pre-tabbed sidebar). **Roughly 45–50% would need retaking.**

## 3. Shot archetypes

Keyword classifier over alt, caption and filename, adjusted against the visual sample (about 380 unclassifiable).

| Archetype | Est. share (≈n) | Examples |
|---|---|---|
| A. Block toolbar: whole toolbar, or one dropdown/menu open | 25% (~580) | `2019/03/Screenshot-2026-03-02…-1024x505.png`, `2022/04/03-site-title-1.jpg`, `2023/06/edit-as-html.png` |
| B. Block inspector panel: Settings/Styles tab, one panel, panel ⋮ menu, variation picker | 18% (~400) | `2019/03/table-block-styles.png`, `2026/09/typography-settings-edited.png`, `2026/05/query-loop-display-options.png` |
| C. Block in canvas (selected or rendered), incl. color picker popovers | 14% (~330) | `2022/11/Screenshot-2022-11-04…png`, `2023/02/button-drag.png` |
| D. Inserter: quick with search term, full library by category, slash | 5% (~110) | `2026/08/Markup-2026-08-18…png`, `2019/03/Screenshot-2026-08-20…png` |
| E. Placeholder / empty state, embed error states | 3% (~60) | `2020/08/image19.jpg`, shared "URL cannot be embedded" image reused 11× |
| F. Document settings sidebar | 3% (~70) | `2020/11/image3-1.png` |
| G. Top bar / Options menu / Preferences / shortcuts modal / command palette | 2% (~40) | `2023/08/Screen-Shot-on-2023-08-05…png` |
| H. List View | 1–2% (~30) | `2021/07/Screenshot-2026-09-04-at-4.18.46-PM.png` |
| I. Site Editor: templates, parts, navigation, pages, patterns, Styles panels | 6% (~135) | `2021/07/site-editor-reset-template.jpg`, `2023/03/typography-3-6.8.png` |
| J. wp-admin list/settings screens | 6% (~130) | `2021/06/themes-administration-screen.png`, `2026/05/dashboard-settings-connector-api-keys.png` |
| K. Media Library / attachment modal / image editor | 1–2% (~30) | `2023/06/attachment-details-1.png` |
| L. Front-end render of a block or theme section | 4% (~90) | `2019/03/Pullquote-block.jpg` |
| M. Classic Customizer / widgets / classic editor metaboxes | 2% (~40) | `2021/06/customizer-menu-locations.png` |
| N. Theme marketing composites (designed graphics, not captures) | 1–2% (~35) | `2024/11/Patterns.jpg`, `2024/10/tt5-template-preview-laptop.jpg` |
| O. Third-party UI (Spotify/Pinterest copy link, Gmail recovery email, hosting panels) | 2% (~45) | `2022/04/01-spotify_copy_link.jpg` |

Rare: mobile/tablet viewport ~14; before/after pairs ~18; numbered step series 15 pages / 104 images (embed pages).

Block pages follow a predictable recipe: inserter, placeholder, toolbar, each inspector panel, front-end result.

## 4. What demo content the shots need

- Posts and pages: "Hello world!" with a comment, Sample Page, 5–10 posts with featured images, categories, tags
  and spread-out dates (query loop, latest posts, archives, calendar, tag cloud, pagination need volume); several
  revisions on one post.
- Media: about 10 licensed photos (current docs include public-domain Apollo shots and an **iStock-watermarked
  image** in the Reddit embed shot); a gallery set of 3+; an MP3, MP4, PDF; site logo and icon.
- Users: admin plus 2–3 named authors with bios and avatars (Gravatar is a network call; use a local avatar filter).
- Comments: threaded set of 3+, enough for pagination, plus pending and spam items.
- Menus: navigation with submenu, home link, custom links; classic menus need 2 locations.
- Patterns/templates: synced patterns, custom template part, modified templates (for "Reset" shots), custom global
  styles (font sizes, palette, gradients). Font Library fonts come from Google Fonts (network).
- Themes: block shots are mostly Twenty Twenty-Five, some TT3/TT4; classic pages need all 10 classic Twenty-*
  themes plus Twenty Twenty-One with Customizer states.
- Plugins: 4+ installed, some inactive (Plugins screen); a plugin that triggers a fatal error (recovery mode); one
  providing a shortcode and a classic widget (Shortcode and Legacy Widget blocks).
- Site settings: title (visible in templates and admin bar; current shots use "My WordPress Website",
  "WPTESTKITCHEN", "WP62", "catcatgirls.com"), tagline, pretty permalinks, static front page vs posts page,
  discussion/avatar settings, the 7.0 Connectors page.
- Network/oEmbed: 34 embed provider pages (~510 images) need live oEmbed from YouTube, Vimeo, Spotify, SoundCloud,
  Mixcloud, Reddit, X, TikTok, Flickr, Imgur, Issuu, Scribd, SlideShare, TED, Bluesky, Pocket Casts, WordPress.tv,
  VideoPress and others. Several are hard or impossible (Facebook/Instagram removed from core, X needs JS).
  **Recommendation:** pin embeds with a `pre_oembed_result` fixture plugin returning captured HTML or a static
  poster, so shots are deterministic and offline. Third-party "copy link" shots cannot be automated; drop them.

## 5. Videos

- 200 embeds, 199 unique sources, 86 pages; mostly block pages (87), working-with-blocks (28), styles-overview
  (21), default themes (15), site-editor README (11). All `src` remote, but 198 have local copies in
  `docs/assets/videos` (248 files, 1.3 GB). 15 declare a poster; those posters exist.
- Length (from `raw/media.json` and `mdls`): median **23 s**, IQR 13–39 s, max 137 s. ≤10 s: 34; 11–20 s: 56;
  21–30 s: 35; 31–60 s: 48; >60 s: 25.
- Resolution mixed, 960×540 to 3840×2160, many odd Retina window sizes. Sources: QuickTime (22), Kapture (13),
  Loom (2), GitHub uploads (16).
- Content (18 samples): ~27% "add block X via inserter/slash"; ~16% styles tweaks (gradients, typography,
  duotone); the rest interactions (drag-reorder gallery, create synced pattern, nested inserter, command palette,
  List View shortcuts, template switch, Accordion, legacy widget). Long ones are whole-page walkthroughs.
- Automation fit: about 90 videos are ≤20 s and about 125 are ≤30 s single interactions that scripted 5–20 s
  clips could replace. The 25 over 60 s should be split or replaced with step stills.

## 6. Alt text and captions

| Alt quality | Refs |
|---|---|
| Descriptive (4+ words; median 8, max 81) | 1,741 (75%) |
| Short label (≤3 words) | 206 (9%) |
| Generic or filename-like | 120 (5%) |
| Empty | 242 (10%) |

Empty alt runs 24–27% in 2018–19 content and external-host images, 3–6% in 2020–2024, 27% again in 2025. Heavy
reuse (same alt up to 11×). 518 refs (22%) have an italic caption line below, often repeating the alt. 209 files
have generic names (`image19.jpg`), 97 have GitHub-UUID names.

Recommendation: put `alt`, optional `caption` and an `annotations` list in each shot definition; generate Markdown
and semantic filenames from it.

## 7. Recommendations and surprises

Shot vocabulary (about 12 types, parameterised by block, panel, state): block-toolbar, block-inspector, inserter,
block-placeholder, block-canvas, document-sidebar, editor-chrome, list-view, site-editor, admin-screen, frontend,
clip. Shared parameters: 2x, fixed viewport, current default theme, `annotate` from selectors, `crop` selector +
padding; optional before/after and steps wrappers.

Seeding plan: one blueprint with fixed title/tagline and a frozen clock; a WXR content pack; a licensed media pack;
per-page fixtures (broken plugin); an oEmbed fixture plugin; separate blueprints for classic themes and Customizer.

Surprises: path year is not capture date; most images are small crops (good for selector cropping); embed pages
are 22% of images and ~90% one repeated template; iStock-watermarked stock exists in the docs; 22 refs are missing
locally (googleusercontent `.img`); 1.3 GB of local videos already exist; contributors already use Playground
("My WordPress Website", "Hello from WordPress Playground!" appear in current shots).
