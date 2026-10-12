# Theme Handbook content inventory

Research for the plan to move the Theme Handbook (https://developer.wordpress.org/themes/) from wp-admin editing to a GitHub Markdown repo imported by the `wporg-markdown` importer. Snapshot taken 2026-10-12.

**Owner's constraint:** the structure does not change. Every page keeps its slug, title, parent and order. Everything below is measured against that constraint.

## Sources and method

| Item | Detail |
|---|---|
| Pages | `https://developer.wordpress.org/wp-json/wp/v2/theme-handbook?per_page=100&page=1..2` (`context=view`, unauthenticated). `X-WP-Total: 139`, 2 pages. All 139 records were fetched. |
| Authors | `https://developer.wordpress.org/wp-json/wp/v2/users/{id}` for the 15 distinct author IDs. One ID (14167654) returns `rest_user_invalid_id`. |
| Live checks | `curl -L` on all 59 unique stale internal link targets, the unpublished parent page, two off-site media hosts, and one live page to compare heading ids. |
| Importer code | `notes/reference/wporg-markdown/class-importer.php` (byte-identical to `wporg-markdown@cddeb14`, per `research/02`). DevHub theme: `~/Developer/wordpress-org/wporg-developer/source/wp-content/themes/wporg-developer-2023/` and `plugins/handbook/`. |
| Comparison manifests | Advanced Administration: `https://raw.githubusercontent.com/WordPress/Advanced-administration-handbook/main/bin/handbook-manifest.json`. The `main/manifest.json` path given in the brief returns **404**. The importer's URL comes from `inc/import-advanced-admin.php:11`. SCF: `https://raw.githubusercontent.com/WordPress/secure-custom-fields/trunk/docs/bin/manifest.json` (`inc/import-scf.php:11`). |
| Analysis | Regex and structure scans of `content.rendered`. Text inside `<pre>`/`<code>` is masked for structural counts, so escaped sample code is not miscounted as page markup. |

**Main caveat.** Unauthenticated REST returns only *rendered* HTML. The raw `post_content` (block comments and shortcodes as stored) needs `context=edit`, which requires authentication. The rendered HTML has already been through:

- `wptexturize` (curly quotes and dashes in prose)
- shortcode expansion
- Photon image rewriting (`i0.wp.com`)
- oEmbed expansion
- lazy-load attributes

Anything below that is inferred about the *source* is marked as inferred. Recommendation: before the spike, get an authenticated export of raw `post_content` and `post_title`, either from the wp-admin exporter for the `theme-handbook` post type or a WP-CLI dump by a meta team member.

## Data files

- `data/theme-handbook-pages.json`: `{meta, pages[]}`. Pages are in navigation order: depth-first, `menu_order ASC, post_title ASC`, matching `plugins/handbook/inc/navigation.php:209-210`. Each page has:
  - identity and placement: `id`, `slug`, `title` (entity-decoded), `title_rendered` (as served), `parent`, `parent_slug`, `menu_order`, `path` (relative to `/themes/`), `depth`, `link`
  - dates: `date`, `date_gmt`, `modified`, `modified_gmt`
  - history: `author`, `author_name`, `revisions` (from the `version-history` link count)
  - `class_list`
  - `content_rendered`: the full rendered HTML

  The one page whose parent is unpublished is appended last.
- `data/theme-handbook-manifest.json`: 139 entries in the importer's keyed-object format. See the manifest section below.

---

## (a) Size and hierarchy

**Totals:**

- 139 published pages: one landing page (`theme-handbook`, ID 5785, served at `/themes/`) and 10 top-level chapters.
- Every top-level post has `parent = 0`. The landing page is a sibling of the chapters, not their parent. This matches how the importer treats the `index` entry.
- About 124k words of rendered text, code included.
- Sibling sort on the site is `menu_order ASC, post_title ASC` (`navigation.php:210`).

**Depth** (path segments under `/themes/`):

| Depth | Pages | Example |
|---|---|---|
| 0 (landing) | 1 | `/themes/` |
| 1 (chapters) | 10 | `/themes/patterns/` |
| 2 | 59 | `/themes/patterns/registering-patterns/` |
| 3 | 64 | `/themes/global-settings-and-styles/settings/color/` |
| 4 | 5 | `/themes/classic-themes/functionality/media/audio/`; `/themes/classic-themes/templates/partial-and-miscellaneous-template-files/comment-template/` |

**Chapters.** Page counts include the chapter page itself. "≤24 mo" counts pages modified on or after 2024-10-12.

| menu_order | Chapter | Pages | Max depth | Oldest modified | Newest modified | ≤24 mo | Rendered size |
|---|---|---|---|---|---|---|---|
| 0 | (landing) `theme-handbook` | 1 | 0 | 2026-05-19 | 2026-05-19 | 1 | 3 KB |
| 10 | `getting-started` | 6 | 2 | 2023-12-14 | 2025-07-11 | 1 | 60 KB |
| 20 | `core-concepts` | 7 | 2 | 2023-12-14 | 2024-01-05 | 0 | 79 KB |
| 30 | `global-settings-and-styles` | 25 | 3 | 2023-10-17 | 2026-07-22 | 5 | 265 KB |
| 40 | `templates` | 5 | 2 | 2023-12-14 | 2024-07-24 | 0 | 78 KB |
| 50 | `patterns` | 8 | 2 | 2024-04-30 | 2024-07-15 | 0 | 146 KB |
| 60 | `features` | 5 | 2 | 2023-11-06 | 2026-05-01 | 1 | 92 KB |
| 70 | `advanced-topics` | 13 | 2 | 2024-01-26 | 2025-08-07 | 1 | 107 KB |
| 100 | `releasing-your-theme` | 7 | 2 | 2021-07-20 | 2026-06-24 | 2 | 24 KB |
| 1000 | `classic-themes` | 59 | 4 | 2015-06-02 | 2026-07-22 | 12 | 621 KB |
| 2000 | `credits` | 2 | 2 | 2023-12-14 | 2024-06-05 | 0 | 3 KB |
| — | (orphan) `theme-security/theme-security-issues` | 1 | 2 | 2024-04-25 | 2024-04-25 | 0 | 8 KB |

**Structural facts the manifest must reproduce:**

- **Duplicate slugs.** 7 slugs are used twice, on 14 pages in total:

  | Slug | Paths |
  |---|---|
  | `templates` | `templates`, `core-concepts/templates`, `templates/templates`, `classic-themes/templates` |
  | `global-settings-and-styles` | top level, and `core-concepts/` |
  | `patterns` | top level, and `global-settings-and-styles/` |
  | `template-parts` | `global-settings-and-styles/`, and `templates/` |
  | `template-hierarchy` | `templates/`, and `classic-themes/basics/` |
  | `internationalization` | `advanced-topics/`, and `classic-themes/functionality/` |
  | `testing` | `advanced-topics/`, and `releasing-your-theme/` |

  `templates` appears at four paths, which is why the seven slugs cover 14 pages. Two duplicated slugs are *parents* of other pages: top-level `templates` and `classic-themes/templates`.
- **Ties in `menu_order`.** 8 sibling groups covering 64 pages share a `menu_order` value, usually 0. Examples: all 13 `settings/*` children, the 6 `releasing-your-theme/*` children, and most of `classic-themes/*`. Their order on the site comes from the title sort, so titles must stay byte-identical or the order shifts.
- **One orphan.** `theme-security-issues` (ID 148747, https://developer.wordpress.org/themes/theme-security/theme-security-issues/) has parent ID 11394, which is not published.
  - `/wp-json/wp/v2/theme-handbook/11394` returns 401, so the post exists but is not public.
  - `/themes/theme-security/` returns a 301 to the child page.
  - The page does not appear in the handbook navigation. It is reachable only by URL.
- **One empty page.** `classic-themes/customize-api/other-resources` (ID 40120) has an empty `content`.
- **Slugs:** all 139 match `^[a-z0-9-]+$`, so they pass the importer's `sanitize_title_with_dashes( slug ) === slug` check.

### Full tree

Pages are in navigation order. Indentation shows depth. Parent is shown as slug and ID.

| # | Path (under /themes/) | Slug | Title | Parent (id) | menu_order | Modified | ID |
|---|---|---|---|---|---|---|---|
| 1 | [(landing)](https://developer.wordpress.org/themes/) | `theme-handbook` | Theme Handbook | — | 0 | 2026-05-19 | 5785 |
| 2 | [getting-started](https://developer.wordpress.org/themes/getting-started/) | `getting-started` | Getting Started | — | 10 | 2023-12-14 | 5794 |
| 3 | &nbsp;&nbsp;[getting-started/what-is-a-theme](https://developer.wordpress.org/themes/getting-started/what-is-a-theme/) | `what-is-a-theme` | What Is a Theme? | getting-started (5794) | 10 | 2023-12-14 | 5800 |
| 4 | &nbsp;&nbsp;[getting-started/who-is-this-handbook-for](https://developer.wordpress.org/themes/getting-started/who-is-this-handbook-for/) | `who-is-this-handbook-for` | Who Is This Handbook For? | getting-started (5794) | 20 | 2023-12-14 | 149311 |
| 5 | &nbsp;&nbsp;[getting-started/reading-this-handbook](https://developer.wordpress.org/themes/getting-started/reading-this-handbook/) | `reading-this-handbook` | Reading This Handbook | getting-started (5794) | 30 | 2023-12-14 | 149314 |
| 6 | &nbsp;&nbsp;[getting-started/tools-and-setup](https://developer.wordpress.org/themes/getting-started/tools-and-setup/) | `tools-and-setup` | Tools and Setup | getting-started (5794) | 40 | 2025-07-11 | 149317 |
| 7 | &nbsp;&nbsp;[getting-started/quick-start-guide](https://developer.wordpress.org/themes/getting-started/quick-start-guide/) | `quick-start-guide` | Quick-Start Guide | getting-started (5794) | 50 | 2024-01-22 | 149320 |
| 8 | [core-concepts](https://developer.wordpress.org/themes/core-concepts/) | `core-concepts` | Core Concepts | — | 20 | 2023-12-14 | 149331 |
| 9 | &nbsp;&nbsp;[core-concepts/theme-structure](https://developer.wordpress.org/themes/core-concepts/theme-structure/) | `theme-structure` | Theme Structure | core-concepts (149331) | 10 | 2024-01-05 | 149333 |
| 10 | &nbsp;&nbsp;[core-concepts/main-stylesheet](https://developer.wordpress.org/themes/core-concepts/main-stylesheet/) | `main-stylesheet` | Main Stylesheet (style.css) | core-concepts (149331) | 20 | 2023-12-14 | 149336 |
| 11 | &nbsp;&nbsp;[core-concepts/templates](https://developer.wordpress.org/themes/core-concepts/templates/) | `templates` | Templates | core-concepts (149331) | 30 | 2023-12-14 | 149340 |
| 12 | &nbsp;&nbsp;[core-concepts/custom-functionality](https://developer.wordpress.org/themes/core-concepts/custom-functionality/) | `custom-functionality` | Custom Functionality (functions.php) | core-concepts (149331) | 40 | 2023-12-16 | 149345 |
| 13 | &nbsp;&nbsp;[core-concepts/including-assets](https://developer.wordpress.org/themes/core-concepts/including-assets/) | `including-assets` | Including Assets | core-concepts (149331) | 50 | 2023-12-14 | 149365 |
| 14 | &nbsp;&nbsp;[core-concepts/global-settings-and-styles](https://developer.wordpress.org/themes/core-concepts/global-settings-and-styles/) | `global-settings-and-styles` | Global Settings and Styles | core-concepts (149331) | 60 | 2023-12-14 | 149367 |
| 15 | [global-settings-and-styles](https://developer.wordpress.org/themes/global-settings-and-styles/) | `global-settings-and-styles` | Global Settings and Styles (theme.json) | — | 30 | 2023-12-14 | 148901 |
| 16 | &nbsp;&nbsp;[global-settings-and-styles/introduction-to-theme-json](https://developer.wordpress.org/themes/global-settings-and-styles/introduction-to-theme-json/) | `introduction-to-theme-json` | Introduction to theme.json | global-settings-and-styles (148901) | 10 | 2026-06-24 | 148903 |
| 17 | &nbsp;&nbsp;[global-settings-and-styles/settings](https://developer.wordpress.org/themes/global-settings-and-styles/settings/) | `settings` | Settings | global-settings-and-styles (148901) | 20 | 2026-05-20 | 148907 |
| 18 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/appearance-tools](https://developer.wordpress.org/themes/global-settings-and-styles/settings/appearance-tools/) | `appearance-tools` | Appearance Tools | settings (148907) | 0 | 2023-10-17 | 149040 |
| 19 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/blocks](https://developer.wordpress.org/themes/global-settings-and-styles/settings/blocks/) | `blocks` | Blocks | settings (148907) | 0 | 2024-02-01 | 149096 |
| 20 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/border](https://developer.wordpress.org/themes/global-settings-and-styles/settings/border/) | `border` | Border | settings (148907) | 0 | 2023-10-17 | 149042 |
| 21 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/color](https://developer.wordpress.org/themes/global-settings-and-styles/settings/color/) | `color` | Color | settings (148907) | 0 | 2023-10-17 | 149045 |
| 22 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/custom](https://developer.wordpress.org/themes/global-settings-and-styles/settings/custom/) | `custom` | Custom | settings (148907) | 0 | 2023-10-17 | 149058 |
| 23 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/dimensions](https://developer.wordpress.org/themes/global-settings-and-styles/settings/dimensions/) | `dimensions` | Dimensions | settings (148907) | 0 | 2023-10-17 | 149060 |
| 24 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/layout](https://developer.wordpress.org/themes/global-settings-and-styles/settings/layout/) | `layout` | Layout | settings (148907) | 0 | 2023-10-17 | 149064 |
| 25 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/lightbox](https://developer.wordpress.org/themes/global-settings-and-styles/settings/lightbox/) | `lightbox` | Lightbox | settings (148907) | 0 | 2023-10-17 | 149068 |
| 26 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/position](https://developer.wordpress.org/themes/global-settings-and-styles/settings/position/) | `position` | Position | settings (148907) | 0 | 2023-10-17 | 149072 |
| 27 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/shadow](https://developer.wordpress.org/themes/global-settings-and-styles/settings/shadow/) | `shadow` | Shadow | settings (148907) | 0 | 2023-10-17 | 149075 |
| 28 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/spacing](https://developer.wordpress.org/themes/global-settings-and-styles/settings/spacing/) | `spacing` | Spacing | settings (148907) | 0 | 2026-07-22 | 149078 |
| 29 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/typography](https://developer.wordpress.org/themes/global-settings-and-styles/settings/typography/) | `typography` | Typography | settings (148907) | 0 | 2026-05-20 | 149087 |
| 30 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/use-root-padding-aware-alignments](https://developer.wordpress.org/themes/global-settings-and-styles/settings/use-root-padding-aware-alignments/) | `use-root-padding-aware-alignments` | Use Root Padding Aware Alignments | settings (148907) | 0 | 2023-10-17 | 149092 |
| 31 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/settings/settings-reference](https://developer.wordpress.org/themes/global-settings-and-styles/settings/settings-reference/) | `settings-reference` | Settings Reference | settings (148907) | 9999 | 2025-10-14 | 149100 |
| 32 | &nbsp;&nbsp;[global-settings-and-styles/styles](https://developer.wordpress.org/themes/global-settings-and-styles/styles/) | `styles` | Styles | global-settings-and-styles (148901) | 30 | 2023-12-14 | 148909 |
| 33 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/styles/applying-styles](https://developer.wordpress.org/themes/global-settings-and-styles/styles/applying-styles/) | `applying-styles` | Applying Styles | styles (148909) | 10 | 2024-01-05 | 149109 |
| 34 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/styles/using-presets](https://developer.wordpress.org/themes/global-settings-and-styles/styles/using-presets/) | `using-presets` | Using Presets | styles (148909) | 20 | 2023-12-14 | 149116 |
| 35 | &nbsp;&nbsp;&nbsp;&nbsp;[global-settings-and-styles/styles/styles-reference](https://developer.wordpress.org/themes/global-settings-and-styles/styles/styles-reference/) | `styles-reference` | Styles Reference | styles (148909) | 30 | 2023-12-14 | 149119 |
| 36 | &nbsp;&nbsp;[global-settings-and-styles/custom-templates](https://developer.wordpress.org/themes/global-settings-and-styles/custom-templates/) | `custom-templates` | Custom Templates | global-settings-and-styles (148901) | 40 | 2023-12-14 | 148911 |
| 37 | &nbsp;&nbsp;[global-settings-and-styles/patterns](https://developer.wordpress.org/themes/global-settings-and-styles/patterns/) | `patterns` | Patterns | global-settings-and-styles (148901) | 50 | 2023-12-14 | 148915 |
| 38 | &nbsp;&nbsp;[global-settings-and-styles/template-parts](https://developer.wordpress.org/themes/global-settings-and-styles/template-parts/) | `template-parts` | Template Parts | global-settings-and-styles (148901) | 60 | 2023-12-14 | 148919 |
| 39 | &nbsp;&nbsp;[global-settings-and-styles/style-variations](https://developer.wordpress.org/themes/global-settings-and-styles/style-variations/) | `style-variations` | Style Variations | global-settings-and-styles (148901) | 70 | 2023-12-14 | 148923 |
| 40 | [templates](https://developer.wordpress.org/themes/templates/) | `templates` | Templates | — | 40 | 2023-12-14 | 149219 |
| 41 | &nbsp;&nbsp;[templates/introduction-to-templates](https://developer.wordpress.org/themes/templates/introduction-to-templates/) | `introduction-to-templates` | Introduction to Templates | templates (149219) | 10 | 2023-12-14 | 149221 |
| 42 | &nbsp;&nbsp;[templates/templates](https://developer.wordpress.org/themes/templates/templates/) | `templates` | Templates | templates (149219) | 20 | 2023-12-14 | 149227 |
| 43 | &nbsp;&nbsp;[templates/template-hierarchy](https://developer.wordpress.org/themes/templates/template-hierarchy/) | `template-hierarchy` | Template Hierarchy | templates (149219) | 30 | 2024-07-24 | 149232 |
| 44 | &nbsp;&nbsp;[templates/template-parts](https://developer.wordpress.org/themes/templates/template-parts/) | `template-parts` | Template Parts | templates (149219) | 40 | 2023-12-14 | 149235 |
| 45 | [patterns](https://developer.wordpress.org/themes/patterns/) | `patterns` | Patterns | — | 50 | 2024-04-30 | 153616 |
| 46 | &nbsp;&nbsp;[patterns/introduction-to-patterns](https://developer.wordpress.org/themes/patterns/introduction-to-patterns/) | `introduction-to-patterns` | Introduction to Patterns | patterns (153616) | 10 | 2024-04-30 | 153618 |
| 47 | &nbsp;&nbsp;[patterns/registering-patterns](https://developer.wordpress.org/themes/patterns/registering-patterns/) | `registering-patterns` | Registering Patterns | patterns (153616) | 20 | 2024-07-15 | 153627 |
| 48 | &nbsp;&nbsp;[patterns/using-php-in-patterns](https://developer.wordpress.org/themes/patterns/using-php-in-patterns/) | `using-php-in-patterns` | Using PHP in Patterns | patterns (153616) | 30 | 2024-04-30 | 153646 |
| 49 | &nbsp;&nbsp;[patterns/usage-in-templates](https://developer.wordpress.org/themes/patterns/usage-in-templates/) | `usage-in-templates` | Usage in Templates | patterns (153616) | 40 | 2024-04-30 | 153652 |
| 50 | &nbsp;&nbsp;[patterns/starter-patterns](https://developer.wordpress.org/themes/patterns/starter-patterns/) | `starter-patterns` | Starter Patterns | patterns (153616) | 50 | 2024-04-30 | 153657 |
| 51 | &nbsp;&nbsp;[patterns/block-type-patterns](https://developer.wordpress.org/themes/patterns/block-type-patterns/) | `block-type-patterns` | Block Type Patterns | patterns (153616) | 60 | 2024-04-30 | 153663 |
| 52 | &nbsp;&nbsp;[patterns/patterns-and-block-locking](https://developer.wordpress.org/themes/patterns/patterns-and-block-locking/) | `patterns-and-block-locking` | Patterns and Block Locking | patterns (153616) | 70 | 2024-04-30 | 153674 |
| 53 | [features](https://developer.wordpress.org/themes/features/) | `features` | Features | — | 60 | 2024-04-30 | 149260 |
| 54 | &nbsp;&nbsp;[features/block-style-variations](https://developer.wordpress.org/themes/features/block-style-variations/) | `block-style-variations` | Block Style Variations | features (149260) | 0 | 2023-11-06 | 149271 |
| 55 | &nbsp;&nbsp;[features/block-stylesheets](https://developer.wordpress.org/themes/features/block-stylesheets/) | `block-stylesheets` | Block Stylesheets | features (149260) | 0 | 2023-11-06 | 149276 |
| 56 | &nbsp;&nbsp;[features/block-variations](https://developer.wordpress.org/themes/features/block-variations/) | `block-variations` | Block Variations | features (149260) | 0 | 2026-05-01 | 149280 |
| 57 | &nbsp;&nbsp;[features/block-patterns](https://developer.wordpress.org/themes/features/block-patterns/) | `block-patterns` | Block Patterns (Archived) | features (149260) | 1000 | 2024-04-30 | 149262 |
| 58 | [advanced-topics](https://developer.wordpress.org/themes/advanced-topics/) | `advanced-topics` | Advanced Topics | — | 70 | 2024-02-06 | 5821 |
| 59 | &nbsp;&nbsp;[advanced-topics/internationalization](https://developer.wordpress.org/themes/advanced-topics/internationalization/) | `internationalization` | Internationalization | advanced-topics (5821) | 10 | 2024-01-26 | 152057 |
| 60 | &nbsp;&nbsp;[advanced-topics/child-themes](https://developer.wordpress.org/themes/advanced-topics/child-themes/) | `child-themes` | Child Themes | advanced-topics (5821) | 20 | 2024-01-26 | 11387 |
| 61 | &nbsp;&nbsp;[advanced-topics/build-process](https://developer.wordpress.org/themes/advanced-topics/build-process/) | `build-process` | Build Process | advanced-topics (5821) | 30 | 2024-01-26 | 152060 |
| 62 | &nbsp;&nbsp;[advanced-topics/privacy](https://developer.wordpress.org/themes/advanced-topics/privacy/) | `privacy` | Privacy | advanced-topics (5821) | 40 | 2024-05-17 | 152063 |
| 63 | &nbsp;&nbsp;[advanced-topics/testing](https://developer.wordpress.org/themes/advanced-topics/testing/) | `testing` | Testing | advanced-topics (5821) | 50 | 2024-02-06 | 152083 |
| 64 | &nbsp;&nbsp;[advanced-topics/debugging](https://developer.wordpress.org/themes/advanced-topics/debugging/) | `debugging` | Debugging | advanced-topics (5821) | 60 | 2024-01-29 | 152066 |
| 65 | &nbsp;&nbsp;[advanced-topics/security](https://developer.wordpress.org/themes/advanced-topics/security/) | `security` | Security | advanced-topics (5821) | 70 | 2024-01-26 | 152068 |
| 66 | &nbsp;&nbsp;[advanced-topics/publishing-themes](https://developer.wordpress.org/themes/advanced-topics/publishing-themes/) | `publishing-themes` | Publishing Themes | advanced-topics (5821) | 80 | 2024-02-06 | 152151 |
| 67 | &nbsp;&nbsp;[advanced-topics/theme-testing](https://developer.wordpress.org/themes/advanced-topics/theme-testing/) | `theme-testing` | Theme Testing | advanced-topics (5821) | 200 | 2025-08-07 | 11403 |
| 68 | &nbsp;&nbsp;[advanced-topics/plugin-api-hooks](https://developer.wordpress.org/themes/advanced-topics/plugin-api-hooks/) | `plugin-api-hooks` | Plugin API Hooks | advanced-topics (5821) | 301 | 2024-01-26 | 11409 |
| 69 | &nbsp;&nbsp;[advanced-topics/ui-best-practices](https://developer.wordpress.org/themes/advanced-topics/ui-best-practices/) | `ui-best-practices` | UI Best Practices | advanced-topics (5821) | 305 | 2024-01-26 | 11399 |
| 70 | &nbsp;&nbsp;[advanced-topics/javascript-best-practices](https://developer.wordpress.org/themes/advanced-topics/javascript-best-practices/) | `javascript-best-practices` | JavaScript Best Practices | advanced-topics (5821) | 310 | 2024-02-23 | 11401 |
| 71 | [releasing-your-theme](https://developer.wordpress.org/themes/releasing-your-theme/) | `releasing-your-theme` | Releasing Your Theme | — | 100 | 2026-05-19 | 5823 |
| 72 | &nbsp;&nbsp;[releasing-your-theme/required-theme-files](https://developer.wordpress.org/themes/releasing-your-theme/required-theme-files/) | `required-theme-files` | Required Theme Files | releasing-your-theme (5823) | 0 | 2026-06-24 | 11421 |
| 73 | &nbsp;&nbsp;[releasing-your-theme/submitting-your-theme-to-wordpress-org](https://developer.wordpress.org/themes/releasing-your-theme/submitting-your-theme-to-wordpress-org/) | `submitting-your-theme-to-wordpress-org` | Submitting Your Theme to WordPress.org | releasing-your-theme (5823) | 0 | 2024-09-16 | 11433 |
| 74 | &nbsp;&nbsp;[releasing-your-theme/testing](https://developer.wordpress.org/themes/releasing-your-theme/testing/) | `testing` | Testing | releasing-your-theme (5823) | 0 | 2022-01-04 | 11424 |
| 75 | &nbsp;&nbsp;[releasing-your-theme/theme-review-guidelines](https://developer.wordpress.org/themes/releasing-your-theme/theme-review-guidelines/) | `theme-review-guidelines` | Theme Review Guidelines | releasing-your-theme (5823) | 0 | 2023-06-08 | 11429 |
| 76 | &nbsp;&nbsp;[releasing-your-theme/updating-your-theme](https://developer.wordpress.org/themes/releasing-your-theme/updating-your-theme/) | `updating-your-theme` | Updating Your Theme | releasing-your-theme (5823) | 0 | 2022-02-17 | 138674 |
| 77 | &nbsp;&nbsp;[releasing-your-theme/writing-documentation](https://developer.wordpress.org/themes/releasing-your-theme/writing-documentation/) | `writing-documentation` | Writing Documentation | releasing-your-theme (5823) | 0 | 2021-07-20 | 11431 |
| 78 | [classic-themes](https://developer.wordpress.org/themes/classic-themes/) | `classic-themes` | Classic themes | — | 1000 | 2023-12-14 | 138748 |
| 79 | &nbsp;&nbsp;[classic-themes/your-first-theme](https://developer.wordpress.org/themes/classic-themes/your-first-theme/) | `your-first-theme` | Your First Theme | classic-themes (138748) | 0 | 2023-12-14 | 5811 |
| 80 | &nbsp;&nbsp;[classic-themes/basics](https://developer.wordpress.org/themes/classic-themes/basics/) | `basics` | Theme Basics | classic-themes (138748) | 1010 | 2026-06-02 | 5817 |
| 81 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/categories-tags-custom-taxonomies](https://developer.wordpress.org/themes/classic-themes/basics/categories-tags-custom-taxonomies/) | `categories-tags-custom-taxonomies` | Categories, Tags, & Custom Taxonomies | basics (5817) | 0 | 2022-01-12 | 11345 |
| 82 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/conditional-tags](https://developer.wordpress.org/themes/classic-themes/basics/conditional-tags/) | `conditional-tags` | Conditional Tags | basics (5817) | 0 | 2024-04-04 | 11307 |
| 83 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/including-css-javascript](https://developer.wordpress.org/themes/classic-themes/basics/including-css-javascript/) | `including-css-javascript` | Including CSS & JavaScript (Archived) | basics (5817) | 0 | 2024-06-06 | 11303 |
| 84 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/linking-theme-files-directories](https://developer.wordpress.org/themes/classic-themes/basics/linking-theme-files-directories/) | `linking-theme-files-directories` | Linking Theme Files & Directories | basics (5817) | 0 | 2017-01-12 | 11300 |
| 85 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/main-stylesheet-style-css](https://developer.wordpress.org/themes/classic-themes/basics/main-stylesheet-style-css/) | `main-stylesheet-style-css` | Main Stylesheet (style.css) | basics (5817) | 0 | 2021-03-01 | 24939 |
| 86 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/organizing-theme-files](https://developer.wordpress.org/themes/classic-themes/basics/organizing-theme-files/) | `organizing-theme-files` | Organizing Theme Files | basics (5817) | 0 | 2022-10-25 | 5829 |
| 87 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/post-types](https://developer.wordpress.org/themes/classic-themes/basics/post-types/) | `post-types` | Post Types | basics (5817) | 0 | 2023-02-13 | 11337 |
| 88 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/reworking-theme-files-organization](https://developer.wordpress.org/themes/classic-themes/basics/reworking-theme-files-organization/) | `reworking-theme-files-organization` | Reworking Theme Files & Organization | basics (5817) | 0 | 2026-07-21 | 12028 |
| 89 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/template-files](https://developer.wordpress.org/themes/classic-themes/basics/template-files/) | `template-files` | Template Files | basics (5817) | 0 | 2023-01-21 | 11980 |
| 90 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/template-hierarchy](https://developer.wordpress.org/themes/classic-themes/basics/template-hierarchy/) | `template-hierarchy` | Template Hierarchy | basics (5817) | 0 | 2024-07-24 | 11281 |
| 91 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/template-tags](https://developer.wordpress.org/themes/classic-themes/basics/template-tags/) | `template-tags` | Template Tags | basics (5817) | 0 | 2022-11-17 | 11285 |
| 92 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/the-loop](https://developer.wordpress.org/themes/classic-themes/basics/the-loop/) | `the-loop` | The Loop | basics (5817) | 0 | 2022-11-17 | 11288 |
| 93 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/theme-functions](https://developer.wordpress.org/themes/classic-themes/basics/theme-functions/) | `theme-functions` | Theme Functions | basics (5817) | 0 | 2026-06-02 | 11295 |
| 94 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/basics/tools-resources](https://developer.wordpress.org/themes/classic-themes/basics/tools-resources/) | `tools-resources` | Tools & Resources | basics (5817) | 10 | 2026-07-20 | 142885 |
| 95 | &nbsp;&nbsp;[classic-themes/functionality](https://developer.wordpress.org/themes/classic-themes/functionality/) | `functionality` | Theme Functionality | classic-themes (138748) | 1020 | 2026-06-04 | 5819 |
| 96 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/404-pages](https://developer.wordpress.org/themes/classic-themes/functionality/404-pages/) | `404-pages` | 404 Pages | functionality (5819) | 0 | 2015-10-17 | 11382 |
| 97 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/accessibility](https://developer.wordpress.org/themes/classic-themes/functionality/accessibility/) | `accessibility` | Accessibility | functionality (5819) | 0 | 2026-06-04 | 11377 |
| 98 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/administration-menus](https://developer.wordpress.org/themes/classic-themes/functionality/administration-menus/) | `administration-menus` | Administration Menus | functionality (5819) | 0 | 2022-10-29 | 11380 |
| 99 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/block-theme-accessibility](https://developer.wordpress.org/themes/classic-themes/functionality/block-theme-accessibility/) | `block-theme-accessibility` | Block theme accessibility | functionality (5819) | 0 | 2023-08-29 | 139317 |
| 100 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/core-supported](https://developer.wordpress.org/themes/classic-themes/functionality/core-supported/) | `core-supported` | Core-Supported Features | functionality (5819) | 0 | 2015-06-02 | 17363 |
| 101 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/custom-backgrounds](https://developer.wordpress.org/themes/classic-themes/functionality/custom-backgrounds/) | `custom-backgrounds` | Custom Backgrounds | functionality (5819) | 0 | 2022-11-17 | 25470 |
| 102 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/custom-front-page-templates](https://developer.wordpress.org/themes/classic-themes/functionality/custom-front-page-templates/) | `custom-front-page-templates` | Custom Front Page Templates | functionality (5819) | 0 | 2026-07-21 | 25410 |
| 103 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/custom-headers](https://developer.wordpress.org/themes/classic-themes/functionality/custom-headers/) | `custom-headers` | Custom Headers | functionality (5819) | 0 | 2022-10-29 | 11314 |
| 104 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/custom-logo](https://developer.wordpress.org/themes/classic-themes/functionality/custom-logo/) | `custom-logo` | Custom Logo | functionality (5819) | 0 | 2022-10-25 | 22327 |
| 105 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/featured-images-post-thumbnails](https://developer.wordpress.org/themes/classic-themes/functionality/featured-images-post-thumbnails/) | `featured-images-post-thumbnails` | Featured Images & Post Thumbnails | functionality (5819) | 0 | 2022-10-27 | 11362 |
| 106 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/internationalization](https://developer.wordpress.org/themes/classic-themes/functionality/internationalization/) | `internationalization` | Internationalization | functionality (5819) | 0 | 2022-11-17 | 11370 |
| 107 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/localization](https://developer.wordpress.org/themes/classic-themes/functionality/localization/) | `localization` | Localization | functionality (5819) | 0 | 2019-12-13 | 11372 |
| 108 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/media](https://developer.wordpress.org/themes/classic-themes/functionality/media/) | `media` | Media | functionality (5819) | 0 | 2017-01-15 | 11360 |
| 109 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/media/audio](https://developer.wordpress.org/themes/classic-themes/functionality/media/audio/) | `audio` | Audio | media (11360) | 0 | 2017-01-15 | 25145 |
| 110 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/media/galleries](https://developer.wordpress.org/themes/classic-themes/functionality/media/galleries/) | `galleries` | Galleries | media (11360) | 0 | 2022-11-01 | 25149 |
| 111 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/media/images](https://developer.wordpress.org/themes/classic-themes/functionality/media/images/) | `images` | Images | media (11360) | 0 | 2022-11-01 | 25136 |
| 112 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/media/video](https://developer.wordpress.org/themes/classic-themes/functionality/media/video/) | `video` | Video | media (11360) | 0 | 2022-10-25 | 25147 |
| 113 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/navigation-menus](https://developer.wordpress.org/themes/classic-themes/functionality/navigation-menus/) | `navigation-menus` | Navigation Menus | functionality (5819) | 0 | 2017-03-17 | 11322 |
| 114 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/pagination](https://developer.wordpress.org/themes/classic-themes/functionality/pagination/) | `pagination` | Pagination | functionality (5819) | 0 | 2022-10-25 | 11354 |
| 115 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/post-formats](https://developer.wordpress.org/themes/classic-themes/functionality/post-formats/) | `post-formats` | Post Formats | functionality (5819) | 0 | 2022-10-29 | 11368 |
| 116 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/sidebars](https://developer.wordpress.org/themes/classic-themes/functionality/sidebars/) | `sidebars` | Sidebars | functionality (5819) | 0 | 2022-10-29 | 11318 |
| 117 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/widgets](https://developer.wordpress.org/themes/classic-themes/functionality/widgets/) | `widgets` | Widgets | functionality (5819) | 0 | 2022-10-29 | 11320 |
| 118 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/functionality/sticky-posts](https://developer.wordpress.org/themes/classic-themes/functionality/sticky-posts/) | `sticky-posts` | Sticky Posts | functionality (5819) | 3 | 2022-10-29 | 24973 |
| 119 | &nbsp;&nbsp;[classic-themes/customize-api](https://developer.wordpress.org/themes/classic-themes/customize-api/) | `customize-api` | Theme Options – The Customize API | classic-themes (138748) | 1040 | 2025-10-01 | 11390 |
| 120 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/customize-api/customizer-objects](https://developer.wordpress.org/themes/classic-themes/customize-api/customizer-objects/) | `customizer-objects` | Customizer Objects | customize-api (11390) | 0 | 2018-07-14 | 25000 |
| 121 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/customize-api/other-resources](https://developer.wordpress.org/themes/classic-themes/customize-api/other-resources/) | `other-resources` | Other Resources | customize-api (11390) | 0 | 2019-06-14 | 40120 |
| 122 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/customize-api/tools-for-improved-user-experience](https://developer.wordpress.org/themes/classic-themes/customize-api/tools-for-improved-user-experience/) | `tools-for-improved-user-experience` | Tools for Improved User Experience | customize-api (11390) | 1 | 2018-01-20 | 25005 |
| 123 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/customize-api/the-customizer-javascript-api](https://developer.wordpress.org/themes/classic-themes/customize-api/the-customizer-javascript-api/) | `the-customizer-javascript-api` | The Customizer JavaScript API | customize-api (11390) | 2 | 2022-11-01 | 25007 |
| 124 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/customize-api/javascriptunderscore-js-rendered-custom-controls](https://developer.wordpress.org/themes/classic-themes/customize-api/javascriptunderscore-js-rendered-custom-controls/) | `javascriptunderscore-js-rendered-custom-controls` | JavaScript/Underscore.js-Rendered Custom Controls | customize-api (11390) | 3 | 2018-03-15 | 25009 |
| 125 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/customize-api/advanced-usage](https://developer.wordpress.org/themes/classic-themes/customize-api/advanced-usage/) | `advanced-usage` | Advanced Usage | customize-api (11390) | 4 | 2022-11-01 | 25013 |
| 126 | &nbsp;&nbsp;[classic-themes/templates](https://developer.wordpress.org/themes/classic-themes/templates/) | `templates` | Template Files | classic-themes (138748) | 1115 | 2025-10-01 | 17401 |
| 127 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/attachment-template-files](https://developer.wordpress.org/themes/classic-themes/templates/attachment-template-files/) | `attachment-template-files` | Attachment Template Files | templates (17401) | 0 | 2022-10-29 | 17405 |
| 128 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/custom-post-type-template-files](https://developer.wordpress.org/themes/classic-themes/templates/custom-post-type-template-files/) | `custom-post-type-template-files` | Custom Post Type Template Files | templates (17401) | 0 | 2021-03-15 | 17407 |
| 129 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/partial-and-miscellaneous-template-files](https://developer.wordpress.org/themes/classic-themes/templates/partial-and-miscellaneous-template-files/) | `partial-and-miscellaneous-template-files` | Partial and Miscellaneous Template Files | templates (17401) | 0 | 2022-10-29 | 17409 |
| 130 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/partial-and-miscellaneous-template-files/comment-template](https://developer.wordpress.org/themes/classic-themes/templates/partial-and-miscellaneous-template-files/comment-template/) | `comment-template` | Comment Template | partial-and-miscellaneous-template-files (17409) | 0 | 2022-10-29 | 11356 |
| 131 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/post-template-files](https://developer.wordpress.org/themes/classic-themes/templates/post-template-files/) | `post-template-files` | Post Template Files | templates (17401) | 0 | 2022-10-25 | 17399 |
| 132 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/taxonomy-templates](https://developer.wordpress.org/themes/classic-themes/templates/taxonomy-templates/) | `taxonomy-templates` | Taxonomy Templates | templates (17401) | 0 | 2022-10-29 | 11341 |
| 133 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/templates/page-template-files](https://developer.wordpress.org/themes/classic-themes/templates/page-template-files/) | `page-template-files` | Page Templates | templates (17401) | 3 | 2026-07-22 | 11273 |
| 134 | &nbsp;&nbsp;[classic-themes/references](https://developer.wordpress.org/themes/classic-themes/references/) | `references` | References | classic-themes (138748) | 2000 | 2026-05-19 | 25050 |
| 135 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/references/list-of-template-tags](https://developer.wordpress.org/themes/classic-themes/references/list-of-template-tags/) | `list-of-template-tags` | List of Template Tags | references (25050) | 0 | 2020-06-19 | 25053 |
| 136 | &nbsp;&nbsp;&nbsp;&nbsp;[classic-themes/references/list-of-conditional-tags](https://developer.wordpress.org/themes/classic-themes/references/list-of-conditional-tags/) | `list-of-conditional-tags` | List of Conditional Tags | references (25050) | 1 | 2026-05-20 | 25063 |
| 137 | [credits](https://developer.wordpress.org/themes/credits/) | `credits` | Credits | — | 2000 | 2023-12-14 | 10877 |
| 138 | &nbsp;&nbsp;[credits/feedback](https://developer.wordpress.org/themes/credits/feedback/) | `feedback` | Feedback | credits (10877) | 0 | 2024-06-05 | 25182 |
| 139 | &nbsp;&nbsp;[theme-security/theme-security-issues](https://developer.wordpress.org/themes/theme-security/theme-security-issues/) | `theme-security-issues` | Theme security issues | (unpublished 11394) | 0 | 2024-04-25 | 148747 |

## (b) Freshness and authorship

**Last modified, by year.** `modified` is `post_modified`, which any save updates.

| Year | 2015 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Pages | 2 | 4 | 3 | 2 | 1 | 3 | 27 | 41 | 33 | 5 | 18 |

**Created, by year:**

| Year | 2014 | 2015 | 2016 | 2017 | 2018 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|
| Pages | 47 | 7 | 2 | 15 | 2 | 4 | 47 | 15 |

**Recency:**

- Modified in the last 12 months (on or after 2025-10-12): **19 pages**. In the last 24 months: **23 pages**. In the last 36 months: 93 pages.
- 16 pages have never been modified after creation.
- The 2023–2024 block-theme rewrite accounts for the bulk of the recent activity.
- The 2026 edits are mostly small fixes in `classic-themes/*` and `global-settings-and-styles/*`.

**Oldest pages by `modified`:**

| Modified | Page |
|---|---|
| 2015-06-02 | https://developer.wordpress.org/themes/classic-themes/functionality/core-supported/ |
| 2015-10-17 | https://developer.wordpress.org/themes/classic-themes/functionality/404-pages/ |
| 2017-01-12 | https://developer.wordpress.org/themes/classic-themes/basics/linking-theme-files-directories/ |
| 2017-01-15 | https://developer.wordpress.org/themes/classic-themes/functionality/media/ |
| 2017-01-15 | https://developer.wordpress.org/themes/classic-themes/functionality/media/audio/ |
| 2017-03-17 | https://developer.wordpress.org/themes/classic-themes/functionality/navigation-menus/ |
| 2018-01-20 | https://developer.wordpress.org/themes/classic-themes/customize-api/tools-for-improved-user-experience/ |
| 2018-03-15 | https://developer.wordpress.org/themes/classic-themes/customize-api/javascriptunderscore-js-rendered-custom-controls/ |

**Newest pages by `modified`:**

| Modified | Pages |
|---|---|
| 2026-07-22 | `classic-themes/templates/page-template-files`, `global-settings-and-styles/settings/spacing` |
| 2026-07-21 | `classic-themes/basics/reworking-theme-files-organization`, `classic-themes/functionality/custom-front-page-templates` |
| 2026-07-20 | `classic-themes/basics/tools-resources` |
| 2026-06-24 | `releasing-your-theme/required-theme-files`, `global-settings-and-styles/introduction-to-theme-json` |

**Authors.** REST exposes `author`, which is the *original creator*. It does not show who last edited a page.

| Author | Pages |
|---|---|
| Justin Tadlock | 61 |
| Samuel Sidler | 44 |
| KafleG | 6 |
| Jon (Kenshino) | 6 |
| (ID 14167654, user lookup returns 404) | 6 |
| Nick Halsey | 5 |
| Akira Tachibana | 3 |
| Eight others | 1 each |

Revision counts per page, from the `version-history.count` link, range from 1 to 99, with a median of 5. 26 pages have a single revision. Per-revision editors are not exposed without authentication. **[unverified]**

## (c) Content features that affect Markdown conversion

Counts are occurrences and distinct pages. Paths are relative to `https://developer.wordpress.org/themes/`.

### Editor format

| Format | Pages | Notes |
|---|---|---|
| Pure block markup | 98 | Paragraphs, headings and lists carry `wp-block-*` classes. |
| Pure classic HTML | 6 | `releasing-your-theme/writing-documentation`, `classic-themes/basics/reworking-theme-files-organization`, `classic-themes/functionality`, `…/functionality/core-supported`, `…/functionality/localization`, `classic-themes/customize-api`. |
| Mixed | 34 | Heuristic: some class-less `<p>`, `<h*>` or lists alongside blocks. This is often a classic block or freeform HTML inside a block page. |
| Empty | 1 | `classic-themes/customize-api/other-resources`. |

**Malformed nesting** that a converter must tolerate:

- `<p><pre>…</pre></p>` on 10 pages. Examples: `classic-themes/functionality/navigation-menus`, `…/404-pages`, `…/media`, `…/media/audio`, `advanced-topics/ui-best-practices`.
- `<pre class="wp-block-code"><code><pre class="wp-block-syntaxhighlighter-code">` (a pre nested in a code block) on 2 pages: `classic-themes/functionality/custom-logo`, `classic-themes/templates/post-template-files`. This is left over from a SyntaxHighlighter-to-core migration.

### Code

| Feature | Count | Pages | Example |
|---|---|---|---|
| `<pre class="wp-block-code"><code lang="X" class="language-X">` | 657 blocks | 94 | `advanced-topics/build-process` |
| Language `php` | 432 | 60 | |
| Language `json` | 98 | 27 | |
| Language `markup` (Prism's name for HTML) | 46 | 21 | |
| Language `css` | 38 | 19 | |
| Language `javascript` | 23 | 5 | |
| Language `js` | 5 | 1 | |
| Language `bash` | 4 | 2 | |
| Language `xml` | 1 | 1 | |
| No language | 10 | 5 | |
| `line-numbers` class | 54 blocks | 10 | `classic-themes/basics/the-loop` |
| Code shortcodes in source (inferred) | | about 10 | See below. |
| Other bare `<pre>` | 1 | 1 | `classic-themes/functionality/media/images` |
| Block markup comments (`&lt;!-- wp:`) inside code samples | 56 blocks | 15 | `classic-themes/basics/template-files`, `patterns/*`, `features/block-patterns` |
| Shortcode text inside code samples (`[video mp4=…]` and similar) | 8 blocks | 2 | `classic-themes/functionality/media/video`, `…/media/audio` |
| HTML markup inside `<pre>` (`<a href>`) | 2 | 1 | `advanced-topics/ui-best-practices` |
| Inline `<code>` | 3,322 | 109 | |
| `<tt>` (obsolete inline code) | 175 | 5 | `advanced-topics/plugin-api-hooks`, `classic-themes/references/list-of-conditional-tags` |
| Fenced-code collisions (backticks inside code) | 0 | 0 | |
| Literal `<code>` tags inside code samples | 0 | 0 | This is the Jetpack-parser bug from `research/04`. Not triggered here. |

**Code shortcodes in the source (inferred).** The `line-numbers` class plus a `<pre>` wrapped in `<p>` is the exact output of DevHub's `[php]`/`[code]`/`[js]`/`[css]` shortcodes (`inc/formatting.php:905-909`). The 10 pages that show it almost certainly still contain those shortcodes in `post_content`. **[inferred; confirm with the raw export]**

The rendered output contains no literal `[code]` or `[php]`.

One broken legacy shortcode: on `classic-themes/functionality/navigation-menus`, `[html]…[/html]` is not a registered shortcode. It renders on the live site as literal text with `<br />` line breaks. This is an existing content bug.

### Callouts

All callouts are the `wporg/notice` block, rendered as `<div class="wp-block-wporg-notice is-{type}-notice">`.

| Type | Occurrences | Pages |
|---|---|---|
| `info` | 79 | 51 |
| `alert` | 33 | 21 |
| `tip` | 30 | 23 |
| `warning` | 6 | 5 |
| **Total** | **148** | **72** |

**What the callouts contain:**

| Content | Occurrences |
|---|---|
| Block-level content (`<p>`, list or `<pre>`) | 109 |
| Two or more paragraphs | 4 |
| A code block | 2 |
| Inline code | 60 (33 pages) |
| Links | 55 (36 pages) |
| `<strong>` | 13 |
| `<br>` | 8 |
| An image | 1 |

There are no legacy `div.callout` callouts and no `[info]`-style shortcodes in the rendered output. Example: https://developer.wordpress.org/themes/advanced-topics/child-themes/.

### Images

**Volume and origin:**

- 152 `<img>` tags on 62 pages, 151 unique files.
- All are served through Photon (`i0.wp.com` 149, `i2.wp.com` 3).

| Underlying origin | Images | Pages |
|---|---|---|
| `developer.wordpress.org/files/…` (DevHub media library) | 144 | 58 |
| `make.wordpress.org/{docs,core,themes}/files/…` | 5 | 4 |
| `nick.halsey.co/wp-content/uploads/…` (personal site; 3 animated GIFs, live 200 today) | 3 | 1 |

- The make.wordpress.org images are on `classic-themes/functionality/featured-images-post-thumbnails`, `…/widgets`, `classic-themes/customize-api/tools-for-improved-user-experience` and `theme-security/theme-security-issues`.
- The nick.halsey.co GIFs are on `classic-themes/customize-api/tools-for-improved-user-experience`.

**Formats and upload years:**

- File types: jpg 98, webp 26, png 24, gif 3, jpeg 1.
- Upload year for DevHub-hosted files: 2014: 16, 2017: 5, 2022: 2, 2023: 91, 2024: 30.

**Alt text:**

- 140 images have non-empty alt text.
- 12 have empty `alt=""`, on 8 pages, for example `classic-themes/basics/template-hierarchy` and `…/custom-backgrounds`.
- No image is missing the `alt` attribute entirely.

**Presentation details:**

- 131 images (53 pages) are wrapped in a link to the full-size file.
- 17 have a `<figcaption>` (9 pages). Another 10 use legacy `wp-caption` markup from the classic `[caption]` shortcode (3 pages, for example `classic-themes/customize-api`).
- Nearly all have `srcset` and `width`/`height`.
- Alignment classes: `aligncenter` on 5 pages, `alignright` on 2, `alignleft` on 1.
- Most `style=` attributes in the content (35 occurrences on 18 pages) are Photon/lazy-load width attributes on images.

### Tables

- 29 tables on 6 pages:
  - `global-settings-and-styles/settings/settings-reference` (12)
  - `…/styles/styles-reference` (9)
  - `…/settings/spacing` (5)
  - `classic-themes/basics/tools-resources`
  - `classic-themes/customize-api/customizer-objects`
  - `…/tools-for-improved-user-experience`
- 4 of the pages use `wp-block-table`.
- Inline code in cells: 27 tables, 4 pages.
- One table has no `<thead>`, on `tools-resources`.
- One cell contains a literal `|`, on `settings-reference`. It must be escaped in GFM.
- No colspan or rowspan. No block content or `<br>` inside cells.

### Embeds and media

| Feature | Count | Pages | Example |
|---|---|---|---|
| WordPress oEmbed (`wp-block-embed` with a `wp-embedded-content` blockquote and iframe) | 7 embeds, 6 iframes | 3 | DevHub pages embedded in `classic-themes/basics/conditional-tags` and `…/including-css-javascript`. Four make.wordpress.org/themes posts embedded in the orphan `theme-security/theme-security-issues`. |
| `<video>` (`wp-block-video`, VideoPress mp4 `videos.files.wordpress.com/GbdhpGF3/video-25313e7f01.mp4`, live 200) | 1 | 1 | `classic-themes/functionality/media/video` |
| YouTube or other third-party iframes | 0 | 0 | |

### HTML with no clean Markdown equivalent

| Feature | Count | Pages | Example |
|---|---|---|---|
| `&nbsp;` | — | 91 | Mostly cosmetic. |
| `<br>` | 127 | 36 | `advanced-topics/theme-testing` |
| `wp-block-group` wrappers | 5 | 5 | `templates/template-parts` |
| `has-*-color`, `has-*-font-size` and `has-text-align-*` formatting classes | 44 | 11 | `classic-themes/basics/template-files` |
| `<b>` / `<i>` | 21 / 15 | 7 / 4 | |
| `<span>` | 62 | 4 | |
| MediaWiki leftovers (`span.mw-headline` with `id="Custom_Site_Front_Page_Template"`-style ids, `a.mw-redirect`) | 75 | 3 | `classic-themes/functionality/custom-front-page-templates`, `classic-themes/references/list-of-*` |
| `<blockquote>` | 7 | 4 | `getting-started/tools-and-setup` (`wp-block-quote` with `<cite>`) |
| `<dl>`/`<dt>`/`<dd>` | 5 lists | 1 | `advanced-topics/plugin-api-hooks`. Markdown Extra has definition lists. |
| `<abbr>` | 3 | 2 | |
| `<hr>` / separator | 2 | 2 | |
| Nested lists | — | 22 | Markdown handles these. No code blocks appear inside list items. |
| `id` on non-heading elements (anchors) | 63 | 6 | `<div id="changelog">`, `mw-headline` spans |
| `target="_blank"` | 41 | 12 | |
| `details`/`summary`, footnotes, `<sup>`, `<kbd>`, iframes other than oEmbed | 0 | 0 | |

### Headings

**Levels:** h2 417, h3 435, h4 89, h5 4. No h1 appears in any page body.

**Explicit ids.** 162 headings on 18 pages carry an explicit `id` in the stored content. Examples:

- 53 on `classic-themes/basics/conditional-tags`
- 23 on `classic-themes/basics/template-hierarchy`
- `releasing-your-theme/*`
- `advanced-topics/ui-best-practices`
- `advanced-topics/javascript-best-practices`

Some of these ids do not match what the TOC would generate, for example `theme_unit_test` and `1-commonly-missed-requirements`.

**Auto ids.** On the live site, every other h2–h4 gets an auto id from the handbook TOC at render time (`is-toc-heading`, with a `-2` suffix for duplicates). Compare the live HTML of https://developer.wordpress.org/themes/core-concepts/theme-structure/ with its REST content, which has no ids. The TOC applies equally to imported posts, so auto ids survive. Explicit ids must become Markdown Extra `{#id}`. `research/04` verified that `{#id}` works.

**Other heading issues:**

- 3 headings contain links, code or bold.
- 1 page skips a heading level (`classic-themes/functionality/media/images`).
- 1 page starts below h2 (`advanced-topics/theme-testing`).

**Fragment links into the handbook: 33 in total.**

| Outcome | Links |
|---|---|
| Hit an explicit id | 10 |
| Hit only an auto TOC id (approximated with a sanitize-title slug) | 20 |
| Point at a page that 404s | 1 |
| Resolve to nothing today | 2: `href="#"` on `reworking-theme-files-organization`; `#loading-text-domain` on `classic-themes/functionality/internationalization` |

### Links

There are 1,791 `<a>` elements.

| Target | Links | Pages |
|---|---|---|
| Code Reference (`developer.wordpress.org/reference/`) | 446 | 50 |
| Theme Handbook (absolute `https://developer.wordpress.org/themes/…`) | 431 | 97 |
| External, non-WordPress (MDN 33, php.net, w3.org and others) | 235 | 73 |
| codex.wordpress.org | 202 | 18 |
| make.wordpress.org | 95 | 33 |
| wordpress.org plugin and theme directories | 26 + 24 | 7 + 15 |
| GitHub | 22 | 13 |
| HelpHub (`wordpress.org/documentation/`, `/support/article/`) | 21 | 11 |
| core.trac.wordpress.org | 21 | 10 |
| Block Editor Handbook | 20 | 13 |
| Developer Blog (`/news/`) | 18 | 14 |
| APIs handbook (`/apis/`) | 18 | 5 |
| Same-page `#` anchors | 18 | 9 |
| learn.wordpress.org | 10 | 2 |
| Plugin Handbook | 6 | 4 |
| Other | small | — |
| Relative or root-relative | 2 | 2 |
| `http://` (not https) | 25 | 13 |

The two relative links are `/themes/advanced-topics/child-themes/`, and a broken `_wp_link_placeholder` on `classic-themes/basics/main-stylesheet-style-css`.

**Stale internal links:**

- 161 of the 431 Theme Handbook links (on 44 pages) point at paths that are not current page paths. They use pre-reorganization URLs such as `/themes/basics/…`, `/themes/functionality/…`, `/themes/release/…` and `/themes/advanced-topics/theme-json/`, plus the typo `/themes/core-conepts/…` and `/theme/advanced-topics/` on the landing page.
- `curl -L` on the 59 unique targets: 53 return a 301 to a live page (WordPress old-slug or guess redirects, plus `inc/redirects.php`).
- **6 targets return 404** (7 links on 6 pages):
  - `/themes/advanced-topics/validating-your-theme/`
  - `/themes/functionality/comments/`
  - `/themes/functionality/pages-posts-custom-post-types/`
  - `/themes/template-files-section/`
  - `/themes/template-files-section/page-template-files/page-templates/`
  - `/themes/template-files-section/partial-and-miscellaneous-template-files/comments/`
- The 6 pages are `advanced-topics/theme-testing`, `classic-themes/basics/the-loop`, `classic-themes/templates` (and two of its children) and `releasing-your-theme/required-theme-files`.

**How the importer treats links.** It does not rewrite absolute `https://developer.wordpress.org/…` links, so keeping links absolute is the zero-risk one-to-one choice. The old-slug redirects depend on the existing post IDs and their `_wp_old_slug` meta. They survive only if the importer *adopts* the existing posts rather than creating new ones (see (e)). **[redirect mechanism inferred]**

### Shortcode text in prose

Literal shortcode text appears in prose on 4 pages: `[audio]`, `[video]`, `[gallery]`, `[caption]…[/caption]` on `classic-themes/functionality/media/{audio,video,galleries,images}`. The rendered output shows them unexecuted, so the source probably escapes them as `[[audio]]` or `&#91;`. **[inferred]** Imported content passes through `do_shortcode` on display, so the Markdown must keep them escaped. The same applies to the 8 shortcode-bearing code samples. Core's `do_shortcode` does not skip `<pre>`. **[verify in spike]**

## (d) Fidelity-risk list, ranked by pages affected

Severity is about one-to-one visual and semantic fidelity under the Jetpack Markdown Extra parser used by `wporg-markdown`.

| # | Risk | Pages | Severity | Notes / mitigation |
|---|---|---|---|---|
| 1 | Inline code (3,322) and `<tt>` (175 on 5 pages) | 109 | Low | Backticks. `<tt>` becomes backticks. Code containing a backtick needs a double-backtick fence. |
| 2 | Code blocks (657) | 94 | Medium | Fences carry the language. Map `markup` to `html`, or keep `markup`, depending on what the DevHub Prism build accepts **[unverified]**. Map `javascript`/`js`. 10 blocks have no language. The `line-numbers` look (54 blocks on 10 pages) is lost unless DevHub adds it to fenced code or the source keeps `[php]` shortcodes. |
| 3 | `&nbsp;` | 91 | Low | Normalize to spaces, except where intentional. |
| 4 | Callouts, `wporg/notice` (148) | 72 | **High** | Markdown has no equivalent. Options are raw `<div class="callout callout-{type}">` (the Gutenberg docs convention) or `[info]`/`[tip]`/`[alert]`/`[warning]` handbook shortcodes. Markdown is **not** parsed inside raw HTML divs unless DevHub adds a re-parse filter like Playground's `parse_callout_markdown`, and 33 pages have inline code inside callouts. Styling differs: the `wporg-notice` block versus `callout-*` CSS. **[visual diff unverified]** |
| 5 | Images (152) | 62 | Medium | Keep absolute `developer.wordpress.org/files/…` URLs, as the Block Editor handbook does. No sideloading is needed. The link-to-full-size wrapper (131), captions (27), alignment (8 pages) and explicit sizes need HTML or are dropped. |
| 6 | `<br>` hard breaks (127) | 36 | Low–Medium | Trailing two spaces or `<br>`. |
| 7 | Cross-page `#fragment` links to any site (71) | 33 | Low | The 33 fragment links into this handbook survive as long as heading text and ids are unchanged. |
| 8 | Nested lists | 22 | Low | |
| 9 | Explicit heading ids (162) | 18 | Medium | Use `{#id}` on every one. MediaWiki-style span ids on 3 pages need either `{#Custom_Site_Front_Page_Template}`, which may fail the id-charset check **[unverified]**, or inline anchors. |
| 10 | Block markup inside code samples (56 blocks) | 15 | **High (verify)** | The stored HTML must keep `&lt;!-- wp:` escaped. If a raw `<!-- wp:` reaches `post_content`, `has_blocks()` turns true and `wpautop` is skipped, so the whole page loses its `<p>` tags (`research/04`). This is the core subject of the block-theme chapters, so test it first in the spike. |
| 11 | `http://` links (25) | 13 | Low | Copy as-is. |
| 12 | `target="_blank"` (41) | 12 | Low | Lost in plain Markdown. Acceptable, or keep inline HTML. |
| 13 | Block formatting classes (44) | 11 | Low | Center alignment and colors are lost. |
| 14 | Malformed nesting: pre inside p (10), pre inside code (2) | 12 | Medium | The converter must repair it. Source shortcode usage is likely on the same pages. |
| 15 | Empty `alt` (12) | 8 | Low | Preserve `![]()`. Do not invent alt text, because content changes are out of scope. |
| 16 | Tables (29) | 6 | Medium | GFM tables are fine (no spans). Escape one `|`. One table needs a synthesized header row, or must stay HTML. |
| 17 | `wp-block-group` wrappers | 5 | Low | Drop the wrapper. |
| 18 | `<b>`/`<i>`/`<span>` | 7/4/4 | Low | |
| 19 | Literal shortcodes in prose | 4 (+2 in code) | Medium | Must stay escaped, or they will execute. |
| 20 | `<blockquote>` / `<cite>` | 4 | Low | `>` quote. `<cite>` becomes text. |
| 21 | MediaWiki leftovers | 3 | Low | Strip `mw-*` classes. Keep ids only if anything links to them. |
| 22 | oEmbeds (7) | 3 | Medium | A bare URL on its own line should re-embed through `WP_Embed::autoembed` on display. **[unverified for imported posts]** |
| 23 | Legacy `wp-caption` | 3 | Low | |
| 24 | `<abbr>`, `<hr>`, `<dl>` (1 page), `<video>` (1 page) | 1–2 | Low | Inline HTML. Markdown Extra supports definition lists. |
| 25 | SyntaxHighlighter leftovers (`[html]` literal, nested pre) | 3 | Low | Fix during conversion, or preserve the bug for one-to-one fidelity. Owner's call. |
| 26 | Empty page `customize-api/other-resources` | 1 | Medium | Behavior on an empty Markdown file is untested (the H1 and title logic). Keep at least an HTML comment, or confirm in the spike. |

## (e) Blockers and decisions for a one-to-one migration

1. **Orphan with an unpublished parent** (`theme-security/theme-security-issues`, parent ID 11394, which returns 401).
   - A manifest cannot express "parent exists but is not published". The importer loads only `publish` posts.
   - On production the existing post would be adopted. `update_post_from_manifest()` compares the manifest `parent` with the current parent's `post_name` and changes nothing if they are equal. The generated manifest therefore sets `parent: "theme-security"` with no `theme-security` entry. **[inferred; depends on the draft's `post_name` actually being `theme-security`]**
   - On a fresh or local import, `process_manifest_doc()` would read `$manifest['theme-security']`, which is undefined, and fail for that page.
   - **Decision needed:** keep it as is (production-only safe), or publish or restore the parent. Publishing the parent would add a page, which is a structural change.
2. **Duplicate slugs rule out Gutenberg's list format**, which requires unique slugs. They also make bare-slug `parent` values ambiguous. For example, `"parent": "templates"` resolves to the top-level `templates` in `process_manifest_doc()`'s `existing[$parent]` lookup. That is wrong for the children of `classic-themes/templates` if they ever have to be created.
   - The generated manifest uses the keyed-object format, with **path-form parents** (`"parent": "classic-themes/templates"`).
   - In code, path-form parents work for both create (`existing[path]` matches because existing keys are permalink paths, `class-importer.php:84-99`) and update (`get_page_by_path( path )` resolves nested pages, `:391-395`).
   - No production manifest uses path-form parents today. Advanced Administration and SCF use bare slugs. **[inferred from code; verify in spike]**
3. **Adoption, not recreation.** The importer matches an existing post when the manifest key equals its permalink path relative to `/themes/` (`get_existing_for_post`). If they differ, it creates a *new* post, and `wp_unique_post_slug` gives it a `-2` slug. The old post remains published, because the importer never deletes.
   - All 139 generated keys were checked against the live `link`s. 0 mismatches.
   - The landing page is matched through `index` → slug `theme-handbook`.
   - Adoption also preserves post IDs, revisions, old-slug redirects (53 of the stale links depend on them) and comments or meta.
   - The importer's DevHub subclass must use base `themes` and post type `theme-handbook`. `inc/handbooks.php:204` maps `theme` to `themes`.
4. **Raw source is not available unauthenticated.** Converting from rendered HTML bakes in smart quotes, Photon URLs, expanded shortcodes and embeds. Get the raw `post_content` and `post_title` export first.
5. **Title byte-equality.** Six titles contain `&` (stored form unknown: `&` or `&amp;`). One renders an en dash (`Theme Options &#8211; The Customize API`, which may be a texturized `-` in the database).
   - The manifest `title` (after `sanitize_text_field`) is compared to `post_title` on every run. A form mismatch would rewrite the title, and possibly keep rewriting it if kses re-encodes `&` on save, bumping `modified` each cron run. **[inferred; verify with raw titles]**
   - The title sort also breaks the 8 `menu_order` ties, so titles must not drift.
6. **`order: 0` is never re-applied** (`! empty( order )`, `class-importer.php:363`). This is harmless for adopted posts, which keep their current `menu_order`. Pages created fresh do get 0 via `isset`.
7. **Manifest order matters.** `process_manifest_doc()` recurses into a missing parent but then does not re-read the parent's ID, so the child is created without a parent. This is a latent bug at lines 207-220. Parents must precede children in the manifest. The generated file is depth-first.
8. **Content in wp-admin becomes read-only.** Every adopted page's content is replaced on the first `import_all_markdown` pass. Any edit made in wp-admin between export and cutover is lost. A content freeze is required.

## Manifest notes

**Format.** The file is a keyed object, as Advanced Administration's is: `{ "<path>": { title, slug, markdown_source, parent, order } }`. Advanced Administration's entries have exactly these five keys. SCF omits `title` and `order`, and takes titles from the H1.

**Keys:**

- Each key is the page path under `/themes/`.
- The landing page's key is `index`, with `slug: "theme-handbook"` and `order: 0`. Advanced Administration uses slug `handbook` and order `-1`. Here the existing slug is kept so the post is adopted.

**`parent`:**

- Top-level pages have `null`.
- All other pages have the parent's **path** (see blocker 2).
- The orphan has `"theme-security"`, which has no matching entry (blocker 1). The importer will warn on a fresh install.

**`order`:** the live `menu_order`, verbatim.

**`title`:** the entity-decoded rendered title. It is unverified against the raw `post_title` (blocker 5).

**Guessed values:**

- **`markdown_source` (guessed).** `https://github.com/WordPress/theme-handbook/blob/trunk/` + `<path>/index.md` for pages that have children, or `<path>.md` for leaves. The landing page is `index.md`. The repository name and branch are placeholders. The `chapter/index.md` layout copies Advanced Administration's. Each source is unique.
- **No `meta` key**, and no extra keys, so the file stays within what the importer reads.
