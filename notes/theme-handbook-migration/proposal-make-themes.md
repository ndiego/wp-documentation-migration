# Proposal: Manage the Theme Handbook on GitHub

*Draft for make.wordpress.org/themes, cross-posted to make/docs and make/meta. Tag: #theme-documentation.
Placeholders in [brackets] need a person's commitment before publishing. Longer background:
`notes/theme-handbook-migration/README.md`.*

---

The [Theme Handbook](https://developer.wordpress.org/themes/) is in good shape after the
[2023 overhaul](https://make.wordpress.org/themes/2023/04/04/theme-handbook-overhaul-proposal/) that
Justin Tadlock (@greenshady) led: 139 pages, a structure that reflects how themes are built today, and a small group
of people who keep it accurate.

This proposal does not change any of that. It changes where the source lives.

Today the handbook is edited in the developer.wordpress.org dashboard. Everyone else contributes through the
[Documentation Issue Tracker](https://github.com/WordPress/Documentation-Issue-Tracker/issues?q=label%3Athemes) and
waits for someone with access to make the edit.

Several sibling handbooks work differently. The
[Block Editor Handbook](https://github.com/WordPress/gutenberg/tree/trunk/docs), the
[Advanced Administration Handbook](https://github.com/WordPress/Advanced-administration-handbook), the
[Secure Custom Fields](https://github.com/WordPress/secure-custom-fields) and Playground docs, and the
[Coding Standards](https://github.com/WordPress/wpcs-docs) are Markdown repositories on GitHub that
developer.wordpress.org imports automatically. Anyone can open a pull request; a maintainer merges; the site updates
within minutes.

Justin asked for exactly this for the Theme Handbook in
[January 2024](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816#issuecomment-1887554471)
("I'd love to have a dedicated GitHub repo for managing this") and again in
[August 2024 on Meta #7520](https://meta.trac.wordpress.org/ticket/7520#comment:19).

**The proposal: move the Theme Handbook to that model as a one-to-one conversion.** Every page keeps its URL, title,
chapter, and order. Readers will notice only a new "Improve it on GitHub" link on each page.

The work is already built and tested, much of it with AI assistance, and the plan is to complete the move within one
week of approval.

## What stays the same, verified

We tested this rather than assumed it. On a local copy of developer.wordpress.org, the real importer recognized all
139 existing pages and updated them in place. Nothing was created or moved. No URL, title, parent, or order changed,
and existing redirects still work.

The converted content matched the live site exactly on 130 pages. The other nine differ only in dead embeds the live
site still shows from cache.

No redirects, no broken anchors, no content changes.

## What changes for contributors

- **Edits are pull requests.** Fix a typo with GitHub's pencil icon, or clone for bigger changes. Credit comes through
  the [Props Bot](https://github.com/WordPress/props-bot-action) and the usual Documentation Contributor badge path.
- **No GitHub account? Open an issue** with your proposed text and a maintainer turns it into a pull request with you
  as co-author, as the Advanced Administration Handbook does today.
- **Open `themes` issues move to the new repository** so discussion sits next to the content; the tracker label points
  there.
- **Dashboard editing is switched off** for this handbook after the move. See below for why.

## How the sync works

The mechanism is the one the other GitHub-backed handbooks already use: the
[wporg-markdown importer](https://github.com/WordPress/wordpress.org/tree/trunk/wordpress.org/public_html/wp-content/plugins/wporg-markdown),
driven by a short per-handbook class in the
[developer theme](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-scf.php).

1. The repository holds one Markdown file per page, in folders that mirror the URL tree, plus a `manifest.json`
   listing each page's title, parent, and order.
2. developer.wordpress.org checks the manifest every 15 minutes. It fetches each file with its last-known ETag, so
   unchanged files cost nothing. Changed files are converted to HTML by the same parser the Block Editor Handbook uses
   and saved into the existing post. A merged pull request is live within 15 minutes.
3. Existing pages are matched by URL path, so the importer takes over the current posts. IDs, revisions, authors, and
   "first published" dates survive.
4. The page template switches to the GitHub-aware variant, adding the "Improve it on GitHub" and "See list of changes"
   links. Nothing else on the page changes.
5. Notices are written as [GitHub alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts)
   so they render on GitHub too. The importer turns them into the notice boxes you see today.
6. Images live in the repository as compressed WebP files next to the pages, so a screenshot update is reviewable in
   the same pull request as the text. The importer copies them into the developer.wordpress.org media library on
   import, the way the
   [Playground importer](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-playground.php)
   already does, so the site never serves images from GitHub. Video is not stored in Git; videos stay hosted on
   WordPress.org or YouTube and are embedded by URL.

The code on the WordPress.org side is a class of about 35 lines plus one include, the same shape as the Secure Custom
Fields importer added in [wporg-developer #547](https://github.com/WordPress/wporg-developer/pull/547) (ticket
[Meta #7917](https://meta.trac.wordpress.org/ticket/7917)).

The repository's own checks validate the manifest before anything can merge, because the import problems past
handbooks ran into were manifest errors.

## Why dashboard editing is switched off

The importer updates a page only when its Markdown changes. A dashboard edit made after the move stays live until that
page's Markdown next changes, then silently disappears.

We have a live example of two sources of truth. The
[Plugin Handbook's GitHub copy](https://github.com/WordPress/developer-plugins-handbook) was created in 2023, and
[Meta #7361](https://meta.trac.wordpress.org/ticket/7361) to connect it stalled. Since then, 34 pull requests have
been merged there that never reached the site, while the site itself kept being edited.

So dashboard editing for `theme-handbook` is removed once the import is live. Administrators keep access for
emergencies.

## Speed, and how AI is used

We want this done fast, and we are open about how.

The research into the importer, the conversion of all 139 pages, the manifest, the validation checks, and the full
dry run against a local copy of developer.wordpress.org were done with AI assistance (Claude Code), directed and
reviewed by people. That is why this proposal arrives with the tooling finished and the result measured, rather than
with a request for volunteers to start converting pages.

It is also in the spirit of the [Meta Janitors](https://make.wordpress.org/meta/handbook/about/projects/meta-janitors/)
mandate to "lean into AI tooling" and to tighten the link between WordPress.org and version-controlled workflows.

What AI does not do: decide. The handbook's maintainers approve the conversion by reviewing the page-by-page
comparison. The Themes and Docs teams approve this proposal. A Meta committer deploys the importer and runs the first
import. Those are the only steps that take calendar time, and they are why the timeline below is one week rather than
one day.

## The first step of something larger

This is the first move in a broader effort to make documentation on WordPress.org work the same way everywhere: one
contribution model (pull requests, with an issue-based path for everyone else), one set of Markdown conventions that
render well on GitHub and on the site, shared tooling for conversion, manifest validation, and reproducible
screenshots, and the same import pipeline for every handbook.

WordPress.org already
[serves every page as Markdown](https://make.wordpress.org/meta/2026/03/03/markdown-now-available-on-wordpress-org/),
and the Meta Janitors mandate explicitly calls for tighter integration between WordPress.org and version-controlled
workflows.

The Theme Handbook is the right first step because its structure is settled, Justin wants the move, and a one-to-one
conversion proves the pipeline without a content debate. What we learn here is meant to carry to the Plugin Handbook
next, and to the wider documentation set after that, each as its own proposal.

## Plan and timeline

**Before approval.** Discussion here, and at the Themes Team meeting on [date] and the Docs Team meeting on [date].
Comments close [date, two weeks out].

In parallel, so no time is lost afterwards: a Meta Trac ticket for the importer, and the `developer-themes-handbook`
repository prepared in the WordPress GitHub organization to the
[repository criteria](https://make.wordpress.org/project/2025/06/04/criteria-for-creating-or-migrating-repositories-under-the-wordpress-github-organization/),
with Justin and [other maintainers] as code owners, validation checks in place, and no content accepted until the
import is live.

**The week after approval.**

| Day | What happens | Who |
|---|---|---|
| 1 | Freeze dashboard edits. Fresh export, conversion, manifest; the page-by-page comparison report goes to the maintainers. | [proposer], with AI tooling |
| 2–3 | Maintainers review the comparison and sign off. Importer pull request opened on wporg-developer. | Justin, [other maintainers]; [Meta committer] reviews |
| 4 | Importer deployed; content merged; first import run and verified: every URL answers, nothing created or moved. | [Meta committer] |
| 5 | Dashboard editing switched off; open `themes` issues moved; Feedback and role pages updated; announcement. | [Meta committer], Justin |

If the Meta committer's availability slips, the week slips with it. Nothing else on the list waits on a person.

## Translation

The only active translation is Japanese, maintained from a
[Markdown repository](https://github.com/jawordpressorg/theme-handbook) that already mirrors the English page tree and
published at [ja.wordpress.org](https://ja.wordpress.org/team/handbook/theme-development/).

That team [asked for an English GitHub source in August 2024](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816#issuecomment-2320498484)
and paused in late 2024 because the structure kept changing. A one-to-one move gives them per-file diffs of English
changes. Nothing here touches HelpHub or the localized sites.

## Questions and (some) answers

**Does any content change?** No. Known small defects (an empty page, a few malformed code blocks) get a separate
pull request after the move, where the diff is visible.

**What happens to the existing images?** All 152 are brought into the repository at cutover as WebP, including the
few currently hosted on make.wordpress.org and on a personal site, with their alt text unchanged. They get new
media-library URLs when imported; the pages look the same.

**What about "Last updated"?** The first import touches every page, so each shows the cutover date once. After that,
dates and Git history reflect real changes.

**Who reviews, and how fast?** Justin and [other maintainers] as code owners, with a target first response within
seven days. Maintainers may merge their own small fixes, as the Secure Custom Fields docs allow.

**Removing or renaming a page?** The importer never deletes. It is a deliberate change: a pull request plus a
redirect, done with a Meta committer. Checks reject accidental ones.

**Is this "all handbooks to GitHub"?** No. This handbook, at its maintainer's request, following its developer-docs
siblings. Later steps get their own proposals.

**Why so fast?** Because the slow parts are already done. The conversion is tested, the import is proven on a local
copy, and the checks that catch the mistakes past handbook imports made are written. What remains is review, a small
deploy, and flipping the switch. Spending weeks on that would not make it safer, and a short window keeps the
dashboard freeze short.

## How to participate

- Comment on this post by [date].
- Themes Team meeting, [date] at 15:00 UTC in #themereview; Docs Team meeting, [date] at 14:00 UTC in #docs.
- If you maintain or translate the handbook, say so below. We want you in the maintainers group.

Props to [reviewers] for feedback on the draft.
