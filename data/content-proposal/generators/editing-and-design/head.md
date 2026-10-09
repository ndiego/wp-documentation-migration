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

