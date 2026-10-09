# Content proposal: WordPress overview and Using WordPress

Scope: every article under `overview/` and `using-wordpress/` in `data/structure.yaml` (95), plus the two root pages `site-health` and `update-php` (97 in all). This is a page-level proposal, not a rewrite or a change to the tree. Changelog sections are ignored. Sources: `data/article-facts.json` (dates, word counts, headings, links), a skim of every page whose fate the facts left unclear, and the redirect list of pages already moved to developer.wordpress.org (Advanced Administration).

## Summary

**97 pages now → 70 pages proposed** (in this part of HelpHub; 5 more pages, plus the sysadmin half of one split, move to developer.wordpress.org).

| Action | Pages | Notes |
|---|---|---|
| KEEP | 40 | Mostly screen reference pages and recently maintained task pages |
| REWRITE | 25 | 11 of them also absorb merged pages |
| MERGE | 21 | Into 18 target pages: 3 are new, 1 (Page/Post Settings sidebar) is outside this scope |
| DELETE (redirect) | 5 | Stubs or removed-UI pages whose job a block page already does |
| MOVE | 5 | To developer.wordpress.org (all to Advanced Administration, except post-content processing) |
| SPLIT | 1 | `reset-your-password`: user half stays, database/FTP/WP-CLI half moves |
| NEW | 4 | Write and publish a post, Back up your site, Keep your site secure, Troubleshoot common problems |

What the numbers mean:

- **Screens are fine; topic pages are not.** Of the 34 Administration Screens pages, 25 stay as they are: they are reference pages that match wp-admin, most were touched in a June 2024 sweep, and they are what the screen help tabs link to. The problems are in the topic sections. Maintenance & security has three pages giving the same checklist. Media has four pages that point at one another. Formatting has three thin Codex-era pages. Where to start was written for the Codex.
- **Freshness.** 27 of the 97 pages were last changed before 2024. Every one of them is marked REWRITE, MERGE, DELETE or MOVE here; none is kept as is. Separately, nearly every page in scope has 2018–2019 screenshots, KEEP pages included. Refreshing screenshots is a job for the screenshot-automation pass and is not counted as a REWRITE here.
- **Block-first leftovers.** Six pages in scope still describe classic UI as if it were current. `pages-add-new-screen` covers meta boxes and the Visual/Text tabs. `use-images` describes the Add Media button. `the-wordpress-gallery-block-editor` uses the media-modal gallery flow. `content-visibility-block-editor` and `what-is-an-excerpt-block-editor` refer to the removed Document tab. `administration-screens` still tours Widgets, Menus and Customizer. All six are rewritten, merged or deleted. The "(Block Editor)" suffix comes off every title that survives, because block is now the default and Classic WordPress is the exception.
- **Developer material.** Five pages move whole to developer.wordpress.org. Several more keep their user half and lose a code-heavy section on rewrite: `protect-posts-with-password` (customizing the password form and cookie), `post-status` (custom statuses), `revisions` (constants), `what-is-post-type` (queries and templates), `use-image-and-file-attachments` (theme usage), `settings-privacy-screen` (the "To Theme Developers" section) and `manage-plugins` (Developing Plugins).

## Per-article actions

One table per sub-section in tree order. Every in-scope article appears exactly once; NEW rows use the proposed slug.

### WordPress overview > Where to start

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `get-started-with-wordpress` | Get started with WordPress | REWRITE | Get started with WordPress (ordered learning path) | Pre-install checklist is Codex-era (FTP, text editor); rebuild as the ordered block-first learning path. |
| `first-steps-with-wordpress-block-editor` | First steps with WordPress (Block Editor) | REWRITE | First steps with WordPress | Tour still points at widgets and older screens; rebuild around a block theme; drop '(Block Editor)' from the title. |
| `wordpress-semantics` | WordPress Semantics | REWRITE | Key WordPress concepts | Codex-era essay (The Loop, template tags, Header tool); rewrite as 'Key WordPress concepts' for the block era. |
| `introduction-to-blogging` | Introduction to Blogging | MERGE → Key WordPress concepts | Section of “Key WordPress concepts” | Blog-versus-CMS framing is one section of a concepts page; untouched since 2023. |
| `wordpress-glossary` | WordPress Glossary | REWRITE | WordPress Glossary (user terms only) | 12,500 words dominated by developer terms (Ajax, Array, Apache); prune to terms users meet. |
| `where-to-find-wordpress-help` | Where to find WordPress help | REWRITE | Where to find WordPress help | Untouched since 2023; web-search advice is dated; keep forums, Learn and docs pointers. |

### WordPress overview > About WordPress

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `learn-about-wordpress-and-version-history` | Learn about WordPress origins and version history | KEEP | Unchanged | Maintained every release; narrative history is distinct from the version tables. |
| `difference-between-wordpress-org-and-wordpress-com` | What's the difference between WordPress.org and WordPress.com? | KEEP | Unchanged | Recurring first-day confusion; content still accurate. |
| `wordpress-versions` | WordPress Versions | KEEP | Unchanged | Reference table maintained every release; absorbs the support policy. |
| `wordpress-versions-0-7-to-4-9` | WordPress Versions 0.7 to 4.9 | KEEP | Unchanged | Archive table split from WordPress Versions for length; pure reference. |
| `supported-versions` | Supported Versions | MERGE → WordPress Versions | Section of “WordPress Versions” | 192-word policy statement; reads naturally as a 'Support policy' section of Versions. |
| `become-a-wordpress-contributor` | Become a WordPress contributor | KEEP | Unchanged | Current (2026) and the only user-facing route into contributing. |

### WordPress overview > Frequently asked questions

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `faq-work-with-wordpress` | FAQ Work with WordPress | DELETE (redirect → Get started with WordPress) | Removed; 301 to “Get started with WordPress” | Link list to other pages with Codex links and dead 'Ideas' site; answers belong in task pages. |
| `faq-installation` | FAQ Installation | MOVE → developer.wordpress.org (Advanced Administration > Before you install) | Leaves HelpHub; 301 to new home | wp-config, databases, 403 errors, cPanel: sysadmin material next to the install guide already there. |
| `faq-troubleshooting` | FAQ Troubleshooting | MOVE → developer.wordpress.org (Advanced Administration > Common errors) | Leaves HelpHub; 301 to new home | phpMyAdmin, wp_options edits, MySQL repair; user-level parts go to 'Troubleshoot common problems'. |
| `faq-i-make-changes-and-nothing-happens` | FAQ I make changes and nothing happens | MERGE → Troubleshoot common problems | Section of “Troubleshoot common problems” [new] | Caching is the first item of a user troubleshooting page, not a page of its own. |
| `faq-my-site-was-hacked` | FAQ My site was hacked | KEEP | Unchanged | Current (2026) crisis task page that users reach from search. |
| `troubleshoot-common-problems` | Troubleshoot common problems | NEW | New page | No user-level first aid: cache, recovery mode, plugin/theme conflicts, Site Health, where to ask. |

### Using WordPress > Administration Screens

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `administration-screens` | Administration Screens | REWRITE | Administration Screens (short menu hub) | 3,260-word tour still covering Widgets, Menus, Customizer and Codex links; make it a short hub of today's menu. |
| `toolbar` | Toolbar | MERGE → Administration Screens | Section of “Administration Screens” | 148 words and a 2019 screenshot; one section of the admin overview. |

### Using WordPress > Administration Screens > Dashboard

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `dashboard-screen` | Dashboard screen | KEEP | Unchanged | Reference for the landing screen; widget list still accurate; screenshots need refresh. |
| `dashboard-updates-screen` | Dashboard Updates screen | KEEP | Unchanged | Screen reference; the how-to lives in the update task page. |

### Using WordPress > Administration Screens > Posts

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `posts-screen` | Posts screen | KEEP | Unchanged | Reference for the posts list table. |
| `posts-categories-screen` | Posts Categories screen | KEEP | Unchanged | Reference; current (2026). |
| `posts-tags-screen` | Posts Tags screen | KEEP | Unchanged | Reference; current (2026). |

### Using WordPress > Administration Screens > Media

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `media-library-screen` | Media Library screen | KEEP | Unchanged | Reference for grid and list views; well linked. |
| `media-add-new-screen` | Media Add New screen | KEEP | Unchanged | Reference for the upload screen; well linked. |

### Using WordPress > Administration Screens > Pages

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `pages-screen` | Pages screen | KEEP | Unchanged | Reference for the pages list table. |
| `pages-add-new-screen` | Pages Add New screen | DELETE (redirect → WordPress Block Editor) | Removed; 301 to “WordPress Block Editor” | Describes the classic edit screen (meta boxes, Visual/Text tabs); Classic Editor section covers it. |

### Using WordPress > Administration Screens > Plugins

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `introduction-to-plugins` | Introduction to Plugins | MERGE → Manage Plugins | Section of “Manage Plugins” | 278 words from 2023 repeating Manage Plugins' 'What are plugins?'. |
| `manage-plugins` | Manage Plugins | REWRITE | Manage Plugins (task page) | Main plugin task page; drop 'Developing Plugins', stop repeating the two screen pages. |
| `plugins-screen` | Plugins screen | KEEP | Unchanged | Reference; current (2026). |
| `plugins-add-new-screen` | Plugins Add New screen | KEEP | Unchanged | Reference for searching, uploading and favourites. |

### Using WordPress > Administration Screens > Users

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `users-screen` | Users screen | KEEP | Unchanged | Reference for the users list table. |
| `users-add-new-screen` | Users Add New screen | KEEP | Unchanged | Reference for adding a user. |
| `users-your-profile-screen` | Users Your Profile screen | KEEP | Unchanged | Reference; well linked. |

### Using WordPress > Administration Screens > Tools

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `tools-screen` | Tools screen | MERGE → Tools Import screen | Section of “Tools Import screen” | 26 words; its only tool points to the Import screen. |
| `tools-import-screen` | Tools Import screen | REWRITE | Tools Import screen (incl. Available Tools) | 2019 importer list (Blogroll, LiveJournal) is dated; absorbs the Tools screen. |
| `tools-export-screen` | Tools Export screen | KEEP | Unchanged | Reference; still accurate. |
| `site-health-screen` | Site Health screen | KEEP | Unchanged | Current (2026) reference; absorbs the root Site Health page. |
| `tools-export-personal-data-screen` | Tools Export Personal Data screen | KEEP | Unchanged | Reference for a privacy tool; drop '4.9.6 included' framing on next edit. |
| `tools-erase-personal-data-screen` | Tools Erase Personal Data screen | KEEP | Unchanged | Reference; touched 2025. |
| `appearance-theme-file-editor-screen` | Appearance Theme File Editor Screen | MOVE → developer.wordpress.org (Advanced Administration, beside the Plugin File Editor) | Leaves HelpHub; 301 to new home | Editing theme PHP/CSS is developer work; the plugin editor page already moved there. |
| `tools-network-screen` | Tools Network screen | MOVE → developer.wordpress.org (Advanced Administration > Multisite) | Leaves HelpHub; 301 to new home | Needs wp-config edits; 'Create a network' already lives in Advanced Administration. |

### Using WordPress > Administration Screens > Settings

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `settings-general-screen` | Settings General screen | KEEP | Unchanged | Reference; current (2026). |
| `settings-writing-screen` | Settings Writing screen | KEEP | Unchanged | Reference; options still match core. |
| `settings-reading-screen` | Settings Reading screen | KEEP | Unchanged | Reference; front-page task lives in its own page. |
| `settings-discussion-screen` | Settings Discussion screen | KEEP | Unchanged | Reference; current (2026). |
| `settings-media-screen` | Settings Media screen | KEEP | Unchanged | Reference; heavily linked from media pages. |
| `settings-permalinks-screen` | Settings Permalinks screen | REWRITE | Settings Permalinks screen (incl. choosing a structure) | Absorbs Customize permalinks so permalink structures are explained once. |
| `settings-privacy-screen` | Settings Privacy screen | REWRITE | Settings Privacy screen | 2019; drop the 'To Theme Developers' section and the overlap with WordPress Privacy. |
| `settings-connectors-screen` | Settings Connectors screen | KEEP | Unchanged | New 2026 screen; current. |

### Using WordPress > Writing & publishing

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `write-and-publish-a-post` | Write and publish a post | NEW | New page | No block-era page walks draft, preview, schedule, publish; the core first-post task. |
| `create-pages` | Create pages | REWRITE | Create pages | Untouched since 2023; mixes concepts, list screen and PHP templates; make it a block-theme task. |
| `post-status` | Post Status | MERGE → Write and publish a post | Section of “Write and publish a post” [new] | User-facing statuses become a section; custom statuses and code references are developer material. |
| `content-visibility-block-editor` | Set blog content visibility (Block Editor) | REWRITE | Control who can see a post | 2018 screenshots of the removed 'Document' tab; absorbs password protection; retitle 'Control who can see a post'. |
| `protect-posts-with-password` | Protect posts with password | MERGE → Control who can see a post | Section of “Control who can see a post” | Duplicates the visibility page; form-text and cookie customizations are code (drop or send to developer docs). |
| `what-is-an-excerpt-block-editor` | What is an excerpt? (Block Editor) | MERGE → Page/Post Settings sidebar | Section of “Page/Post Settings sidebar” | 132 words; excerpt is one panel of the settings sidebar; feed advice conflates concepts. |
| `revisions` | Revisions | KEEP | Unchanged | Current (2026-09); move constant/storage sections to developer docs on next edit. |

### Using WordPress > Writing & publishing > Organizing your site

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `what-is-post-type` | What is Post Type? | MERGE → Key WordPress concepts | Section of “Key WordPress concepts” | User half is posts versus pages; template files and queries are developer material. |
| `taxonomies` | Taxonomies | REWRITE | Categories and tags | 2023, developer-leaning; becomes 'Categories and tags', the user task for organizing posts. |
| `assign-custom-fields` | Assign custom fields | KEEP | Unchanged | Current (2026) and block-editor aware. |
| `customize-permalinks` | Customize permalinks | MERGE → Settings Permalinks screen | Section of “Settings Permalinks screen” | Repeats the permalink structures listed on the screen page; one concept, once. |
| `create-a-static-front-page` | Create a static front page | KEEP | Unchanged | Current task page with videos. |
| `create-a-search-page` | Create a search page | DELETE (redirect → Search block) | Removed; 301 to “Search block” | 125 words; block themes ship a search template and the Search block page covers the rest. |
| `customize-date-and-time-format` | Customize date and time format | REWRITE | Customize date and time format | Leads with the_date()/the_time(); refocus on format strings in Settings and the Date block. |
| `search-engine-optimization` | Search Engine Optimization | REWRITE | Search engine optimization | Codex-era submission advice; refocus on built-in features (permalinks, sitemaps, search visibility). |

### Using WordPress > Writing & publishing > Formatting & special characters

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `what-are-emoji` | What are Emoji? | REWRITE | Emoji, smilies and special characters | Becomes 'Emoji, smilies and special characters', the one page for this topic. |
| `what-are-smilies` | What are smilies? | MERGE → Emoji, smilies and special characters | Section of “Emoji, smilies and special characters” | Untouched since 2023; the settings toggle is gone; one short section is enough. |
| `use-character-entities` | Use character entities | MERGE → Emoji, smilies and special characters | Section of “Emoji, smilies and special characters” | Untouched since 2023; HTML entity tables; the editor inserts characters directly. |
| `how-wordpress-processes-post-content` | How WordPress processes Post Content | MOVE → developer.wordpress.org | Leaves HelpHub; 301 to new home | wpautop and texturize filters; developer material written for the Visual editor. |

### Using WordPress > Media

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `use-images` | Use Images | REWRITE | Add and manage media | 230-word link hub describing the classic 'Add Media' button; becomes 'Add and manage media'. |
| `use-image-and-file-attachments` | Use image and file attachments | MERGE → Add and manage media | Section of “Add and manage media” | Attachments and link options are sections of the media task; theme usage is developer material. |
| `inserting-images-into-posts-and-pages-block-editor` | Inserting images into posts and pages (Block Editor) | DELETE (redirect → Image block) | Removed; 301 to “Image block” | Stub that already defers to the Image block page. |
| `the-wordpress-gallery-block-editor` | The WordPress Gallery (Block Editor) | DELETE (redirect → Gallery block) | Removed; 301 to “Gallery block” | 2019 media-modal workflow no longer matches the Gallery block, which has its own page. |
| `edit-media` | Edit Media | KEEP | Unchanged | Reference for the edit media page; touched 2024. |
| `image-size-and-quality` | Image size and quality | REWRITE | Image size and quality | 2023; ignores generated sizes, responsive images and modern formats. |

### Using WordPress > Comments

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `comments-in-wordpress` | Comments in WordPress | REWRITE | Turn on and manage comments | Overlaps Comments screen and Discussion settings; make it the 'turn on and manage comments' task. |
| `comment-moderation` | Comment moderation | KEEP | Unchanged | Current (2026) task page. |
| `understand-comment-spam` | Understanding comment spam | KEEP | Unchanged | Current (2026) concept page. |
| `trackbacks-and-pingbacks` | Trackbacks and Pingbacks | KEEP | Unchanged | Accurate concept reference; touched 2025. |
| `comments-screen` | Comments screen | REWRITE | Comments screen | Untouched since January 2023, 2019 screenshots; refresh as reference. |

### Using WordPress > Users, roles & profiles

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `roles-and-capabilities` | Roles and Capabilities | KEEP | Unchanged | Current (2026); users look up what each role can do. |
| `use-gravatars` | Use Gravatars | KEEP | Unchanged | Current (2026). |
| `reset-your-password` | Reset your password | SPLIT → Reset your password; Reset a password without email access (developer.wordpress.org) | User half stays; sysadmin half moves | Lost-password flow is a user task; MySQL, phpMyAdmin, FTP and WP-CLI methods are sysadmin. |
| `troubleshoot-login-issues` | Troubleshoot login issues | MERGE → Reset your password | Section of “Reset your password” | 200 words from 2023; cookie and firewall tips fit the login help page. |

### Using WordPress > Installation & hosting

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `hosting-wordpress` | Hosting WordPress | REWRITE | Choose a host and install WordPress | 264 words from 2023; becomes 'Choose a host and install WordPress', linking the developer install guide. |
| `use-automated-installation` | Use automated installation | MERGE → Choose a host and install WordPress | Section of “Choose a host and install WordPress” | 2018 screenshots of Fantastico/APS; one-click installers deserve a paragraph, not a page. |

### Using WordPress > Maintenance & security

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `administer-your-blog` | Administer your Blog | MERGE → Maintain your site | Section of “Maintain your site” | Codex-era routine with Codex links; third page covering the same maintenance checklist. |
| `wordpress-housekeeping` | WordPress Housekeeping | MERGE → Maintain your site | Section of “Maintain your site” | Same checklist as the maintenance page (update, prune plugins/themes, clean database). |
| `wordpress-site-maintenance` | WordPress site maintenance | REWRITE | Maintain your site | Target of three overlapping pages; drop raw SQL and dead link-checker lists; retitle 'Maintain your site'. |
| `updating-wordpress` | Updating WordPress | REWRITE | Update WordPress, plugins and themes | Manual FTP update duplicates the developer guide; absorb auto-updates; retitle 'Update WordPress, plugins and themes'. |
| `plugins-themes-auto-updates` | Plugin and themes auto-updates | MERGE → Update WordPress, plugins and themes | Section of “Update WordPress, plugins and themes” | Untouched since January 2023; auto-updates are one section of the update task. |
| `recovery-mode` | Recovery Mode | KEEP | Unchanged | Current (2025) recovery task page. |
| `password-best-practices` | Password Best Practices | KEEP | Unchanged | Current (2026) and stands alone. |
| `why-should-i-use-https` | Why should I use HTTPS | MERGE → Keep your site secure | Section of “Keep your site secure” [new] | 334 words from 2023; one section of a security overview. |
| `wordpress-privacy` | WordPress Privacy | REWRITE | WordPress Privacy (overview) | Repeats the three privacy screen pages; make it the overview that links to them. |
| `back-up-your-site` | Back up your site | NEW | New page | Every update page says 'back up first' but the only backup guide is the developer manual-backup page. |
| `keep-your-site-secure` | Keep your site secure | NEW | New page | No user security overview since hardening moved to developer docs; absorbs HTTPS. |

### Root pages

| Slug | Title | Action | Result / target | Why (≤ 20 words) |
|---|---|---|---|---|
| `site-health` | Site Health: keep your website healthy | MERGE → Site Health screen | Section of “Site Health screen” | 2019 promo page duplicating the Site Health screen; redirect keeps the URL working. |
| `update-php` | Get a faster, more secure website: update your PHP today | REWRITE | Update your PHP version (same URL) | Linked from wp-admin PHP notices; PHP 7.4/5.6 figures and Codex link are stale. Keep the URL. |
## Proposed end state

Page titles are proposed titles; slugs are kept unless marked [new]. "[merged from: …]" lists the slugs that fold in.

- **WordPress overview > Where to start**
  - Get started with WordPress [rewrite]: the ordered path (try it, choose a host, install, first steps, first post, get help), not a reading list.
  - First steps with WordPress [rewrite]: after install, a tour of a fresh site with a block theme (log in, dashboard, Site Editor, first settings).
  - Key WordPress concepts [rewrite, merged from: wordpress-semantics, introduction-to-blogging, what-is-post-type]: posts and pages, blocks and patterns, themes and templates, plugins, users.
  - WordPress Glossary [rewrite]: terms users meet; developer terms point to developer.wordpress.org.
  - Where to find WordPress help [rewrite]: forums, Learn, docs, local meetups, and how to ask a good question.
- **WordPress overview > About WordPress**
  - Learn about WordPress origins and version history: narrative history.
  - What's the difference between WordPress.org and WordPress.com?: the self-hosted versus hosted service distinction.
  - WordPress Versions [merged from: supported-versions]: release tables plus support policy.
  - WordPress Versions 0.7 to 4.9: archive table.
  - Become a WordPress contributor: ways to give back.
- **WordPress overview > Frequently asked questions**
  - Troubleshoot common problems [new, merged from: faq-i-make-changes-and-nothing-happens, user parts of faq-troubleshooting]: user-level first aid before the support forum.
  - My site was hacked: what to do right now.
- **Using WordPress > Administration Screens**
  - Administration Screens [rewrite, merged from: toolbar]: short hub mirroring today's admin menu (with block theme), toolbar, screen options, help tab.
  - Dashboard: Dashboard screen; Dashboard Updates screen.
  - Posts: Posts screen; Posts Categories screen; Posts Tags screen.
  - Media: Media Library screen; Media Add New screen.
  - Pages: Pages screen.
  - Plugins: Manage Plugins [rewrite, merged from: introduction-to-plugins] (the plugin task: find, install, update, remove); Plugins screen; Plugins Add New screen.
  - Users: Users screen; Users Add New screen; Users Your Profile screen.
  - Tools: Tools Import screen [rewrite, merged from: tools-screen]; Tools Export screen; Site Health screen [merged from: site-health]; Tools Export Personal Data screen; Tools Erase Personal Data screen.
  - Settings: General; Writing; Reading; Discussion; Media; Permalinks [rewrite, merged from: customize-permalinks]; Privacy [rewrite]; Connectors.
- **Using WordPress > Writing & publishing**
  - Write and publish a post [new, merged from: post-status]: draft, preview, schedule, publish, update; what each status means.
  - Create pages [rewrite]: create, nest and template pages with a block theme.
  - Control who can see a post [rewrite, merged from: protect-posts-with-password]: public, private, password-protected; hiding a whole site.
  - Revisions: compare and restore.
  - *Organizing your site*: Categories and tags [rewrite]; Assign custom fields; Create a static front page; Customize date and time format [rewrite]; Search engine optimization [rewrite].
  - *Formatting & special characters*: Emoji, smilies and special characters [rewrite, merged from: what-are-smilies, use-character-entities].
- **Using WordPress > Media**
  - Add and manage media [rewrite, merged from: use-images, use-image-and-file-attachments]: upload from a block or the library, attachments, link options, supported file types.
  - Edit Media: the edit media page.
  - Image size and quality [rewrite]: what WordPress generates, choosing upload sizes, formats.
- **Using WordPress > Comments**
  - Turn on and manage comments [rewrite]: enable or close comments site-wide and per post, then the daily routine.
  - Comment moderation; Understanding comment spam; Trackbacks and Pingbacks; Comments screen [rewrite].
- **Using WordPress > Users, roles & profiles**
  - Roles and Capabilities; Use Gravatars.
  - Reset your password [split, merged from: troubleshoot-login-issues]: lost-password flow, admin resets, cookie and firewall issues; links the sysadmin methods.
- **Using WordPress > Installation & hosting**
  - Choose a host and install WordPress [rewrite, merged from: use-automated-installation]: requirements in plain words, one-click installers, link to the manual guide.
- **Using WordPress > Maintenance & security**
  - Maintain your site [rewrite, merged from: administer-your-blog, wordpress-housekeeping]: a periodic checklist.
  - Update WordPress, plugins and themes [rewrite, merged from: plugins-themes-auto-updates]: one-click and automatic updates; manual update links out.
  - Back up your site [new]: host backups, backup plugins, testing a restore; manual methods link out.
  - Keep your site secure [new, merged from: why-should-i-use-https]: updates, passwords, HTTPS, trusted plugins, two-factor sign-in, what to do if hacked.
  - Recovery Mode; Password Best Practices.
  - WordPress Privacy [rewrite]: overview of privacy duties and the three privacy tools.
- **Root pages**
  - Update your PHP version [rewrite]: keeps `/update-php/` because wp-admin links to it.

Leaves HelpHub: faq-installation, faq-troubleshooting (sysadmin parts), appearance-theme-file-editor-screen, tools-network-screen, how-wordpress-processes-post-content and the sysadmin half of reset-your-password, all to developer.wordpress.org. Redirect only: faq-work-with-wordpress, pages-add-new-screen, create-a-search-page, inserting-images-into-posts-and-pages-block-editor, the-wordpress-gallery-block-editor.

## Decisions for humans

1. **Which way the permalinks merge goes.** Proposed: `customize-permalinks` merges into `settings-permalinks-screen`. That keeps the Settings screens a complete mirror of wp-admin, and it is the page the screen's help tab links to. *Alternative:* keep `customize-permalinks` as the task page under Organizing your site and cut the screen page down to a short reference that links to it. Either way, the list of structures appears once.
2. **Moving the Theme File Editor screen.** Proposed: MOVE, because editing theme PHP and CSS is developer work and the Plugin File Editor page already went to Advanced Administration. *Alternative:* keep it in Tools, because it is a real wp-admin screen and the Tools section mirrors the menu. Either way it gets a strong warning and a link to child themes and the Site Editor.
3. **Deleting `pages-add-new-screen`.** Proposed: delete it and redirect to the block editor page. *Alternative:* move it into Classic WordPress > Classic Editor, beside `write-posts-classic-editor`. Its content duplicates that page, but Classic Editor users would land on a page that matches their screen.
4. **Thinning the FAQ section.** Moving the installation and troubleshooting FAQs, and deleting `faq-work-with-wordpress`, leaves two pages: the new Troubleshoot common problems and My site was hacked. *Alternative:* keep FAQ Installation and FAQ Troubleshooting with only their user questions (language, renaming the folder, the maintenance message). Or put the new troubleshooting page in Maintenance & security and dissolve FAQ in a later structure pass.
5. **Merging `post-status` into a new first-post page.** Proposed: the user-facing statuses become a section of Write and publish a post. *Alternative:* keep Post Status as a short reference page, rewritten without the developer statuses. It has no inbound links, so a merge loses nothing.
6. **Rewriting the Glossary rather than splitting it.** At 12,500 words it is by far the largest page in scope. Proposed: prune the developer terms and link to developer.wordpress.org. *Alternative:* SPLIT into a user glossary and a developer glossary moved to developer.wordpress.org, if that site will take one.
7. **Keeping both version tables and the history page.** Proposed: KEEP `learn-about-wordpress-and-version-history`, `wordpress-versions` and `wordpress-versions-0-7-to-4-9` (folding only `supported-versions` in). *Alternative:* merge the 0.7–4.9 archive into WordPress Versions, or turn the 3,600-word history page (it has no H2s) into per-era sections of the Versions page. That needs the release team, who maintain these pages.
8. **Folding `site-health` into Site Health screen.** Proposed: merge and redirect. *Alternative:* keep it as a short root landing page if any core or wp-admin string still links to `/documentation/site-health/`. Check core before redirecting. `update-php` stays at its root URL for exactly that reason (`wp_get_update_php_url()`).
9. **Four new pages.** All four fill gaps on the main user journey. Write and publish a post is the first-post task. Back up your site, Keep your site secure and Troubleshoot common problems exist because "back up first", "stay secure" and "try deactivating plugins" are advice repeated across many pages with no user-level page behind them. *Alternative:* don't create Keep your site secure and Back up your site; instead give Maintain your site a fuller security and backup section. That means fewer pages, but neither topic can then be found from search.
