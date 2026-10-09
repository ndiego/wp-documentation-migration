"""Per-article decisions for the Editing & design content proposal. Loaded by gen.py."""
K='KEEP';R='REWRITE';M='MERGE';S='SPLIT';X='DELETE';MV='MOVE'
TRIM='Trimmed block reference'
D={}
def d(slug,a,t,res,why): D[slug]=[a,t,res,why]
# Block editor top level
d('wordpress-block-editor',K,None,'Block editor overview (section opener)','Current (2026-09) overview of the editor workspace; the natural entry point for the section.')
d('page-post-settings-sidebar',K,None,'Reference: post/page settings sidebar','Substantive reference, well linked; verify against current sidebar, last touched 2024-10.')
d('preferences-overview',K,None,'Reference: editor preferences','Unique reference; six inbound links; current.')
d('how-to-use-the-preview-function',K,None,'Task: preview a post or page','Distinct task; current. Consider slug alias matching the "View" title.')
d('distraction-free-mode',K,None,'Reference: Distraction Free mode','Current, distinct feature; drop the "new" framing.')
d('keyboard-shortcuts-block-editor',K,None,'Reference: keyboard shortcuts','Pure reference, current; classic counterpart already lives in Classic WordPress.')
d('notes',K,None,'Task: leave and resolve Notes','New 7.0 collaboration feature, current; needs inbound links from editor overview.')
# Working with blocks
d('work-with-blocks',R,None,'Hub for the shared block material (toolbar, settings sidebar, Settings/Styles tabs)','Becomes the single home for the toolbar and settings blurbs repeated on 100+ block pages; trim duplicated how-tos.')
d('adding-a-new-block',K,None,'Task: add a block','Shared concept with 122 inbound links; block pages link here instead of repeating it.')
d('moving-blocks',K,None,'Task: move blocks','Shared concept (80 inbound); replaces the Moving-blocks blurb copied into 54 pages.')
d('list-view',K,None,'Reference: List View','Current, distinct tool.')
d('more-options',K,None,'Reference: block More options menu','Shared concept (121 inbound); replaces the More options paragraph copied into block pages.')
d('link-editing',K,None,'Reference: Link control','Shared concept used by many text blocks; current.')
d('more-text-editing-overview',K,None,'Reference: rich text toolbar options','Shared concept (17 inbound); text block pages link here.')
d('page-jumps',K,None,'Task: link to a section (HTML anchors)','Real user task; current.')
d('block-directory',K,None,'Task: install blocks from the Block Directory','Core feature, user-facing; drop the "new way" framing.')
d('block-error-unexpected-or-invalid-content',K,None,'Troubleshooting: invalid block content','Unique troubleshooting page; needs inbound links from Work with blocks.')
# Block settings
for s,why in [('layout-settings-overview','Maps 1:1 to an inspector panel; shared target for block pages.'),
 ('colors-settings-overview','Shared panel reference (65 inbound); current.'),
 ('background-settings-overview','Maps to an inspector panel; current.'),
 ('typography-settings-overview','Shared panel reference (75 inbound); current.'),
 ('border-settings-overview','Shared panel reference (50 inbound); current enough (2025-04).'),
 ('advanced-settings-overview','Shared panel reference (117 inbound); replaces the Advanced list copied into 46 pages.'),
 ('responsive-styles','New feature, current; add inbound links from panel pages.')]:
    d(s,K,None,'Reference: block settings panel',why)
d('position-settings-overview',K,None,'Reference: Position panel','One page per inspector panel; stale (2024-06) and unlinked, verify sticky options.')
d('dimension-controls-overview',K,None,'Reference: Dimensions panel','Shared panel reference (73 inbound); last touched 2024-06, verify controls.')
d('filters-settings-overview',K,None,'Reference: Filters (duotone) panel','Short but maps to a real panel; last touched 2024-06, verify.')
# Patterns
d('block-pattern',K,None,'Task + concept: use and create patterns','Core concept page with 16 inbound links; current.')
d('reusable-blocks',R,None,'"Synced patterns" (title drops "Reusable blocks"; adds pattern overrides)','Feature renamed in 6.3; title and framing still lead with the old name.')
d('comparing-patterns-template-parts-and-reusable-blocks',R,None,'"Patterns, synced patterns and template parts compared"','Useful decision aid, but title and text still centre on Reusable blocks.')
d('block-pattern-directory',K,None,'Task: find and insert patterns from the directory','User-facing, current.')
d('submit-your-block-pattern-to-the-directory',MV,'wordpress.org/patterns (Pattern Directory help pages)','—','Contributor workflow for a wordpress.org service, not site editing; untouched since 2023-01.')
# Blocks list index
d('blocks-list',R,None,'Blocks reference index, grouped by family','Groups pages by family, lists variations under their parent, holds the redirects; drop "new Block Editor" framing.')
# Text blocks: one page each
for s in ['code-block','details-block','heading-block','list-block','math-block','paragraph-block','preformatted-block','pullquote-block','quote-block','table-block','verse-block']:
    d(s,K,None,TRIM,'Distinct content block users insert directly; keep one page, strip copied toolbar/settings text.')
d('classic-block',K,None,TRIM,'Still needed for legacy content; short and template-heavy, trim to what is unique.')
d('footnotes-block',K,None,TRIM,'Distinct block; drop "WordPress 6.3 introduces" framing.')
# Media
for s in ['audio-block','cover-block','file-block','gallery-block','image-block','media-text-block','playlist-block','video-block','icon-block']:
    d(s,K,None,TRIM,'Distinct content block users insert directly; keep one page, strip copied toolbar/settings text.')
# Design
for s in ['accordion-block','buttons-block','columns-block','more-block','separator-block','spacer-block','tabs-block']:
    d(s,K,None,TRIM,'Distinct content block users insert directly; keep one page, strip copied toolbar/settings text.')
d('page-break-block',K,None,TRIM,'Distinct block; last touched 2024-06, verify.')
d('group-block',R,None,'"Group block": the container, linking to Row, Stack and Grid','Shared container settings live here once; Row, Stack and Grid pages link back instead of repeating them.')
for s,n in [('row-block','Row'),('stack-block','Stack'),('grid-block','Grid')]:
    d(s,K,None,TRIM,n+' is its own inserter item (Group variation); own page per the inserter rule, shared settings link to Group.')
d('button-block',X,'Buttons block','—','21-word deprecation stub.')
# Widgets
for s in ['archives-block','calendar-block','categories-list-block','custom-html','latest-comments-block','latest-posts-block','page-list-block','rss-block','search-block','shortcode-block','social-icons','tag-cloud-block']:
    d(s,K,None,TRIM,'Distinct block usable in any post or template; keep one page, strip copied toolbar/settings text.')
# Theme blocks
# INSERTER RULE (project owner): a block gets its own page if it appears as its own item in the block
# inserter, regardless of how core registers it (block, variation with scope 'inserter', taxonomy variation).
# Boundary: blocks with `parent`/`ancestor` in block.json only appear inside their container, so they stay
# merged into the container's page (Comment Template children, Comments Title/Pagination, Post Template,
# Query Total, Navigation children). Checked against Gutenberg trunk block.json / variations.js, 2026-10-09.
OWN=' is its own inserter item; own page per the inserter rule.'
CM='Comments block'
d('comments-block',R,None,'Comments block, absorbing Comment Template and its inner blocks, Comments Title and Comments Pagination','Container for 8 blocks restricted to it (parent/ancestor); becomes the one reference for them.')
for s in ['comment-author-name-block','comment-content-block','comment-date-block','comment-edit-link-block','comment-reply-link-block','comment-template-block','comment-pagination-block','comments-title-block']:
    d(s,M,CM,'Section on the Comments block page','Only insertable inside the Comments block (parent/ancestor); page is mostly copied boilerplate.')
for s,n in [('comments-count-block','Comments Count'),('comment-link-block','Comments Link'),('post-comments-form-block','Comments Form')]:
    d(s,K,None,TRIM,n+' is its own inserter item (no parent restriction); own page per the inserter rule.')
d('query-loop-block',R,None,'Query Loop block, absorbing Post Template, Query Total and the removed Posts List variation','Key page (23 inbound); Post Template and Query Total only exist inside it.')
d('post-template-block',M,'Query Loop block','Section on the Query Loop page','Inner block of Query Loop only; explained better in context.')
d('query-total-block',M,'Query Loop block','Section on the Query Loop page','Ancestor-restricted to Query Loop; still written as "6.8 is set to introduce".')
d('posts-list-block',X,'Query Loop block','—','Variation removed in 6.7; page only points to Query Loop.')
d('pagination-block',K,None,TRIM,'Distinct, substantive block with its own inner blocks.')
d('query-title-block',R,None,'Query Title block: shared settings, linking to Archive Title and Search Results Title','Becomes the shared reference its two inserter variations link to; drop duplicated variation text.')
for s,n in [('archive-title-block','Archive Title'),('search-results-title-block','Search Results Title')]:
    d(s,K,None,TRIM,n+' is its own inserter item (Query Title variation); own page per the inserter rule.')
d('term-description-block',K,None,TRIM,'Term Description'+OWN)
d('navigation-block',R,None,'Navigation block, absorbing Submenu, Custom Link and Home Link','Hub for menus (11 inbound); its child blocks only exist inside it (parent restriction).')
for s,n in [('submenu-block','Submenu'),('custom-link-block','Custom Link'),('home-link-block','Home Link')]:
    d(s,M,'Navigation block','Section "'+n+'" on the Navigation page','Only insertable inside the Navigation block (parent restriction).')
d('post-navigation-link-block',R,None,'Post Navigation Link block: shared settings, linking to Next Post and Previous Post','57% boilerplate today; becomes the shared reference its two inserter variations link to.')
for s,n in [('next-post-block','Next Post'),('previous-post-block','Previous Post')]:
    d(s,K,None,TRIM,n+' is its own inserter item (Post Navigation Link variation); own page per the inserter rule.')
d('title-block',R,None,'Title block: full reference (absorbs the old Post Title page)','Own inserter item but only 157 words; thinness is fixed by writing the page, not merging it.')
d('post-title-block',X,'Title block','—','15-word rename stub; Post Title is the Title block, which has its own page.')
for s,n in [('post-content-block','Content'),('post-excerpt-block','Excerpt'),('post-featured-image-block','Featured Image'),('read-more-block','Read More'),('time-to-read-block','Time to Read'),
 ('post-author-name-block','Author Name'),('post-author-biography-block','Author Biography'),('avatar-block','Avatar'),
 ('site-title-block','Site Title'),('site-tagline-block','Site Tagline')]:
    d(s,K,None,TRIM,n+OWN)
d('site-logo-block',K,None,TRIM,'Site Logo is its own inserter item; own page, links to the Identity task.')
d('date-block',K,None,TRIM,'Date is its own inserter item (base of Post Date and Modified Date); explain how the three differ.')
d('post-date-block',K,None,TRIM,'Post Date is its own inserter item (Date variation); own page per the inserter rule.')
d('post-modified-date-block',K,None,TRIM,'Modified Date is its own inserter item (Date variation); own page per the inserter rule.')
d('categories-block',K,None,TRIM,'Categories is its own inserter item (Post Terms variation); own page per the inserter rule.')
d('post-tags-block',K,None,TRIM,'Tags is its own inserter item (Post Terms variation); own page per the inserter rule.')
d('post-author-block',X,'Author Name block','—','32-word stub; Author block deprecated in 7.0 and hidden from the inserter.')
d('template-part-block',K,None,TRIM,'Substantive, low boilerplate, eight inbound links; key to header/footer editing.')
d('breadcrumbs-block',K,None,TRIM,'New, substantive block; works on its own.')
d('terms-query-block',K,None,TRIM,'New, substantive container block; needs inbound links.')
d('login-out-block',K,None,TRIM,'Standalone block; unlinked and last touched 2024-06, verify.')
# Embeds
d('embeds',R,None,'Embeds: how embedding works, plus the provider table linking to each provider page','Section index explains the shared paste-URL workflow once; provider pages link here instead of repeating it.')
d('embed-block',K,None,TRIM,'Generic Embed is its own inserter item; own page per the inserter rule, workflow links to Embeds.')
prov={'amazon-kindle-embed':'Amazon Kindle','animoto-embed':'Animoto','bluesky-embed':'Bluesky','cloudup-embed':'Cloudup','crowdsignal-embed':'Crowdsignal','dailymotion-embed':'Dailymotion','flickr-embed':'Flickr','imgur-embed':'Imgur','issuu-embed':'Issuu','kickstarter-embed':'Kickstarter','mixcloud-embed':'Mixcloud','pinterest-embed':'Pinterest','pocket-casts-embed':'Pocket Casts','reddit-embed':'Reddit','reverbnation-embed':'ReverbNation','scribd-embed':'Scribd','smugmug-embed':'SmugMug','soundcloud-embed':'SoundCloud','speaker-deck-embed':'Speaker Deck','spotify-embed':'Spotify','ted-embed':'TED','tiktok-embed':'TikTok','tumblr-embed':'Tumblr','twitter-embed':'Twitter','videopress-embed':'VideoPress','vimeo-embed':'Vimeo','wolfram-embed':'Wolfram','wordpress-embed':'WordPress','wordpress-tv-embed-block':'WordPress.tv','youtube-embed':'YouTube'}
for s,n in prov.items():
    why=n+' is its own inserter item (Embed variation); own page per the inserter rule, shared workflow links to Embeds.'
    if s=='twitter-embed': why='Own inserter item (Embed variation); keep, but retitle X (twitter.com/x.com URLs).'
    d(s,K,None,TRIM,why)
d('facebook-embed',X,'Embeds','—','oEmbed endpoint closed in 2020; embedding no longer works. One note on Embeds suffices.')
d('instagram-embed',X,'Embeds','—','oEmbed endpoint closed in 2020; embedding no longer works. One note on Embeds suffices.')
d('slideshare-embed',X,'Embeds','—','Block removed in WordPress 6.6.')
d('screencast-block',X,'Embeds','—','Variation removed in Gutenberg 21.1 (PR 70480, June 2025), so gone from the inserter since WordPress 6.9.')
# Site editor
d('site-editor',R,None,'Site Editor hub: workspace, then links to each task page','30 inbound links; 2,300 words mixing tour and how-tos now covered by task pages.')
d('site-editor-navigation',R,None,'Task: "Create and manage menus"','Still framed as "6.3 introduces"; becomes the menu task page, Navigation block stays reference.')
d('site-editor-identity',R,None,'Task: "Set your site title, logo and icon" (absorbs Create a Favicon)','272 words; natural home for site icon instructions.')
d('site-editor-pages',K,None,'Task: manage pages in the Site Editor','Substantive and current (2025-08).')
d('template-editor',R,None,'Task: "Create and edit templates"','"Template Editor" is no longer a distinct UI; templates live in Site Editor > Templates.')
d('site-editor-patterns',K,None,'Reference: Patterns screen in the Site Editor','Current; covers managing patterns and template parts.')
d('styles-overview',S,'Styles overview; Change colors and fonts with Styles; Add custom CSS','Reference + two task pages','4,140 words, 42 images: reference, colour/font task and CSS task in one page.')
d('the-font-library',K,None,'Task: add and manage fonts','Distinct, current; linked from the fonts task.')
d('zoom-out-view',K,None,'Reference: Zoom out view','Current, distinct.')
d('site-editor-command-palette',K,None,'Reference: Command Palette','Current; also used in the post editor.')
d('additional-guide-to-using-the-site-editor',R,None,'Task: "Set up your homepage"','Grab-bag from 2024-02; homepage part is a real gap, rest duplicates Identity and Styles.')
# Themes
d('work-with-themes',R,None,'Task: "Find, install and activate a theme"','Says Twenty Twenty-Two is default; template-hierarchy and creating-themes parts belong on developer.wordpress.org (link).')
d('appearance-themes-screen',R,None,'Reference: Appearance > Themes screen','Untouched since 2023-01; still names Twenty Nineteen as the default theme.')
d('block-themes',K,None,'Concept: what a block theme is','Core concept, 13 inbound links, current.')
d('create-a-favicon',M,'Set your site title, logo and icon','Site icon section of the Identity task','Site icon is set in Identity or Settings > General; pre-6.5 half is obsolete.')
d('twenty-twenty-five',K,None,'Theme guide (current default)','Guide to templates, style variations and patterns of the active default; verify against latest version.')
d('twenty-twenty-four',K,None,'Theme guide','Substantive user guide for a widely used block theme; last touched 2024-08.')
d('twenty-twenty-three',K,None,'Theme guide','Mostly style variations; last touched 2024-08, could shrink to a stub.')
d('twenty-twenty-two',K,None,'Theme guide','First default block theme; last touched 2024-08, could shrink to a stub.')
for s in ['twenty-twenty-five-changelog','twenty-twenty-four-changelog','twenty-twenty-three-changelog','twenty-twenty-two-changelog']:
    d(s,K,None,'Theme changelog (unchanged)','Changelogs are a separate decision; left as is.')
# No theme-block family hubs (Post blocks, Post meta blocks, Site identity blocks): under the inserter rule every
# member has its own page, and the Blocks list index already groups them by family, so a hub would only duplicate it.
NEW=[
 dict(slug='edit-your-header-and-footer',title="Edit your site's header and footer",section='Site Editor',result='Task: edit, replace or create header/footer template parts',why='Most common Site Editor task has no page; template-part content is scattered across three references.'),
]
