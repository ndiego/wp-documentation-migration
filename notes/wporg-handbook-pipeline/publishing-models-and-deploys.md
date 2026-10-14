# The three ways content reaches wordpress.org, and how a deploy actually happens

Date: 2026-10-14. Sources: `WordPress/wporg-main-2022` (AGENTS.md, `.github/workflows/content-update.yml`,
`env/export-content/index.php`, `env/page-manifest.json`, PR #759), the Meta handbook page "Deploying
WordPress.org" (rewritten 2026-08-25), and `research/05-process-governance-deployment.md` §3. Worked example:
https://github.com/WordPress/wporg-main-2022/pull/759.

## 1. Three publishing models coexist

| Model | Source of truth | How content goes live | Human step to go live | Examples |
|---|---|---|---|---|
| **A. Edit in WordPress** | the site's database | Press Publish | none beyond publishing | HelpHub, Theme/Plugin/APIs handbooks, Learn, most make/* handbooks, Developer Blog |
| **B. GitHub pulled into WordPress** | Markdown + manifest in a GitHub repo | `wporg-markdown` importer on WP-Cron every 15 min writes posts | none; merge is the last human step (4 to 15 min measured latency) | Block Editor, Playground, REST API, SCF, Advanced Admin, Coding Standards, WP-CLI, make/hosting, make/test |
| **C. WordPress exported to GitHub, deployed as code** | the live database is the *authoring* source, but the committed PHP pattern file is what renders | hourly GitHub Action exports page content to pattern files and opens a PR; merge, then a Meta committer syncs to SVN and deploys | **two**: merge the bot PR, then sync + deploy | wordpress.org main site pages (`wporg-main-2022`): About, Download, Data Liberation, release pages, etc. |

Model C is the one dd32 held up on Meta #7520 as "a hybrid approach, where the page can be edited visually, but
edits aren't made live without a review first". It is the reverse direction of model B.

## 2. Model C in detail (wporg-main-2022)

- Each page's block template contains only a pattern reference, for example
  `templates/page-data-liberation.html` holds `<!-- wp:pattern {"slug":"wporg-main-2022/data-liberation"} /-->`.
  Visitors see the pattern PHP file. The stored `post_content` in the database is never rendered on the front end.
- `env/page-manifest.json` maps page ID and slug to a template file and a pattern file. IDs are used because slugs
  are not unique across parent pages.
- `env/export-content/index.php` fetches each page from
  `https://wordpress.org/wp-json/wp/v2/pages?context=wporg_export&include=<id>` and regenerates the pattern and
  template. Strings are wrapped in `esc_html_e()` / `_e()` with text domain `wporg`, which makes them GlotPress
  translation sources for Rosetta sites. Content without an H1 gets the page title folded in (`inc/page-title.php`).
- `.github/workflows/content-update.yml` runs this hourly (`17 * * * *`) and on `workflow_dispatch`. The `sync` job is
  read-only; the `publish` job commits the artifact to branch `automated/content-update`, opens or updates one PR
  titled "Content updates from Page Editor", labelled `Automated Content Update`, and posts before/after screenshots
  from a `content-update-screenshots` storage branch keyed by a content hash. Body says "Please review, merge, and deploy."
- Adding a page: publish it in wp-admin; the workflow's `npm run add:page -- --new` adds it to the manifest and the
  next export generates its pattern and template.
- `build.yml` on every push to trunk compiles the theme and force-pushes it to the `build` branch with the short SHA
  appended to the `style.css` version.

### Gotchas recorded in the repo's own AGENTS.md

- "Merging to trunk deploys nothing." A Meta committer must run `bin/sync/main.sh` on their sandbox.
- "The data flow is one-way: page content in the wordpress.org DB → pattern file." Editing a pattern file without
  making the same change in wp-admin is silently reverted by the next hourly sync.
- "Never commit to the `automated/content-update` branch." It is rebuilt from trunk every hour.
- Any string change, including attribute reordering by the exporter, creates a new msgid and drops existing
  translations until locale teams re-translate. PR #759's diff is mostly attribute reordering plus one real URL change.
- A failed editor save can write rendered HTML back into `post_content`; the pattern file is the recovery source.

### Who does it

obenland merged the last six content-update PRs (#741 to #758, 2026-09-01 to 2026-10-13), so in practice one Meta
committer both merges and deploys.

## 3. The generic deploy, for any GitHub-developed component

From the Meta handbook "Deploying WordPress.org" page (2026-08-25):

- Requires RW access to `meta.svn` and/or `dotorg.svn` (a Meta committer, granted per area with no application form),
  an SSH sandbox, an SVN password and 2FA. Working copies live under `/home/wporg/public_html`.
- GitHub-developed repos are never hand-committed to SVN. Each has a sync script on the sandbox:
  `bin/sync/wporg-developer.sh`, `bin/sync/wporg-make.sh`, `bin/sync/learn.sh`, `bin/sync/pattern-directory.sh`,
  `bin/sync/wporg-two-factor.sh`, `bin/sync/wporg-mu-plugins.sh`, `bin/sync/github-wordpress.org.sh <pr>`, and per
  wporg-main-2022's docs `bin/sync/main.sh`; per wporg-documentation-2022 PR #113, `bin/sync/wporg-documentation.sh`.
  Most read the repo's `build` branch, so wait for the build Action first.
- Sequence: merge PR → confirm `build` branch → on the sandbox `bin/sync/<repo>.sh` → `svnup-all.sh` →
  `deploy-dotorg.sh wporg` (or `deploy all` for shared code).
- "A deploy takes roughly four to eight minutes, and is not atomic." "A deploy ships all code in the tree, not just
  your changes … You must be ready to respond to breakage you did not cause."
- The `WordPress/wordpress.org` GitHub repo (which holds `wporg-markdown` and the `handbook` plugin) is a read-only
  mirror of Meta SVN; a committer commits the patch to SVN and the PR auto-resolves.
- Activating a plugin on a site is a manual step: add an `svn:externals` entry, deploy, then
  `wp --url=<site> plugin activate <slug>`.
- Rollback options: pin WordPress trunk to a known revision, roll back Gutenberg via `svn:externals`, or
  `svn merge -c -<rev>` and redeploy.
- `support-helphub` (HelpHub's plugin) has two upstreams, Meta SVN and `wporg-documentation-2022`, and the sync
  overwrites SVN wholesale, so SVN-only commits can be reverted by a sync (PR #113, July 2026). The last HelpHub sync
  was r14527 (2025-09-10).

## 4. What this means for the HelpHub plan

- Any importer code we propose is a **code** change and goes through model C's second half regardless of which
  content model we choose: PR, build branch, sandbox sync, SVN commit, deploy, plugin activation. Budget a Meta
  committer's time and a Meta Trac ticket for it.
- Model B gives us zero-touch content publishing after merge; model C gives review-before-live but needs a committer
  deploy for every content change, which does not scale to 320 articles edited by many people. Model C is worth
  citing as the existing precedent for "edit in WordPress, version in GitHub", not as the mechanism for HelpHub.
- Model C's exporter (`env/export-content/`, a block-to-pattern parser with PHPUnit tests) is reusable prior art if we
  ever need WordPress-to-Markdown export in the other direction, for example to seed a repo from live HelpHub or to
  reconcile edits made in wp-admin after the switch.
