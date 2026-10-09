# Content proposal: Classic WordPress, plus three cross-cutting policies

Date: 2026-10-09. Scope: the 36 articles under `classic-wordpress/` (`classic: true`) and three policies
that apply to the whole doc set. Page-level only; the tree in `data/structure.yaml` is taken as settled.
Machine-readable copy: `data/content-proposal/classic-and-policies.json`.

Inputs: `data/article-facts.json`, `raw/articles.json`, the Markdown in `docs/classic-wordpress/`, and a
check of what WordPress core itself links to (wordpress-develop trunk, fetched 2026-10-09). That check
matters, because four pages in scope are wp-admin help-tab targets and eleven are readme.txt targets:

| Linked from core | Page |
|---|---|
| `wp-admin/edit-form-advanced.php` help sidebar | `write-posts-classic-editor` |
| `wp-admin/widgets-form.php` (classic Widgets screen) | `appearance-widgets-screen-classic-editor` |
| `wp-admin/nav-menus.php` | `appearance-menus-screen` |
| `wp-admin/customize.php` | `customizer` |
| `wp-content/themes/<theme>/readme.txt`, every version entry | `<theme>-changelog#Version_X.Y` (all 15 theme changelogs) |
| `wp-admin/about.php` ("release notes") | `/documentation/wordpress-version/version-X-Y/` (release pages, policy c) |

Those slugs keep their URLs whatever happens to their titles or content.

## Summary

The section is a frozen appendix: accurate for people on a classic theme, the Classic Editor plugin or the
Classic Widgets plugin, not grown. The proposal mostly consolidates the Classic Editor pages, fixes the widget
pages' framing, and keeps the theme pages and changelogs because core links to them.

| Sub-section | Pages now | Proposed | Change |
|---|---|---|---|
| Classic Editor | 11 | 5 | small single-field pages fold into one guide; media into one page; one new shortcode reference; two pages kept (rewritten) |
| Widgets, Menus and the Customizer | 5 | 4 | `manage-wordpress-widgets` splits into the two widget pages |
| Classic default themes | 20 | 21 | all kept; one new index page with a table (it also replaces the two changelog-only stubs) |
| **Total** | **36** | **30** | |

Actions on the 36 existing articles: **KEEP 20, REWRITE 7, MERGE 6, SPLIT 2, DELETE 1**, plus **NEW 2**
(`media-shortcodes`, `classic-default-themes` index). Eight URLs need redirects (6 merges, 1 delete, and
`manage-wordpress-widgets` after its split).

**Answers to the two framing questions**

- *Do 9 classic theme pages + 11 changelogs earn their keep, versus one table page?* The changelogs do, for a
  reason that has nothing to do with readers: every bundled theme's `readme.txt` links each release to
  `…/<theme>-changelog/#Version_X.Y`, and the docs team updates them every core release (all 11 were modified
  2026-08-19/20). They are published release notes with an external URL contract, not docs pages, and they stay.
  The 9 theme guides document theme-specific options (front-page sections, header media, cover template, post
  formats, patterns) that exist nowhere else, were mostly rewritten in 2024, and cost almost nothing to keep.
  The table idea is still right, as the **section index** rather than a replacement.
- *Do the "(Classic Editor)" pairs need separate pages?* No. Three of the eleven are one field or one box of the
  same edit screen (excerpt 101 words, sticky 162, visibility 553), and `write-posts-classic-editor` already
  describes that screen, Publish box included. They fold into one "Using the Classic Editor" guide. Media folds into one
  "Add media" page. `first-steps-with-wordpress-classic` is a near-verbatim copy of the block version and is deleted.

**Removed, hidden or wrongly framed features** (fix during the REWRITE/MERGE work):

- Classic widgets (`appearance-widgets-screen-classic-editor`, half of `manage-wordpress-widgets`): since 5.8
  the classic Widgets screen and Text/RSS widget forms appear only with the **Classic Widgets plugin**. The page
  title says "(Classic Editor)", which is the wrong plugin.
- Appearance > Menus and the Customizer are absent with block themes (both pages already say so; keep the notes).
- `sticky-posts-classic-editor`: its first half gives block-editor steps via a "Document" tab that no longer exists.
- `content-visibility-classic-editor`: "hiding the entire blog is not part of core; there are possible plans"
  is stale (2018 text).
- `keyboard-shortcuts-classic-editor`: notes for Macs on WordPress < 4.2; comment shortcuts mislabelled as editor shortcuts.
- `write-code-in-your-posts-classic-editor`: `<tt>`, "older versions converted < and >".
- `audio-shortcode` / `video-shortcode`: "Related" links go to Codex pages for caption, embed, gallery, playlist.
- `first-steps-with-wordpress-classic`: Twenty Nineteen and 2018 screenshots. (The block twin still cites
  Twenty Twenty-Two and links widgets/menus pages; flagged for the overview reviewer.)
- In-links to retarget after merges: `more-block` and `post-excerpt-block` (block pages) link to the *classic*
  excerpt page; `twenty-sixteen` links it too; `users-your-profile-screen` links the classic keyboard page for
  comment shortcuts.

## Per-article actions

`Result / target` anchors (`#excerpt`) are the section the merged content lands in. Every MERGE and DELETE source
gets a 301 in `data/redirects.json` at merge time.

### Classic Editor

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `write-posts-classic-editor` | Write posts (Classic Editor) | REWRITE | Retitle "Using the Classic Editor"; becomes the section index; absorbs excerpt, visibility, sticky. Slug kept (linked from wp-admin edit-form-advanced.php) | Core help tab links here; already covers the Publish box, the natural home for small classic pages. |
| `first-steps-with-wordpress-classic` | First steps with WordPress (Classic Editor) | DELETE (redirect → first-steps-with-wordpress-block-editor) | redirect → first-steps-with-wordpress-block-editor | Near-verbatim copy of the block version with 2018 screenshots and Twenty Nineteen; only the editor differs. |
| `what-is-an-excerpt-classic-editor` | What is an excerpt? (Classic Editor) | MERGE → write-posts-classic-editor | write-posts-classic-editor (#excerpt) | 101 words; the Excerpt box is one field of the classic edit screen. |
| `content-visibility-classic-editor` | Set blog content visibility (Classic Editor) | MERGE → write-posts-classic-editor | write-posts-classic-editor (#visibility) | Only the Publish-box steps are classic; the rest duplicates the block twin. Drops stale "not in core" claim. |
| `sticky-posts-classic-editor` | Sticky Posts (Classic Editor) | MERGE → write-posts-classic-editor | write-posts-classic-editor (#sticky-posts) | 162 words; first half is outdated block-editor steps ("Document tab"); the classic half is one checkbox. |
| `inserting-images-into-posts-and-pages-classic` | Inserting images into posts and pages (Classic Editor) | REWRITE | Retitle "Add media in the Classic Editor"; absorbs the gallery page. Slug kept | Most-linked classic page (8 in-links); the Add Media modal covers images and galleries in one flow. |
| `the-wordpress-gallery-classic-editor` | The WordPress Gallery (Classic Editor) | MERGE → inserting-images-into-posts-and-pages-classic | inserting-images-into-posts-and-pages-classic (#gallery); [gallery] shortcode section → media-shortcodes | Same Add Media modal as images; 0 in-links. |
| `audio-shortcode` | Audio Shortcode | MERGE → media-shortcodes | media-shortcodes | Identical structure to video-shortcode; Related section links legacy Codex pages. |
| `video-shortcode` | Video shortcode | MERGE → media-shortcodes | media-shortcodes | Identical structure to audio-shortcode; one reference page serves both. |
| `write-code-in-your-posts-classic-editor` | Write code in your posts (Classic Editor) | REWRITE | Trim to Visual/Text-tab behaviour; entity list → link use-character-entities | Duplicates use-character-entities; mentions obsolete `<tt>` and "older versions" behaviour. |
| `keyboard-shortcuts-classic-editor` | Use keyboard shortcuts (Classic Editor) | SPLIT → keyboard-shortcuts-classic-editor; comments-screen | keyboard-shortcuts-classic-editor (editor shortcuts); comments-screen (comment moderation shortcuts) | Comment shortcuts work with any editor and are switched on in the profile, not the Classic Editor. |
| `media-shortcodes` | Audio, video and gallery shortcodes | NEW | [merged from: audio-shortcode, video-shortcode, gallery shortcode section] | One shortcode reference instead of two clones plus Codex links. |

### Widgets, Menus and the Customizer

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `customizer` | Customizer | KEEP | — | Linked from wp-admin customize.php; accurate for classic themes. |
| `block-based-widgets-editor` | Block-based Widgets Editor | REWRITE | Retitle "Widgets"; becomes the widgets page; absorbs widget/widget-area concepts from manage-wordpress-widgets | Default widgets screen for classic themes since 5.8; should lead, not the classic screen. |
| `manage-wordpress-widgets` | Manage WordPress widgets | SPLIT → block-based-widgets-editor; appearance-widgets-screen-classic-editor | block-based-widgets-editor (what widgets and widget areas are); appearance-widgets-screen-classic-editor (classic steps, Text/RSS widgets). Redirect → block-based-widgets-editor | Mixes concepts with classic-only steps already repeated on the classic Widgets screen page. |
| `appearance-widgets-screen-classic-editor` | Appearance Widgets Screen (Classic Editor) | REWRITE | Retitle "Classic Widgets screen" (Classic Widgets plugin). Slug kept (linked from wp-admin widgets-form.php) | Title is wrong: this screen needs the Classic Widgets plugin, not the Classic Editor. |
| `appearance-menus-screen` | Appearance Menus Screen | KEEP | — | Linked from wp-admin nav-menus.php; recently updated with a block-theme note. |

### Classic default themes

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `classic-default-themes` | Classic default themes | NEW | [new] section index: table of theme, release year, WordPress version, theme directory, guide, changelog | Replaces the generated intro and the two changelog-only stubs (Fourteen, Thirteen) with one scannable table. |
| `twenty-twenty-one` | Twenty Twenty-One | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-twenty-one-changelog` | Twenty Twenty-One changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-twenty` | Twenty Twenty | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-twenty-changelog` | Twenty Twenty changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-nineteen` | Twenty Nineteen | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-nineteen-changelog` | Twenty Nineteen changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-seventeen` | Twenty Seventeen | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-seventeen-changelog` | Twenty Seventeen changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-sixteen` | Twenty Sixteen | REWRITE | Bring to the 2024 theme-page template (Quick Specs, Patterns, Support & resources) | Pre-2024 shape and 2018 screenshots; links the classic excerpt page; no Patterns section. |
| `twenty-sixteen-changelog` | Twenty Sixteen changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-fifteen` | Twenty Fifteen | REWRITE | Bring to the 2024 theme-page template (Quick Specs, Patterns, Support & resources) | Pre-2024 shape and 2018 screenshots; links the classic excerpt page; no Patterns section. |
| `twenty-fifteen-changelog` | Twenty Fifteen changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-fourteen-changelog` | Twenty Fourteen changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-thirteen-changelog` | Twenty Thirteen changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-twelve` | Twenty Twelve | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-twelve-changelog` | Twenty Twelve changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-eleven` | Twenty Eleven | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-eleven-changelog` | Twenty Eleven changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |
| `twenty-ten` | Twenty Ten | KEEP | — | Unique how-to for a still-updated bundled theme; reviewed in 2024; cheap to keep. |
| `twenty-ten-changelog` | Twenty Ten changelog | KEEP | — | Bundled theme readme.txt links each version to #Version_X.Y here; updated every core release. |

## Proposed end state

- **Classic WordPress** (section intro unchanged)
  - **Classic Editor**
    - Using the Classic Editor (`write-posts-classic-editor`, section index) [rewrite] [merged from: what-is-an-excerpt-classic-editor, content-visibility-classic-editor, sticky-posts-classic-editor]
    - Add media in the Classic Editor (`inserting-images-into-posts-and-pages-classic`) [rewrite] [merged from: the-wordpress-gallery-classic-editor]
    - Audio, video and gallery shortcodes (`media-shortcodes`) [new] [merged from: audio-shortcode, video-shortcode, gallery shortcode section]
    - Write code in your posts (Classic Editor) [rewrite]
    - Use keyboard shortcuts (Classic Editor) [rewrite: comment shortcuts moved to `comments-screen`]
  - **Widgets, Menus and the Customizer**
    - Customizer
    - Widgets (`block-based-widgets-editor`) [rewrite] [merged from: manage-wordpress-widgets, concepts]
    - Classic Widgets screen (`appearance-widgets-screen-classic-editor`) [rewrite] [merged from: manage-wordpress-widgets, classic steps]
    - Appearance Menus Screen
  - **Classic default themes** (`classic-default-themes`, index) [new: table of all 11 themes]
    - Twenty Twenty-One → Twenty Twenty-One changelog
    - Twenty Twenty → Twenty Twenty changelog
    - Twenty Nineteen → Twenty Nineteen changelog
    - Twenty Seventeen → Twenty Seventeen changelog
    - Twenty Sixteen [rewrite] → Twenty Sixteen changelog
    - Twenty Fifteen [rewrite] → Twenty Fifteen changelog
    - Twenty Fourteen changelog (direct child of the index; the generated stub section goes, see decisions)
    - Twenty Thirteen changelog (same)
    - Twenty Twelve → Twenty Twelve changelog
    - Twenty Eleven → Twenty Eleven changelog
    - Twenty Ten → Twenty Ten changelog

30 pages (5 + 4 + 21). The index table columns: theme, year, shipped with WordPress X.Y, theme directory link,
guide link (none for Fourteen/Thirteen), changelog link. No new prose is written for Fourteen or Thirteen.

## Policies

### a. Changelog sections

**Numbers** (from `raw/articles.json`, text after the last `Changelog` H2): 169 articles per
`article-facts.json` (171 with a looser heading match), **≈12,300 words**, about 3.9% of all article text
(317,676 words). They hold ≈870 dated "Created/Updated YYYY-MM-DD" entries and ≈380 `@user` props. The median
section is 48 words; the largest is `blocks-list` (886). 141 of the articles have a 2026 entry, so the habit is
alive. The 15 theme `*-changelog` *articles* (26,353 words) are not covered by this policy: they are product
release notes linked from `readme.txt` and stay as pages.

**Recommendation: drop from the body, archive once, add `last_reviewed`.**

1. One-time export of every section to `data/changelog-archive.json`, keyed by slug: `{date, props[], notes[]}`
   per entry, plus the raw HTML for fidelity. Not published as a page; it is a contributor and credit record.
2. Remove the H2 and its list from the Markdown in the same conversion pass (the converter already knows the
   `div.changelog` group).
3. Add frontmatter `last_reviewed: YYYY-MM-DD` (newest entry) and, optionally, `reviewed_for: "7.1"`. From
   then on, a PR that reviews a page bumps `last_reviewed`; git history and the PR record what changed and who.
4. Props move to the PR: a co-author trailer or the props bot convention used in the Gutenberg repo.

Caveat: the importer strips frontmatter, so `last_reviewed` reaches wordpress.org only if the HelpHub importer
subclass maps it to post meta. Without that, the live page still shows "Last updated" from `post_modified`.

**Alternative: keep the sections in the body.** Familiar to the docs team, visible to readers, needs no tooling.
Cost: duplicates git, produces merge conflicts at the end of every file when two PRs touch one page, and keeps
12k words of reader-irrelevant text in search excerpts and translations (Rosetta locales translate them too).

### b. "(Block Editor)" / "(Classic Editor)" paired pages

Suffixed pairs today (titles in `article-facts.json`):

| Block-first page | Classic twin | Twin after this proposal |
|---|---|---|
| `first-steps-with-wordpress-block-editor` | `first-steps-with-wordpress-classic` | deleted (redirect to the block page) |
| `inserting-images-into-posts-and-pages-block-editor` | `inserting-images-into-posts-and-pages-classic` | kept, "Add media in the Classic Editor" |
| `the-wordpress-gallery-block-editor` | `the-wordpress-gallery-classic-editor` | `inserting-images-…-classic#gallery` |
| `content-visibility-block-editor` | `content-visibility-classic-editor` | `write-posts-classic-editor#visibility` |
| `what-is-an-excerpt-block-editor` | `what-is-an-excerpt-classic-editor` | `write-posts-classic-editor#excerpt` |
| `keyboard-shortcuts-block-editor` | `keyboard-shortcuts-classic-editor` | kept |

Classic-only suffixed titles with no twin: `write-posts-classic-editor`, `sticky-posts-classic-editor`,
`write-code-in-your-posts-classic-editor`, `appearance-widgets-screen-classic-editor`. One unsuffixed pair:
`block-based-widgets-editor` ↔ `appearance-widgets-screen-classic-editor`.

**Recommendation.**

- Block-first titles drop the suffix: "First steps with WordPress", "Inserting images into posts and pages",
  "The WordPress Gallery", "Set content visibility", "What is an excerpt?", "Use keyboard shortcuts".
  The block editor is the default, so it needs no qualifier.
- **Slugs do not change.** URLs are flat and stable (see `notes/helphub-structure-analysis.md` §4); renaming
  six slugs buys nothing a reader sees and costs six redirects plus Rosetta link breakage.
- Only Classic WordPress pages carry a qualifier, and it names what the reader has installed: "(Classic Editor)"
  for editor pages, "Classic Widgets" for the widgets plugin. Keep it even inside the section, because search
  results and wp-admin help links show the title without its section.
- Cross-reference with one standard line, not ad-hoc notes. Block page, first line after the H1:
  `> [!NOTE]` "Using the Classic Editor plugin? See [Using the Classic Editor › Excerpt](…#excerpt)." Classic page:
  the mirror line back to the block page. Today each pair words this differently, and some pairs lack it.
- Alternative: a frontmatter field `classic_counterpart: <slug>#anchor` rendered as the note. Cleaner, but it needs the
  importer subclass and a theme change; the hand-written line works today and can be generated from the field later.

### c. Version and history pages

The actions for these pages belong to the overview reviewer; this is the policy they should apply.

**Principle: the user docs describe current WordPress and link to history; they do not restate release notes.**

- **Release pages (935, `helphub_version`).** Out of scope for the migration and they stay where they are, on the
  `helphub_version` post type at `/documentation/wordpress-version/…`. `wp-admin/about.php` builds that URL for
  every release, and the theme changelogs link it too, so it is a live contract. The docs link to them
  absolutely (the converter already does). Moving them into Git, if ever, is a separate data project: one
  file per major or structured frontmatter, generated, not 935 hand-edited pages in the docs tree.
- **`wordpress-versions` (Release archive).** Keep: it is the landing page `/wordpress-version/` redirects to
  and the one index of releases. Treat its tables as data: generate them from `raw/versions.json` plus the
  major-release terms, rather than hand-adding a row each release. `wordpress-versions-0-7-to-4-9` exists only to
  keep one page short; once generated, fold it into the archive with collapsed majors (redirect) or keep it as a
  generated second page. Either is fine; generated is the point.
- **`supported-versions`.** Keep. 192 words of support policy is what readers need; link to the core security
  FAQ for detail.
- **`learn-about-wordpress-and-version-history`.** Keep the origins narrative (b2/cafelog, licence, community).
  Most of its 3,590 words are one paragraph per major release, 0.7 to 7.1, with contributor counts and
  highlights, edited every release. Cut that to a year-by-year line linking the News post and the Release archive.

**Alternative:** treat the docs as the canonical history and curate per-version summaries in the user docs.
Rejected: it duplicates News posts and release pages, and it ages faster than anything else in the tree.

## Decisions for humans

1. **Theme stubs.** Twenty Fourteen and Twenty Thirteen have generated sections whose only child is a changelog.
   Proposal: drop the two stubs and hang their changelogs directly under the new index. That is a small
   `structure.yaml` change; the alternative is writing two theme guides, which the frozen-appendix rule argues against.
2. **Merge targets keep old slugs** (`write-posts-classic-editor` for "Using the Classic Editor",
   `inserting-images-into-posts-and-pages-classic` for "Add media…"). Slug and title then disagree. Accept, or
   rename with redirects? Core links `write-posts-classic-editor`, so a rename needs a core patch or a permanent redirect.
3. **`media-shortcodes`.** Keep shortcodes in the user docs (users type them in the Shortcode block), or move the
   reference to developer.wordpress.org? This proposal keeps them.
4. **Changelog policy (a)** is a docs-team process change, not just a migration choice. It needs sign-off from the
   team that writes them, and a decision on how props are credited in PRs.
5. **`last_reviewed` on wordpress.org** requires the HelpHub importer subclass to map it to meta and the theme to
   show it. Worth it, or rely on "Last updated"?
6. **Block-theme default theme changelogs** (4, outside this scope) follow the same KEEP rule; the overview/editing
   reviewers should not merge them away.
