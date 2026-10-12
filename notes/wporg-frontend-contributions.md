# Contributing front-end fixes to WordPress.org docs pages

Research from 2026-10-11, prompted by two small UI items on the new DevHub layout: the "In this article" mobile
toggle lacking a pointer cursor, and a proposed "Copy page (as Markdown)" action in the article sidebar.

## Where the pieces live

| UI element | Block | Repo and path |
|---|---|---|
| "In this article" box (desktop list, mobile collapsible bar) | `wporg/table-of-contents` | `WordPress/wporg-mu-plugins` → `mu-plugins/blocks/table-of-contents/` (`index.php`, `postcss/style.pcss`, `src/view.js`) |
| "Chapters" box | `wporg/chapter-list` | `wporg-mu-plugins` → `mu-plugins/blocks/chapter-list/` (styles in `src/style.scss`) |
| Sticky sidebar wrapper, divider and "↑ Back to top" | `wporg/sidebar-container` | `wporg-mu-plugins` → `mu-plugins/blocks/sidebar-container/` |
| Where DevHub places the sidebar | pattern `wporg-developer-2023/article-sidebar` | `WordPress/wporg-developer` → `source/wp-content/themes/wporg-developer-2023/patterns/article-sidebar.php` (sidebar container wrapping the TOC block; the `add/copy-page-sidebar` branch adds the copy-page block after it) |

The theme contributes nothing to the sidebar beyond the pattern. All behaviour is in the shared mu-plugins blocks,
which are also used by the documentation site, Learn and News. A change there ships to every site.

## Table of contents block

- `index.php` regex-parses `<h1-6>` from `get_the_content()` (filtered by `wporg_table_of_contents_post_content`),
  needs at least 2 headings, lists levels 1–3 (h1 included, h4+ skipped), injects ids and `is-toc-heading` into the content at `the_content` priority 5.
- Header is an h2 ("In this article", filter `wporg_table_of_contents_heading`) plus a `<button
  class="wporg-table-of-contents__toggle" aria-expanded>` absolutely positioned over the whole header.
- Mobile (`max-width: 1299px`): bordered box, list hidden, button toggles `display:block` via `view.js`.
  Desktop (`min-width: 1300px`): button hidden, list shown.
- **Bug fixed (PR WordPress/wporg-mu-plugins#779, approved 2026-10-12):** the button had no `cursor: pointer`.
  Chapter-list's identical toggle already had it (`src/style.scss` line ~116). Confirmed missing in the production
  CSS at `developer.wordpress.org/wp-content/mu-plugins/pub-sync/blocks/table-of-contents/build/style.css`.

## Sidebar container and "Back to top"

- `render()` appends `<p class="has-small-font-size is-link-to-top"><a href="#wp--skip-link--target">↑ Back to top</a></p>`
  after the inner blocks when attribute `hasBackToTop` is true (default true). `inlineBreakpoint` defaults to `1300px`.
- `.is-link-to-top` is `display:none`; it becomes `display:block` only inside `.is-fixed-sidebar`, which `view.js`
  adds when the page has scrolled so that `main` reaches the local nav (only while `is-floating-sidebar`, i.e. ≥1300px).
  So "Back to top" appears on scroll, desktop only.
- The divider is `& * + .is-link-to-top { padding-top; border-top: 1px solid light-grey-1 }` inside
  `.is-floating-sidebar`: it belongs to the back-to-top paragraph and only draws when something precedes it.
  That is why the line is visible before the link is.
- Below 1300px the container never floats: no back-to-top, TOC collapses to the bar.

## Markdown output on WordPress.org (for the "Copy page" idea)

- Announced by dd32 on make/meta 2026-03-03: https://make.wordpress.org/meta/2026/03/03/markdown-now-available-on-wordpress-org/
- Works on most .org sites via `?output_format=md` **or** `Accept: text/markdown`. Response is `text/markdown`
  with a `Title / Published / Last modified` preamble, then the converted body (TOC links rewritten to the md URL).
- Every HTML page carries `<link rel="alternate" type="text/markdown" href="...?output_format=md">` in `<head>`
  (with a `data-llm-hint` attribute), built with `add_query_arg( 'output_format', 'md' )` on the current request.
- Conversion uses Dennis Snell's https://github.com/dmsnell/html-to-md (HTML API based). Issues go there or on the post.
- **The wiring is not public.** Not in wporg-mu-plugins, wporg-developer, or public meta SVN (`mu-plugins/` there only
  has `pub/`, which is synced into wporg-developer; grep found nothing). It lives in private dotorg code, so
  **local wp-env sites do not serve Markdown by default**. html-to-md is itself a WordPress plugin that does the same thing (query arg, Accept header, and the alternate link tag), so it is cloned to `~/Developer/wordpress-org/local-plugins/html-to-md` and mounted via the DevHub `.wp-env.override.json`.
- Usage-stats follow-up: https://make.wordpress.org/systems/2026/03/30/markdown-usage-stats/
- Related but separate: `pub/wporg-llms.php` serves `/llms.txt` on WordPress.org only.

## "Copy page": what was built (2026-10-11/12)

Layout: TOC list → divider → Copy page → View as Markdown → Back to top (appears on scroll). Desktop only.

- **New block `wporg/copy-page` in wporg-mu-plugins** (branch `add/copy-page-block`): `index.php`, `render.php`,
  `src/{block.json,index.js,view.js}`, `postcss/style.pcss`. Interactivity API store; `fetch` of the Markdown URL
  with `Accept: text/markdown`, content-type checked, written to the clipboard via a promise-valued `ClipboardItem`
  (keeps Safari's user-gesture window) with a `writeText` fallback. Icons: `copySmall`, `check` from
  `@wordpress/icons` and a hand-drawn stroke Markdown glyph. The URL is `add_query_arg( 'output_format', 'md' )` on
  the current request (filter `wporg_copy_page_markdown_url`), so archives such as `/cli/commands/` copy the right
  page. `hasViewLink` attribute (default true) toggles the link. Template-only (`inserter: false`).
- **Sidebar container** (same branch): "Back to top" uses the `arrowUp` icon in the same icon+gap structure so the
  labels align (string becomes "Back to top", existing translations need redoing); the copy block is hidden except
  in `.is-floating-sidebar`, like Back to top; the divider moves to whichever footer item comes first; back to top
  is omitted from Markdown renderings. Yes, this teaches the container about the copy block; the alternative
  (a `hasCopyPage` attribute) would have put a content action in a layout block on every site, which was judged
  worse. The hiding/divider rules could be generalised to a footer-item class later if a third item appears.
- **Shared helper** `Helpers\is_markdown_request()` (filter `wporg_is_markdown_request`) mirrors html-to-md's
  checks; both blocks return nothing on Markdown requests, so the converted document has no "Copy page",
  "View as Markdown" or "Back to top".
- **DevHub** (wporg-developer branch `add/copy-page-sidebar`): `<!-- wp:wporg/copy-page /-->` added to
  `patterns/article-sidebar.php`, which every handbook, code reference, CLI command and the CLI commands archive
  template includes. Other sites (documentation, make, 5ftf) use the sidebar container but not the block.
- **Deploy order:** the mu-plugins change must be synced and deployed before the DevHub pattern, or the pattern
  renders an unregistered block (empty on the front end, "unsupported block" in the site editor).
- Open design notes: pages with fewer than two headings show the copy rows alone at the top of the sidebar; the
  view module and `wp-a11y` are enqueued on every page even where CSS hides the block; for GitHub-sourced handbooks
  "View as Markdown" is the converted render, not the source `.md` on GitHub.

## Procedure and local environment

Documented in `~/Developer/wordpress-org/README.md` (forks, wp-env setup, gotchas, the merge → `build` branch →
sandbox sync → deploy chain, who deploys, how to confirm a change is live, PR conventions). Keep that file current
rather than this section. CI on a wporg-mu-plugins PR runs `composer run lint` (phpcs, `wporg` standard),
`npm run lint:css` and `npm run lint:js`; `build.yml` also gates the `build` branch on PHPUnit.
