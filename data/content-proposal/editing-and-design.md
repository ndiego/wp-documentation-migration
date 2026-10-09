# Content proposal: Editing & design

Scope: every article whose `proposed_path` starts with `editing-and-design/` (190 articles: Block editor 167, Site Editor 11, Themes 12 including the four block default themes and their changelogs). Page-level decisions only; the tree in `data/structure.yaml` is unchanged except where a merge or split removes or adds a page inside an existing section. Machine-readable version: `data/content-proposal/editing-and-design.json`.

## Summary

**190 pages now → 170 pages proposed** (−20).

| Action | Count | Notes |
|---|---|---|
| KEEP | 147 | 105 of these are block reference pages that get the mechanical "template trim" below; not counted as REWRITE |
| REWRITE | 19 | 4 absorb merged pages (Comments, Query Loop, Navigation, Identity); 4 become the shared reference their inserter variations link to (Group, Query Title, Post Navigation Link, Embeds); 3 hubs or indexes; 8 freshness, task-orientation or thin-page rewrites |
| MERGE | 14 | 13 container-only inner blocks → Comments (8), Query Loop (2), Navigation (3) (see the rule below); Create a Favicon → Identity |
| SPLIT | 1 | Styles overview → 3 pages |
| DELETE | 8 | 3 deprecation/rename stubs, 1 removed variation, 4 dead or removed embeds; all redirect |
| MOVE | 1 | Pattern submission guide → wordpress.org/patterns |
| NEW | 1 | 1 Site Editor task page |

Per area:

| Area | Now | Proposed |
|---|---|---|
| Block editor (top level) | 7 | 7 |
| Working with blocks (incl. Block settings) | 20 | 20 |
| Patterns | 5 | 4 |
| Blocks reference (index + 6 groups) | 135 | 114 |
| Site Editor | 11 | 14 |
| Themes (incl. default themes and changelogs) | 12 | 11 |

**Template trim (applies to every block reference page that survives).** Delete the hand-written "Go back to the list of Blocks" line (the hierarchy does that), the generic toolbar walkthrough (mover, drag handle, Transform to, More options), the "Block settings panel … click the cog" paragraph, the Advanced settings list and every "Read about these and other settings" note. Replace them with one short "Common tools" line linking to Work with blocks, More options, Moving blocks and the relevant Block settings panel pages. What stays on each block page: what the block does, how it differs from neighbours, its block-specific toolbar buttons and settings, and gotchas. This is mechanical and scriptable against the boilerplate sentences already measured (§2 of `notes/helphub-structure-analysis.md`), so it is not counted as REWRITE.

**Block reference model.** One rule, decided by the project owner: **a block gets its own page if it appears as its own item in the block inserter, regardless of how core registers it.** Users see "YouTube", "Row", "Archive Title" or "Modified Date" as blocks; they do not know these are variations of Embed, Group, Query Title or Date. Applied:

1. **Every inserter item keeps one page.** That covers content blocks (Text, Media, Design, Widgets), standalone theme blocks (Title, Content, Excerpt, Featured Image, Site Title, Avatar, Date, Comments Form …) and inserter-visible variations: Row, Stack and Grid (Group); Archive Title and Search Results Title (Query Title); Next Post and Previous Post (Post Navigation Link); Post Date and Modified Date (Date); Categories and Tags (Post Terms); the generic Embed block and the 30 provider embeds still in the inserter. Checked against Gutenberg trunk (`block.json` and `variations.js` `scope`, 2026-10-09).
2. **Parent pages become the shared reference.** Group, Query Title, Post Navigation Link and the Embeds section index explain the shared settings or workflow once; each variation page links there and keeps only what differs.
3. **The boundary: inner blocks that only appear inside a container stay on the container's page.** These have `parent` or `ancestor` in `block.json`, so the inserter only offers them inside that container: Comment Template and its children (Author Name, Content, Date, Edit Link, Reply Link), Comments Title and Comments Pagination → Comments block; Post Template and Query Total → Query Loop; Submenu, Custom Link and Home Link → Navigation.
4. **Thin is a content problem, not a reason to hide a page.** An inserter item with little unique text today (Title block, 157 words) is rewritten, not merged.
5. **Deprecated, renamed or removed blocks get no page**: a redirect plus a row in the "Deprecated blocks" table on the Blocks list. That covers blocks hidden from the inserter (Post Author, Button outside Buttons), removed variations (Posts List, SlideShare, Screencast) and dead embeds (Facebook, Instagram).

Result: Text 13, Media 9, Design 12 (from 13), Widgets 12, Theme 35 (from 51), Embeds 32 (from 36), plus the Blocks list index: **114 pages instead of 135**. Container pages use one H2 per absorbed inner block with a stable anchor matching the old slug (for example `#comment-date-block`), so redirects land on the right section. The Blocks list index groups pages by family, so no separate family hub pages are added.

**Where the shared material lives once.** Block toolbar, the Settings/Styles tabs and the settings sidebar: Work with blocks (rewritten as the hub). Inserting: Adding a new block. Moving: Moving blocks. More options menu: More options. Rich text toolbar: More rich text editing options and Link control. Each inspector panel: its Block settings page (Layout, Position, Colors, Background, Typography, Dimensions, Border & Shadow, Filters, Advanced, Responsive styles). Block pages link to these and never restate them.

**Task vs reference.** Block editor top level and the Block settings pages are reference. The Site Editor becomes task-led: the hub page tours the workspace, then routes to "Edit your site's header and footer" (new), "Create and edit templates", "Change colors and fonts with Styles", "Create and manage menus", "Set your site title, logo and icon", "Set up your homepage" and "Manage pages". Most of these come from rewriting or splitting existing pages rather than adding new ones. Themes gets a task page ("Find, install and activate a theme") next to the screen reference and the block-theme concept page.

**Freshness flags found.** Renamed or removed features: Reusable blocks → Synced patterns (two page titles), "Template Editor" (no longer a distinct UI), Post Title → Title, Post Author → Avatar/Author Name, Posts List variation (removed 6.7), SlideShare embed (removed 6.6), Screencast embed (removed in Gutenberg 21.1, so WordPress 6.9), Facebook/Instagram embeds (dead since 2020), Twitter → X. Pages untouched since before 2024: `appearance-themes-screen` (2023-01, names Twenty Nineteen as default), `submit-your-block-pattern-to-the-directory` (2023-01). Touched in 2024 only, verify: `additional-guide-to-using-the-site-editor`, `page-break-block`, `login-out-block`, `position-settings-overview`, `dimension-controls-overview`, `filters-settings-overview`, `page-post-settings-sidebar`, `twenty-twenty-two/-three/-four/-five`. Stale "new"/"introduces" framing in pages otherwise current: `site-editor-navigation`, `query-total-block`, `footnotes-block`, `distraction-free-mode`, `block-directory`, `pocket-casts-embed`, `blocks-list`, `work-with-themes` ("Twenty Twenty-Two is the default"). No article in scope is primarily developer documentation; the developer passages inside `work-with-themes` (template files, template hierarchy, cPanel/FTP install, creating themes) are cut to links to developer.wordpress.org as part of its rewrite.

## Per-article actions

Every in-scope article appears once; NEW rows are proposed pages. "Trimmed block reference" = KEEP plus the template trim above.

### Block editor

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `wordpress-block-editor` | WordPress Block Editor | KEEP | Block editor overview (section opener) | Current (2026-09) overview of the editor workspace; the natural entry point for the section. |
| `page-post-settings-sidebar` | Page/Post Settings sidebar | KEEP | Reference: post/page settings sidebar | Substantive reference, well linked; verify against current sidebar, last touched 2024-10. |
| `preferences-overview` | Preferences overview | KEEP | Reference: editor preferences | Unique reference; six inbound links; current. |
| `how-to-use-the-preview-function` | How to use the View feature | KEEP | Task: preview a post or page | Distinct task; current. Consider slug alias matching the "View" title. |
| `distraction-free-mode` | Distraction Free mode | KEEP | Reference: Distraction Free mode | Current, distinct feature; drop the "new" framing. |
| `keyboard-shortcuts-block-editor` | Use keyboard shortcuts (Block Editor) | KEEP | Reference: keyboard shortcuts | Pure reference, current; classic counterpart already lives in Classic WordPress. |
| `notes` | Notes | KEEP | Task: leave and resolve Notes | New 7.0 collaboration feature, current; needs inbound links from editor overview. |

### Block editor > Working with blocks

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `work-with-blocks` | Work with blocks | REWRITE | Hub for the shared block material (toolbar, settings sidebar, Settings/Styles tabs) | Becomes the single home for the toolbar and settings blurbs repeated on 100+ block pages; trim duplicated how-tos. |
| `adding-a-new-block` | Adding a new block | KEEP | Task: add a block | Shared concept with 122 inbound links; block pages link here instead of repeating it. |
| `moving-blocks` | Moving blocks | KEEP | Task: move blocks | Shared concept (80 inbound); replaces the Moving-blocks blurb copied into 54 pages. |
| `list-view` | List view | KEEP | Reference: List View | Current, distinct tool. |
| `more-options` | More options | KEEP | Reference: block More options menu | Shared concept (121 inbound); replaces the More options paragraph copied into block pages. |
| `link-editing` | Link control | KEEP | Reference: Link control | Shared concept used by many text blocks; current. |
| `more-text-editing-overview` | More rich text editing options | KEEP | Reference: rich text toolbar options | Shared concept (17 inbound); text block pages link here. |
| `page-jumps` | Page Jumps | KEEP | Task: link to a section (HTML anchors) | Real user task; current. |
| `block-directory` | Block Directory | KEEP | Task: install blocks from the Block Directory | Core feature, user-facing; drop the "new way" framing. |
| `block-error-unexpected-or-invalid-content` | Block Error: Unexpected or Invalid Content | KEEP | Troubleshooting: invalid block content | Unique troubleshooting page; needs inbound links from Work with blocks. |

### Block editor > Working with blocks > Block settings

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `layout-settings-overview` | Layout Settings overview | KEEP | Reference: block settings panel | Maps 1:1 to an inspector panel; shared target for block pages. |
| `position-settings-overview` | Position Settings overview | KEEP | Reference: Position panel | One page per inspector panel; stale (2024-06) and unlinked, verify sticky options. |
| `colors-settings-overview` | Colors Settings overview | KEEP | Reference: block settings panel | Shared panel reference (65 inbound); current. |
| `background-settings-overview` | Background Settings Overview | KEEP | Reference: block settings panel | Maps to an inspector panel; current. |
| `typography-settings-overview` | Typography Settings overview | KEEP | Reference: block settings panel | Shared panel reference (75 inbound); current. |
| `dimension-controls-overview` | Dimension Settings overview | KEEP | Reference: Dimensions panel | Shared panel reference (73 inbound); last touched 2024-06, verify controls. |
| `border-settings-overview` | Border & Shadow Settings overview | KEEP | Reference: block settings panel | Shared panel reference (50 inbound); current enough (2025-04). |
| `filters-settings-overview` | Filters Settings overview | KEEP | Reference: Filters (duotone) panel | Short but maps to a real panel; last touched 2024-06, verify. |
| `advanced-settings-overview` | Advanced Settings overview | KEEP | Reference: block settings panel | Shared panel reference (117 inbound); replaces the Advanced list copied into 46 pages. |
| `responsive-styles` | Responsive styles | KEEP | Reference: block settings panel | New feature, current; add inbound links from panel pages. |

### Block editor > Patterns

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `block-pattern` | Block Patterns | KEEP | Task + concept: use and create patterns | Core concept page with 16 inbound links; current. |
| `reusable-blocks` | Synced Patterns (Reusable blocks) | REWRITE | "Synced patterns" (title drops "Reusable blocks"; adds pattern overrides) | Feature renamed in 6.3; title and framing still lead with the old name. |
| `comparing-patterns-template-parts-and-reusable-blocks` | Comparing Patterns, Template Parts, and Synced Patterns (Reusable Blocks) | REWRITE | "Patterns, synced patterns and template parts compared" | Useful decision aid, but title and text still centre on Reusable blocks. |
| `block-pattern-directory` | Block Pattern Directory | KEEP | Task: find and insert patterns from the directory | User-facing, current. |
| `submit-your-block-pattern-to-the-directory` | Submit your Block Pattern to the Directory | MOVE → wordpress.org/patterns (Pattern Directory help pages) | — | Contributor workflow for a wordpress.org service, not site editing; untouched since 2023-01. |

### Block editor > Blocks list

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `blocks-list` | Blocks list | REWRITE | Blocks reference index, grouped by family | Groups pages by family, lists variations under their parent, holds the redirects; drop "new Block Editor" framing. |

### Block editor > Blocks list > Text blocks

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `classic-block` | Classic block | KEEP | Trimmed block reference | Still needed for legacy content; short and template-heavy, trim to what is unique. |
| `code-block` | Code block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `details-block` | Details block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `footnotes-block` | Footnotes block | KEEP | Trimmed block reference | Distinct block; drop "WordPress 6.3 introduces" framing. |
| `heading-block` | Heading block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `list-block` | List block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `math-block` | Math block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `paragraph-block` | Paragraph block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `verse-block` | Poetry block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `preformatted-block` | Preformatted block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `pullquote-block` | Pullquote block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `quote-block` | Quote block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `table-block` | Table block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |

### Block editor > Blocks list > Media blocks

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `audio-block` | Audio block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `cover-block` | Cover block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `file-block` | File block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `gallery-block` | Gallery block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `icon-block` | Icon block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `image-block` | Image block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `media-text-block` | Media & Text block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `playlist-block` | Playlist block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `video-block` | Video block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |

### Block editor > Blocks list > Design blocks

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `accordion-block` | Accordion block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `buttons-block` | Buttons block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `columns-block` | Columns block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `grid-block` | Grid block | KEEP | Trimmed block reference | Grid is its own inserter item (Group variation); own page per the inserter rule, shared settings link to Group. |
| `group-block` | Group block | REWRITE | "Group block": the container, linking to Row, Stack and Grid | Shared container settings live here once; Row, Stack and Grid pages link back instead of repeating them. |
| `more-block` | More block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `page-break-block` | Page Break block | KEEP | Trimmed block reference | Distinct block; last touched 2024-06, verify. |
| `row-block` | Row block | KEEP | Trimmed block reference | Row is its own inserter item (Group variation); own page per the inserter rule, shared settings link to Group. |
| `separator-block` | Separator block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `spacer-block` | Spacer block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `stack-block` | Stack block | KEEP | Trimmed block reference | Stack is its own inserter item (Group variation); own page per the inserter rule, shared settings link to Group. |
| `tabs-block` | Tabs block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `button-block` | (Deprecated)Button block | DELETE (redirect → Buttons block) | — | 21-word deprecation stub. |

### Block editor > Blocks list > Widget blocks

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `archives-block` | Archives block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `calendar-block` | Calendar block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `categories-list-block` | Categories List block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `custom-html` | Custom HTML | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `latest-comments-block` | Latest Comments block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `latest-posts-block` | Latest Posts block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `page-list-block` | Page List block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `rss-block` | RSS block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `search-block` | Search block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `shortcode-block` | Shortcode block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `social-icons` | Social Icons block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |
| `tag-cloud-block` | Tag Cloud block | KEEP | Trimmed block reference | Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text. |

### Block editor > Blocks list > Theme blocks

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `archive-title-block` | Archive Title block | KEEP | Trimmed block reference | Archive Title is its own inserter item (Query Title variation); own page per the inserter rule. |
| `post-author-name-block` | Author Name block | KEEP | Trimmed block reference | Author Name is its own inserter item; own page per the inserter rule. |
| `avatar-block` | Avatar block | KEEP | Trimmed block reference | Avatar is its own inserter item; own page per the inserter rule. |
| `breadcrumbs-block` | Breadcrumbs block | KEEP | Trimmed block reference | New, substantive block; works on its own. |
| `categories-block` | Categories block | KEEP | Trimmed block reference | Categories is its own inserter item (Post Terms variation); own page per the inserter rule. |
| `comment-author-name-block` | Comment  Author Name block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comment-content-block` | Comment Content block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comment-date-block` | Comment Date block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comment-edit-link-block` | Comment Edit Link block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comment-reply-link-block` | Comment Reply Link block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comment-template-block` | Comment Template block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comments-block` | Comments block | REWRITE | Comments block, absorbing Comment Template and its inner blocks, Comments Title and Comments Pagination | Container for 8 blocks restricted to it (parent/ancestor); becomes the one reference for them. |
| `comments-count-block` | Comments Count block | KEEP | Trimmed block reference | Comments Count is its own inserter item (no parent restriction); own page per the inserter rule. |
| `comment-link-block` | Comments Link block | KEEP | Trimmed block reference | Comments Link is its own inserter item (no parent restriction); own page per the inserter rule. |
| `comment-pagination-block` | Comments Pagination block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `comments-title-block` | Comments Title block | MERGE → Comments block | Section on the Comments block page | Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate. |
| `post-content-block` | Content block | KEEP | Trimmed block reference | Content is its own inserter item; own page per the inserter rule. |
| `custom-link-block` | Custom Link block | MERGE → Navigation block | Section "Custom Link" on the Navigation page | Only insertable inside the Navigation block (parent restriction). |
| `date-block` | Date Block | KEEP | Trimmed block reference | Date is its own inserter item (base of Post Date and Modified Date); explain how the three differ. |
| `post-excerpt-block` | Excerpt block | KEEP | Trimmed block reference | Excerpt is its own inserter item; own page per the inserter rule. |
| `home-link-block` | Home Link block | MERGE → Navigation block | Section "Home Link" on the Navigation page | Only insertable inside the Navigation block (parent restriction). |
| `login-out-block` | Login-out block | KEEP | Trimmed block reference | Standalone block; unlinked and last touched 2024-06, verify. |
| `post-modified-date-block` | Modified Date block | KEEP | Trimmed block reference | Modified Date is its own inserter item (Date variation); own page per the inserter rule. |
| `navigation-block` | Navigation block | REWRITE | Navigation block, absorbing Submenu, Custom Link and Home Link | Hub for menus (11 inbound); its child blocks only exist inside it (parent restriction). |
| `next-post-block` | Next Post block | KEEP | Trimmed block reference | Next Post is its own inserter item (Post Navigation Link variation); own page per the inserter rule. |
| `pagination-block` | Pagination block | KEEP | Trimmed block reference | Distinct, substantive block with its own inner blocks. |
| `post-author-biography-block` | Post Author Biography block | KEEP | Trimmed block reference | Author Biography is its own inserter item; own page per the inserter rule. |
| `post-comments-form-block` | Post Comments Form block | KEEP | Trimmed block reference | Comments Form is its own inserter item (no parent restriction); own page per the inserter rule. |
| `post-date-block` | Post Date block | KEEP | Trimmed block reference | Post Date is its own inserter item (Date variation); own page per the inserter rule. |
| `post-featured-image-block` | Post Featured Image block | KEEP | Trimmed block reference | Featured Image is its own inserter item; own page per the inserter rule. |
| `post-navigation-link-block` | Post Navigation Link block | REWRITE | Post Navigation Link block: shared settings, linking to Next Post and Previous Post | 57% boilerplate today; becomes the shared reference its two inserter variations link to. |
| `post-tags-block` | Post Tags block | KEEP | Trimmed block reference | Tags is its own inserter item (Post Terms variation); own page per the inserter rule. |
| `post-template-block` | Post Template block | MERGE → Query Loop block | Section on the Query Loop page | Inner block of Query Loop only; explained better in context. |
| `post-title-block` | Post Title block | DELETE (redirect → Title block) | — | 15-word rename stub; Post Title is the Title block, which has its own page. |
| `posts-list-block` | Posts List block | DELETE (redirect → Query Loop block) | — | Variation removed in 6.7; page only points to Query Loop. |
| `previous-post-block` | Previous Post block | KEEP | Trimmed block reference | Previous Post is its own inserter item (Post Navigation Link variation); own page per the inserter rule. |
| `query-loop-block` | Query Loop block | REWRITE | Query Loop block, absorbing Post Template, Query Total and the removed Posts List variation | Key page (23 inbound); Post Template and Query Total only exist inside it. |
| `query-title-block` | Query Title block | REWRITE | Query Title block: shared settings, linking to Archive Title and Search Results Title | Becomes the shared reference its two inserter variations link to; drop duplicated variation text. |
| `query-total-block` | Query Total block | MERGE → Query Loop block | Section on the Query Loop page | Ancestor-restricted to Query Loop; still written as "6.8 is set to introduce". |
| `read-more-block` | Read More block | KEEP | Trimmed block reference | Read More is its own inserter item; own page per the inserter rule. |
| `search-results-title-block` | Search Results Title block | KEEP | Trimmed block reference | Search Results Title is its own inserter item (Query Title variation); own page per the inserter rule. |
| `site-logo-block` | Site Logo block | KEEP | Trimmed block reference | Site Logo is its own inserter item; own page, links to the Identity task. |
| `site-tagline-block` | Site Tagline block | KEEP | Trimmed block reference | Site Tagline is its own inserter item; own page per the inserter rule. |
| `site-title-block` | Site Title block | KEEP | Trimmed block reference | Site Title is its own inserter item; own page per the inserter rule. |
| `submenu-block` | Submenu block | MERGE → Navigation block | Section "Submenu" on the Navigation page | Only insertable inside the Navigation block (parent restriction). |
| `template-part-block` | Template Part block | KEEP | Trimmed block reference | Substantive, low boilerplate, eight inbound links; key to header/footer editing. |
| `term-description-block` | Term Description block | KEEP | Trimmed block reference | Term Description is its own inserter item; own page per the inserter rule. |
| `terms-query-block` | Terms Query block | KEEP | Trimmed block reference | New, substantive container block; needs inbound links. |
| `time-to-read-block` | Time to Read block | KEEP | Trimmed block reference | Time to Read is its own inserter item; own page per the inserter rule. |
| `title-block` | Title block | REWRITE | Title block: full reference (absorbs the old Post Title page) | Own inserter item but only 157 words; thinness is fixed by writing the page, not merging it. |
| `post-author-block` | (Deprecated) Post Author block | DELETE (redirect → Author Name block) | — | 32-word stub; Author block deprecated in 7.0 and hidden from the inserter. |

### Block editor > Blocks list > Embeds

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `embeds` | Embeds | REWRITE | Embeds: how embedding works, plus the provider table linking to each provider page | Section index explains the shared paste-URL workflow once; provider pages link here instead of repeating it. |
| `embed-block` | Embed block | KEEP | Trimmed block reference | Generic Embed is its own inserter item; own page per the inserter rule, workflow links to Embeds. |
| `amazon-kindle-embed` | Amazon Kindle Embed | KEEP | Trimmed block reference | Amazon Kindle is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `animoto-embed` | Animoto Embed | KEEP | Trimmed block reference | Animoto is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `bluesky-embed` | Bluesky embed | KEEP | Trimmed block reference | Bluesky is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `cloudup-embed` | Cloudup Embed | KEEP | Trimmed block reference | Cloudup is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `crowdsignal-embed` | Crowdsignal embed | KEEP | Trimmed block reference | Crowdsignal is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `dailymotion-embed` | Dailymotion embed | KEEP | Trimmed block reference | Dailymotion is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `facebook-embed` | Facebook embed | DELETE (redirect → Embeds) | — | oEmbed endpoint closed in 2020; embedding no longer works. One note on Embeds suffices. |
| `flickr-embed` | Flickr embed | KEEP | Trimmed block reference | Flickr is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `imgur-embed` | Imgur embed | KEEP | Trimmed block reference | Imgur is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `instagram-embed` | Instagram embed | DELETE (redirect → Embeds) | — | oEmbed endpoint closed in 2020; embedding no longer works. One note on Embeds suffices. |
| `issuu-embed` | Issuu embed | KEEP | Trimmed block reference | Issuu is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `kickstarter-embed` | Kickstarter embed | KEEP | Trimmed block reference | Kickstarter is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `mixcloud-embed` | MixCloud embed | KEEP | Trimmed block reference | Mixcloud is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `pinterest-embed` | Pinterest embed | KEEP | Trimmed block reference | Pinterest is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `pocket-casts-embed` | Pocket Casts embed | KEEP | Trimmed block reference | Pocket Casts is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `reddit-embed` | Reddit embed | KEEP | Trimmed block reference | Reddit is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `reverbnation-embed` | ReverbNation embed | KEEP | Trimmed block reference | ReverbNation is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `screencast-block` | Screencast embed | DELETE (redirect → Embeds) | — | Variation removed in Gutenberg 21.1 (PR 70480, June 2025), so gone from the inserter since WordPress 6.9. |
| `scribd-embed` | Scribd embed | KEEP | Trimmed block reference | Scribd is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `smugmug-embed` | SmugMug embed | KEEP | Trimmed block reference | SmugMug is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `soundcloud-embed` | SoundCloud embed | KEEP | Trimmed block reference | SoundCloud is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `speaker-deck-embed` | Speaker Deck embed | KEEP | Trimmed block reference | Speaker Deck is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `spotify-embed` | Spotify embed | KEEP | Trimmed block reference | Spotify is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `ted-embed` | TED embed | KEEP | Trimmed block reference | TED is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `tiktok-embed` | TikTok embed | KEEP | Trimmed block reference | TikTok is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `tumblr-embed` | Tumblr embed | KEEP | Trimmed block reference | Tumblr is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `twitter-embed` | Twitter embed | KEEP | Trimmed block reference | Own inserter item (Embed variation); keep, but retitle X (twitter.com/x.com URLs). |
| `videopress-embed` | VideoPress embed | KEEP | Trimmed block reference | VideoPress is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `vimeo-embed` | Vimeo embed | KEEP | Trimmed block reference | Vimeo is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `wolfram-embed` | Wolfram embed | KEEP | Trimmed block reference | Wolfram is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `wordpress-embed` | WordPress embed | KEEP | Trimmed block reference | WordPress is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `wordpress-tv-embed-block` | WordPress.tv embed | KEEP | Trimmed block reference | WordPress.tv is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `youtube-embed` | YouTube embed | KEEP | Trimmed block reference | YouTube is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds. |
| `slideshare-embed` | Slideshare embed (Removed) | DELETE (redirect → Embeds) | — | Block removed in WordPress 6.6. |

### Site Editor

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `site-editor` | Site Editor | REWRITE | Site Editor hub: workspace, then links to each task page | 30 inbound links; 2,300 words mixing tour and how-tos now covered by task pages. |
| `site-editor-navigation` | Site Editor navigation | REWRITE | Task: "Create and manage menus" | Still framed as "6.3 introduces"; becomes the menu task page, Navigation block stays reference. |
| `site-editor-identity` | Site Editor Identity | REWRITE | Task: "Set your site title, logo and icon" (absorbs Create a Favicon) | 272 words; natural home for site icon instructions. |
| `site-editor-pages` | Site Editor Pages | KEEP | Task: manage pages in the Site Editor | Substantive and current (2025-08). |
| `template-editor` | Template Editor | REWRITE | Task: "Create and edit templates" | "Template Editor" is no longer a distinct UI; templates live in Site Editor > Templates. |
| `site-editor-patterns` | Site Editor Patterns | KEEP | Reference: Patterns screen in the Site Editor | Current; covers managing patterns and template parts. |
| `styles-overview` | Styles overview | SPLIT → Styles overview; Change colors and fonts with Styles; Add custom CSS | Reference + two task pages | 4,140 words, 42 images: reference, colour/font task and CSS task in one page. |
| `the-font-library` | The Font Library | KEEP | Task: add and manage fonts | Distinct, current; linked from the fonts task. |
| `zoom-out-view` | Zoom out view | KEEP | Reference: Zoom out view | Current, distinct. |
| `site-editor-command-palette` | Command Palette | KEEP | Reference: Command Palette | Current; also used in the post editor. |
| `additional-guide-to-using-the-site-editor` | Additional guide to using the Site Editor | REWRITE | Task: "Set up your homepage" | Grab-bag from 2024-02; homepage part is a real gap, rest duplicates Identity and Styles. |
| `edit-your-header-and-footer` | Edit your site's header and footer | NEW | Task: edit, replace or create header/footer template parts | Most common Site Editor task has no page; template-part content is scattered across three references. |

### Themes

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `work-with-themes` | Work with themes | REWRITE | Task: "Find, install and activate a theme" | Says Twenty Twenty-Two is default; template-hierarchy and creating-themes parts belong on developer.wordpress.org (link). |
| `appearance-themes-screen` | Appearance Themes Screen | REWRITE | Reference: Appearance > Themes screen | Untouched since 2023-01; still names Twenty Nineteen as the default theme. |
| `block-themes` | Block themes | KEEP | Concept: what a block theme is | Core concept, 13 inbound links, current. |
| `create-a-favicon` | Create a Favicon | MERGE → Set your site title, logo and icon | Site icon section of the Identity task | Site icon is set in Identity or Settings > General; pre-6.5 half is obsolete. |

### Themes > Default themes

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `twenty-twenty-five` | Twenty Twenty-Five | KEEP | Theme guide (current default) | Guide to templates, style variations and patterns of the active default; verify against latest version. |
| `twenty-twenty-five-changelog` | Twenty Twenty-Five changelog | KEEP | Theme changelog (unchanged) | Changelogs are a separate decision; left as is. |
| `twenty-twenty-four` | Twenty Twenty-Four | KEEP | Theme guide | Substantive user guide for a widely used block theme; last touched 2024-08. |
| `twenty-twenty-four-changelog` | Twenty Twenty-Four changelog | KEEP | Theme changelog (unchanged) | Changelogs are a separate decision; left as is. |
| `twenty-twenty-three` | Twenty Twenty-Three | KEEP | Theme guide | Mostly style variations; last touched 2024-08, could shrink to a stub. |
| `twenty-twenty-three-changelog` | Twenty Twenty-Three Changelog | KEEP | Theme changelog (unchanged) | Changelogs are a separate decision; left as is. |
| `twenty-twenty-two` | Twenty Twenty-Two | KEEP | Theme guide | First default block theme; last touched 2024-08, could shrink to a stub. |
| `twenty-twenty-two-changelog` | Twenty Twenty-Two changelog | KEEP | Theme changelog (unchanged) | Changelogs are a separate decision; left as is. |
## Proposed end state

- **Block editor**
  - WordPress Block Editor: overview of the editor workspace and how to write in it.
  - Page/Post Settings sidebar: reference for the document settings panel.
  - Preferences overview: reference for editor preferences.
  - How to use the View feature: preview a post or page before publishing.
  - Distraction Free mode: reference for the focused writing mode.
  - Use keyboard shortcuts (Block Editor): shortcut reference.
  - Notes: leave, reply to and resolve editorial notes.
  - **Working with blocks**
    - Work with blocks `[rewrite]`: block anatomy, toolbar, Settings/Styles tabs; the one place the shared block material lives.
    - Adding a new block: every way to insert a block.
    - Moving blocks: mover, drag and drop, List View.
    - List view: navigate and select blocks.
    - More options: every item in the block's ⋮ menu.
    - Link control: add and edit links.
    - More rich text editing options: rich text toolbar extras.
    - Page Jumps: link to a section with HTML anchors.
    - Block Directory: install blocks from inside the editor.
    - Block Error: Unexpected or Invalid Content: troubleshoot invalid blocks.
    - **Block settings** (one page per inspector panel): Layout, Position, Colors, Background, Typography, Dimensions, Border & Shadow, Filters, Advanced, Responsive styles.
  - **Patterns**
    - Block Patterns: use, create and manage patterns.
    - Synced patterns `[rewrite]`: create, edit, detach and override synced patterns.
    - Patterns, synced patterns and template parts compared `[rewrite]`: which to use when.
    - Block Pattern Directory: find and insert patterns from wordpress.org.
  - **Blocks list** `[rewrite]`: index grouped by family, plus a "Deprecated blocks" table with redirects.
    - **Text blocks** (13, one page each): Classic, Code, Details, Footnotes, Heading, List, Math, Paragraph, Poetry, Preformatted, Pullquote, Quote, Table.
    - **Media blocks** (9, one page each): Audio, Cover, File, Gallery, Icon, Image, Media & Text, Playlist, Video.
    - **Design blocks** (12)
      - Accordion, Buttons, Columns, More, Page Break, Separator, Spacer, Tabs: one page each.
      - Group block `[rewrite]`: the container block and its shared settings; links to Row, Stack and Grid.
      - Row, Stack, Grid: one page each (Group variations that are their own inserter items).
    - **Widget blocks** (12, one page each): Archives, Calendar, Categories List, Custom HTML, Latest Comments, Latest Posts, Page List, RSS, Search, Shortcode, Social Icons, Tag Cloud.
    - **Theme blocks** (35)
      - Site identity: Site Title, Site Tagline, Site Logo: one page each.
      - Post content: Title `[rewrite]`, Content, Excerpt, Featured Image, Read More, Time to Read: one page each.
      - Post meta: Author Name, Author Biography, Avatar, Date, Post Date, Modified Date, Categories, Tags: one page each.
      - Post Navigation Link block `[rewrite]`: shared settings; links to Next Post and Previous Post, which keep one page each.
      - Query Loop block `[rewrite]` `[merged from: Post Template, Query Total]`: list posts by any criteria.
      - Pagination block: page through Query Loop results.
      - Query Title block `[rewrite]`: shared settings; links to Archive Title and Search Results Title, which keep one page each.
      - Term Description block: show a term's description on archives.
      - Terms Query block: list categories, tags or other terms.
      - Comments block `[rewrite]` `[merged from: Comment Template and its 5 inner blocks, Comments Title, Comments Pagination]`: display and style comments.
      - Comments Count, Comments Link, Comments Form: one page each (standalone inserter items).
      - Navigation block `[rewrite]` `[merged from: Submenu, Custom Link, Home Link]`: reference for the menu block and its items.
      - Template Part block: reference for headers, footers and other parts.
      - Breadcrumbs block: show the visitor's location.
      - Login/out block: add a login or logout link.
    - **Embeds** (32)
      - Embeds `[rewrite]`: how embedding works, plus the provider table (service, content types, URL format) linking to each provider page; troubleshooting and a note on removed providers (Facebook, Instagram, SlideShare, Screencast).
      - Embed block: the generic block for any oEmbed URL.
      - 30 provider pages, one each: Amazon Kindle, Animoto, Bluesky, Cloudup, Crowdsignal, Dailymotion, Flickr, Imgur, Issuu, Kickstarter, Mixcloud, Pinterest, Pocket Casts, Reddit, ReverbNation, Scribd, SmugMug, SoundCloud, Speaker Deck, Spotify, TED, TikTok, Tumblr, X (retitled from Twitter), VideoPress, Vimeo, Wolfram, WordPress, WordPress.tv, YouTube.
- **Site Editor**
  - Site Editor `[rewrite]`: hub; what the Site Editor is, the workspace, links to every task below.
  - Edit your site's header and footer `[new]`: edit, swap or create template parts.
  - Create and edit templates `[rewrite]`: from "Template Editor"; add, edit, assign, reset and delete templates.
  - Styles overview `[rewrite]` (split): how global styles, style variations, Style Book and revisions work.
  - Change colors and fonts with Styles `[new from split]`: task page for palette, typography and style variations.
  - Add custom CSS `[new from split]`: site-wide and per-block CSS.
  - The Font Library: install and manage fonts.
  - Create and manage menus `[rewrite]`: from "Site Editor navigation"; build a menu and place it in the header.
  - Set your site title, logo and icon `[rewrite]` `[merged from: Site Editor Identity, Create a Favicon]`.
  - Set up your homepage `[rewrite]`: from "Additional guide…"; latest posts vs static page, and its template.
  - Site Editor Pages: create and edit pages from the Site Editor.
  - Site Editor Patterns: manage patterns and template parts.
  - Zoom out view: reference.
  - Command Palette: reference.
- **Themes**
  - Find, install and activate a theme `[rewrite]`: from "Work with themes"; theme directory, Live Preview, install, activate; developer material reduced to links.
  - Appearance Themes Screen `[rewrite]`: reference for the screen as it is today.
  - Block themes: concept page; what a block theme is and how it differs from classic.
  - **Default themes** (section intro links to all default themes in the theme directory and to Classic default themes)
    - Twenty Twenty-Five (+ changelog): guide to the current default theme.
    - Twenty Twenty-Four (+ changelog), Twenty Twenty-Three (+ changelog), Twenty Twenty-Two (+ changelog): theme guides.

## Decisions for humans

**Resolved.** Decided by the project owner: inserter-visible = own page. A block that appears as its own item in the block inserter gets its own page, whatever core registers it as (block, variation or taxonomy variation). This settles the earlier open questions on theme-block families, Featured Image and Content inside "Post blocks", one Embeds page vs provider pages, and Row/Stack/Grid inside Group.

1. **Inner blocks consolidated into their container.** Proposed: the 13 blocks the inserter only offers inside a container (Comment Template and its 5 children, Comments Title, Comments Pagination; Post Template, Query Total; Submenu, Custom Link, Home Link) become sections on Comments, Query Loop and Navigation. This is where the inserter rule stops. Alternative: one page each for these too, linked from the container. Redirects to anchors keep URLs alive either way.
2. **Thin pages kept by the inserter rule.** Every inserter item keeps a page, but some widget pages are thin after the trim (Archives 58% boilerplate, Calendar, Tag Cloud), and so are several theme and embed pages. Proposed: write them up rather than merge them. Alternative: keep the pages but ship them as short stubs that link to the parent or Embeds page until rewritten.
3. **Provider list vs what core registers.** The 30 kept provider pages match the embed variations in Gutenberg trunk today. Several services (Cloudup, Crowdsignal, Amazon Kindle) may have changed behaviour without being removed from core; confirm each still embeds before its page is trimmed.
4. **Default themes: keep four per-theme guides vs one Default themes page.** Proposed: keep them; they are real user guides to templates, style variations and patterns, and the changelog nesting already depends on them. Alternative: keep Twenty Twenty-Five only and fold 2022–2024 into the section intro (a table linking to the theme directory), which also simplifies the changelog decision. If a newer default theme (Twenty Twenty-Six) has shipped, a page for it is a gap this proposal does not fill; confirm.
5. **Styles split into three.** Proposed: reference + colour/font task + CSS task. Alternative: keep one long Styles page with a task-shaped table of contents. The split is what produces the "Change colors and fonts with Styles" task page without writing it from scratch.
6. **Pattern submission guide moved off HelpHub.** It describes a wordpress.org service for pattern authors, not site editing. Alternative: merge it into Block Pattern Directory as a "Submit your own" section.
7. **Create a Favicon merged across sections into Site Editor > Identity.** Alternative: keep it under Themes (it is a long-standing, well-searched URL) and link from Identity. The redirect preserves the URL in either case.
8. **Retitles that change familiar names.** "Template Editor" → "Create and edit templates", "Synced Patterns (Reusable blocks)" → "Synced patterns", "Work with themes" → "Find, install and activate a theme". Slugs stay; the question is whether search users still need the old term in the title. Proposed: old term goes in the first paragraph, not the title.
