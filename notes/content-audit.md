# HelpHub content audit

Generated 2026-10-07 from `raw/` (REST API `content.rendered`) with `scripts/audit.py`. The raw
numbers are in `notes/audit-stats.json`. Link and redirect data comes from `scripts/resolve_redirects.py`
(`data/redirects.json`), and asset numbers come from the converter (`docs/assets/images-manifest.json`).

**Scope:** the 321 articles (`helphub_article`) and the 7 static pages. The 935 release pages are
described in one paragraph at the end. They are out of scope.

Counts are written as "occurrences / articles". Example slugs are in parentheses.

## Headline numbers

| | |
|---|---|
| Articles | 321 (all `publish`); 317 are in a parent+child category pair, 4 have a single category |
| Static pages | 7. The 4 landing pages have empty content. The front page (`support-forums`) is a layout page. `site-health` and `update-php` are real content |
| Headings | 3,838 (h2 1,911, h3 1,529, h4 385, h5 13, no h1, no h6). 1,058 have an explicit `id` |
| `<img>` | 2,309 / 262 articles, 2,241 unique `src` URLs |
| Self-hosted `<video>` | 202 / 87 articles (.mp4/.mov in `/documentation/files/`) |
| VideoPress | 57 iframes / 38 articles (35 `wp-block-jetpack-videopress` blocks, 21 VideoPress oEmbeds, 4 legacy `video.wordpress.com`) |
| YouTube | 0 embeds (2 plain links only) |
| Callout boxes | ~870: 866 `p.has-background` / 170 articles, 5 `wporg/notice`, 8 `div.callout` |
| Tables | 80 / 14 articles. 1 uses colspan, 26 have no header row, 9 have lists or `<br>` in cells |
| Internal article links | 2,529 rewritten; 2,012 absolute `/documentation/article/*` + 584 relative `/support/article/*` + 44 absolute legacy `/support/article/*` |
| Media library | 7,201 items, of which **2,338 (32%)** are referenced by article or page content (including VideoPress originals and posters matched by guid) |

## 1. HTML elements and Gutenberg blocks

| Element / class | Count | Notes and examples |
|---|---|---|
| `p.wp-block-paragraph` | 8,734 / 321 | |
| `wp-block-heading` | 3,838 / 315 | 1,058 have an `id`. Live anchors also come from the TOC (`sanitize_title`, see §4) |
| `ul`/`ol` `wp-block-list` | 2,978 / 305 | Nested once 957× (191 articles), twice 9× (`reset-your-password`, `media-text-block`, `submit-your-block-pattern-to-the-directory`) |
| `wp-block-image` | 2,280 / 261 | `is-resized` 1,051, `aligncenter` 1,271, `alignright` 51 |
| `figcaption` | 618 / 143 | 546 on images, 57 on videos, 7 on galleries (`adding-a-new-block`, `administration-screens`) |
| `wp-block-group` | 228 / 190 | Mostly the **Changelog** box: `div.changelog` 184 articles, `id="changelog"` 187 |
| `wp-block-video` | 218 / 95 | `<video controls src=… style="aspect-ratio">` (`image-block`, `accordion-block`) |
| `wp-block-jetpack-videopress` | 35 / 21 | iframe + inline `<script>` (`zoom-out-view`, `colors-settings-overview`, `block-pattern`) |
| `wp-block-embed` | 24 / 20 | VideoPress 21, X 1 (`twitter-embed`), Bluesky 1 (`bluesky-embed`), WordPress.tv 1 (`difference-between-wordpress-org-and-wordpress-com`) |
| `wp-block-preformatted` / `wp-block-code` | 84 / 26 and 26 / 9 | 117 `<pre>` total. Language hints only from SyntaxHighlighter `brush: php` (4 articles) and `language-php` (2): `faq-installation`, `twenty-sixteen`, `roles-and-capabilities` |
| `code` (inline) | 1,150 / 129 | 10 have a link inside `<code>` (`post-status`, `get-started-with-wordpress`) |
| `kbd` | 66 / 43 | Block keyboard shortcuts (`archives-block`, `adding-a-new-block`) |
| `wp-block-columns` / `column` | 40 / 20 and 81 | Layout only (`audio-block`, `blocks-list`, `border-settings-overview`) |
| `wp-block-media-text` | 14 / 4 | `media-text-block`, `media-add-new-screen`, `more-text-editing-overview` |
| `wp-block-gallery` | 26 / 22 | Nested `figure.wp-block-image` (`twenty-twenty-four`, `cloudup-embed`). Jetpack tiled gallery in 2 (`pinterest-embed`, `wolfram-embed`). Classic `[gallery]` output in 1 (`work-with-themes`) |
| `wp-block-quote` / `blockquote` | 9 / 5 and 11 / 7 | `faq-installation`, `first-steps-with-wordpress-classic` |
| `details`/`summary` | 10 / 2 | `twenty-twenty-one` (raw HTML), `understand-comment-spam` (9 `wp-block-details`) |
| `wp-block-spacer` | 51 / 22 | Dropped |
| `wp-lightbox-container` + `button.lightbox-trigger` + `svg` | 14 / 3 | Image lightbox chrome (`colors-settings-overview`, `template-editor`, `typography-settings-overview`) |
| `script` | 59 / 40 | 56 VideoPress player JS, 1 Bluesky, 1 Twitter |
| MathML `<math>` | 1 / 1 | `math-block`. Has a TeX `annotation` |
| `mark` | 2 / 2 | `site-editor-pages`, `supported-versions` |
| `sup`/`sub`, `del`, `hr` | rare | `hr` in 4 |
| HTML comments | 0 | Block delimiters are already stripped in `content.rendered` |
| Shortcodes left unrendered | none real | Literal examples only: `[gallery]` ×10 (`the-wordpress-gallery-classic-editor`), `[audio]` ×2 (`audio-shortcode`). `[block]`, `[s]`, `[slug]`, `[domain]` are ordinary prose in brackets. **`video-shortcode` is a content bug**: its examples were rendered by WordPress into real `<video>` players with fake `src` such as `http://video-source.mp4?_=3` |
| `<form>`, footnotes, RTL | 0 in articles | The front page has a search `<form>`. No `dir="rtl"` content |

### Inline styles

There are 2,235 `style` attributes. Almost all are presentational and are dropped:

- `img` width/height and `aspect-ratio`: 1,035 / 163. Only meaningful for the 40 deliberately tiny `is-resized` images (≤240 px), which the converter keeps as `<img width>`.
- `p` `background-color`: 837 / 164. This is the callout colour (see §2).
- `video` `aspect-ratio`: 197.
- One table uses `text-align` per cell (`customize-date-and-time-format`).
- `span style="color: initial;, sans-serif"`: paste artefacts, 35 spans / 21 articles (`site-editor`, `comment-moderation`).

## 2. Callouts and notes

| Pattern | Count | Mapping in the converter |
|---|---|---|
| `p.has-background` `#e5f5fa` | 773 | callout-info (the house style for "Learn more…" and "Note:" boxes) |
| `p.has-background` `#e5f4fa` | 40 | callout-info |
| `has-very-light-gray-background-color` (p) | 16 | callout-info (`dashboard-updates-screen`) |
| `has-deep-blueberry`, `pale-cyan-blue`, `#eaf3f9`, `#e7eff4`, `#e9ebee`, … | ~20 | callout-info |
| `has-lemon-3` / `has-pomegrade-3` | 1 / 2 | callout-warning / callout-alert |
| `wp-block-wporg-notice is-info-notice` / `is-tip-notice` | 4 / 1 | callout-info / callout-tip (`page-post-settings-sidebar`, `posts-tags-screen`) |
| `div.callout.callout-info` (inline style) | 8 / 7 | callout-info (`query-total-block`, `archive-title-block`, `site-logo-block`) |
| Colour swatch paragraphs in default-theme articles (`#21759b`, `#28303d`, …) | 23 | **Not callouts.** Background dropped, text kept (`twenty-twelve`, `twenty-twenty-one`, `twenty-twenty-two`) |
| Plain paragraphs starting "Note:" / "Important:" / "Warning:" without a box | 108 / 8 / 3 | Left as paragraphs |

About a third of the boxes contain only a single "Learn more about X" link, for example
"[Detailed instructions on adding blocks]". This applies to almost every block article.

## 3. Images

- **2,309** `<img>` in 262 articles, with **2,241** unique `src` values. After picking the unsized original and normalising Photon URLs there are **2,243** unique image files, plus 64 VideoPress posters.
- Hosts: wordpress.org 2,095 `src` (2,165 under `/documentation/files/`, 16 under legacy `/support/files/`, which still resolves and is also served under `/documentation/files/`), Jetpack Photon `i0–i2.wp.com/wordpress.org/documentation/files/…` 87 (normalised), `lh3–lh6.googleusercontent.com` 84 (no extension, in 18 articles: Google Docs paste, so these are **at risk**), `user-images.githubusercontent.com` 36, `private-user-images.githubusercontent.com` 1 (signed URL, **404**), `codex.wordpress.org` 3, `support.files.wordpress.com` 3, and 1 smiley from `wp-includes`.
- `srcset`: 1,954 / 249 articles. 585 images show a resized variant (`-1024x637.png`) whose original also exists. The manifest records both the original (`source_url`) and the variant that was displayed (`displayed_variant`).
- Formats: png 1,861, jpg/jpeg 294, gif 36 (27 articles, animated demos), webp 34, no SVG.
- 159 images are inside links (63 articles). 116 links point at the image file itself and are dropped. The rest are kept as linked images.
- 546 image figures have captions (134 articles). 240 images have empty alt text (94 articles).
- 6 images are not in a figure (inline). 2 are in list items and 1 is in a table cell (`what-are-smilies`).
- **Media library usage:** 2,338 of 7,201 items (32%) are referenced by article or page content. By type: png 1,758, jpeg 291, mp4 153, VideoPress 50 (of 67), quicktime 40, webp 35, gif 32, webm 4. If you include the release pages, 2,757 items are referenced anywhere. The other ~4,400 items are orphans: old screenshots, replaced files, and attachments for content that no longer exists.
- 290 image files used in content are **not** in the media library: external hosts, Photon variants, and codex thumbnails.

## 4. Links

There are 215 distinct hosts. The main link groups, as occurrences / articles:

| Target | Count | Handling |
|---|---|---|
| `wordpress.org/documentation/article/*` | 2,012 / 243 (301 distinct slugs) | Rewritten to relative `.md` |
| …with `#fragment` | 158 / 59 | Fragment kept |
| Legacy `/support/article/*`, relative | 584 / 63 | Made absolute, then resolved by slug (545 fixed) |
| Legacy `wordpress.org/support/article/*`, absolute | 44 / 18 | Same as above |
| Stale slugs (not in the dataset) | 75 distinct | `data/redirects.json`: 40 → 301 to an existing article (e.g. `blocks`→`blocks-list`, `wordpress-editor`→`wordpress-block-editor`), 33 → 301 to `developer.wordpress.org/advanced-administration/…` (rewritten to that URL), 2 → **404** (`weblog-client`, `wordpress-lessons`) |
| `/documentation/category/*` | 2 / 1 | Rewritten to the folder `README.md` |
| `/documentation/wordpress-version/*` | 1,369 / 31 | Kept absolute (release pages are out of scope) |
| `/documentation/files/*` (direct file links) | 73 / 33 | Rewritten to the local asset and added to the manifest |
| `core.trac.wordpress.org` | 1,886 / 22 | Mostly default-theme changelogs |
| `codex.wordpress.org` | 1,370 / 55 | Legacy. The Codex now redirects, but links are kept as is. 44 contain spaces (emitted as `<…%20…>`) |
| `wordpress.org/news` | 909 / 10 | |
| `developer.wordpress.org` | 105 / 37 | |
| `make.wordpress.org` | 70 / 29 | |
| `learn.wordpress.org` | 23 / 13 | |
| `profiles.wordpress.org` | 33 / 20 | Changelog props |
| `wordpress.org/plugins`, `/themes`, `/support/forum…` | 70, 42, 56 | |
| Same-page `#anchor` | 279 / 27 | |
| Other external | 473 / 89 | Wikipedia 108, GitHub 35, … |

**Anchors.** On the live site the heading ids are generated at render time by `wporg/table-of-contents`.
The id is the stored `id` if there is one, otherwise `sanitize_title(text)`, with `-2`/`-3` added for
duplicates (see `notes/site-structure.md` §3). Using that rule, **43 `#fragment` links are already broken
on the live site** (`data/link-check.json`). The conversion introduces no new broken fragments. 36 links
target ids on non-heading elements (for example `<p id>` in `keyboard-shortcuts-block-editor`). These
are preserved as `<a id>`.

## 5. Weird or hard content

- **Nesting:** groups inside columns inside groups. Galleries contain figures. Lists nest up to 3 levels, and one list item contains a callout and an image.
- **Tables:** only 1 table needs raw HTML: `customize-date-and-time-format`, which uses `colspan` section rows. 13 tables have no `<th>` but a bold first row, so that row becomes the header. 13 have no header at all, so an empty GFM header row is emitted (`keyboard-shortcuts-block-editor` has 10 of these).
- **Paste artefacts:** `<strong> </strong>` (whitespace-only emphasis), nested `<strong>a <strong>+</strong></strong>` (92), adjacent `<strong>a</strong><span><strong>:</strong></span>`, `<br>` at the start or end of blocks (94), `<br>` inside link text (`site-health-screen`), and leading `&nbsp;` indentation (`speaker-deck-embed`).
- **Literal HTML and entities in prose:** `use-character-entities`, `write-code-in-your-posts-classic-editor`, `faq-work-with-wordpress` (a full RSS sample). These must be escaped in Markdown.
- `<pre>` blocks with links inside (`use-character-entities`, `video-shortcode`). The URLs are lost in a code fence.
- `<pre>` with `<br>` instead of newlines (`keyboard-shortcuts-classic-editor`).
- **Embedded social posts** (X, Bluesky) carry the quoted text plus a script. No forms, footnotes or RTL content in articles.
- **Hard-coded "Go back to the list of Blocks"** right-aligned link: this is the first paragraph of 73 block articles. After import the excerpt becomes the first line, so these articles would get that link text as their excerpt.

## 6. Static pages

- `customization`, `support-guides`, `overview`, `technical-guides`: empty `content`. The theme templates render the category listings. **Skipped.**
- `support-forums` (front page, ID 8): a near-copy of the theme pattern (hero, search form, cards). **Skipped**, because the theme pattern is the source of truth.
- `site-health` (`page-full-width.php`) and `update-php` (`page-update-php.php`): simple paragraphs, lists and one image. Converted to `docs/site-health.md` and `docs/update-php.md`.

## 7. Release pages (`helphub_version`, out of scope)

The 935 release pages are highly uniform and hand-maintained text from a template:

- 787 start with "On {date}, WordPress X.Y was released to the public."
- Then come the sections `Installation/Update Information` (810), `Summary` (799), `List of Files Revised` (523, mostly long `<pre>` file lists; 859 pages have a `<pre>`) and `Change log`/`Changelog` (262).
- Credits and props make `profiles.wordpress.org` the most linked host (4,962 links). There are 1,494 Trac links.
- Only 18 pages have images. The median size is 3 KB of HTML, but recent majors are large (`version-7-0` is 104 KB).
- 565 have a `helphub_major_release` term and 370 have none.

They would convert cleanly with the same converter (no new block types). Because they are effectively a
data set (version, date, codename, db_version, Trac revision, file lists), it would be better to treat
them separately: generate them from structured front matter, or keep them as one Markdown file per major
release, rather than mixing 935 files into the docs tree.
