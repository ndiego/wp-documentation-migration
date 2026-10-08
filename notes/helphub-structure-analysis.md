# How HelpHub is organised today, and the case for hierarchical pages

Date: 2026-10-08. Numbers come from `raw/articles.json` (321 articles) and `raw/categories.json`, plus the
live-site findings in `notes/site-structure.md`. Scripts used are inline in the session; the figures are
reproducible from the raw JSON.

## 1. The current model

- One flat custom post type, `helphub_article`, at `/documentation/article/<slug>/`.
- Structure is expressed only through the `category` taxonomy: 4 real top-level terms, 19 leaves, plus
  Uncategorized (2 articles) and two empty legacy terms (DevHub, Mobile App).
- **Every article is in exactly one leaf plus that leaf's parent. Zero articles are cross-listed.**
  The taxonomy is being used as a strict tree. None of the things a taxonomy is for (many-to-many
  classification, faceting, archives that mix sections) are in use.
- Articles are not ordered. `menu_order` is 0 for 308 of 321, so every listing is alphabetical.
- There are no section pages. The 4 landing pages are empty posts rendered by a theme block; the front
  page is a hard-coded pattern; section order lives in hidden term meta. Nothing a contributor can edit.
- The only hierarchy deeper than two levels is faked: the 15 `*-changelog` articles are nested under their
  theme by a slug-suffix special case in theme code.
- 128 articles open with a hand-written "Go back to the list of Blocks" paragraph. That is a manual
  breadcrumb, a symptom of the model having no parent concept.
- 66 articles have no inbound links from any other article. They are reachable only from an alphabetical
  category archive.

## 2. What the content actually looks like

### Three reference clusters dominate

| Cluster | Count | Today | Natural shape |
|---|---|---|---|
| "* block" reference pages | 99 (plus 33 "* embed" pages inside that) | spread across 6 leaf categories | one Blocks reference section, grouped by block category, with shared concept pages above it |
| "* screen" pages | 33 of the 46 Dashboard articles | one flat alphabetical list | the wp-admin menu: Dashboard, Posts, Media, Pages, Comments, Appearance, Plugins, Users, Tools, Settings |
| "Twenty *" default themes | 28 (13 themes + 15 changelogs) | one flat list, changelog nesting faked in code | theme > changelog, 3 levels |

That is 160 of 321 articles (50%) whose organising principle is a hierarchy the current model can't express.

### The link graph already contains the hierarchy

Most-linked articles (distinct linking articles):

| In-links | Article | Role |
|---|---|---|
| 144 | Blocks list | the de facto parent of every block page |
| 122 | Adding a new block | shared concept |
| 121 | More options | shared concept |
| 117 | Advanced Settings overview | shared concept |
| 80 | Moving blocks | shared concept |
| 75 / 73 / 65 / 50 | Typography / Dimension / Colors / Border settings overviews | shared concepts |
| 30 | Site Editor | section hub |

83 of the 99 block articles link to at least four of those eight shared pages. The Block Editor section
has a two-tier structure in practice (concepts, then per-block reference) that the category tree flattens.

### Thin and templated pages

Length is not the main problem: the median article is ~660 words excluding code, media and changelog,
and only 8 articles are under 150 words (`post-title-block` 15 words, `button-block` 21, `tools-screen`
26, `post-author-block` 32, two excerpt articles, `create-a-search-page`, `toolbar`).

Repetition is. Measuring sentences that appear verbatim in two or more other articles:

| Section | Median share of boilerplate sentences |
|---|---|
| Embed blocks (36) | 40% |
| Text blocks (13) | 34% |
| Theme blocks (51) | 31% |
| Design blocks (13) | 26% |
| Widget blocks (12) | 23% |
| Media blocks (9) | 19% |
| everything else | 0–8% |

Top repeated sentences: "Read about these and other settings." (96 articles), the Moving-blocks blurb (54),
the Advanced settings list (46), the Block settings and More options paragraphs (36 each). The embed and
theme-block pages are mostly a template with the block name swapped in. 25 articles are more than 45%
boilerplate. These are the "pages with no content": they exist because the model has one page per block
and nowhere to put the shared material except copy-paste.

### Misfiled articles (examples)

"WordPress Block Editor", "Video shortcode" and "What is Post Type?" sit in Dashboard. "Site Editor",
"Introduction to Plugins" and "Manage Plugins" sit in Appearance. "Block-based Widgets Editor" is in
Dashboard while "Manage WordPress widgets" is next to it and "Widget blocks" is a different section.
Technical guides has 13 articles left after 62 moved to developer.wordpress.org; it is a residue, not a
section.

## 3. Hierarchical pages versus the category tree

| | Category tree (today) | Hierarchical pages (`post_parent`) |
|---|---|---|
| Depth | arbitrary in theory, 2 rendered | arbitrary, rendered by breadcrumbs and nav for free |
| Section intro pages | none; theme-generated | real pages (`README.md` → index) that contributors edit |
| Ordering | global `menu_order`, unused | per-parent `menu_order`; curated reading order per section |
| Cross-listing | possible, unused | not possible; needs a secondary taxonomy |
| Shared concept pages | flat peers of the pages that reference them | parent or sibling; "Go back to…" paragraphs disappear |
| URL | flat, stable | hierarchical by default, but see §4 |
| wporg importer fit | needs a subclass mapping folders → terms | native: `parent` + `order` from `manifest.json` |
| Handbook plugin (TOC, sidebar nav, breadcrumbs) | not applicable | works as on developer.wordpress.org |
| Rosetta translations | per-locale copies by slug | same, as long as slugs stay stable |
| Consistency with other wp.org docs | odd one out | same model as every developer.wordpress.org handbook |

Because no article is cross-listed today, converting leaf categories to parents loses no information.

## 4. URLs can be decided separately from hierarchy

The one real cost of hierarchy is the URL change, and it is avoidable. WordPress lets a hierarchical post
type keep flat permalinks (`rewrite => ['hierarchical' => false]`), so articles can gain parents, ordering,
breadcrumbs and section pages while staying at `/documentation/article/<slug>/`. HelpHub URLs are linked
from wp-admin help tabs, core, plugins, forums and search; keeping them avoids 321 redirects and keeps
every Rosetta locale's links valid. Hierarchical URLs can be adopted later, section by section, once the
tree is settled.

Recommendation: keep `helphub_article` (not core `page`, which would mix docs with the site's utility
pages and lose the type-specific tooling), register it hierarchical with page attributes, keep flat URLs
for now, and demote `category` to an optional cross-cutting facet (or retire it).

## 5. A target tree (sketch, for discussion)

```
WordPress overview
  Where to start            ← ordered as a learning path, not alphabetically
  About WordPress
  FAQ
Using WordPress             ← today's "Support guides"
  Dashboard & screens       ← mirrors the wp-admin menu
    Dashboard · Posts · Media · Pages · Comments · Appearance · Plugins · Users · Tools · Settings
  Writing & publishing
  Media
  Users, roles & profiles
Editing & design           ← today's "Customization"
  Block editor
    Working with blocks     ← adding, moving, list view, settings overviews (the 8 shared pages)
    Patterns & synced patterns
    Blocks reference
      Text · Media · Design · Widgets · Theme · Embeds   (99 pages, templated parts collapsed into the parent)
  Site editor
    Templates & template parts · Styles · Navigation · Patterns · Pages
  Themes
    Working with themes
    Default themes
      Twenty Twenty-Five → Changelog, … (13 themes)
Technical guides            ← 13 articles; merge into "Using WordPress" or point to developer.wordpress.org
```

Where this pays off immediately:

- The 36 embed pages and most theme-block pages can shrink to what is unique about each block, with the
  shared toolbar/settings material living once at "Working with blocks". That removes most of the
  boilerplate measured above and the 128 manual breadcrumbs.
- "Where to start" becomes an ordered path instead of an alphabetical pile.
- Default themes gain the three-level structure the theme already fakes.
- Section index pages become real content, written in Markdown like everything else.

## 6. What stays hard regardless of model

- Classic Editor pages (11 titles carry "(Classic Editor)") either become a dedicated legacy section or get
  a facet; a tree alone doesn't express "same task, two editors".
- Duplicate-slug risk under hierarchy: a flat URL scheme needs globally unique slugs, which the current
  content already has.
- `site-editor` is both a section and an article slug; one of them must move.
- Changelog sections inside 184 articles don't fit any tree; they are a separate decision (git history).
