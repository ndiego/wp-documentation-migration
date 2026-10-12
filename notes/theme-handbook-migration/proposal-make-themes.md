# Proposal: Manage the Theme Handbook on GitHub

*Draft for make.wordpress.org/themes, cross-posted to make/docs and make/meta. Tag: #theme-documentation.
Placeholders in [brackets] need a person's commitment before publishing. Source material:
`notes/theme-handbook-migration/README.md` and its research reports.*

---

The [Theme Handbook](https://developer.wordpress.org/themes/) got a full overhaul in 2023 and 2024. It is in good
shape: 139 pages, a structure that reflects how themes are built today, and a small group of people who keep it
accurate. This proposal is not about changing any of that. It is about where the words live.

Today the handbook is edited in the developer.wordpress.org dashboard. A handful of people have access, and everyone
else contributes by opening an issue in the Documentation Issue Tracker and waiting for one of them to make the edit.
Several of our sibling handbooks, the [Block Editor Handbook](https://developer.wordpress.org/block-editor/), the
[Advanced Administration Handbook](https://developer.wordpress.org/advanced-administration/), the Playground and
Secure Custom Fields docs, and the Coding Standards, work differently: their source is a Markdown repository on
GitHub, and developer.wordpress.org imports it automatically. Anyone can open a pull request; a maintainer reviews
and merges; the site updates itself within minutes.

**I propose we move the Theme Handbook to that model, as a one-to-one conversion.** Nothing about the handbook's
organization changes. Every page keeps its URL, title, place in the chapter list, and order. Readers will not notice
a difference, apart from a new "Improve it on GitHub" link at the bottom of each page. What changes is how
contributors get an edit in.

## What stays exactly the same

This was the first requirement, and we have verified it rather than assumed it. On a local copy of
developer.wordpress.org we ran the real importer against the converted handbook. Result: it recognized all 139
existing pages and updated them in place. Nothing was created, nothing moved, no URL, title, parent, or order
changed, and old URLs that redirect today still redirect. The converted content matched the live site exactly on
130 pages; the other nine differ only in things like dead embeds the live site still shows from cache.

That means no redirects to maintain, no broken deep links (the 162 explicit heading anchors are preserved), and no
"the handbook feels different" moment for readers.

## What changes for contributors

- **Edits become pull requests.** Fix a typo with the pencil icon on GitHub, or clone the repo for bigger changes.
  Maintainers review and merge. You get credit through the Props Bot and the usual Documentation Contributor badge
  path.
- **No GitHub account? Still fine.** Open an issue, or comment with your proposed text, and a maintainer will turn it
  into a pull request with you as co-author. This is how the Advanced Administration Handbook works today, and it
  keeps the lowest-barrier path open.
- **The Documentation Issue Tracker stays the front door** for reporting problems. Open `themes` issues will move to
  the new repository so the discussion lives next to the content.
- **Dashboard editing is switched off** for the Theme Handbook after the move. More on why below.

## How the sync works

For the technically curious, here is the mechanism, which is the same one the other GitHub-backed handbooks use.

1. **The repository holds one Markdown file per page**, in folders that mirror the URL tree
   (`core-concepts/templates.md` is `/themes/core-concepts/templates/`), plus a `manifest.json` that lists every page
   with its title, parent, and order.
2. **developer.wordpress.org checks the manifest every 15 minutes** (a WordPress cron event). For each page it
   fetches the Markdown from GitHub, sending the file's last-known ETag so unchanged files cost nothing. Changed files
   are converted to HTML by the same Markdown parser the Block Editor Handbook uses and saved into the existing
   handbook post. A merged pull request is live within 15 minutes.
3. **Existing pages are matched by their URL path**, so the importer takes over the current posts rather than creating
   new ones. Post IDs, revisions, authors, and "first published" dates survive.
4. **The page template switches automatically** to the GitHub-aware variant, which adds the "Improve it on GitHub" and
   "See list of changes" links. Everything else on the page is unchanged.
5. **Notices, code, images, and headings** come through unchanged. Notices are written as GitHub alerts in the
   Markdown, so they look right on GitHub too, and the importer renders them as the notice boxes you see today. Images
   keep their current URLs in the developer.wordpress.org media library.

The wiring on the wordpress.org side is small: a short importer class in the developer theme, modeled on the one
Secure Custom Fields added in February 2025, and one line to include it. The repository's own checks validate the
manifest before anything can merge, because the two handbook imports that stumbled in the past both stumbled on a
malformed manifest.

## Why dashboard editing has to be switched off

The importer only updates a page when its Markdown changes. If someone edits a page in the dashboard after the move,
that edit stays live until the next time the Markdown for that page changes, and then it silently disappears. The
Plugin Handbook has a GitHub copy that was created in late 2023 but never connected; people have merged 34 pull
requests there that never reached the site, while the site itself kept being edited. Two sources of truth is the one
failure mode we know about, so the proposal removes the ability to edit `theme-handbook` pages in the dashboard
once the import is live. Administrators keep access for emergencies.

## The plan

1. **Discussion** here, and at the Themes Team meeting on [date] and the Docs Team meeting on [date]. Feedback window
   closes [date, about two weeks out].
2. **Meta ticket and repository.** A Meta Trac ticket for the importer, and a new repository in the WordPress GitHub
   organization, `developer-themes-handbook`, with [maintainer names] as code owners and a group of Themes and Docs
   contributors with merge rights. The repository accepts no content pull requests until the import is live.
3. **Conversion and review.** We convert the handbook from a fresh export and review the result page by page against
   the live site. The conversion tooling is already written and tested.
4. **Cutover, in one day.** A short freeze on dashboard edits, a final export and conversion, deploy of the importer
   by [Meta committer], the first import, verification that every URL still answers, then the editing switch-off and
   the move of open issues.
5. **Announcement**, and the first content pull requests.

Realistically this is four to eight weeks from agreement, most of it discussion and review rather than engineering.

## Translation

The Theme Handbook has one active translation, Japanese, which the ja.wordpress.org team maintains from a Markdown
repository that already mirrors the English page tree file for file. They asked for an English GitHub source in 2024
and paused in late 2024 because the structure kept changing. A one-to-one move with no structural change is the best
case for them: they get a per-file diff of what changed in English. No other translation exists, and nothing about
this proposal touches HelpHub or the localized sites.

## Questions and (some) answers

**Does the content change?** No. Known small defects, such as one empty page and a couple of malformed code blocks,
will be fixed in a separate pull request after the move, where everyone can see the diff.

**What about the "Last updated" date?** The first import touches every page, so every page will show the cutover
date once. After that, dates reflect real changes. Git history shows the true history of every page from then on.

**Who reviews pull requests, and how fast?** [Maintainer names] as code owners, with a stated target of a first
response within seven days. Maintainers can merge their own small fixes directly, as the Secure Custom Fields docs
allow, so routine upkeep does not slow down.

**Can I still edit on the site?** No, by design (see above). The "Edit" link on each page takes you to GitHub
instead.

**What if a page needs to be removed or renamed?** The importer never deletes. Removals and renames are a deliberate,
rare change: a pull request plus a redirect, done with a Meta committer. The repository's checks reject accidental
ones.

**Is this "all handbooks move to GitHub"?** No. It is this handbook, at its maintainers' request, following the model
its developer-docs siblings already use. HelpHub and the team handbooks are separate conversations.

**What happens to my open issues?** They move to the new repository with their comments intact, and the tracker's
`themes` label will point there.

## How to participate

- Comment on this post by [date].
- Join the Themes Team meeting on [date] at 15:00 UTC in #themereview, or the Docs Team meeting on [date] at
  14:00 UTC in #docs.
- If you maintain or translate the handbook, say so below; we want you in the maintainers group.

Props to [reviewers] for feedback on the draft.
