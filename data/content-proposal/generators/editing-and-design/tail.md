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
