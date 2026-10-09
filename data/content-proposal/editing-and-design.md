# Content proposal: Editing & design

Scope: every article whose `proposed_path` starts with `editing-and-design/` (190 articles: Block editor 167, Site Editor 11, Themes 12 including the four block default themes and their changelogs). Page-level decisions only; the tree in `data/structure.yaml` is unchanged except where a merge or split removes or adds a page inside an existing section. Machine-readable version: `data/content-proposal/editing-and-design.json`.

## Summary

**190 pages now → 114 pages proposed** (−76).

| Action | Count | Notes |
|---|---|---|
| KEEP | 89 | 47 of these are block reference pages that get the mechanical "template trim" below; not counted as REWRITE |
| REWRITE | 18 | 8 are merge targets or family pages that absorb other pages; 10 are freshness or task-orientation rewrites |
| MERGE | 74 | 31 embed providers + generic Embed block → Embeds; 38 theme blocks → 8 family/parent pages; 3 Group variations; Create a Favicon → Identity |
| SPLIT | 1 | Styles overview → 3 pages |
| DELETE | 7 | 3 deprecation/rename stubs, 1 removed variation, 3 dead or removed embeds; all redirect |
| MOVE | 1 | Pattern submission guide → wordpress.org/patterns |
| NEW | 4 | 3 theme-block family pages, 1 Site Editor task page |

Per area:

| Area | Now | Proposed |
|---|---|---|
| Block editor (top level) | 7 | 7 |
| Working with blocks (incl. Block settings) | 20 | 20 |
| Patterns | 5 | 4 |
| Blocks reference (index + 6 families) | 135 | 58 |
| Site Editor | 11 | 14 |
| Themes (incl. default themes and changelogs) | 12 | 11 |

**Template trim (applies to every block reference page that survives).** Delete the hand-written "Go back to the list of Blocks" line (the hierarchy does that), the generic toolbar walkthrough (mover, drag handle, Transform to, More options), the "Block settings panel … click the cog" paragraph, the Advanced settings list and every "Read about these and other settings" note. Replace them with one short "Common tools" line linking to Work with blocks, More options, Moving blocks and the relevant Block settings panel pages. What stays on each block page: what the block does, how it differs from neighbours, its block-specific toolbar buttons and settings, and gotchas. This is mechanical and scriptable against the boilerplate sentences already measured (§2 of `notes/helphub-structure-analysis.md`), so it is not counted as REWRITE.

**Block reference model.** One rule, applied by family:

1. **Content blocks** (blocks people insert directly into posts and pages: Text, Media, Design, Widgets) keep **one page per block**. They are what people search for by name ("table block", "cover block"), each has a distinct workflow, and after the trim they are 300–1,500 words of unique material.
2. **Variations live on their parent block's page.** Row, Stack and Grid → Group; Archive Title and Search Results Title → Query Title; Next/Previous Post → Post Navigation Link; Modified Date → Date; Categories and Tags (Post Terms variations) together; the 31 provider embeds → Embed.
3. **Inner blocks live on their container's page.** The 11 comment inner blocks → Comments block; Post Template → Query Loop; Submenu, Custom Link and Home Link → Navigation.
4. **Theme blocks that only make sense in a template are grouped by what they show**: Post blocks, Post meta blocks, Site identity blocks, Archive title blocks. Theme blocks that are substantive on their own keep a page: Query Loop, Navigation, Template Part, Pagination, Breadcrumbs, Terms Query, Login/out.
5. **Deprecated, renamed or removed blocks get no page**: a redirect plus a row in the "Deprecated blocks" table on the Blocks list.

Result: Text 13, Media 9, Design 9, Widgets 12, Theme 13 (from 51), Embeds 1 (from 36), plus the Blocks list index: **58 pages instead of 135**. Family pages use one H2 per block with a stable anchor matching the old slug (for example `#comment-date-block`), so redirects land on the right section and the Blocks list can link each block by name.

**Where the shared material lives once.** Block toolbar, the Settings/Styles tabs and the settings sidebar: Work with blocks (rewritten as the hub). Inserting: Adding a new block. Moving: Moving blocks. More options menu: More options. Rich text toolbar: More rich text editing options and Link control. Each inspector panel: its Block settings page (Layout, Position, Colors, Background, Typography, Dimensions, Border & Shadow, Filters, Advanced, Responsive styles). Block pages link to these and never restate them.

**Task vs reference.** Block editor top level and the Block settings pages are reference. The Site Editor becomes task-led: the hub page tours the workspace, then routes to "Edit your site's header and footer" (new), "Create and edit templates", "Change colors and fonts with Styles", "Create and manage menus", "Set your site title, logo and icon", "Set up your homepage" and "Manage pages". Most of these come from rewriting or splitting existing pages rather than adding new ones. Themes gets a task page ("Find, install and activate a theme") next to the screen reference and the block-theme concept page.

**Freshness flags found.** Renamed or removed features: Reusable blocks → Synced patterns (two page titles), "Template Editor" (no longer a distinct UI), Post Title → Title, Post Author → Avatar/Author Name, Posts List variation (removed 6.7), SlideShare embed (removed 6.6), Facebook/Instagram embeds (dead since 2020), Twitter → X. Pages untouched since before 2024: `appearance-themes-screen` (2023-01, names Twenty Nineteen as default), `submit-your-block-pattern-to-the-directory` (2023-01). Touched in 2024 only, verify: `additional-guide-to-using-the-site-editor`, `page-break-block`, `login-out-block`, `position-settings-overview`, `dimension-controls-overview`, `filters-settings-overview`, `page-post-settings-sidebar`, `twenty-twenty-two/-three/-four/-five`. Stale "new"/"introduces" framing in pages otherwise current: `site-editor-navigation`, `query-total-block`, `footnotes-block`, `distraction-free-mode`, `block-directory`, `pocket-casts-embed`, `blocks-list`, `work-with-themes` ("Twenty Twenty-Two is the default"). No article in scope is primarily developer documentation; the developer passages inside `work-with-themes` (template files, template hierarchy, cPanel/FTP install, creating themes) are cut to links to developer.wordpress.org as part of its rewrite.

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
| `blocks-list` | Blocks list | REWRITE | Blocks reference index, grouped by family | Must reflect the family model and redirects; drop "new Block Editor" framing. |

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
| `grid-block` | Grid block | MERGE → Group block | Section "Grid" on the Group block page | Grid is a Group variation; its layout settings differ, little else does. |
| `group-block` | Group block | REWRITE | "Group block" incl. Row, Stack and Grid variations | Row, Stack and Grid are Group variations; one page explains the shared container and the layout choice. |
| `more-block` | More block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `page-break-block` | Page Break block | KEEP | Trimmed block reference | Distinct block; last touched 2024-06, verify. |
| `row-block` | Row block | MERGE → Group block | Section "Row" on the Group block page | Row is a Group variation; its layout settings differ, little else does. |
| `separator-block` | Separator block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `spacer-block` | Spacer block | KEEP | Trimmed block reference | Distinct content block users insert directly; keep one page, strip copied toolbar/settings text. |
| `stack-block` | Stack block | MERGE → Group block | Section "Stack" on the Group block page | Stack is a Group variation; its layout settings differ, little else does. |
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
| `archive-title-block` | Archive Title block | MERGE → Archive title blocks | Section on the family page | Query Title variation; 58% boilerplate. |
| `post-author-name-block` | Author Name block | MERGE → Post meta blocks | Section on "Post meta blocks" | Post-context block; 43% boilerplate. |
| `avatar-block` | Avatar block | MERGE → Post meta blocks | Section on "Post meta blocks" | Author/comment context block; settings fit one section. |
| `breadcrumbs-block` | Breadcrumbs block | KEEP | Trimmed block reference | New, substantive block; works on its own. |
| `categories-block` | Categories block | MERGE → Post meta blocks | Section on "Post meta blocks" | Post Terms variation; 43% boilerplate. |
| `comment-author-name-block` | Comment  Author Name block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-content-block` | Comment Content block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-date-block` | Comment Date block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-edit-link-block` | Comment Edit Link block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-reply-link-block` | Comment Reply Link block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-template-block` | Comment Template block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comments-block` | Comments block | REWRITE | Family page: Comments block and its inner blocks | Container for 11 dependent blocks that cannot be used alone; becomes the one comments reference. |
| `comments-count-block` | Comments Count block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-link-block` | Comments Link block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comment-pagination-block` | Comments Pagination block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `comments-title-block` | Comments Title block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `post-content-block` | Content block | MERGE → Post blocks | Section on "Post blocks" | Template-only block; 41% boilerplate. |
| `custom-link-block` | Custom Link block | MERGE → Navigation block | Section "Custom Link" on the Navigation page | Only usable inside the Navigation block. |
| `date-block` | Date Block | MERGE → Post meta blocks | Section on "Post meta blocks" | Date, Post Date and Modified Date now overlap; one section explains all three. |
| `post-excerpt-block` | Excerpt block | MERGE → Post blocks | Section on "Post blocks" | Template-only block; 46% boilerplate. |
| `home-link-block` | Home Link block | MERGE → Navigation block | Section "Home Link" on the Navigation page | Only usable inside the Navigation block. |
| `login-out-block` | Login-out block | KEEP | Trimmed block reference | Standalone block; unlinked and last touched 2024-06, verify. |
| `post-modified-date-block` | Modified Date block | MERGE → Post meta blocks | Section on "Post meta blocks" | Modified Date is a Date variation; 43% boilerplate. |
| `navigation-block` | Navigation block | REWRITE | Navigation block, absorbing Submenu, Custom Link and Home Link | Hub for menus (11 inbound); its child blocks only exist inside it. |
| `next-post-block` | Next Post block | MERGE → Post Navigation Link block | Section on the Post Navigation Link page | Variation of Post Navigation Link; content near-identical. |
| `pagination-block` | Pagination block | KEEP | Trimmed block reference | Distinct, substantive block with its own inner blocks. |
| `post-author-biography-block` | Post Author Biography block | MERGE → Post meta blocks | Section on "Post meta blocks" | Post-context block; small unique content. |
| `post-comments-form-block` | Post Comments Form block | MERGE → Comments block | Section on the Comments block page | Only usable inside the Comments block; page is mostly copied boilerplate. |
| `post-date-block` | Post Date block | MERGE → Post meta blocks | Section on "Post meta blocks" | Overlaps Date block; 42% boilerplate. |
| `post-featured-image-block` | Post Featured Image block | MERGE → Post blocks | Section on "Post blocks" | Template/Query Loop block; unique settings fit one section. |
| `post-navigation-link-block` | Post Navigation Link block | REWRITE | Post Navigation Link block incl. Next Post and Previous Post | Next and Previous Post are its variations; 57% boilerplate today. |
| `post-tags-block` | Post Tags block | MERGE → Post meta blocks | Section on "Post meta blocks" | Post Terms variation; 38% boilerplate. |
| `post-template-block` | Post Template block | MERGE → Query Loop block | Section on the Query Loop page | Inner block of Query Loop only; explained better in context. |
| `post-title-block` | Post Title block | DELETE (redirect → Post blocks) | — | 15-word rename stub (now Title block). |
| `posts-list-block` | Posts List block | DELETE (redirect → Query Loop block) | — | Variation removed in 6.7; page only points to Query Loop. |
| `previous-post-block` | Previous Post block | MERGE → Post Navigation Link block | Section on the Post Navigation Link page | Variation of Post Navigation Link; content near-identical. |
| `query-loop-block` | Query Loop block | REWRITE | Query Loop block, absorbing Post Template and the removed Posts List variation | Key page (23 inbound); Post Template cannot exist outside it. |
| `query-title-block` | Query Title block | REWRITE | Family page: "Archive title blocks" (Query Title, Archive Title, Search Results Title, Term Description, Query Total) | Archive Title and Search Results Title are Query Title variations; all label archive views. |
| `query-total-block` | Query Total block | MERGE → Archive title blocks | Section on the family page | Small archive helper; still written as "6.8 is set to introduce". |
| `read-more-block` | Read More block | MERGE → Post blocks | Section on "Post blocks" | Only meaningful inside Query Loop. |
| `search-results-title-block` | Search Results Title block | MERGE → Archive title blocks | Section on the family page | Query Title variation; only the label differs. |
| `site-logo-block` | Site Logo block | MERGE → Site identity blocks | Section on "Site identity blocks" | Substantive but belongs with title and tagline; links to Identity task. |
| `site-tagline-block` | Site Tagline block | MERGE → Site identity blocks | Section on "Site identity blocks" | 63% boilerplate; same settings as Site Title. |
| `site-title-block` | Site Title block | MERGE → Site identity blocks | Section on "Site identity blocks" | 59% boilerplate; same settings as Site Tagline. |
| `submenu-block` | Submenu block | MERGE → Navigation block | Section "Submenu" on the Navigation page | Only usable inside the Navigation block. |
| `template-part-block` | Template Part block | KEEP | Trimmed block reference | Substantive, low boilerplate, eight inbound links; key to header/footer editing. |
| `term-description-block` | Term Description block | MERGE → Archive title blocks | Section on the family page | Archive-only block; 62% boilerplate, little unique content. |
| `terms-query-block` | Terms Query block | KEEP | Trimmed block reference | New, substantive container block; needs inbound links. |
| `time-to-read-block` | Time to Read block | MERGE → Post blocks | Section on "Post blocks" | Small post-context block. |
| `title-block` | Title block | MERGE → Post blocks | Section on "Post blocks" | 157 words; cannot stand alone. |
| `post-author-block` | (Deprecated) Post Author block | DELETE (redirect → Post meta blocks) | — | 32-word deprecation stub (deprecated in 7.0). |
| `post-blocks` | Post blocks | NEW | Family page: Title, Content, Excerpt, Featured Image, Read More, Time to Read | Template blocks showing post content share context and settings; one page replaces six. |
| `post-meta-blocks` | Post meta blocks | NEW | Family page: Author Name, Author Biography, Avatar, Date, Post Date, Modified Date, Categories, Tags | Small post-context blocks, 25–47% boilerplate; one page replaces eight. |
| `site-identity-blocks` | Site identity blocks | NEW | Family page: Site Title, Site Tagline, Site Logo | Three blocks with near-identical settings; 59–63% boilerplate today. |

### Block editor > Blocks list > Embeds

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `embeds` | Embeds | REWRITE | Embeds: how embedding works, provider table, per-provider notes | One page replaces 36: the provider pages repeat the same paste-URL workflow. |
| `embed-block` | Embed block | MERGE → Embeds | "How to embed" section on Embeds | Generic block and the section index describe the same workflow. |
| `amazon-kindle-embed` | Amazon Kindle Embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Amazon Kindle specifics become a table row or note. |
| `animoto-embed` | Animoto Embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Animoto specifics become a table row or note. |
| `bluesky-embed` | Bluesky embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Bluesky specifics become a table row or note. |
| `cloudup-embed` | Cloudup Embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Cloudup specifics become a table row or note. |
| `crowdsignal-embed` | Crowdsignal embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Crowdsignal specifics become a table row or note. |
| `dailymotion-embed` | Dailymotion embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Dailymotion specifics become a table row or note. |
| `facebook-embed` | Facebook embed | DELETE (redirect → Embeds) | — | oEmbed endpoint closed in 2020; embedding no longer works. One note on Embeds suffices. |
| `flickr-embed` | Flickr embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Flickr specifics become a table row or note. |
| `imgur-embed` | Imgur embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Imgur specifics become a table row or note. |
| `instagram-embed` | Instagram embed | DELETE (redirect → Embeds) | — | oEmbed endpoint closed in 2020; embedding no longer works. One note on Embeds suffices. |
| `issuu-embed` | Issuu embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Issuu specifics become a table row or note. |
| `kickstarter-embed` | Kickstarter embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Kickstarter specifics become a table row or note. |
| `mixcloud-embed` | MixCloud embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Mixcloud specifics become a table row or note. |
| `pinterest-embed` | Pinterest embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Pinterest specifics become a table row or note. |
| `pocket-casts-embed` | Pocket Casts embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Pocket Casts specifics become a table row or note. |
| `reddit-embed` | Reddit embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Reddit specifics become a table row or note. |
| `reverbnation-embed` | ReverbNation embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; ReverbNation specifics become a table row or note. |
| `screencast-block` | Screencast embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Screencast specifics become a table row or note. |
| `scribd-embed` | Scribd embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Scribd specifics become a table row or note. |
| `smugmug-embed` | SmugMug embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; SmugMug specifics become a table row or note. |
| `soundcloud-embed` | SoundCloud embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; SoundCloud specifics become a table row or note. |
| `speaker-deck-embed` | Speaker Deck embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Speaker Deck specifics become a table row or note. |
| `spotify-embed` | Spotify embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Spotify specifics become a table row or note. |
| `ted-embed` | TED embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; TED specifics become a table row or note. |
| `tiktok-embed` | TikTok embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; TikTok specifics become a table row or note. |
| `tumblr-embed` | Tumblr embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Tumblr specifics become a table row or note. |
| `twitter-embed` | Twitter embed | MERGE → Embeds | Row in the provider table | Same workflow as every embed; row should say X (twitter.com/x.com URLs). |
| `videopress-embed` | VideoPress embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; VideoPress specifics become a table row or note. |
| `vimeo-embed` | Vimeo embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Vimeo specifics become a table row or note. |
| `wolfram-embed` | Wolfram embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; Wolfram specifics become a table row or note. |
| `wordpress-embed` | WordPress embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; WordPress specifics become a table row or note. |
| `wordpress-tv-embed-block` | WordPress.tv embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; WordPress.tv specifics become a table row or note. |
| `youtube-embed` | YouTube embed | MERGE → Embeds | Row in the provider table | Same paste-URL workflow as every embed; YouTube specifics become a table row or note. |
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
    - **Design blocks** (9)
      - Accordion, Buttons, Columns, More, Page Break, Separator, Spacer, Tabs: one page each.
      - Group block `[rewrite]` `[merged from: Row, Stack, Grid]`: the container block and its layout variations.
    - **Widget blocks** (12, one page each): Archives, Calendar, Categories List, Custom HTML, Latest Comments, Latest Posts, Page List, RSS, Search, Shortcode, Social Icons, Tag Cloud.
    - **Theme blocks** (13)
      - Site identity blocks `[new]` `[merged from: Site Title, Site Tagline, Site Logo]`: show the site's name, tagline and logo.
      - Post blocks `[new]` `[merged from: Title, Content, Excerpt, Featured Image, Read More, Time to Read]`: show a post's content in templates and Query Loops.
      - Post meta blocks `[new]` `[merged from: Author Name, Author Biography, Avatar, Date, Post Date, Modified Date, Categories, Tags]`: show author, date and terms.
      - Post Navigation Link block `[rewrite]` `[merged from: Next Post, Previous Post]`: link to adjacent posts.
      - Query Loop block `[rewrite]` `[merged from: Post Template]`: list posts by any criteria.
      - Pagination block: page through Query Loop results.
      - Archive title blocks `[rewrite]` `[merged from: Archive Title, Search Results Title, Term Description, Query Total]`: label archive and search views.
      - Terms Query block: list categories, tags or other terms.
      - Comments block `[rewrite]` `[merged from: 10 comment inner blocks and Post Comments Form]`: display and style comments.
      - Navigation block `[rewrite]` `[merged from: Submenu, Custom Link, Home Link]`: reference for the menu block and its items.
      - Template Part block: reference for headers, footers and other parts.
      - Breadcrumbs block: show the visitor's location.
      - Login/out block: add a login or logout link.
    - **Embeds** (1)
      - Embeds `[rewrite]` `[merged from: generic Embed block + 31 provider embed pages]`: how embedding works, provider table (service, content types, URL format, notes), troubleshooting.
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

1. **Theme blocks as families (51 → 13 pages) vs one page per block.** Proposed: group by container or purpose, keep standalone only blocks that are substantive alone. Alternative: keep one page per block and rely on the template trim alone; that leaves about 40 pages of 150–300 unique words each. Middle option: families for Comments and Site identity only (the most templated), everything else per block.
2. **Featured Image and Content inside "Post blocks" vs standalone.** Post Featured Image is searched for by name and has 834 words. Alternative: keep `post-featured-image-block` (and possibly `post-content-block`) as their own pages and make "Post blocks" a lighter family page. Redirects to anchors keep URLs alive either way.
3. **One Embeds page vs a handful of provider pages.** Proposed: one page with a provider table and per-provider notes. Alternative: keep pages for the 3–4 providers with real per-service steps or search demand (YouTube, Vimeo, Spotify, X) and table the rest. The provider list itself needs checking against the embed variations core registers today; several services (Cloudup, Screencast, Crowdsignal, Amazon Kindle) may have changed or closed.
4. **Row, Stack and Grid merged into Group.** They show as separate blocks in the inserter, so people look for them by name. Alternative: keep three short pages that each link to Group for the shared container settings.
5. **Content blocks stay one page per block.** Consistent rule, but some widget pages are thin after the trim (Archives 58% boilerplate, Calendar, Tag Cloud). Alternative: a "Site archive blocks" family (Archives, Calendar, Categories List, Tag Cloud, Latest Posts, Latest Comments).
6. **Default themes: keep four per-theme guides vs one Default themes page.** Proposed: keep them; they are real user guides to templates, style variations and patterns, and the changelog nesting already depends on them. Alternative: keep Twenty Twenty-Five only and fold 2022–2024 into the section intro (a table linking to the theme directory), which also simplifies the changelog decision. If a newer default theme (Twenty Twenty-Six) has shipped, a page for it is a gap this proposal does not fill; confirm.
7. **Styles split into three.** Proposed: reference + colour/font task + CSS task. Alternative: keep one long Styles page with a task-shaped table of contents. The split is what produces the "Change colors and fonts with Styles" task page without writing it from scratch.
8. **Pattern submission guide moved off HelpHub.** It describes a wordpress.org service for pattern authors, not site editing. Alternative: merge it into Block Pattern Directory as a "Submit your own" section.
9. **Create a Favicon merged across sections into Site Editor > Identity.** Alternative: keep it under Themes (it is a long-standing, well-searched URL) and link from Identity. The redirect preserves the URL in either case.
10. **Retitles that change familiar names.** "Template Editor" → "Create and edit templates", "Synced Patterns (Reusable blocks)" → "Synced patterns", "Work with themes" → "Find, install and activate a theme". Slugs stay; the question is whether search users still need the old term in the title. Proposed: old term goes in the first paragraph, not the title.
