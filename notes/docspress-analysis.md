# DocsPress and wordpress.org/documentation: structural and technical analysis

Date: 2026-10-08. Sources: https://docs.press/docs/ (all guide and reference pages),
Automattic/docspress at commit 8584e70 (2026-08-03), the code dossier in
`notes/reference/docspress-architecture.md`, and the HelpHub/wporg findings in
`notes/site-structure.md` and `toolkit/CONVENTIONS.md`. Theme/visual differences are out of scope.

## 1. What DocsPress actually is

DocsPress is three loosely coupled pieces:

| Piece | Form | Required? | Role |
|---|---|---|---|
| DocsPress Action / CLI | Node 20 GitHub Action, npm package `docspress` | Yes | Converts Markdown to block markup on the CI runner and writes to WordPress via the core REST API |
| DocsPress Blocks | WordPress plugin | Optional (required for `docspress/*` blocks and versioning) | 15 content blocks, `docspress_versions` taxonomy, "Was this helpful" endpoint |
| DocsPress Theme | Block theme | Optional | Docs templates, sidebar nav, TOC, search, breadcrumbs, `.md` twin routes, `llms.txt` |

The Action is the heart. Everything on the WordPress side is passive: there is no webhook receiver, no in-WordPress cron, no GitHub App. WordPress never reaches out to GitHub.

## 2. How it maps onto what wordpress.org has today

| Concern | HelpHub today | wporg-markdown importer (Block Editor handbook) | DocsPress |
|---|---|---|---|
| Post type | `helphub_article` + `helphub_version` | any hierarchical CPT, configured per handbook | core `page` only, hard-coded (`src/wordpress.js` `pagesEndpoint()`) |
| Hierarchy | taxonomy (`category`, 2 levels) | `post_parent` from manifest | `post_parent` from folder tree or manifest |
| URLs | flat `/article/<slug>/` | path-based `/block-editor/a/b/c/` | path-based under one `root-slug` |
| Ordering | `menu_order` desc, then title | `menu_order` from manifest `order` | `menu_order` from `sidebar_position` frontmatter |
| Source of truth | WordPress editor | Markdown in GitHub | Markdown in GitHub (with optional reverse PRs) |
| Sync direction | n/a | **pull**: WordPress fetches `manifest.json` + raw files on cron | **push**: GitHub Action POSTs to `/wp-json/wp/v2/pages` |
| Credential | n/a | none inbound (public GitHub reads) | write token in GitHub Actions secret |
| Auth mechanism | wporg SSO + 2FA | n/a | WordPress.com OAuth (`global` scope) or Bearer token; core Application Passwords (Basic auth) not supported |
| Output HTML | block markup | classic HTML via Jetpack GFM parser | block markup (core blocks + `core/html`), serialised by the Action |
| Images | wp.org media library | absolute URLs (developer.wordpress.org/files) | URLs passed through unchanged, nothing uploaded |
| Callouts | coloured paragraphs / `wporg/notice` | raw HTML `<div class="callout">` | `docspress/callout` block via a JSON comment envelope; plain `> [!NOTE]` becomes a `core/quote` |
| Redirects | 71 hard-coded 301s in mu-plugin | handbook subclass redirect table (301) | "This page moved" placeholder Pages, not HTTP 301s |
| TOC | theme, from headings at render time | handbook plugin | theme block |
| Feedback | login-gated private comment | none | anonymous REST POST, counts in post meta, no nonce/rate limit |
| i18n | Rosetta sites per locale | none in importer; Playground docs import per-locale trees | none; no locale model |
| Manifest | n/a | `manifest.json` keyed by path: slug, parent, title, order, markdown_source | own `manifest.json`: `pages[]` with id, slug, parent, title, markdown_source. **Incompatible**: feeding the wporg format parses to zero pages and would mark every managed page for deletion |

## 3. The auth and trust model (your main concern)

**Direction is the whole story.** The wporg importer is pull-based. wordpress.org's cron fetches a public
manifest and public raw files from GitHub. GitHub holds no credential for wordpress.org; a compromised
GitHub account can at worst merge bad content, which is reviewable and revertible in git. DocsPress is
push-based. A token with write access to the live site sits in a GitHub Actions secret and is exercised
on every push to `main` and, in reconcile mode, every five minutes by a scheduled job.

What that means on wordpress.org specifically:

- **WordPress.com OAuth does not apply.** wordpress.org is not a WordPress.com site. The OAuth path with
  `global` scope is irrelevant here, which removes the thing you were worried about, but it leaves only
  the self-hosted path.
- **The self-hosted path needs an auth plugin.** The Action only sends `Authorization: Bearer <token>`.
  Core WordPress has no Bearer handler. Application Passwords use Basic auth and won't work. wordpress.org
  would have to add a Bearer-token authentication layer (JWT plugin or a custom mu-plugin) to the
  documentation site. That is new attack surface on a site that currently has no API write path at all.
- **The token acts as a wordpress.org user.** Whatever user owns the token has to be able to create,
  edit, publish and delete pages. That user bypasses wporg SSO and 2FA for every automated write. Rotation,
  scoping and audit are all on the systems team.
- **Reconcile mode doubles the exposure.** The scheduled job also needs `contents: write` and
  `pull-requests: write` on the GitHub repo, and the repo setting "Allow GitHub Actions to create and
  approve pull requests". So one workflow holds write credentials to both systems.
- **Contributors are fine either way.** In both models contributors only ever open PRs; they never see
  the credential. The difference is what a merge triggers: a public fetch (wporg) versus an authenticated
  write with a long-lived secret (DocsPress).
- **Deletion is automated.** A Markdown file removed from `docs/` trashes (or with `delete-mode: force`,
  permanently deletes) the live page on the next run. A bad merge or a misconfigured `root-slug` can
  trash a tree. The importer never deletes.

Verdict on this axis: DocsPress's auth model is a poor fit for wordpress.org's security posture. It could be
made to work, but only by adding an inbound write path the site deliberately doesn't have today, while the
existing importer achieves the same GitHub-as-source-of-truth outcome with no inbound credential.

## 4. Structural fit

**The `page` assumption is the hard blocker.** DocsPress reads and writes `wp/v2/pages` only, in both the
Action and the PHP. HelpHub is `helphub_article` with categories. Adopting DocsPress means one of:

1. Migrate HelpHub content to core pages under `/documentation/docs/` (or similar), add ~320 redirects,
   rewrite the theme's category-driven landing pages and local nav, and give up the taxonomy the Rosetta
   sites and the theme rely on. Large, visible change.
2. Fork DocsPress to target a configurable post type and taxonomy. Then you own a fork of a pre-1.0
   project with one maintainer.

**The sentinel is a liability on wordpress.org.** Sync identity lives inside `post_content` as an HTML
comment containing JSON, including the whole Markdown source base64-encoded. It is saved into every
revision, is visible in the REST API `content.rendered` unless the DocsPress theme strips it, and would
need wporg's own theme to strip it too. Post meta would have been the normal place; this choice is why
the theme and Action are more coupled than they look.

**Block output is a plus, with a catch.** DocsPress produces real block markup, which is closer to what
HelpHub stores today than the importer's classic HTML. But callouts, code tabs and the other 15 blocks are
`docspress/*` blocks. Either the Blocks plugin ships on wordpress.org permanently, or those get mapped to
`wporg/notice` and friends, which means modifying the converter anyway.

**Images aren't handled.** URLs pass through. For HelpHub that is workable only because 2,165 of 2,309
images already live at `wordpress.org/documentation/files/`. It gives no path for the in-repo screenshots
this project just extracted; they'd need separate sideloading, exactly as with the importer.

**Redirects are placeholder pages, not 301s.** wordpress.org has a 301 table in an mu-plugin and SEO
expectations to match. DocsPress's approach would regress that.

**No i18n model.** HelpHub is translated on Rosetta sites per locale. DocsPress has nothing here; each
locale would be a separate root with a separate token. The importer has the same gap, but the Playground
docs import shows the pattern for per-locale trees already exists in wporg code.

**Front-end weight.** The theme's search embeds up to 12 KB of text per article as JSON in every page.
At ~40 pages docs.press's `/docs/` is ~253 KB; at 321 articles that approach doesn't scale and would be
replaced by wporg's Jetpack search regardless.

## 5. Project health

- Repo created 2026-07-09. ~142 commits, ~138 by one author. Last commit to `main` 2026-08-03.
  Nothing merged in two months; outside PRs open since late July.
- Pre-1.0 (`wordpress-0.10.7`). ~150 JS tests, no PHP tests.
- Open PR #44 (2026-09-16) renames the whole project to "Autodocs Publish", including the block namespace.
  That would break every stored `docspress/*` block and the sentinel format for existing adopters.
- Only known deployment is docs.press itself, on WordPress.com.
- License mismatch: README badge says GPL-3.0-or-later, LICENSE file says GPL-2.0-or-later. Fine for
  wordpress.org either way, but a sign of early-stage polish.

For a wordpress.org system that the Docs team and systems team would carry for years, this is too early
and too single-threaded to adopt as a dependency.

## 6. What is worth taking from it

DocsPress gets several things right that the wporg importer lacks, and they are portable as ideas or code:

1. **Three-way reconcile with a hash baseline.** Record the hash of what was last imported; on the next
   run, if WordPress differs from the baseline and Markdown differs too, stop and report instead of
   overwriting. The importer today overwrites silently. This is ~100 lines in a HelpHub importer subclass
   and would protect against editor edits being lost.
2. **Reverse sync as a rolling PR.** WordPress-side edits become one action-owned branch and PR,
   rewriting only the changed source regions. For HelpHub, where contributors are used to editing in
   wp-admin, this is the feature that would make GitHub-as-source-of-truth socially viable. It can be
   built as a GitHub Action that reads the public REST API (no credential needed; HelpHub content is
   public) and opens PRs with the repo's own `GITHUB_TOKEN`. That inverts DocsPress's model: read-only
   towards WordPress, write only to GitHub.
3. **Markdown-to-blocks conversion.** `src/block-markdown.js` (remark + GFM + frontmatter to block
   markup) is MIT-compatible GPL code that could seed a blocks-producing path in the importer, replacing
   Jetpack's classic HTML output. The `WordPress/php-toolkit` Markdown component is the PHP-native
   alternative and probably the better fit for wporg.
4. **`.md` twin routes and `llms.txt`.** Serving each article's source Markdown at `<url>.md` and an
   index at `/llms.txt` is a small theme/plugin addition that wporg could adopt independently.
5. **Draft-first, dry-run-first rollout.** Their staged rollout (dry run, draft write, then push trigger,
   then reconcile) is a good operational template for the HelpHub import regardless of tooling.

## 7. Recommendation

Do not adopt DocsPress as the HelpHub publishing system. The decisive reasons are structural, not
cosmetic: it is hard-wired to core pages with `post_parent` hierarchy, it requires an inbound write token
and a Bearer auth layer that wordpress.org does not have and should not want, its redirects and i18n
story regress what exists, and the project is a two-month-dormant pre-1.0 with one maintainer and a
pending rename.

Keep the plan already in motion: Markdown in GitHub, pulled by a HelpHub subclass of the
`wporg-markdown` importer that maps folders to categories, keeps flat URLs, converts GFM alerts to
`wporg/notice`, and sideloads images. Then borrow from DocsPress the three things it does better:
a hash-baseline conflict check in the importer, a read-only reverse-sync Action that turns wp-admin edits
into PRs, and `.md` twin routes for AI and tooling. That gets the DocsPress workflow benefits with zero
inbound credentials and no new dependency.

If a block-producing importer is wanted (so HelpHub keeps storing block markup rather than classic HTML),
evaluate `WordPress/php-toolkit`'s Markdown component first and DocsPress's `block-markdown.js` second.
