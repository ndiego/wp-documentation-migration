# 05 — Process, governance, deployment and history

How the WordPress Docs team works on end-user documentation (HelpHub) today, how changes to wordpress.org code get shipped, and what the governance path would look like for moving HelpHub from "edited in wp-admin" to "Markdown in GitHub, imported into WordPress" (the model the Block Editor Handbook uses).

Research date: 2026-10-11. Raw material (fetched posts, mailing-list copies of Trac tickets, PR stats) is saved in the session scratchpad under `process-research/`. Quotes are verbatim. Items marked **[unverified]** could not be confirmed from a primary source.

Note on sources: meta.trac.wordpress.org now sits behind a JavaScript bot challenge and returns HTTP 403 to scripts. Ticket contents below come from the `wp-meta` mailing list archive (lists.wordpress.org/pipermail/wp-meta), which mirrors every Trac comment. make.wordpress.org pages also accept `?output_format=md`, which is useful for scripted reading.

---

## TL;DR

1. **This has been tried before, and the attempt stalled.** In September 2023 the Docs team created [`WordPress/documentation-end-user`](https://github.com/WordPress/documentation-end-user) to hold all of HelpHub as Markdown in per-language folders with manifests. It came out of Javier Casares's [translation/localization proposal](https://make.wordpress.org/project/2023/09/06/documentation-translation-localization/) (2023-09-06). The repo holds only a skeleton (`en/index.md` plus 11 language manifests). Its last commit was 2024-02-16 and **no content was ever migrated**. By March 2024 the plan had shifted to "go for GlotPress", and then stalled on tooling.
2. **The strongest objection on record comes from Meta lead Dion Hulse (@dd32).** It is on [Meta #7520](https://lists.wordpress.org/pipermail/wp-meta/2024-March/057767.html), "Move Handbooks to GitHub" (March 2024). His points: GitHub plus Markdown "isn't accessible to all"; it works great for Block Editor docs because "the docs and code changes can happen in the same Gutenberg PR" but "can be total shambles for other content"; it is "a workaround" for wordpress.org lacking a suggest-edits flow; and it complicates translation (Phase 4 multilingual "will be reliant upon having WordPress posts as the source-of-truth"). Any HelpHub proposal must answer this directly.
3. **The Docs team's own pain is throughput and review, not editing tools.** As of 2026-10-11 there are 231 open HelpHub issues and 469 open issues overall. A tiny core group (Estela Rueda, Milana Cap, Andrea Roenning, Akira Tachibana) holds wp-admin publish rights. The December 2025 [workflow proposal](https://make.wordpress.org/docs/2025/12/02/proposal-to-change-the-user-documentation-workflow/) moved toward *less* pre-publish review: write directly in WordPress, schedule for release day, review afterwards. Today drafts live in GitHub issue comments or Google Docs and are then pasted into wp-admin by someone with access.
4. **Advanced Administration Handbook (AAH) is the direct precedent, and it worked.** It was proposed in July 2022 ([Meta #6411](https://lists.wordpress.org/pipermail/wp-meta/2022-July/050234.html)), started in a personal repo (zzap), moved to the WordPress org in November 2022, and went live on 2023-03-28 after dd32 "fix[ed] a bunch of broken things on the WordPress.org side, and fix[ed] the manifest file that was very incorrect". It was led by Javier Casares, Milana Cap and LucP across the Docs and Hosting teams. Since then: 197 merged PRs from 89 distinct authors. However, the median time-to-merge for the last 50 PRs is about 34 days, the repo has no PR template, no CI and no CONTRIBUTING file, and 11 PRs are open.
5. **Deployment of the importer is a Meta-committer job.** Content flows from GitHub to the live site with no human in the loop: the importer cron runs every 15 minutes, and I measured roughly 4–15 minutes from merge to live (below). *Code* changes (for example, a HelpHub importer subclass) must go through PR to `wporg-documentation-2022` or `WordPress/wordpress.org`, then a sync script on a sandbox, then `deploy-dotorg.sh`, run by a Meta committer. Since April 2026 the "Meta Janitors" group has a mandate to move fast and "explore tighter integration between WordPress.org and version-controlled workflows", which is a favourable opening.
6. **Translation is the hardest governance question.** About 8 Rosetta sites run localized HelpHub copies, created by a one-off import and then maintained independently, with no sync or notification tooling. A GitHub source of truth could help (diffs and notifications) or hurt (it diverges from the GlotPress plan that Polyglots and Meta favour). This needs a joint Docs/Polyglots/Meta decision.

---

## 1. The Docs team today

### 1.1 Structure and people

- **Team reps.** The handbook page [The team](https://make.wordpress.org/docs/handbook/the-team/) (last updated 2026-04-23) lists @kenshino, @atachibana and @milana_cap. On 2026-06-03 Milana posted [Welcome Estela as a team rep](https://make.wordpress.org/docs/2026/06/03/welcome-estela-as-a-team-rep/): "We are extremely happy that she accepted our proposal to join the co-rep position". The authoritative list is [make.wordpress.org/updates/team-reps](https://make.wordpress.org/updates/team-reps/).
- **Who does HelpHub work in practice** (authors of HelpHub-labelled issues created since 2025-10-01, n=244): estelaris 117, zzap (Milana) 39, andreawetzel (Andrea Roenning, @awetz583) 33, then a long tail of 1–6 each. @atachibana is the listed "Issues reviewer (end user docs)" and closes many issues. Velda (@supernovia) and Corey Hall are active in 2026 meeting notes.
- **Project roles** ([End-user roles](https://make.wordpress.org/docs/handbook/get-involved/team-roles/project-based/end-user/)): general end-user docs, block editor end-user docs, and feedback curator (moderates HelpHub article feedback comments in `wordpress.org/documentation/wp-admin/edit-comments.php` and turns them into GitHub issues).
- **Meetings.** All are Tuesdays at 14:00 UTC in #docs: discussion meetings, a monthly planning call, and a monthly 2-hour online Contributor Day (per the make/docs sidebar and the [2026-09-15 notes](https://make.wordpress.org/docs/2026/09/22/documentation-team-meeting-notes-september-15-2026/)). The team took summer breaks in both 2025 and 2026. Milana posts a weekly "Documentation Team Update" x-post to make/updates.
- **Morale and capacity context (2025).** [Docs team participation in WordPress releases](https://make.wordpress.org/docs/2025/09/10/docs-team-participation-in-wordpress-releases/) (Estela, 2025-09-10) objects to the Docs lead being dropped from the 6.8/6.9 release squads: "Documentation is not a 'nice-to-have,' it is a survival requirement." Estela also writes that contributors who stay "often feel burned out and have to take breaks". The comment thread became heated (personal accusations by one contributor), and a "stepping away of a team member" post followed on 2025-09-19. **This is relevant context: any proposal that looks like it takes control of HelpHub away from the Docs team will be read through this lens.**

### 1.2 Who can publish to HelpHub

- [End-user roles](https://make.wordpress.org/docs/handbook/get-involved/team-roles/project-based/end-user/): "Updating the documentation page/article is usually done by one of the project reps or active contributors who have access to the dashboard … Consistent contribution over time allows project reps to get to know you and gain trust in you, which can result in giving you access to the dashboard".
- [User documentation process before a major release](https://make.wordpress.org/docs/handbook/workflows/user-documentation-process-before-a-major-version-release/) (2026-03-24): "HelpHub editing access is limited to established Documentation team members who regularly contribute to the team's work."
- The 2025-09-10 post adds: "For now, we will not give access to the docs site to core committers who are not members of the docs team." It notes that @audrasjb, @desrosj, @jeffpaul, @johnbillion, @peterwilsoncc, @poena and @sergeybiryukov already have access, and "this will not be revoked."
- The [overhaul post](https://make.wordpress.org/docs/2026/02/02/how-to-help-with-the-overhaul-of-documentation-issue-tracker-in-github/) (2026-02-02): "Need to edit the docs site? Ping @estelaris or @milana_cap for access."

**Implication:** publish rights are a deliberate quality gate controlled by the Docs team. In a GitHub model, the equivalent gate is merge rights plus CODEOWNERS. The Docs team will want the same control there, and that should be offered up front.

### 1.3 Documentation Issue Tracker → edits in wp-admin

- Repo: [WordPress/Documentation-Issue-Tracker](https://github.com/WordPress/Documentation-Issue-Tracker), created 2021-08-17. It covers DevHub, HelpHub and the Docs handbook. The [handbook page](https://make.wordpress.org/docs/handbook/github-repository-and-projects/documentation-issue-tracker/) says: "No actual documentation is hosted in this repository. Its purpose is to track all the issues for any part of WordPress documentation."
- [Fixing an issue](https://make.wordpress.org/docs/handbook/workflows/fixing-an-issue/) (2024-09-16): "We don't have Pull Requests there because no actual documentation is hosted in the repository, so we can't use some other GitHub features, such as 'Request review' etc. Also, due to permissions, contributors can't assign themselves or move issues through our project boards." The flow is:
  1. Comment to claim the issue.
  2. A maintainer assigns it and sets "In progress".
  3. Ping @zzap or @atachibana for review.
  4. "After review you'll be either asked to fix something or if you'd like to update documentation yourself."
  5. Done.
- Automation (`.github/workflows`): label-driven project assignment, status-label sync, `/assign` and `/review` comment commands, and team notifications ("Heads up @WordPress/docs-issues-coordinators…").
- Issue templates include `new-release-enduser-issue.md` (title `[HelpHub]: `; checklist: Gutenberg PRs for 6.X, screenshots, videos, alt text, sentence-case headings, convert reusable blocks, **update the changelog**), `helphub-feedback-reports.md`, `good-first-issue--end-user--{screenshots,videos,ALT-attributes,headings}.md`, `doc-issue-fix.md` and `new-doc.md`.
- There are about 100 `[Block] X` labels, one per core block, which fits the "one block, one page" content model.
- Volume: 469 open issues, 231 open with `user documentation (HelpHub)`, and 56 open `HelpHub feedback`. In the last 12 months, 473 HelpHub issues were closed (a large triage push: 79 in Dec 2025, 50–63 per month in Mar–Sep 2026). See [WordPress Documentation Team Closes 200+ Issues](https://make.wordpress.org/docs/2026/04/21/wordpress-documentation-team-closes-200-issues-and-needs-your-help/) (2026-04-21): "the Documentation Team has triaged and labeled nearly 800 issues"; HelpHub had "358 open issues" at that time. The post asks helpers to "draft doc changes and comment with markdown or a link to your draft". **Contributors already write Markdown into issue comments, which are then retyped into the block editor by a publisher.**
- The 2026 overhaul post sets the rule: "Write your final updates in the comments first, before you update the actual article in WordPress." Goals include "Use the changelog to recognise contributors" ("Add anyone who suggested something … to the changelog. You only need to contribute once to become a Docs contributor!").

### 1.4 Release-cycle process

- Each release gets a GitHub project: [6.7 #223](https://github.com/orgs/WordPress/projects/223), [6.8 #235](https://github.com/orgs/WordPress/projects/235), [6.9 #262](https://github.com/orgs/WordPress/projects/262), [7.0 #286](https://github.com/orgs/WordPress/projects/286), [7.1 #295](https://github.com/orgs/WordPress/projects/295), [7.2 #305](https://github.com/orgs/WordPress/projects/305). Issues are auto-added by version label.
- [Before a major release](https://make.wordpress.org/docs/handbook/workflows/user-documentation-process-before-a-major-version-release/) (2026-03-24, edited 2026-04-07): identify changes from the roadmap, then Beta 1, then RC1. Draft "directly in a GitHub issue. This is the most common path" or in a Google Doc. Reviews use the "Needs 1st Review" status. Publishing is scheduled "ideally within 30 minutes of the release itself". "Always include a changelog or update the current changelog … at the bottom of the documentation."
- [Release day](https://make.wordpress.org/docs/handbook/workflows/documentation-process-during-a-major-version-release/): duplicate the previous Version page (a `helphub_version` post), fill in the jazzer, db_version and Trac revision; update [WordPress Versions](https://wordpress.org/documentation/article/wordpress-versions/), Roadmap and History. The handbook notes that Roadmap and History "will be pushed to the sandbox together", because those pages are theme code in wporg-main-2022, not HelpHub content.
- [Proposal to change the user documentation workflow](https://make.wordpress.org/docs/2025/12/02/proposal-to-change-the-user-documentation-workflow/) (Estela, 2025-12-02). It lists the 13 status columns and diagnoses the problem: drafts "usually in Google Docs … often sit more than a week waiting for a first review … by the time they are updated, the release has already shipped". It proposes: "For WordPress 6.9, the HelpHub documentation was written directly in WordPress, scheduled for release day, without review waiting time … reviews should occur after publication." Comments:
  - @annezazu: "the current process felt very cumbersome … I ended up going out on a limb and scheduling them to go live"; she wants "a bit of a tiered system … new contributors need reviews before publishing but more tenured … don't."
  - @awetz583 wants public previews so people without edit rights can review.
  - @stevenlinx wants the Dev Notes columns kept.
- **Implication for a GitHub model:**
  - The team's direction is *fewer* gates and *faster* publishing. A PR model gives tiered review for free: CODEOWNERS for maintainers, required review for first-timers.
  - It also gives public previews: the PR diff, or a Playground preview.
  - It must support **scheduled or release-gated publishing**, for example a manifest flag or a release branch. Today that is just WordPress post scheduling. (Precedent: the Block Editor handbook was briefly pinned to the `wp/5.4` branch in 2020, [Meta #5020](https://meta.trac.wordpress.org/ticket/5020), then reverted to trunk, [#5266](https://meta.trac.wordpress.org/ticket/5266). See [gutenberg#21858](https://github.com/WordPress/gutenberg/issues/21858).)

### 1.5 Recent content direction (2024–2026)

- [#1747 "Find ways to simplify the end user documentation and reduce the maintenance burden"](https://github.com/WordPress/Documentation-Issue-Tracker/issues/1747) (ndiego, 2024-10-23). It proposes removing manual "Blocks that include X" lists and linking shared sections. @carolinan: "can this information not be provided a by a plugin, automated? Because this can be parsed from the block library." Estela closed it on 2026-04-13: "this has been implemented in the block articles."
- [Important changes to the documentation articles](https://make.wordpress.org/docs/2026/06/01/important-changes-to-the-documentation-articles/) (2026-06-01): the Versions page is split and reordered; block pages now link to shared advanced settings ([#2287](https://github.com/WordPress/Documentation-Issue-Tracker/issues/2287)).
- [2026-05-26 notes](https://make.wordpress.org/docs/2026/05/27/documentation-team-meeting-notes-may-26-2026/): a "broader initiative to improve overall documentation structure", covering editor-to-doc links, dashboard links, FAQ revamp, and "Support vs. Documentation" confusion.
- AI: [Responsible AI workflow proposal](https://make.wordpress.org/docs/2025/07/24/proposal-responsible-ai-workflow-for-creating-new-documentation-for-wordpress-6-9/) (2025-07-24). In the 2026-09-15 notes the team agreed to label AI-assisted articles ("written by AI, reviewed by human"), and Corey Hall is testing Claude to check finished articles against their input issues.

### 1.6 Docs-related repos under the WordPress org

| Repo | Created | Status |
|---|---|---|
| [Documentation-Issue-Tracker](https://github.com/WordPress/Documentation-Issue-Tracker) | 2021-08 | Active; issues only |
| [Advanced-administration-handbook](https://github.com/WordPress/Advanced-administration-handbook) | 2022-08 (moved to org 2022-11) | Active; Markdown, imported to developer.wordpress.org/advanced-administration/ |
| [documentation-end-user](https://github.com/WordPress/documentation-end-user) | 2023-09-01 | **Dormant since 2024-02-16**; skeleton only |
| [WordPress-Documentation-Style-Guide](https://github.com/WordPress/WordPress-Documentation-Style-Guide) | 2020-09 | Style guide source |
| [HelpHub](https://github.com/WordPress/HelpHub) | 2016-01 | **Archived**; the old HelpHub dev repo |
| [wporg-documentation-2022](https://github.com/WordPress/wporg-documentation-2022) | 2022-11 | Theme and `support-helphub` plugin for wordpress.org/documentation (Meta-owned code) |
| [Documentation-Issue-Tracker-fr_FR](https://github.com/WordPress/Documentation-Issue-Tracker-fr_FR) | 2026-09-10 | Empty; "Issue Tracker for localizing the WordPress User Documentation into the fr_FR locale" **[purpose/owner unverified]** |
| Others imported to developer.wordpress.org | — | developer-plugins-handbook, wpcs-docs, Playground handbook, plus team handbooks on make (hosting-, test-, plugins-, contributor-day-, accessibility-team-handbook, spain-handbook) |

The [Criteria for repositories under the WordPress GitHub org](https://make.wordpress.org/project/2025/06/04/criteria-for-creating-or-migrating-repositories-under-the-wordpress-github-organization/) (2025-06-04) require:
- "at least one active maintainer under an established Make Contributor team … noted in the repository's README.md … and within the CODEOWNERS file";
- a problem statement;
- a Make-blog tag;
- an archiving policy: inactive after 6 months leads to archive.

A new HelpHub content repo needs this from day one. `documentation-end-user` is itself an archive candidate, or it could be revived.

---

## 2. History of HelpHub and of the "move it to GitHub" idea

### 2.1 Timeline

| Date | Event |
|---|---|
| 2015-01 | [Kicking off HelpHub](https://make.wordpress.org/support/2015/01/kicking-off-helphub/) and the [spec](https://make.wordpress.org/meta/2015/01/13/help-hub-spec/): replace the Codex's user docs |
| 2015–2019 | Codex → HelpHub/DevHub migration ([State of HelpHub Feb 2018](https://make.wordpress.org/docs/2018/02/26/state-of-helphub-february-2018/)); HelpHub plugin developed in the WordPress/HelpHub repo (now archived) |
| 2019-06-20 | [HelpHub & Handbooks Localisation](https://make.wordpress.org/meta/2019/06/20/helphub-handbooks-localisation/): HelpHub plugin activated on selected Rosetta sites; "The English HelpHub will remain the source of truth"; @ocean90 "doesn't think GlotPress is designed to deal with what we're proposing" |
| 2022-07-18 | [Meta #6411](https://lists.wordpress.org/pipermail/wp-meta/2022-July/050234.html): Advanced Administration handbook proposed, initially "maintained from the dashboard so we don't need connected GitHub repository" |
| 2022-08-13 | After the Hosting team joined, the plan switched to "generated from its own GitHub repository" ([comment](https://lists.wordpress.org/pipermail/wp-meta/2022-August/050446.html)) |
| 2022-10-11 / 10-19 | [Renaming Support to Documentation](https://make.wordpress.org/meta/2022/10/11/renaming-wordpress-org-support-to-documentation/); [New design for HelpHub](https://make.wordpress.org/docs/2022/10/19/new-design-for-helphub-in-wordpress-org/): new site map (4 categories) and a **per-article changelog** "to keep historic information on each article" |
| 2023-01 (end) | New wordpress.org/documentation launched by Docs and Meta ([Future plans for HelpHub](https://make.wordpress.org/docs/2023/02/07/future-plans-for-helphub/), 2023-02-07: "It has been 8 years since the HelpHub project kicked-off … Most of the initial members are not around") |
| 2023-03-28 / 04-10 | AAH goes live; developer-jargon articles moved out of HelpHub ([Introducing the AAH](https://make.wordpress.org/docs/2023/04/10/introducing-the-advanced-administration-handbook/)) |
| 2023-05-03 | [Notification form between documentation and Rosetta sites](https://make.wordpress.org/polyglots/2023/05/03/explorations-for-a-notification-form-between-documentation-and-rosetta-sites/) (Estela) |
| 2023-09-06 | [Proposal: Documentation translation / localization](https://make.wordpress.org/project/2023/09/06/documentation-translation-localization/) (Javier Casares): all docs in GitHub as Markdown, per-language folders, manifests |
| 2023-09-25 | [End-user docs repo – workflows and settings](https://make.wordpress.org/docs/2023/09/25/end-user-docs-repo-workflows-and-settings/) (Milana): `documentation-end-user` created; user-story project [#140](https://github.com/orgs/WordPress/projects/140) |
| 2024-02-16 | Last commit to `documentation-end-user` |
| 2024-03 | [Meta #7520](https://lists.wordpress.org/pipermail/wp-meta/2024-March/057736.html) "Move Handbooks to GitHub" debate (see 2.3) |
| 2024-04 → 06 | Spanish team starts translating ([Torrelodones](https://make.wordpress.org/docs/2024/04/04/translation-of-end-user-documentation-project-started-at-wordcamp-torrelodones-spain/)); [WCEU 2024 meeting notes](https://make.wordpress.org/updates/2024/07/16/localization-and-translation-of-helphub-meeting-notes/) |
| 2024-10-09 | [Using GlotPress to Translate Content](https://make.wordpress.org/polyglots/2024/10/09/using-glotpress-to-translate-content/) (Jesús Amieiro); [GlotPress PR #1856](https://github.com/GlotPress/GlotPress/pull/1856) still **open** |
| 2024-10-23 | [#1747](https://github.com/WordPress/Documentation-Issue-Tracker/issues/1747) simplification proposal |
| 2025-09-10 | Docs team vs. smaller-release-squad dispute |
| 2025-12-02 | Workflow proposal: write in WordPress, publish on release day, review after |
| 2026-02 → 04 | Issue-tracker overhaul; 200+ issues closed |
| 2026-04-23 | [Meta Janitors](https://make.wordpress.org/meta/handbook/about/projects/meta-janitors/) created |
| 2026-06-03 | Estela becomes co-rep |

### 2.2 The 2023 GitHub/Markdown proposal: what was planned

From the [2023-09-06 proposal](https://make.wordpress.org/project/2023/09/06/documentation-translation-localization/):

- "To simplify maintenance and access, we have decided to host the foundational documentation on GitHub. Each segment of documentation will have its own dedicated repository".
- "All documents will be stored in Markdown format … Each document will feature an initial H1 … followed by a final H2 … labeled 'Changelog'".
- "The final decision to publish documentation will rest with the maintainers … a configuration file, often referred to as a 'manifest' … Once content is integrated into this manifest, it will automatically be converted from Markdown to HTML or the relevant block format."
- "GlotPress … will not be used in this initiative".
- Reviewers credited: @estelaris, @nullbyte, @milana_cap, @otto, @clorith, @kenshino, @coachbirgit, @femkreations.

From [End-user docs repo – workflows and settings](https://make.wordpress.org/docs/2023/09/25/end-user-docs-repo-workflows-and-settings/):
- "Before we start translating, we must move all existing docs to the repo. After that is done, all translations, as well as creating new documentation in English and updating the existing one, will happen in that same repository."
- It defines personas: first-time contributor, experienced contributor, repo maintainer, issues coordinator, reviewers, translator, translation editor.

**Why it stalled** (synthesis; no explicit post-mortem was found **[unverified]**):
1. It was framed as a *translation* project, so it depended on the translation workflow being solved first.
2. Javier wrote on #7520 that "Over time has changed to 'go for GlotPress'".
3. Meta pushback in March 2024 (below).
4. GlotPress long-text support never shipped (PR #1856 is still open).
5. Docs team bandwidth went to releases and the issue backlog.

### 2.3 Arguments raised for and against

**For GitHub/Markdown:**
- **@oglekler** (Meta #7520, 2024-03-15): "it looks there are no easy way to raise ticket and make PR with proposed changes. Tickets in Trac are much less convenient and transparent."
- **@netweb** (Meta #6411, 2022-09-12): "One of the reasons to have a GitHub repository for the pages at developer.wordpress.org allows for easier contributions as contributors do not require a user account on developer.wordpress.org/wp-admin".
- **@JavierCasares** (#7520): "we've been working with very-non-technical people in Spain … and a quick guide and a quick reference guide". "Right now, all documentation is managed from GitHub, either by leaving the texts directly on GitHub, on Google Docs or similar… which end up becoming Markdown or WordPress content". "At the Community Summit 23, the conclusion was reached that this system, for now, is the least bad option". He also says @matt asked for "the ability to discuss before and after the translation, be collaborative".
- **@kenshino** (2023 proposal comments): non-technical translators can file issues, and "one of the Docs team members can review the issue and help create the PR. This also means that some of these issues will get cleared slower. But that's fine".
- **@flexseth** (#7520): some timeliness issues persist even with "60 editors".

**Against, or cautionary:**
- **@dd32** (Meta lead, [#7520 comment, 2024-03-20](https://lists.wordpress.org/pipermail/wp-meta/2024-March/057767.html)):
  - "using GitHub for documentation is 'easier' for a segment of the user-base, but it's not accessible to all, nor is it clear to many how it will look after converting markdown to WordPress Blocks (and Markdown is something that some absolutely love, and others absolutely hate). It works great for some documentation (ie. Block Editor, the docs and code changes can happen in the same Gutenberg PR) but can be total shambles for other content."
  - "I wish those suggestions didn't have to be managed via a GitHub account and PRs on markdown. Especially when WordPress is a CMS."
  - "Using GitHub for handbooks is more of a workaround for the underlying issue of 'WordPress.org doesn't have a way for users to offer textual edits and suggestions for content'".
  - On translation: "there needs to be a single source-of-truth that translations are based off. Gutenberg Phase 4 (Multilingual WordPress) will be reliant upon having WordPress posts as the source-of-truth, and managing the content outside of WordPress is going to create future work to support that."
  - "tl;dr: Simply converting handbooks to GitHub 'to make contributions easier' isn't easier for all, and causes other problems IMHO."
  - [2024-03-28](https://lists.wordpress.org/pipermail/wp-meta/2024-March/057912.html): "There's zero need for Github to be involved in that process [GitHub→GlotPress]; It can just as easily (and perhaps even easier) pull from a WordPress post. I don't know the background on the Community summit decisions, but it doesn't mean they were the correct decisions, or were made without input from those who were needed."
  - He also pointed to wporg-main-2022's hybrid model: pages are edited in the Page Editor and synced to the theme via automated PRs, "a hybrid approach, where the page can be edited visually, but edits aren't made live without a review first."
- **@bsanevans** (Training): many contributors "are not developers … updating the handbook in the Editor would seem to be 'easier'".
- **@tobifjellner** (Polyglots): "The idea of being forced to fork a repo, make that edit locally (probably directly in HTML), raise a PR, and finally commit it feels unneeded and heavy."
- **@flexseth**: GitHub "sets up an additional step, that creates more tickets and more information spread out".
- **@felipevelzani** (Plugins, [plugin-review-internal-scanner#51](https://github.com/WordPress/plugin-review-internal-scanner/issues/51), 2024-03): after the Plugin Developer Handbook moved to GitHub and syncing broke, he asked whether to revert to "the old way": "it would make sense for the regular docs, but I personally don't see a lot of value for these handbooks".
- **@akirk** (2023 proposal): without GlotPress, how do translators know what changed? Diffs, and segmenting by block.

**Alternatives floated:**
- [Revisions Extended](https://github.com/wordpress/revisions-extended) for suggest-an-edit (@courane01). dd32 said it "doesn't really achieve anything that's needed … the biggest flaw … is the lack of a public edit log, a public editing interface, and publicly trackable awaiting-review text change suggestions."
- A Playground-based edit flow (@flexseth); @zieladam built a prototype, [adamziel/playground-docs-workflow](https://github.com/adamziel/playground-docs-workflow) (2024-04-02): pages stored in GitHub, edited in Playground, saved back to the repo.

**What our proposal must answer:**
- (a) the accessibility of contribution for non-developers, for example with a Playground or web-editor path;
- (b) how Markdown maps to blocks (screenshots, video, callouts, tables, changelog);
- (c) the translation source of truth;
- (d) why not a WordPress-native suggest-edits flow instead.

The strongest *new* argument is that HelpHub is now block-centric, and block docs belong next to block code. This is dd32's own "works great … in the same Gutenberg PR" case. Supporting evidence is the [block.json auto-generation proposal](https://make.wordpress.org/core/2026/05/05/proposal-auto-generate-block-editor-handbook-docs-from-block-json/) (2026-05-05); per-block reference pages already exist in the Block Editor Handbook (for example `core-block-table`).

---

## 3. Meta/Systems: how code reaches wordpress.org

### 3.1 Repos and the SVN backbone

- The canonical code for wordpress.org lives in **SVN** (`meta.svn.wordpress.org`, plus private `dotorg.svn`). [WordPress/wordpress.org](https://github.com/WordPress/wordpress.org) is a read-only mirror. Its README says: "Staged Git PR changes will not be merged directly on GitHub; a Meta committer will review and commit the patch to the Meta repository, which will automatically sync and resolve the PR on GitHub." The repo now has AGENTS.md and CLAUDE.md; PRs are linked to Meta Trac tickets by a webhook; and a Props Bot workflow was added in January 2026 (r14639).
- Several sites are developed on GitHub and **synced into SVN by scripts** (`bin/sync/*.sh` on a sandbox): wporg-developer, wporg-mu-plugins, wporg-make, Learn, pattern-directory, wporg-two-factor, and wporg-documentation-2022 (`bin/sync/wporg-documentation.sh`, per PR #113).
- **wordpress.org/documentation code:** [wporg-documentation-2022](https://github.com/WordPress/wporg-documentation-2022) holds the theme plus `source/wp-content/plugins/support-helphub`. Pushes to trunk trigger `build.yml`, which pushes to the `build` branch; a committer then runs the sync and deploy.
  - 34 PRs ever, 24 merged, 11 distinct authors.
  - Merged by adamwoodnz (9), ryelle (8), dd32 (3), obenland (2), KokkieH, desrosj.
  - Median time-to-merge is 0.8 days, but activity is sporadic (1 merge in 2025, 6 in 2026).
  - [PR #113](https://github.com/WordPress/wporg-documentation-2022/pull/113) (obenland, 2026-07-27) shows the two-upstream hazard: "`support-helphub` has two upstreams. It lives in meta SVN … which is directly committable — but `bin/sync/wporg-documentation.sh` syncs it *from this repository*, overwriting SVN wholesale … Running the sync today would **revert both**." The last HelpHub sync was r14527 (2025-09-10).
- **wporg-markdown** (the generic handbook importer) lives in meta SVN at `wordpress.org/public_html/wp-content/plugins/wporg-markdown/`. Recent commits: r14817 (2026-04, "Handbook Markdown Importer…") and r14956 (2026-06, "Handbook Imports: Reject a…"). There is also a newer `plugins/handbook/inc/importer.php` with per-handbook `cron_interval` config (default `hourly`), used for make.wordpress.org team handbooks (details are in research note 02). DevHub's importers live in wporg-developer `inc/import-docs.php` (`$cron_interval = '15_minutes'`).

### 3.2 Who can deploy, how, and how long

From [Deploying WordPress.org](https://make.wordpress.org/meta/handbook/tutorials-guides/wordpress-org-sandboxes/deploying-wordpress-org/) (rewritten 2026-08-25):
- Prerequisites: "RW access to `meta.svn` and/or `dotorg.svn`", a sandbox, an SVN password, and 2FA.
- "A deploy ships all code in the tree, not just your changes … You must be ready to respond to breakage you did not cause."
- "A deploy takes roughly four to eight minutes, and is not atomic."
- For GitHub components: "do not hand-commit the change. Use the sync script". For wporg-developer: merge the PR, wait for the `build` branch, then `bin/sync/wporg-developer.sh`, `svnup-all.sh`, `deploy-dotorg.sh wporg`.
- Adding a new plugin needs an `svn:externals` entry, a deploy, then `wp --url=… plugin activate <slug>`. **This is how a plugin gets activated on a given site**; activation is a manual WP-CLI step by a committer.

From [Becoming a Meta committer](https://make.wordpress.org/meta/handbook/about/projects/becoming-a-meta-committer/) (2026-08-25):
- "granted to contributors with a track record on Meta, and it is granted per-area rather than all at once".
- "There is no application form … be around in `#meta`".
- "Prefer pull requests … Merging your own PR is fine when the change is small or urgent. Be available after you deploy."

[Meta Janitors](https://make.wordpress.org/meta/handbook/about/projects/meta-janitors/) (2026-04-23) "grants a trusted group of contributors WordPress.org sandbox access in order to make changes and improvements without 'approval or feedback needed from any team, group, stakeholder, commenter, or approval from anyone but me (Matt).'" "Participants are encouraged to lean into AI tooling, explore tighter integration between WordPress.org and version-controlled workflows (SVN, Git, Trac, GitHub)". Members: @4thhubbard, @annezazu, @barry, @dd32, @eugeneb222, @grierson, @nacin, @noel_tock, @markjaquith, @nickhamze, @westonruter, @yaniiliev. Updates are posted in #meta-janitors.

### 3.3 Cron on wordpress.org

- wordpress.org runs **Cavalcade** (Human Made's database-backed cron runner) rather than page-load WP-Cron. Evidence from meta code:
  - `plugin-directory/jobs/class-manager.php`: "This must be run after plugins_loaded, as that's when Cavalcade hooks in"; `wp_cache_delete( 'jobs', 'cavalcade-jobs' )`.
  - `official-wordpress-events.php`: "Cavalcade isn't fully loaded before [init]".
  - A test fixture stubbing `HM\Cavalcade\Plugin\Job`.
  - So importer `wp_schedule_event()` jobs run on server-side workers. **[Strongly indicated by code; not confirmed by Systems in writing.]**
- Measured content latency (merge → REST `modified_gmt`, 2026-10-11):

| Gutenberg commit (UTC) | Handbook page updated | Lag |
|---|---|---|
| 09:44:50 Video min-size (#83974) | `core-block-video` 09:48:57 | ~4 min |
| 09:48:39 Icon (#83971) | `core-block-icon` 10:03:57 | ~15 min |
| 10:04:07 Table (#83949) | `core-block-table` 10:18:56 | ~15 min |
| 10:14:09 Post Navigation Link (#83973) | `core-blocks` 10:19:01 | ~5 min |
| AAH 14:00:33 2026-09-29 (#5xx typos) | adv-admin pages 14:06:15 | ~6 min |

  **Content changes go live within one 15-minute cron cycle with no manual step.**

### 3.4 Typical turnaround to ship "add a HelpHub importer"

Evidence-based estimate:
- **AAH** (closest precedent): the repo was ready in November 2022, the content was declared "ready" on 2023-03-27, and it was imported the next day. About 8.5 months passed from ticket to live; the actual Meta work took about 1 day once content was ready, but needed dd32 personally ("I'm not 100% on the steps").
- **Plugin Handbook** (GitHub, early 2024): merged PRs did not reach the site for weeks ("there is a known issue and Dion is working on it").
- **Developer Reference parser** (a related automated pipeline, [post](https://make.wordpress.org/core/2026/02/25/developer-documentation-restored/) 2026-02-25): silently broken from 6.4 to 6.9.1, "over two years out of date". Lessons quoted: "The process for generating and deploying documentation updates is in dire need of its own documentation. A challenge … has been knowing where to run updates and what updates to run … A contributing factor … was a failure to notify developers when source code changes broke the documentation generation process."
- **Realistic path:**
  1. Make/docs proposal, cross-posted to meta, polyglots and core.
  2. Meta Trac ticket (component HelpHub).
  3. PR to wporg-documentation-2022 (and/or a meta SVN patch for wporg-markdown).
  4. Review by a Meta committer: obenland, dd32, adamwoodnz or ryelle are the recent active ones.
  5. Sync and deploy.
  6. WP-CLI activation and first import on the documentation site.
  7. Redirect checks.

  Code work is small; **calendar time is dominated by consensus and by finding a committer**: weeks to months. Meta Janitors could shorten this.

---

## 4. Block Editor Handbook as the model

- **Flow:** docs live in `gutenberg/docs/` and package READMEs; `docs/manifest.json` is generated by `npm run docs:build`. A PR is reviewed by Gutenberg maintainers or docs folks and merged to trunk. The wporg-developer importer (`15_minutes` cron) fetches the manifest and Markdown from GitHub raw and updates `blocks-handbook` posts. No manual step; measured lag 4–15 minutes (3.3).
- **Source branch:** trunk. A 2020 attempt to pin to `wp/5.4` was reverted ([gutenberg#21858](https://github.com/WordPress/gutenberg/issues/21858): "Docs are now back to being pulled from the `master` branch since … #5266"). The consequence is that plugin-only or experimental features can appear in the handbook before they ship in core. For end-user docs, which must match the released UI, this is a real gap: HelpHub publishes on release day.
- **Known complaints and issues:**
  - [gutenberg#61206](https://github.com/WordPress/gutenberg/issues/61206): pages not updated when two Markdown files share a name.
  - [wporg-developer#240](https://github.com/WordPress/wporg-developer/issues/240): no "View source" link, open since 2023.
  - [#294](https://github.com/WordPress/wporg-developer/issues/294): no per-page contributor props.
  - [#464/#505](https://github.com/WordPress/wporg-developer/issues/505): `post_modified` is not taken from the last commit.
  - [#466](https://github.com/WordPress/wporg-developer/issues/466): Markdown parsing bugs.
  - [#345](https://github.com/WordPress/wporg-developer/issues/345): "Last updated" removed.
  - The 2026-09-15 Docs meeting notes that adding images to the handbook needed special access.
  - The props/changelog gap matters for HelpHub, because the Docs team now uses the article changelog *specifically to credit contributors*.
- **Governance lesson (2026):** the block.json auto-docs PR [#77350](https://github.com/WordPress/gutenberg/pull/77350) "was merged but subsequently reverted ([#77590](https://github.com/WordPress/gutenberg/pull/77590)) due to insufficient community discussion before landing", then re-proposed on make/core with a Hallway Hangout. **Post a make proposal before landing structural docs changes.**

---

## 5. Advanced Administration Handbook: the precedent

- **Origin.** In a Zoom call the Docs reps (@kenshino, @atachibana, @estelaris, @milana_cap) proposed a home for HelpHub "Technical guides" plus unmigrated Codex pages ([#6411, 2022-07-18](https://lists.wordpress.org/pipermail/wp-meta/2022-July/050234.html)). The initial plan was wp-admin; it switched to GitHub after the Hosting team joined (2022-08-13).
- **Leads.** @JavierCasares (Hosting), @lucp, @milana_cap ([announcement on make/hosting, 2022-09-07](https://make.wordpress.org/hosting/2022/09/07/wordpress-advanced-administration-handbook/)). Current handbook reps: @javiercasares and @lucp.
- **Workflow adopted** (Milana, [2022-08-13](https://lists.wordpress.org/pipermail/wp-meta/2022-August/050446.html)):
  - an inventory project, [#47](https://github.com/orgs/WordPress/projects/47);
  - issues in the Docs tracker with an `advanced administration` label and automation that adds them to the project;
  - bot notifications;
  - a content repo with `manifest.json`;
  - "Hosting team members … granted maintainers access to Docs issue tracker repo";
  - shared maintenance by Docs and Hosting "just as we have Themes handbook being shared between Themes and Docs teams";
  - one issue per page to migrate, so contributors could pick one at Contributor Days (WCUS, WC Netherlands, WC Valencia 2022).
- **Timeline:**
  - personal repo `zzap/WordPress-Advanced-administration-handbook`, 2022-08;
  - first version done 2022-11-16;
  - transferred via dd32 to the WordPress org 2022-11-23, with the Documentation and Hosting GitHub teams given maintain access and Javier/Milana admin "to avoid bugging meta team for small things";
  - [status post 2023-01-15](https://make.wordpress.org/hosting/2023/01/15/advanced-administration-handbook-status-2023-01-15/): 63 pages, 10 sections, 51 items to move from Support, Codex or APIs;
  - import set up 2023-03-28 (r12504 plus [AAH PR #190](https://github.com/WordPress/Advanced-administration-handbook/pull/190) fixing the manifest);
  - HelpHub redirects ([wporg-documentation-2022#59](https://github.com/WordPress/wporg-documentation-2022/issues/59)) and announcement on 2023-04-10;
  - ticket closed 2023-04-04.
- **Onboarding non-GitHub users:**
  - The status post's tools list: "A GitHub account … connect it to your WordPress account" plus "A text / Markdown editor".
  - The Hosting [Contributor Day page](https://make.wordpress.org/hosting/handbook/get-involved/contributor-day/) explains GitHub signup and linking the GitHub username on profiles.wordpress.org for credit.
  - Javier's [handbook Markdown quick reference](https://github.com/javiercasares/wordpress-handbook-markdown).
  - The repo includes an `.obsidian` config, suggesting the Obsidian editor was used **[usage unverified]**.
  - The README lists style-guide links and example-domain/IP conventions.
- **Repo hygiene today:** no `.github` folder (no PR template, CI, CODEOWNERS or CONTRIBUTING file). Labels are minimal (`needs reviewers`, `contributorday`, `WCEU2023`, `WCUS26`, …).
- **Stats** (2026-10-11):
  - 262 PRs: 197 merged, 54 closed unmerged, 11 open.
  - Merged by year: 2022: 41, 2023: 64, 2024: 34, 2025: 25, 2026: 33.
  - 89 distinct merged authors; javiercasares 47.
  - Median time-to-merge 0.7 days overall but **~34 days for the last 50**.
  - Last 40 merges by kittenkamala 18, mindctrl 13, zunaid321 4, others.
  - Open issues: 33 in the tracker under the advanced administration label ([2026-04-21](https://make.wordpress.org/docs/2026/04/21/wordpress-documentation-team-closes-200-issues-and-needs-your-help/)).
- **Lessons** (no formal retrospective found **[unverified]**):
  1. It worked because there was a clear inventory, a cross-team owner, and Contributor-Day-sized issues.
  2. Launch depended on one Meta person, and the manifest was wrong until he fixed it. **Validate the manifest in CI.**
  3. Review latency grew as the founders moved on, and reviewers are now mostly newer maintainers. **Name maintainers in CODEOWNERS and README, and set a review SLA.**
  4. It is a *new* handbook of technical content; HelpHub is an *existing*, screenshot-heavy, end-user site with localized copies. **Migration, redirects and media are the hard parts AAH barely touched.**

---

## 6. Translations

- **Today:** HelpHub is enabled per Rosetta site on request ([Translating HelpHub](https://make.wordpress.org/docs/handbook/helphub/translating-helphub/), last updated 2020-12):
  - Polyglots Global Mentors grant the first "HelpHub Administrator".
  - English articles are bulk-imported once (WXR export of "Articles", import with attachments, set to Draft, per the Polyglots [locale forum deployment page](https://make.wordpress.org/polyglots/handbook/polyglots-global-team-leads-and-mentors/deployment/creating-a-new-locale-forum/)).
  - Locale editors then translate in wp-admin.
  - Status is tracked in a Google Sheet ("HelpHub Migration Worksheet").
  - The guide says "Keep post slugs in English for now so that current redirect rules will continue to work."
  - Tracking English changes relies on third-party tools: [wp-info.org helphubchanges](https://wp-info.org/tools/helphubchanges.php) and [developerka.org helphub-updates](https://developerka.org/helphub-updates/).
  - **No sync tool exists.** Re-imports are manual Meta requests: zh_CN asked to "clear and re-import" ([2024-04-15](https://make.wordpress.org/polyglots/2024/04/15/request-to-clear-and-update-helphub-support-articles/), [Meta #7587](https://lists.wordpress.org/pipermail/wp-meta/2024-April/058306.html)). That request was still unresolved in June 2025: "I am waiting for … using-glotpress-to-translate-content, but it seems to be progressing very slowly."
- **Measured footprint, all 199 Rosetta sites** (2026-10-12; every locale site linked from the [Polyglots teams page](https://make.wordpress.org/polyglots/teams/), probed at `/support/wp-json/wp/v2/articles` and read `X-WP-Total`). English (wordpress.org/documentation) has 321 articles.

  | Locale site | Published HelpHub articles |
  |---|---|
  | fr.wordpress.org | 296 |
  | ja.wordpress.org | 264 |
  | it.wordpress.org | 239 |
  | es-mx.wordpress.org | 59 |
  | ru.wordpress.org | 48 |
  | es.wordpress.org | 22 |
  | cn.wordpress.org | 13 |
  | br.wordpress.org | 13 |
  | ve.wordpress.org | 11 |
  | pt-ao.wordpress.org | 11 |
  | sr.wordpress.org | 3 |
  | ko.wordpress.org | 3 |
  | bn, es-ar, nl, snd, vi | HelpHub enabled, 0 published |
  | the other 182 | no HelpHub (404 on the endpoint) |

  So 17 locales have HelpHub enabled, 12 have published something, and only 3 (fr, ja, it) are anywhere near complete. **Caveat:** the REST count sees published posts only. The documented import creates the English articles as *drafts*, so a locale that imported but is still translating (or never got past the import) shows 0 here. Locales with a tiny count (sr, ko, ve, pt-ao) are probably in that state rather than "translated 3 articles". A wp-admin view, or asking the locale's HelpHub admin, is the only way to see the full picture.
- **WCEU 2024** ([notes](https://make.wordpress.org/updates/2024/07/16/localization-and-translation-of-helphub-meeting-notes/)):
  - "the Meta team doesn't know the scope of adding this page to Rosetta sites"; "this process will need a dedicated meta team member".
  - "The French community has about 90% of the end-user translated", and redirect tables are needed to preserve it.
  - On URLs: "it is better to keep everything in English … easier to synchronize".
  - GlotPress concerns: string-based, needs segment context, versioning.
- **Block Editor Handbook:** not translated at all.
- **The GlotPress route:** the [2024-10-09 post](https://make.wordpress.org/polyglots/2024/10/09/using-glotpress-to-translate-content/) envisions "Updates to the English Documentation would lead to automatic updates of the GlotPress projects" and auto-publish "at a certain translation threshold". [GlotPress PR #1856](https://github.com/GlotPress/GlotPress/pull/1856) has been open since 2024-08-15.
- **Revival signals:** in December 2025, @tobifjellner joined #docs "interested in understanding the documentation workflow to continue the translation project". `Documentation-Issue-Tracker-fr_FR` was created 2026-09-10 (empty).
- **What GitHub-based HelpHub would mean for localizers.**
  - Positive: a clean, per-article Git diff and commit history for "what changed in English since my translation", which is exactly what [akirk asked for](https://make.wordpress.org/project/2023/09/06/documentation-translation-localization/). It also enables automatic notifications (GitHub Action → issue in a locale tracker) and could feed GlotPress segment extraction from Markdown just as easily as from posts.
  - Negative: dd32's single-source-of-truth concern (Phase 4 assumes WP posts). Locales that translate in wp-admin would lose the "import from English HelpHub" path unless the importer also writes to Rosetta sites or the English site remains readable via REST. It does: the English site stays a normal WP site, so existing Rosetta flows keep working.
  - **Recommendation:** keep English-only in GitHub for phase 1 and don't promise translation tooling. Publish per-article content hashes or commit links so locale teams can detect drift.

### 6.1 Risk: the English overhaul does not reach the Rosetta copies

Everything in this study (Markdown source, automated import, restructuring, cleanup) touches only the English site. The localized HelpHubs are independent WordPress posts on each Rosetta site, created by a one-time import and edited by hand there. Consequences to state plainly in any proposal:

- **Nothing propagates.** A cleaned-up English article leaves fr, ja, it and the rest exactly as they are, including articles that were merged or deleted in English years ago. Drift continues at today's rate because there is still no change notification.
- **Restructuring makes a later re-import harder.** Renames, merges and removals widen the structural gap between English and each copy, so a locale that later asks Meta to "clear and re-import" (as zh_CN did in 2024, still unresolved in 2025) faces a bigger reconciliation than it would today.
- **The Rosetta import path depends on English staying a normal WordPress site.** The documented flow exports English as WXR and imports it on the locale site. That keeps working only while the imported Markdown lands in ordinary posts with the content in `post_content`. Anything that lives in the repo but not in the post (front matter, assets referenced by relative path, build-time transforms) is invisible to localizers.
- **Expectation risk.** The Docs, Polyglots and Meta teams have disagreed since 2023 about GitHub-versus-GlotPress for translation. A proposal that appears to decide that question will be read through that history and stall the way `documentation-end-user` did.

What the overhaul *can* offer localizers without solving translation: a per-article Git history (the diff "what changed in English since my translation" that @akirk asked for in 2023), a cheap notification hook (GitHub Action → issue in a locale tracker; `Documentation-Issue-Tracker-fr_FR` already exists, empty), and a clean, structured source that the GlotPress long-form plan could consume if PR #1856 ever ships.

**Recommendation:** scope the proposal as English-only; keep the English site readable the way the Rosetta import expects; ship diff/notification as a localizer benefit; say explicitly that translation is unchanged and remains a joint Docs/Polyglots/Meta decision. Concentrate any outreach on fr, ja and it, the three locales with a real investment to protect.

---

## 7. Open questions for the Docs and Meta teams

**Docs team (ownership and workflow)**
1. Who are the named maintainers and CODEOWNERS of a HelpHub content repo? Does the Docs team keep exclusive merge rights, mirroring today's publish-rights policy?
2. Tiered review (annezazu's idea): can experienced contributors self-merge small fixes while first-timers need one approval? What is the review SLA? (AAH's recent median is about 34 days.)
3. Release-day publishing: hold release docs in a branch, a `draft`/`publish_after` manifest flag, or merged-but-unlisted? Who presses the button on release day?
4. Does the per-article changelog (used for contributor credit) stay hand-written, or is it generated from commit co-authors? How do GitHub contributions earn the Documentation Contributor badge? (Props Bot exists for meta.)
5. Revive `WordPress/documentation-end-user` (already approved in 2023, with history) or create a new repo? Its per-language folder layout would need rethinking for English-only.
6. Should Documentation-Issue-Tracker remain the intake, with PRs in the content repo, or should HelpHub issues move to the content repo?
7. Non-GitHub contributors: keep "comment with your draft in an issue" as an accepted path, with maintainers converting it to a PR (Kenshino's 2023 position)? Is a Playground or GitHub web-editor flow acceptable?
8. Screenshots and video: where do images live (repo vs. media library), and who can add them? This was a blocker for images in the Block Editor Handbook as recently as September 2026.
9. Which content goes first? Block pages (one per inserter-visible block) are the strongest case, because they can live next to block code or be partly generated from `block.json`.

**Meta team (code, deploy, operations)**
10. Who will review and deploy the importer change, and which Meta committer is the long-term owner? (dd32, obenland, adamwoodnz, ryelle were recently active on these repos.) Can Meta Janitors sponsor it?
11. Import into the existing `helphub_article` post type (keeping IDs, URLs, comments/feedback and Rosetta relationships) or a new handbook post type? How do category and taxonomy assignments come from the manifest?
12. Fix the two-upstream problem for `support-helphub` (PR #113) before adding importer code there. Should the importer live in wporg-documentation-2022, in wporg-markdown, or in the newer `handbook` plugin importer?
13. Monitoring: how do we avoid a silent failure like the two-year Code Reference outage? Options: a CI check of the manifest in the content repo, an import-error alert to #docs or #meta, and a visible "last imported commit" on the page.
14. Cron cadence (15 minutes vs. hourly default), and whether imports can be triggered by a GitHub webhook on merge.
15. Redirects and rollback: if a bad merge publishes, is reverting the commit sufficient? Are revisions kept?

**Polyglots and Meta (translation)**
16. Does a GitHub source of truth conflict with the GlotPress content-translation plan (PR #1856)? Could the GlotPress importer read from the Markdown repo instead of posts?
17. How do Rosetta HelpHub sites (fr 296, ja 264, it 239 articles) learn about English changes? Could an Action open issues in per-locale trackers like the new `Documentation-Issue-Tracker-fr_FR`?
18. dd32's Phase 4 concern: is a Markdown source acceptable if the English WP posts remain the canonical *published* artifact that multilingual tooling reads from?

**Process**
19. Proposal venue: a make/docs post cross-posted to meta, polyglots, core (and training/support), plus a Meta Trac ticket (HelpHub component). Hold a Hallway Hangout before any merge, given the block.json revert precedent.
20. Address #7520's open framing directly: we are not proposing "all handbooks to GitHub". We are proposing that end-user docs tightly coupled to Gutenberg features (blocks) be versioned with them, with WordPress remaining the rendering and translation surface.
