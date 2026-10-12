# Theme Handbook: migration plan to a GitHub Markdown source

> **Naming.** The handbook's title is "Theme Handbook" (page `<title>` and the landing post's `post_title`). Its own
> intro paragraph and the Themes team's About page say "Theme Developer Handbook"; quotes below keep whatever
> wording the source used. These notes use "Theme Handbook".

**Status:** plan, 2026-10-12. Synthesised from four research reports (listed at the end) and a working local spike.
Nothing has been proposed publicly yet.

## 1. The one-paragraph version

The Theme Handbook (developer.wordpress.org/themes, post type `theme-handbook`, 139 published pages) is
edited in wp-admin by a small group. Its organization is settled and must not change. The goal is to move the
*source* to a Markdown repo in the WordPress GitHub org and have developer.wordpress.org import it through the same
`DevHub_Docs_Importer` pipeline that already serves the Block Editor, Playground, Secure Custom Fields (SCF),
Coding Standards and Advanced Administration (AAH) handbooks. The spike proved the round trip: with a path-keyed
manifest the real importer **adopts all 139 existing posts in place** (0 created, 139 updated; IDs, URLs, titles,
parents and order untouched), the converted content matches production on 130 of 139 pages exactly and on the
other 9 only in ways that are not organizational, and a no-change re-run costs 0.13 s. The wiring is one
~35-line importer subclass plus one `require`. The hard parts are not code: a content freeze and a wp-admin editing
lock at cutover (the plugin handbook's 2023 mirror diverged because neither happened), a CI guard against a slug
hijack the importer is prone to, one orphaned page under an unpublished parent, and lining up a Meta committer
before posting the proposal. The trusted maintainer, Justin Tadlock, asked for exactly this move in public in
January and August 2024, and the only translation team (Japanese, 139 Markdown files mirroring the English tree)
asked for a GitHub source the same year. Realistic calendar: 4 to 8 weeks once a committer is named.

## 2. What "one-to-one" means, concretely

These are the invariants every step below protects. The spike verified each on a full local copy.

| Invariant | How it is kept |
|---|---|
| Every URL identical (139 of 139 return 200 at the same path) | Manifest keyed by the page's permalink path under `/themes/`; importer base `'themes'`; existing posts adopted by path match |
| Same post IDs, revisions, authors, first-published dates | Adoption, not re-creation; the importer never writes `post_date` or `post_author` on update |
| Same titles, byte for byte | Manifest `title` = raw `post_title`; 64 pages tie on `menu_order` and are sorted by title, so titles are load-bearing |
| Same parents and chapter order | `parent` = parent's path key (bare slugs are ambiguous: 7 slugs are reused on 14 pages); `order` = current `menu_order` verbatim |
| Same deep links | 162 explicit heading ids carried as `{#id}`; 940 of 941 headings matched (the one miss is an empty `<h2>` in production) |
| Old-URL redirects keep working | They are core slug-guessing on `post_name`, which adoption preserves; **the redirect map is empty** |
| Same landing page at `/themes/` | Manifest entry `index` with `slug: theme-handbook` (the existing slug, not AAH's `handbook`) |
| Images unchanged | All 152 stay as absolute `developer.wordpress.org/files/` URLs; no sideloading |
| Notices, code, tables render the same | 148/148 notices, 657 code blocks and 29/29 tables matched after the converter and transform fixes in §4 |

Out of scope by design: any rename, merge, reorder, rewrite, or alt-text improvement. Content defects found by the
inventory (an empty page, a legacy `[html]` block, nested `<pre>` on two pages, six dead internal links) are listed
for a *follow-up* content PR after cutover, owned by the maintainer.

## 3. What exists today (measured 2026-10-12)

- 139 published pages: landing page plus 10 chapters, depth 0 to 4, about 124k words. Classic Themes is 59 pages.
- Low churn: 19 pages modified in the last 12 months, 23 in 24. Oldest page 2015. A freeze costs nothing.
- Authors on record: Justin Tadlock 61 pages, Samuel Sidler 44. 2026 editing done by Cheyne (@chekle), inferred from
  issue-close times matching page `modified` times.
- Content features: 657 code blocks on 94 pages (php 432, json 98, markup 46, css 38; 56 blocks contain block-markup
  comments as sample code); 148 notices on 72 pages (info 79, alert 33, tip 30, warning 6); 152 images on 62 pages
  (3 on a personal domain); 29 tables; 7 embeds; 1,791 links (446 to the code reference, 202 to the Codex).
- Two structural oddities: 7 slugs reused across 14 pages (`templates` appears at four paths), and
  `theme-security/theme-security-issues` is published under an **unpublished** parent (ID 11394).
- Ownership: Themes team "maintains" it; Docs team lists three Theme Handbook reps. Intake is the
  Documentation-Issue-Tracker `themes` label (73 open issues). No GlotPress project; one translation (ja).
- No theme-handbook repo exists in the WordPress org. Precedents: AAH (new handbook, 2023, dd32 fixed the manifest
  himself), SCF (ticket and importer merged the same day, 2025-02-20), Accessibility handbook (in flight, first import
  failed on manifest errors), and the Plugin Developer Handbook mirror (never switched; 65 of 102 pages edited in
  wp-admin since, 34 repo PRs never reached the site).

## 4. The design

### 4.1 Content repo

- **Name:** `WordPress/developer-themes-handbook` (first choice: the org convention is `<topic>-handbook`, and the
  `developer-` prefix is how `developer-plugins-handbook` is told apart from the Plugins *Team* `plugins-handbook`;
  Themes has the same ambiguity). `theme-developer-handbook` (the official title's word order) is the acceptable
  alternative; let Meta settle it in the ticket. Default branch `trunk`. Must meet the 2025-06 org repo criteria: named maintainers from an established
  team in README and CODEOWNERS, problem statement, make-blog tag.
- **Layout:** one folder per chapter, `index.md` for pages with children, `<slug>.md` for leaves, mirroring the URL
  tree exactly (this is also the Japanese team's layout). `manifest.json` at the repo root, keyed by path:
  `{ "<path>": { title, slug, markdown_source, parent, order } }`, parents before children, `parent` = parent key,
  `index` = the landing page.
- **CI (required checks, copied from SCF's `docs-manifest.yml` and extended):** regenerate the manifest and fail if
  stale; keys unique and equal to the frozen list of 139 paths (additions allowed, removals and renames fail without
  a linked redirect PR); **a new entry's slug must not equal any existing slug** (the importer's slug fallback
  silently hijacks the existing post, reproduced in the spike); `parent` is null or an existing key, with
  `theme-security` as the one documented exception; `order` is an integer equal to the frozen value; exactly one plain
  H1 equal to `title`; `markdown_source` is a `github.com/…/blob/trunk/…` URL (raw URLs break the edit link); no
  unescaped `<!-- wp:` outside code fences (it disables `wpautop` for the whole page); link check; Props Bot.
- **Governance:** CODEOWNERS `* @justintadlock @chekle`; GitHub team `theme-handbook-maintainers` (Justin, chekle,
  kafleg, carolinan, TeBenachi) with write; Documentation team with triage. Branch protection: one approving review
  from a CODEOWNER, required checks, no force-push, admin bypass as the maintainer's fast path (audited by GitHub).
  Maintainers may self-merge their own PRs, as SCF does; a 7-day first-response target for others. Keep the
  "paste your text in an issue, a maintainer opens the PR with `Co-authored-by`" path for people without GitHub.
  Transfer the 73 open `themes` tracker issues in one batch after re-creating the labels; keep #816 as the umbrella.
  Keep `credits.md` at slug `credits` (the theme's `autolink_credits()` depends on it).

### 4.2 Conversion

Use this repo's converter (`scripts/convert.py`) with the five fixes the spike made, not dmsnell/html-to-md, which
indents code fences, loses images and table separators, and dropped links. Convert from a **raw** export
(`post_content` and `post_title` via WP-CLI or WXR), not from the public REST API, which returns texturized,
shortcode-expanded HTML. Conventions the spike validated:

- Notices are written as **GitHub alerts** in the Markdown (`> [!NOTE]` → info, `[!TIP]` → tip, `[!WARNING]` →
  warning, `[!CAUTION]` → alert; `[!IMPORTANT]` falls back to alert), so they render well on GitHub and follow this
  repo's 2026-10-07 convention for HelpHub (`notes/markdown-conventions.md`). The importer's `before_transform`
  filter (drafted and tested in research 02) rewrites them to the handbook shortcodes `[info]`, `[tip]`,
  `[warning]`, `[alert]`, which DevHub renders to exactly the production `wporg/notice` markup (148/148 identical in
  the spike, including inline code inside notices). Do **not** emit `.callout-*` divs: they are styled differently
  and are what the Block Editor handbook uses today (raw HTML, unstyled on GitHub); converting Gutenberg's 41 files
  to alerts is a separate consistency PR.
- Fenced code with the language; the importer transform adds `wp-block-code` so the Copy and Expand buttons return.
- `{#id}` on every explicit heading id; `<br>` and `&nbsp;` normalized; tables as GFM; one table keeps HTML.
- Literal `[audio]`, `[video]`, `[gallery]`, `[caption]` on the four media pages stay escaped (`[[…]]`); entity
  escaping does not survive kses.
- Images keep their absolute URLs; captions and link-to-full-size wrappers stay as inline HTML.
- Block-markup samples inside code fences stay escaped (tested: no page lost its paragraphs).

### 4.3 Importer wiring (wporg-developer)

- `inc/import-theme.php`: a `DevHub_Docs_Importer` subclass calling `do_init( 'theme', 'themes', $manifest_url )`,
  plus one `require` in `functions.php`. `inc/handbooks.php` already lists `theme` and pluralizes it to `themes`;
  **the `'themes'** base is load-bearing** (any other value breaks path matching and the duplicated slugs collide).
- Per-handbook transforms (all spike-tested): GitHub alerts → notice shortcodes, shortcode escaping inside code,
  `wp-block-code` on `<pre>`, relative `.md` link rewriting. Drafts are in research 02 §5.1 and `spike/importer/import-theme.php`.
- Editing lock: a `map_meta_cap` filter removing `edit_post` on `theme-handbook` for everyone but administrators,
  verified in the spike. See §5 decision 3.
- Optional hardening PR to `wporg-markdown` (meta SVN or `WordPress/wordpress.org`): match exact path first and fall
  back to slug only when unique; keep the parent ID after recursive creation; key existing posts by `get_page_uri()`.
  Not required for production adoption (the path match hits first), but it is what made a *fresh* import correct in
  the spike, and it protects every handbook with repeated slugs.
- Deploying the importer before the manifest exists is safe: it 404s and does nothing. The go-live switch is the
  manifest appearing at the configured URL.

### 4.4 What changes for readers and editors

- Pages switch to the `single-handbook-github` template automatically: "Improve it on GitHub" and "See list of
  changes" links appear. "Last updated" shows the cutover date on every page (wporg-developer #464/#505 are open).
- Edits happen by PR; the wp-admin "Edit" link redirects to GitHub. Repo merges reach the site within 15 minutes.
- The Feedback page, the Docs role page, the Themes "Projects" entry and the tracker bot pings need updating.

## 5. Decisions to settle before starting (with recommendations)

| # | Decision | Recommendation |
|---|---|---|
| 1 | **The `theme-security` parent.** The published page `theme-security/theme-security-issues` sits under an unpublished parent. Adoption keeps it as is on production; a manifest entry for the parent would create a published duplicate; a fresh import fails for the child. | Keep it as is for cutover (no manifest entry; documented CI exception). Ask the maintainer whether the section page should be published later as a deliberate content change. The spike's "private parent" importer support is the fallback if they want the page gone from fresh imports. |
| 2 | **Repo name and branch** | `developer-themes-handbook`, `trunk` (alternative `theme-developer-handbook`); Meta's call. |
| 3 | **wp-admin editing after cutover** | Lock it (admins only) and say so in the proposal. The importer only warns, and an edit survives until the file next changes, then vanishes. This is the plugin-mirror failure mode. Optional: a nightly drift check alerting #docs. |
| 4 | **Issue intake** | Transfer the open `themes` issues to the repo; pin a pointer in the tracker. |
| 5 | **Assets** | Keep images in the media library at their current URLs. Moving 152 images into the repo is a separate, optional change. |
| 6 | **Code UI parity** | Add `wp-block-code` in the theme-handbook transform now; propose the same for the base importer later (Block Editor, AAH and SCF lack Copy/Expand today). |
| 7 | **"Last updated" at cutover** | Accept the cutover date, or ask Meta to keep `post_modified` with a one-off filter during the first import. |
| 8 | **Japanese team** | Tell them before cutover, publish the "conversion only" commit, offer a path map. Their 139-file tree already matches. |

## 6. Phased plan

**Phase 0: pre-wire (1 week).** Confirm with Justin Tadlock and Cheyne that they want the move and will co-author
the proposal; agree CODEOWNERS and the editing lock; get one Meta committer (dd32 or coffee2code) to agree to review
the importer PR and run the first import. Ask an admin for the count of non-published `theme-handbook` posts.

**Phase 1: proposal (2 to 3 weeks).** Post on make/themes (tag `#theme-documentation`), cross-post to make/docs and
make/meta. Lead with "no URL, title or order changes" and attach the zero-diff URL list. State the editing lock, the
freeze window, intake transfer, and translation impact. Two-week comment window plus an agenda item at a Themes
meeting and a Docs meeting. Then a Meta Trac ticket in the Developer Hub component scoped to this one handbook,
citing Justin's #7520 comment and the SCF precedent.

**Phase 2: build (1 to 2 weeks, overlapping Phase 1).** Create the repo in the org (or build privately and transfer,
with the manifest URLs updated after transfer, the Accessibility handbook's lesson). Land CI first. Open the
wporg-developer importer PR. Convert from a raw export and open the content PR for the maintainer to review by diff
report and screenshot comparison (the spike's `compare.py` and `screenshots.mjs`). Prepare the Japanese team.

**Phase 3: dry run (days).** On a sandbox or wp-env seeded with a copy of production rows, run both cron events and
confirm "created 0, updated 139", identical paths, parents, orders, titles, and a clean rendered diff. Clear ETags
and re-run after any transform change. Check watcher emails (Email Post Changes) and oEmbeds that the local site
cannot render.

**Phase 4: cutover (one day, ordered).**
1. Announce the freeze; from this point every wp-admin edit must be re-applied in Git.
2. Raw export and full backup of `theme-handbook` rows (rollback source).
3. Regenerate Markdown and manifest from that export; CI green.
4. Merge the importer PR; sync and deploy (inert until the manifest exists).
5. Merge the content PR with `manifest.json` at the configured path.
6. A Meta committer runs, in order, `wp cron event run devhub_theme_import_manifest` then
   `devhub_theme_import_all_markdown`, immediately, to avoid a 15-minute window of GitHub template around old content.
7. Verify: post count unchanged, no new IDs, 139 URLs 200 with the GitHub links, `/themes/` still the landing page.
8. Apply the editing lock; transfer issues; update the Feedback page and role pages; announce.
9. Trash nothing, move nothing, re-slug nothing in wp-admin, ever (the importer re-creates trashed pages and
   duplicates re-slugged ones).

Rollback is content-only because IDs and URLs never change: revert the `functions.php` line, delete the
`wporg_markdown_*` meta, restore `post_content` from the backup, unschedule the two events.

**Phase 5: after cutover.** Follow-up content PR for the known defects; propose the `wporg-markdown` matching fix
and the base-importer `wp-block-code` change; review the 7-day SLA at the first monthly Themes meeting.

## 7. Risks

| Risk | Mitigation |
|---|---|
| Dual source of truth after cutover | Editing lock, short freeze, every "how to contribute" page updated the same day |
| No Meta committer picks it up (#7520 idle since 2024-08) | Name one in Phase 0; write the importer PR ourselves; scope to one handbook |
| dd32's #7520 objection reused | This is developer docs, his stated "works great" case; the issue-comment path stays; the only translators asked for GitHub |
| Maintainer bandwidth (Automattic-sponsored; AAH reviews run 34 to 38 days) | Two CODEOWNERS, maintainer bypass, 7-day SLA, monthly triage |
| First import breaks on the manifest (AAH 2023, Accessibility 2026) | CI validation, dry run, build in the final repo |
| Slug hijack by a future new page | CI rule; optional upstream matching fix |
| Drafts and private pages invisible to the importer | Inventory with an admin before conversion |
| Read as a structural rewrite | Lead with the zero-change invariants and the URL diff |
| Silent import stall (Code Reference precedent) | Ask Meta for a "last imported commit" indicator or a stale-import alert |

## 8. People

Justin Tadlock (content owner, proposal author), Cheyne (2026 editor), Themes reps @bijayyadav and @fahimmurshed,
Docs Theme Handbook reps @kafleg, @poena, @utz119, Docs reps @estelaris and @milana_cap for acknowledgement, Meta
@dd32 or @coffee2code for review and deploy, and the Japanese team (@t-hamano, @mkismy) as downstream. The fifteen
questions to put to them are in research 04 §8.

## 9. Research files

| File | Contents |
|---|---|
| `research/01-content-inventory.md` | Full tree, freshness, every conversion-relevant construct with counts, ranked fidelity risks, blockers; data in `research/data/` (page export, generated manifest) |
| `research/02-pipeline-precedents.md` | Importer contract with file/line references, transforms, template behaviour, AAH and plugin-mirror history, draft `import-theme.php`, deploy and cutover steps, CI invariants, open questions |
| `research/03-spike.md` | The local round trip: converter decision, importer fixes, page-by-page fidelity, cutover behaviours, timings, ranked fixes |
| `research/04-governance-process.md` | Ownership evidence, 2023 to 2026 history, AAH and SCF process comparison, proposal path, repo design decisions, translation, risks, questions |
| `spike/` | Rerunnable scripts (fetch, convert, serve, compare, screenshots), the importer subclass, the manifest, sample Markdown, results and screenshots |
