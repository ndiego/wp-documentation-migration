# How WordPress.org publishes GitHub-hosted documentation, and what that means for HelpHub

Date: 2026-10-11. This is the synthesis of five research reports in `research/` (desk research by
parallel agents plus one hands-on spike). Read this first; go to the numbered reports for evidence,
file paths and commit SHAs. Everything marked **[unverified]** in the reports stays unverified here.

| Report | Covers |
|---|---|
| `research/01-gutenberg-source-side.md` | How the Block Editor handbook is authored and built in `WordPress/gutenberg` |
| `research/02-wporg-consumer-side.md` | How developer.wordpress.org pulls, imports, renders and deploys it |
| `research/03-handbook-landscape-survey.md` | Every .org docs site compared; the 2023 proposal to move HelpHub to GitHub |
| `research/04-importer-spike.md` | The real importer run against this repo's `docs/` on a local WordPress |
| `research/05-process-governance-deployment.md` | Docs team process, Meta deployment, translations, open questions |
| `spike/` | Re-runnable spike: test plugin, ETag server, fixtures, sample output |
| `documentation-inventory.md` | Every WordPress.org documentation section, how it is published today, and which tier of scope it belongs to |

## 1. The one-paragraph version

Every GitHub-backed handbook on WordPress.org works the same way. Markdown lives in a GitHub repo together
with a `manifest.json` that lists each page's slug, parent, title and source file. On the WordPress side a
small plugin, `wporg-markdown`, runs two WP-Cron jobs every 15 minutes: one fetches the manifest and creates
or updates posts in a hierarchical custom post type (parent and menu order from the manifest), the other
fetches each page's Markdown, converts it to classic HTML with Jetpack's GitHub-flavored Markdown parser,
runs it through kses, and saves it. Nothing is pushed from GitHub, nothing is ever deleted, and every
handbook-specific concern (link rewriting, image hosting, callouts, redirects, the "Edit on GitHub" link)
is handled by a per-handbook PHP subclass that lives in the .org theme repo, not in the docs repo.

## 2. The Block Editor handbook end to end

### 2.1 Source side (Gutenberg repo)

- **`docs/toc.json`** is a hand-edited tree of file paths plus three expansion tokens (`{{components}}`,
  `{{blocks}}`, `{{packages}}`). `npm run docs:gen` (now in the `tools/docs/` workspace,
  `@wordpress/docs-tools`) flattens it into **`docs/manifest.json`**, a JSON array of
  `{title, slug, parent, markdown_source}`. Array order is menu order. There is no `order` field and no
  frontmatter anywhere.
- The slug is the file basename (folder name for `README.md`) and must be unique across the whole handbook;
  the generator throws on duplicates. The title is the first `# H1`. `markdown_source` is relative
  (`../docs/x.md`) and the importer resolves it against the manifest URL on `trunk`.
- **362 of 551 pages come from outside `docs/`**: package READMEs, component READMEs and per-block pages
  generated from `block.json` and JSDoc. CI (`static-checks.yml`) runs the whole `docs:build` and fails on any
  diff, so generated docs can never be stale on trunk.
- Conventions: one H1 per page; links written as repo-root-absolute file paths (`/docs/.../file.md`) that
  the importer rewrites; links inside callouts are not rewritten and must be full URLs; images must be
  uploaded by hand to the developer.wordpress.org media library (GitHub-hosted images got rate-limited);
  videos are YouTube iframes; callouts are raw `<div class="callout callout-info">` HTML.
- Review: CODEOWNERS for `/docs` is two people; PRs carry `[Type] Developer Documentation`; roughly 40% of
  docs PRs also change code. The handbook publishes from trunk, so it documents unreleased features. That
  is a long-standing open complaint.
- **The Gutenberg repo has no redirect mechanism.** A rename needs a second PR to `wporg-developer` to add
  a line to a hard-coded PHP array. The proposal to put `redirect_from` in the manifest has stalled since 2023.

### 2.2 Consumer side (developer.wordpress.org)

- `wporg-markdown` is the generic engine (its three PHP files are byte-identical to the copy in
  `notes/reference/wporg-markdown/`). Six handbooks subclass a theme base class, `DevHub_Docs_Importer`:
  Block Editor, Playground, REST API, Coding Standards, Advanced Administration and Secure Custom Fields.
- Two cron events per handbook, `devhub_{type}_import_manifest` and `devhub_{type}_import_all_markdown`,
  each every 15 minutes, **not ordered**, so a brand-new page can be live with empty content for up to one
  tick. No webhook, no wp-cli command; imports are triggered with `wp cron event run`.
- Change detection is a per-post **ETag** on the raw GitHub URL. Post IDs are stable across runs. A failed
  manifest fetch changes nothing.
- **Nothing is ever deleted or trashed.** A page dropped from the manifest stays published. A slug change
  creates a new post and leaves the old one live, which is why `import-block-editor.php` carries about 70
  hard-coded redirects.
- The Block Editor subclass's `before_transform` strips the H1 (so titles come from the manifest), rewrites
  `(../)+docs/`, `/docs/` and `/packages/` links to absolute developer.wordpress.org URLs, and converts
  `~~x~~`. Its `after_transform` turns `{% codetabs %}` into tabbed HTML. Only Playground's subclass
  sideloads images; everything else expects absolute image URLs.
- Rendering: block templates `single-handbook-github` and `single-handbook-block-editor`; the sidebar is the
  `wporg/chapter-list` block ordered by `menu_order`; heading ids and the in-page TOC come from
  `wporg/table-of-contents` at render time. Code is `<pre><code class="language-x">` highlighted by the Code
  Syntax Block plugin.
- The stored HTML is classic. The parser strips bare `<p>` tags and relies on `wpautop` at render time.
  If any block comment is present, `has_blocks()` disables `wpautop` and the page loses all its paragraphs.
- kses strips `iframe`, `script`, `style`, `svg`, `source` and `form`; `details`, `kbd`, `<video src>`,
  `class`, safe `style` and `data-*` survive.
- The "Edit on GitHub" link only works for Block Editor because of a `get_post_metadata` hack that rewrites
  the stored raw URL. Playground's live edit link points at the raw file.

### 2.3 Deployment

- `wordpress.org` on GitHub is a **mirror of the Meta SVN repo**. Changes to `wporg-markdown` or the
  `handbook` plugin need a Meta Trac ticket and an SVN commit by a Meta committer.
- `wporg-developer` and `wporg-documentation-2022` take GitHub PRs to `trunk`; a workflow builds and
  force-pushes a `build` branch; the step from there to production is internal **[unverified]**.
- A merged docs change needs no deploy and is live in about 15 to 20 minutes, unless it renames or moves a
  page.

## 3. What the hands-on spike showed

The real importer ran against this repo's `docs/manifest.json` unchanged (relative `markdown_source` paths
resolve against the manifest URL) on a native WordPress 7.1.3 with Jetpack 16.3.

- **Structure imports perfectly.** 362 entries became 362 posts; every parent, slug, `menu_order`, permalink
  and title matched. No PHP warnings. About 4 seconds locally.
- **Every relative link and image is broken.** The base importer rewrites nothing: 2,254 `.md` links on 273
  pages and 2,300 `../../assets/` image paths on 261 pages are stored verbatim. A proof-of-concept rewrite
  that resolves them from the manifest is in `spike/helphub-spike-importer`. The transform filters do not
  receive the post, so the subclass has to override `update_post_from_markdown_source()` to know which file
  it is processing.
- **`> [!NOTE]` callouts render as literal text** on 174 pages, and adjacent callouts merge into one
  blockquote. We need either HTML callouts in the Markdown or a conversion in the subclass.
- **Titles:** the H1 wins only if it is the first line after frontmatter and is plain text (backticks and
  link syntax end up literally in the title). A manifest title change is ignored while the file is
  unchanged. A UTF-8 BOM or a `---` inside a frontmatter value corrupts the page.
- **Lifecycle:** unchanged re-runs touch nothing when the host sends ETags, and bump every `post_modified`
  when it does not. Removed pages stay live. Renamed slugs duplicate. **A duplicate slug anywhere in the
  manifest silently takes over the existing post with that slug**, moving it and replacing its content.
  A child listed before its parent briefly gets no parent. `order: 0` is ignored.
- **kses depends on how cron is triggered.** Under WP-CLI only the importer's explicit kses pass runs. Under
  HTTP `wp-cron.php` kses runs again on title and excerpt, turning `&` into `&amp;` in 8 titles.
- One parser bug: literal `<code>` tags inside a fenced block let raw HTML through
  (`write-code-in-your-posts-classic-editor`).

Section 7 of the spike report is the concrete checklist for our converter, manifest and CI.

## 4. Where HelpHub differs from every GitHub-backed handbook

| Importer assumption | HelpHub reality |
|---|---|
| Hierarchical post type; URL path from the `parent` chain | `helphub_article` is flat: `/documentation/article/{slug}/` |
| Grouping through `post_parent` and `menu_order` (chapter list) | Grouping through the `category` taxonomy plus theme-rendered landing pages |
| Importer runs on developer.wordpress.org, subclass in `wporg-developer` | Code would live in `support-helphub` inside `wporg-documentation-2022`; `wporg-markdown` must be active on the documentation site **[unverified]** |
| Images are absolute URLs, uploaded by hand | HelpHub has its own media library with 7,200 attachments already |
| New handbook, no existing content | About 320 live articles with IDs, URLs, comments and inbound links |

Consequences:

- A HelpHub importer subclass needs **taxonomy assignment** (`wp_set_object_terms`, since `tax_input` fails
  under cron with no user), a flat `get_base()`, link and image rewriting, callout conversion, and its own
  redirect and orphan handling. None of this exists today.
- **Slug matching adopts existing articles in place.** A manifest entry whose slug equals a live article
  takes it over, keeping its ID, URL and comments, and overwrites its content on the next run. That is the
  migration path and also the biggest risk (see the duplicate-slug finding above).
- Alternatively, HelpHub's content model changes to a hierarchical post type with path URLs, which is what
  this repo's restructure proposal already assumes. That is a Meta-team decision, and it makes the
  importer fit without modification but needs a redirect map for every existing `/article/` URL
  (HelpHub already keeps 71 hard-coded redirects in its mu-plugin).

## 5. This has been proposed before

- **2023-09-06**, Javier Casares on make/project: move foundational docs to GitHub, one repo per segment,
  ISO language folders, a manifest, H1 plus a final "Changelog" H2 per article, maintainer and translation
  editor roles.
- **2023-09-25**, Milana Cap on make/docs: the Docs and Polyglots teams are "moving complete end-user
  documentation (HelpHub)" into `WordPress/documentation-end-user`.
- The repo got stub `index.md` files, one-entry manifests per language, and **no commits since
  2024-02-16**. No article was ever migrated. The README cites unspecified "technical challenges". No public
  post explains the stall.
- **2025-12-02**, Estela Rueda on make/docs: the current direction is to write **directly in WordPress** and
  review after publication, with GitHub used only for issue tracking. The 2026 posts do not mention
  Markdown or GitHub as a source of truth.
- Related cautionary case: `WordPress/developer-plugins-handbook` (created 2023-11-12) is neither a mirror nor a
  finished migration: Meta #7361 stalled after one comment, no importer was ever added, wp-admin stayed writable, and
  both sides diverged (65 of 102 live pages edited in wp-admin since; 34 repo PRs merged, none on the site, as of
  2026-10-12). See `notes/theme-handbook-migration/README.md` §3.1 and research 02 §4.2 for the measured state and the
  cutover rules derived from it.
- **Generate the manifest in CI.** WP-CLI regenerates it on push via a bot PR; Secure Custom Fields fails a
  PR with a stale manifest; Playground generates it from the Docusaurus sidebar. Advanced Administration and
  Coding Standards hand-edit theirs and have no CI at all.
- **Solve images up front.** Only Playground sideloads them. Advanced Administration's images are spread over
  HelpHub's media library, GitHub issue attachments, the repo and the Codex.
- **Plan deletions and redirects outside the importer.** Every repo's README says removed pages are deleted
  by hand on the .org side.
- **Never create a mirror without switching the importer.**
- **Advanced Administration is the closest precedent**: a Docs-team-owned handbook, moved to GitHub in
  2022 to 2023, still active with a small group of maintainers, and the first import needed a Meta committer
  to fix branch, slug and parent mistakes in the hand-written manifest.

## 7. Process, people and deployment

Details and citations are in `research/05-process-governance-deployment.md`.

- **Who publishes HelpHub today.** A small group holds wp-admin publish rights: mainly Estela Rueda, Milana Cap,
  Akira Tachibana, with Andrea Roenning writing much of the release documentation. Access is requested by DM in
  Slack. The team has deliberately refused publish rights to core committers who are not Docs members, so a
  GitHub repo needs equivalent gatekeeping (CODEOWNERS and required reviews).
- **Intake.** Issues go through `WordPress/Documentation-Issue-Tracker` (templates, `/assign` and `/review`
  comment commands, per-release project boards). There were 231 open HelpHub issues on 2026-10-11. Contributors
  without access already paste Markdown drafts into issue comments, which a publisher retypes in wp-admin.
  That is a de facto GitHub-to-WordPress hand-copy workflow.
- **Release cycle.** One issue per article per release, screenshots posted as issue comments, uploaded by someone
  with media rights. The December 2025 proposal moves toward writing directly in WordPress, scheduling for
  release day, and reviewing after publication. The team's stated pain is review throughput, not the editor.
- **The main objection on record** is from Meta lead Dion Hulse on Meta Trac #7520 (March 2024): GitHub plus
  Markdown "isn't accessible to all"; it "works great" for Block Editor docs because docs and code change in the
  same PR but "can be total shambles for other content"; it is "a workaround" for WordPress.org lacking a
  suggest-edits flow; and Gutenberg Phase 4 multilingual work "will be reliant upon having WordPress posts as
  the source-of-truth". Training and Polyglots contributors agreed. The strongest reply available to us is his
  own exception: HelpHub is now block-centric, and per-block user docs belong next to block code.
- **Content deploys itself; code does not.** Measured on 2026-10-11, Gutenberg docs commits reached
  developer.wordpress.org in 4 to 15 minutes with no human step. Code changes (an importer subclass) need a PR
  to `wporg-documentation-2022` or a Meta SVN patch, then a Meta committer runs a sync script on a sandbox and
  `deploy-dotorg.sh`, then activates plugins per site with WP-CLI. WordPress.org runs Cavalcade for cron
  **[indicated by code, not confirmed by Systems]**.
- **A hazard in the HelpHub codebase.** `support-helphub` has two upstreams, Meta SVN and the GitHub repo, and
  running the sync can silently revert SVN-only changes (nearly happened in July 2026, PR #113). Fix that
  before adding importer code there.
- **Turnaround.** Advanced Administration took about 8.5 months from Meta ticket to live, but the Meta work was
  about one day once content was ready. The Plugin Handbook's GitHub move stopped syncing for weeks in
  2024. The developer Code Reference silently stopped updating for over two years. Calendar time is dominated
  by consensus and by finding a committer, and silent failure needs monitoring.
- **A favourable opening.** The Meta Janitors group (April 2026, includes dd32 and annezazu) is told to "explore
  tighter integration between WordPress.org and version-controlled workflows". Counterweight: the block.json
  auto-docs PR was reverted in 2026 for "insufficient community discussion", so post a make/docs proposal first.
- **Translation is the hardest question.** Of 199 Rosetta sites, 17 have HelpHub enabled and 12 have published
  articles; only fr (296), ja (264) and it (239) are near complete (measured 2026-10-12, published posts only;
  see research 05 §6). Each copy is a one-time WXR import maintained independently with no sync or change
  notification, so **an English overhaul changes nothing on those sites and makes a later re-import harder**
  (research 05 §6.1). The Polyglots plan is GlotPress-based content translation (GlotPress PR #1856, open
  since 2024-08). A Git history gives locale teams the per-article diff they have asked for, but a GitHub source
  of truth collides with the "WP posts are canonical" assumption. Recommendation from the report: English-only
  in GitHub for phase 1, publish per-article commit links so locale teams can detect drift, promise no
  translation tooling.

## 8. Open questions for the Docs and Meta teams

The full list of 20 is at the end of `research/05-process-governance-deployment.md`. The ones that change what
we build:

1. **Content model.** Import into the existing flat `helphub_article` type (keeps IDs, URLs, feedback comments,
   Rosetta relationships; needs taxonomy support in a subclass) or move HelpHub to a hierarchical post type with
   path URLs (fits the importer as is; needs a redirect for every `/article/` URL)?
2. **Scope of the first move.** All 320 articles, or only the per-block pages where the "docs next to code"
   argument is strongest?
3. **Where the importer code lives.** `support-helphub` in `wporg-documentation-2022`, the generic `handbook`
   plugin importer (config-driven, no subclass), or additions to `wporg-markdown` itself (Meta SVN)?
4. **Images.** Repo-hosted and sideloaded by the importer (Playground's model), or hand-uploaded to the HelpHub
   media library with absolute URLs (Block Editor's model)?
5. **Release-day publishing.** How do articles for an unreleased WordPress version stay unpublished until
   release day: a branch, a manifest flag, or merged-but-unlisted?
6. **Non-GitHub contributors.** Is "paste a draft in an issue, a maintainer opens the PR" an accepted path? Is a
   Playground or GitHub web-editor flow acceptable to the Docs team?
7. **Deletions and renames.** Who trashes orphaned posts and maintains the redirect map, given the importer does
   neither?
8. **Monitoring.** How is an import failure surfaced (CI manifest check, alert to #docs or #meta, a visible
   "last imported commit" on the page)?
9. **Translation.** Does a Markdown source conflict with the GlotPress plan, or can GlotPress read segments from
   the repo as easily as from posts?
10. **Sponsorship.** Which Meta committer owns review and deploy, and can Meta Janitors sponsor it?
