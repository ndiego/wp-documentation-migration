# Proposal: Manage the Theme Handbook on GitHub

*Draft for make.wordpress.org/themes, cross-posted to make/docs and make/meta. Tag: #theme-documentation.
Placeholders in [brackets] need a person's commitment before publishing. Longer background:
`notes/theme-handbook-migration/README.md`.*

---

The [Theme Handbook](https://developer.wordpress.org/themes/) is in good shape after the
[2023 overhaul](https://make.wordpress.org/themes/2023/04/04/theme-handbook-overhaul-proposal/) led by
Justin Tadlock (@greenshady): 139 pages, a structure that reflects how themes are built today, and a small group of
people who keep it accurate. This proposal changes none of that. It changes where the source lives.

Today the handbook is edited in the developer.wordpress.org dashboard, and everyone else contributes through the
[Documentation Issue Tracker](https://github.com/WordPress/Documentation-Issue-Tracker/issues?q=label%3Athemes) and
waits for someone with access. The [Block Editor Handbook](https://github.com/WordPress/gutenberg/tree/trunk/docs),
the [Advanced Administration Handbook](https://github.com/WordPress/Advanced-administration-handbook), the
[Secure Custom Fields](https://github.com/WordPress/secure-custom-fields) and Playground docs, and the
[Coding Standards](https://github.com/WordPress/wpcs-docs) work differently: their source is a Markdown repository
on GitHub that developer.wordpress.org imports automatically. Anyone can open a pull request, a maintainer merges, and
the site updates within minutes. Justin asked for this for the Theme Handbook in
[January 2024](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816#issuecomment-1887554471) and
again on [Meta #7520](https://meta.trac.wordpress.org/ticket/7520#comment:19).

**The proposal: move the Theme Handbook to that model as a one-to-one conversion.** Every page keeps its URL, title,
chapter, and order; readers see only a new "Improve it on GitHub" link. The tooling is built and tested, much of it
with AI assistance, and the move completes within one week of approval.

## What stays the same, verified

On a local copy of developer.wordpress.org, the real importer recognized all 139 existing pages and updated them in
place: nothing created or moved, no URL, title, parent, or order changed, existing redirects intact. The converted
content matched the live site exactly on 130 pages; the other nine differ only in dead embeds the live site still
shows from cache. No redirects, no broken anchors, no content changes.

## What changes for contributors

- **Edits are pull requests.** Fix a typo with GitHub's pencil icon or clone for bigger changes. Credit comes through
  the [Props Bot](https://github.com/WordPress/props-bot-action) and the usual Documentation Contributor badge path.
- **No GitHub account? Open an issue** with your proposed text; a maintainer turns it into a pull request with you as
  co-author, as the Advanced Administration Handbook does today.
- **Open `themes` issues move to the new repository**, and the tracker label points there.
- **Dashboard editing is switched off** for this handbook after the move (see below).

## How the sync works

The mechanism is the
[wporg-markdown importer](https://github.com/WordPress/wordpress.org/tree/trunk/wordpress.org/public_html/wp-content/plugins/wporg-markdown)
the other GitHub-backed handbooks use, driven by a short per-handbook class in the
[developer theme](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-scf.php).

1. The repository holds one Markdown file per page, in folders that mirror the URL tree, plus a `manifest.json`
   listing each page's title, parent, and order.
2. developer.wordpress.org checks the manifest every 15 minutes and fetches each file with its last-known ETag, so
   unchanged files cost nothing. Changed files are converted to HTML by the same parser the Block Editor Handbook uses
   and saved into the existing post. A merged pull request is live within 15 minutes.
3. Existing pages are matched by URL path, so the importer takes over the current posts. IDs, revisions, authors, and
   "first published" dates survive.
4. The page template switches to the GitHub-aware variant, adding the "Improve it on GitHub" and "See list of changes"
   links.
5. Notices are written as [GitHub alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts),
   which render on GitHub and are turned into today's notice boxes on import.
6. Images live in the repository as compressed WebP next to the pages, so a screenshot update is reviewed in the same
   pull request as the text. The importer copies them into the media library on import, as the
   [Playground importer](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-playground.php)
   does, so the site never serves images from GitHub. Video stays hosted on WordPress.org or YouTube and is embedded
   by URL.

The WordPress.org side is a class of about 35 lines plus one include, the same shape as the Secure Custom Fields
importer in [wporg-developer #547](https://github.com/WordPress/wporg-developer/pull/547) (ticket
[Meta #7917](https://meta.trac.wordpress.org/ticket/7917)). The repository's checks validate the manifest before
merge, because the import problems past handbooks hit were manifest errors.

## Why dashboard editing is switched off

The importer updates a page only when its Markdown changes, so a dashboard edit made after the move stays live until
that page's Markdown next changes, then silently disappears. The
[Plugin Handbook's GitHub copy](https://github.com/WordPress/developer-plugins-handbook) shows the result of two
sources of truth: created in 2023, [Meta #7361](https://meta.trac.wordpress.org/ticket/7361) to connect it stalled,
and 34 pull requests have since been merged there that never reached the site while the site kept being edited.
Dashboard editing for `theme-handbook` is therefore removed once the import is live; administrators keep access for
emergencies.

## Speed, and how AI is used

The research into the importer, the conversion of all 139 pages, the manifest, the validation checks, and the full
dry run against a local copy of developer.wordpress.org were done with AI assistance (Claude Code), directed and
reviewed by people. The proposal therefore arrives with the tooling finished and the result measured, in the spirit
of the [Meta Janitors](https://make.wordpress.org/meta/handbook/about/projects/meta-janitors/) mandate to lean into
AI tooling and tighten the link between WordPress.org and version-controlled workflows.

AI does not decide. The maintainers approve the conversion by reviewing the page-by-page comparison, the Themes and
Docs teams approve this proposal, and a Meta committer deploys the importer and runs the first import. Those are the
only steps that take calendar time.

## The first step of something larger

This is the first move toward documentation on WordPress.org working the same way everywhere: one contribution model,
one set of Markdown conventions that render on GitHub and on the site, shared tooling for conversion, manifest
validation, and reproducible screenshots, and the same import pipeline for every handbook. WordPress.org already
[serves every page as Markdown](https://make.wordpress.org/meta/2026/03/03/markdown-now-available-on-wordpress-org/).
The Theme Handbook is the right first step because its structure is settled, its maintainer wants the move, and a
one-to-one conversion proves the pipeline without a content debate. The Plugin Handbook is the intended next step,
as its own proposal.

## Plan and timeline

**Before approval.** Discussion here and at the Themes Team meeting on [date] and the Docs Team meeting on [date];
comments close [date, two weeks out]. In parallel: a Meta Trac ticket for the importer, and the
`developer-themes-handbook` repository prepared in the WordPress GitHub organization to the
[repository criteria](https://make.wordpress.org/project/2025/06/04/criteria-for-creating-or-migrating-repositories-under-the-wordpress-github-organization/),
with Justin and [other maintainers] as code owners, checks in place, and no content accepted until the import is live.

**The week after approval.**

| Day | What happens | Who |
|---|---|---|
| 1 | Freeze dashboard edits; fresh export, conversion, manifest; comparison report to the maintainers | [proposer], with AI tooling |
| 2–3 | Maintainers review and sign off; importer pull request opened on wporg-developer | Justin, [other maintainers]; [Meta committer] reviews |
| 4 | Importer deployed; content merged; first import run and verified | [Meta committer] |
| 5 | Dashboard editing switched off; issues moved; Feedback and role pages updated; announcement | [Meta committer], Justin |

Only the Meta committer's availability can move this week.

## Translation

The only active translation is Japanese, maintained from a
[Markdown repository](https://github.com/jawordpressorg/theme-handbook) that already mirrors the English page tree and
published at [ja.wordpress.org](https://ja.wordpress.org/team/handbook/theme-development/). That team
[asked for an English GitHub source in 2024](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816#issuecomment-2320498484)
and paused later that year because the structure kept changing; a one-to-one move gives them per-file diffs. Nothing
here touches HelpHub or the localized sites.

## Questions and answers

**Does any content change?** No. Known small defects (an empty page, a few malformed code blocks) get a separate
pull request after the move.

**What happens to the existing images?** All 152 are brought into the repository as WebP, including the few hosted
on make.wordpress.org and on a personal site, with alt text unchanged. They get new media-library URLs on import; the
pages look the same.

**What about "Last updated"?** Every page shows the cutover date once; after that, dates and Git history reflect real
changes.

**Who reviews, and how fast?** Justin and [other maintainers] as code owners, with a target first response within
seven days. Maintainers may merge their own small fixes, as the Secure Custom Fields docs allow.

**Removing or renaming a page?** The importer never deletes. It is a deliberate change: a pull request plus a
redirect, done with a Meta committer.

**Is this "all handbooks to GitHub"?** No. This handbook, at its maintainer's request. Later steps get their own
proposals.

**Why so fast?** The slow parts are done: the conversion is tested, the import is proven, and the checks are written.
What remains is review, a small deploy, and flipping the switch. A short window also keeps the dashboard freeze short.

## How to participate

- Comment on this post by [date].
- Themes Team meeting, [date] at 15:00 UTC in #themereview; Docs Team meeting, [date] at 14:00 UTC in #docs.
- If you maintain or translate the handbook, say so below; we want you in the maintainers group.

Props to [reviewers] for feedback on the draft.
