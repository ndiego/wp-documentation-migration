# 04 — Governance, people and process for moving the Theme Handbook to GitHub

Scope: who owns https://developer.wordpress.org/themes/ (139 `theme-handbook` posts, edited in wp-admin), who has to agree to a one-to-one move into a GitHub Markdown repo imported by the DevHub importer, who does the work, what process the new repo should run, and what could derail it. The structure is treated as fixed; this is a conversion plus wiring.

Research date: 2026-10-12. This builds on, and does not repeat:
- `notes/wporg-handbook-pipeline/research/05-process-governance-deployment.md` (Docs team process, AAH precedent, Meta deployment, Meta Janitors, Meta #7520 objections). Cited below as **R05**.
- `notes/wporg-handbook-pipeline/research/03-handbook-landscape-survey.md` (importer families, the diverged plugin-handbook mirror). Cited as **R03**.
- `notes/wporg-handbook-pipeline/research/02-wporg-consumer-side.md` and `04-importer-spike.md` (importer adoption and sync semantics). Cited as **R02** and **R04**.
- `notes/theme-handbook-migration/research/01-content-inventory.md` (the 139 pages). Cited as **TH01**.

Method and limits: make.wordpress.org REST and `?output_format=md`; developer.wordpress.org REST (`/wp-json/wp/v2/theme-handbook`); `gh` against GitHub; the `wp-meta` mailing-list archive for Meta Trac (meta.trac returns 403 to scripts, see R05). **Not available:** a Slack export (no Slack search was possible, so Slack-only discussions are missing), per-revision editors of handbook pages (REST `revisions` returns 401), and GitHub org project boards (token lacks `read:project`). Items that rest on inference are marked **[unverified]** or **[inferred]**. Raw pulls are in the session scratchpad under `gov/`.

---

## TL;DR

1. **Ownership is shared and documented as such, but the real maintainer set is three to four people.** The Themes team's handbook says it "maintains the Theme Developer Handbook"; the Docs team's role page says it is "created and maintained in collaboration with the Themes team". In practice, Justin Tadlock (@greenshady, Themes rep 2026, Automattic-sponsored) wrote the 2023-24 block-theme overhaul (61 of 139 pages created under his account, 94 of 236 `themes` issues filed, 97 assigned). In 2026 the visible editor is **Cheyne (@chekle on GitHub, Automattic)**, who closed 21 of the 24 `themes` issues closed this year, in a July 2026 batch that matches the pages' `modified` timestamps to the minute.
2. **The trusted maintainer already asked for this move, twice, in public.** On 2024-01-11 Justin wrote on the overhaul tracking issue: "I'd love to have a dedicated GitHub repo for managing this." On 2024-08-30 he commented on Meta #7520: "it would be highly beneficial to the folks who maintain the Theme Handbook to have this particular handbook connected to GitHub … Right now, only 2-3 people actively contribute to the handbook at all." Nothing happened after that; #7520 has had no activity on the mailing list since August 2024.
3. **The Theme Handbook is translated, in exactly one place, and that team wants GitHub.** The Japanese locale team keeps a 139-file Markdown mirror (`jawordpressorg/theme-handbook`, last push 2026-07-25) and publishes it at ja.wordpress.org/team/handbook/theme-development/. Publication was paused on 2024-12-25 "because the content and structure of the original have changed significantly", and translation work resumed in 2026. A one-to-one move with no structural change is the best case for them, and @t-hamano asked for a GitHub source in 2024. No GlotPress project and no other Rosetta copy was found.
4. **The cheapest proposal path is the SCF one, not the AAH one.** SCF went from Meta ticket (#7917) to merged importer (wporg-developer #547) on the **same day, 2025-02-20**, because the content owner wrote the importer PR and @dd32 reviewed and merged it. AAH took about 8.5 months, almost all of it content and consensus. Since the content and structure here are settled, the critical path is (a) Themes + Docs sign-off, (b) a repo in the WordPress org, and (c) one Meta committer (dd32 or coffee2code) to merge a roughly 35-line importer class and run the first import.
5. **The biggest structural risk is the same one that left the plugin mirror stale: two sources of truth.** The importer only *warns* in wp-admin ("Content, title, and slug edits here will be discarded on next sync"). It does not block editing, and it only overwrites a page when that page's Markdown changes. Cutover must remove wp-admin edit capability for `theme-handbook` or accept silent divergence.
6. **The second risk is people capacity.** The handbook's active maintainers are Automattic-sponsored. @carolinan noted in April 2025 that progress depended on "if Automattic is going to change their contribution hours back". AAH shows what happens when founders move on: the median time to merge for its last 50 PRs is about 34 days, and 38 days for 2026 merges (measured 2026-10-12). The new repo needs at least two named CODEOWNERS and a review SLA from day one.

---

## 1. Ownership today

### 1.1 What the teams' own pages say

| Source | What it says | Date |
|---|---|---|
| [Themes team: About](https://make.wordpress.org/themes/handbook/about/) | The Themes Team "reviews and approves themes … and maintains the [Theme Developer Handbook]"; the list adds "Contributes to the Theme Developer Handbook". | page last modified 2023-08-04 |
| [Docs: Developer roles, Themes handbook](https://make.wordpress.org/docs/handbook/get-involved/team-roles/project-based/developer-roles/#themes) | "The Themes handbook is created and maintained in collaboration with the Themes team. To contribute to the handbook you can contact either the Documentation or Themes team." Label `themes`. | 2023-02-15 |
| [Docs: The team](https://make.wordpress.org/docs/handbook/the-team/) | "Theme Handbook Rep: @kafleg, @utz119, @poena" (a dead `acalfieri` profile link is also embedded). | 2026-04-23 |
| [Themes: Projects](https://make.wordpress.org/themes/handbook/get-involved/projects/#theme-developer-handbook) | "Theme Developer Handbook. Leads: @acalfieri, @aristath", plus a Trello board. | 2020-06-04, **stale** |
| [Theme Handbook: Feedback](https://developer.wordpress.org/themes/credits/feedback/) | Feedback goes to #docs on Slack, by joining "the Documentation Team as an editor", or through the Documentation Issue Tracker `themes` label. | 2024-06-05 |
| Doc tracker bot [`notify-team-on-label.yml`](https://github.com/WordPress/Documentation-Issue-Tracker/blob/main/.github/workflows/notify-team-on-label.yml) | `themes=@kafleg @TeBenachi`. Justin is **not** pinged. | read 2026-10-12 |
| R05 (AAH origin, 2022-08-13) | Milana Cap: "just as we have Themes handbook being shared between Themes and Docs teams". | 2022 |

So the answer to "which team owns it" is **both, formally**. The Docs team owns the intake (the tracker) and the editor role on paper. The Themes team owns the subject matter and, in practice, the people. The make/themes projects page is out of date, and the Docs "Theme Handbook Rep" list does not include the person who wrote most of the current handbook.

### 1.2 Team reps

| Team | Reps (2026) | Source |
|---|---|---|
| Themes | @bijayyadav (Bijay Yadav, Elementor-sponsored), @fahimmurshed (Fahim Murshed), @greenshady (Justin Tadlock, "Automattic sponsors him to contribute full-time to Documentation, Support, and Themes") | [make/updates team reps](https://make.wordpress.org/updates/team-reps/) (modified 2026-09-28); [Introducing new Themes Team representatives for 2026](https://make.wordpress.org/themes/2026/01/07/introducing-new-themes-team-representatives-for-the-2026/) (KafleG, 2026-01-07) |
| Documentation | @kenshino, @milana_cap, @atachibana, @estelaris | same; see R05 §1.1 |
| Meta | @tellyworth, @coffee2code | same |

Themes team meetings in 2025-26 are small (3 to 7 attendees) and focus on theme-review statistics. Examples: [2026-07-28 notes](https://make.wordpress.org/themes/2026/07/30/themes-team-meeting-notes-for-july-28-2026/) list 3 attendees, and [2025-08-26 notes](https://make.wordpress.org/themes/2025/08/27/themes-team-meeting-notes-for-august-26-2025/) list 7. The handbook comes up only occasionally in open floor. @kafleg (Ganga Kafle) writes most Themes posts and is a Docs "Theme Handbook Rep".

### 1.3 Who actually maintains it (evidence)

**Page authorship** (REST `author` is the original creator, not the last editor; see TH01 §b). Justin Tadlock 61, Samuel Sidler 44 (2014 originals), KafleG 6, Kenshino 6, user 14167654 (not resolvable) 6, Nick Halsey 5, Akira Tachibana 3, and others 1 each. Pages by `modified` year: 2022: 27, 2023: 41, 2024: 33, **2025: 5**, 2026: 18.

**`themes` label on the Documentation Issue Tracker** (pulled 2026-10-12, 236 issues, 0 PRs):

| | |
|---|---|
| Open / closed | 73 open, 163 closed |
| Created per year | 2022: 72, 2023: 86, 2024: 46, 2025: 26, 2026: 6 |
| Closed per year | 2022: 42, 2023: 63, 2024: 31, **2025: 3**, 2026: 24 |
| Top issue authors (all time) | justintadlock 94, nielslange 31, carolinan 16, kafleg 10, TeBenachi 6 |
| Assignees (all time) | justintadlock 97, kafleg 9, carolinan 6, chekle 5 |
| Closers 2024-2025 | justintadlock 29, carolinan 2, estelaris 1, flexseth 1, dd32 1 |
| **Closers 2026** | **chekle 21**, estelaris 3 |
| Open issues by creation year | 2022: 17, 2023: 14, 2024: 20, 2025: 18, 2026: 4; 28 assigned (18 to Justin); 16 labelled `new document`; 17 titled "overhaul" |

The R05 figure of "Themes 146 open" comes from [Estela's 2026-04-21 post](https://make.wordpress.org/docs/2026/04/21/wordpress-documentation-team-closes-200-issues-and-needs-your-help/). A label search gives about 92 open on that date (73 open now, 71 of them created before 2026-04-21, plus 21 closed since). The post probably counted something broader. **[discrepancy, unresolved]**

**The July 2026 batch.** For example, #1850 was closed by chekle at 2026-07-22T01:39:36Z ("I've rewritten the File Organization of Page Templates section"), and `/themes/classic-themes/templates/page-template-files/` was modified at 2026-07-22T01:37:39Z. The other 2026 `modified` stamps (2026-05-19/20, 06-02/04, 06-24, 07-20/22) line up with chekle's closures of #2017, #2023, #2002, #1994, #1105, #1675, #850, #868, #616 and others. Cheyne (GitHub `chekle`, "Happiness Engineer, Automattic") has been active on the tracker since 2021 and in 2026 closed HelpHub and DevHub issues as well (125 issues involve them). **Inference:** chekle holds `handbook_editor` (or higher) on developer.wordpress.org and is today's de facto fix-up editor; Justin is the subject-matter owner and author. **[editor identity inferred from timestamps; revisions are not public]**

**Justin's activity and availability.**
- He posted on [2025-08-26](https://make.wordpress.org/themes/2025/08/27/themes-team-meeting-notes-for-august-26-2025/) that he is "hoping to return to the Theme Handbook overhaul project soon", and proposed moving old classic docs into the Classic Themes chapter first. @bijayyadav agreed. The current tree has 59 pages under `/classic-themes/` (TH01), so that move happened.
- In 2026 he has only commented on the tracker: [#2170](https://github.com/WordPress/Documentation-Issue-Tracker/issues/2170), 2026-01-27, on the accessibility section, and #816, #1357, #1414, #1634, #1635 and #2113 updated 2026-04-07/13.
- On [#816](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816), 2025-04-09, @carolinan wrote: "none of us can answer if Automattic is going to change their contribution hours back."

**Conclusion for the proposal.** Name Justin as the content owner and lead CODEOWNER, and Cheyne as the second maintainer, after confirming both. Include @kafleg, @poena (carolinan) and @utz119 (TeBenachi) as the Docs-listed Theme Handbook reps. The owner says there is "a trusted maintainer in charge"; every signal points at Justin, but confirm before naming anyone in public.

### 1.4 How an edit gets in today

1. Someone files an issue in the Documentation Issue Tracker with the `themes` label (the bot adds `developer documentation (DevHub)` and pings @kafleg and @TeBenachi). Some reports go to **Meta Trac** instead (component *Handbooks*): [#8011](https://lists.wordpress.org/pipermail/wp-meta/2025-June/) and #8012 (tomd6r, 2025-06, theme.json examples; status `new`, no owner, per the last list message).
2. The fix is proposed as text in the issue, or, for new pages, drafted in **Google Docs**. That was the overhaul's [Phase 2 method](https://make.wordpress.org/themes/2023/05/17/theme-handbook-overhaul-phase-2-creating-content/): "it will eventually need to be added manually to the Theme Handbook".
3. Someone with wp-admin access (Justin until 2024, chekle in 2026) retypes it into the block editor and closes the issue. The Docs role page: "Updating the page in the handbook is usually done by one of the project reps or active contributors who have access to the dashboard … Consistent contribution over time … can result in giving you access".

Justin described this on Meta #7520, [comment 19, 2024-08](https://lists.wordpress.org/pipermail/wp-meta/2024-August/059896.html): "The current process is overly complicated and requires first filing a ticket … Then, manually writing fixes in the ticket, which have to be transferred elsewhere. For new handbook pages, they are generally written in Google Docs to be reviewed. Then, they have to be migrated to WordPress."

**Credits today.** There is no per-article changelog. A REST scan of all 139 pages found 0 headings named Changelog, Credits or Contributors, which differs from HelpHub (R05 §1.3). There is one handbook-wide [Credits page](https://developer.wordpress.org/themes/credits/) with 93 `@username` entries, last modified 2023-12-14. The DevHub theme autolinks `@names` on it: `DevHub_Handbooks::autolink_credits()` applies to `is_single( 'credits' )` (themes handbook) in [`inc/handbooks.php`](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/handbooks.php). Credit is therefore manual, and so is the Docs badge (§3.3).

---

## 2. Recent history (2023 to 2026)

| Date | Event | Driver | Source |
|---|---|---|---|
| 2023-02-27 to 03-06 | Personal repo `justintadlock/theme-handbook`: chapter analyses for an overhaul (Markdown notes, not content) | Justin | [repo](https://github.com/justintadlock/theme-handbook) |
| 2023-04-04 | **Theme Handbook Overhaul Proposal** on make/themes; outline in Google Docs; feedback period to 2023-04-28; meetings 04-11 and 04-18 in #themereview | Justin | [post](https://make.wordpress.org/themes/2023/04/04/theme-handbook-overhaul-proposal/) |
| 2023-05-01 | Tracking issue [#816](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816) opened (still open) | Justin | GitHub |
| 2023-05-17 | Phase 2 (Creating Content): "Source of truth: GitHub ticket"; content drafted, then "added manually" | Justin; props @poena, @kafleg | [post](https://make.wordpress.org/themes/2023/05/17/theme-handbook-overhaul-phase-2-creating-content/) |
| 2023-09-15 | Phase 3 (Publishing Content), chapter by chapter | Justin | [post](https://make.wordpress.org/themes/2023/09/15/theme-handbook-overhaul-phase-3-publishing-content/) |
| 2024-01-11 | Progress post: five chapters published in 2023; target "end of Quarter 2 (June 30) of 2024" | Justin | [post](https://make.wordpress.org/themes/2024/01/11/new-block-focused-theme-handbook-docs-and-whats-coming-in-2024/) |
| **2024-01-11** | On #816, @javiercasares offers to move the handbook to a GitHub repo "like the plugin one". Justin: "I'd love to have a dedicated GitHub repo for managing this … something @richtabor and I recently discussed … I'm personally fine helping to move the content over to Markdown"; CCs @kafleg and @carolinan. Javier points to Meta #7358 and #7361 (the plugin handbook syncs). | Javier, Justin | [#816 comments](https://github.com/WordPress/Documentation-Issue-Tracker/issues/816) |
| 2024-03 to 04 | Meta #7520 "Move Handbooks to GitHub to ease ability to contribute content"; @dd32's objection (R05 §2.3); @zieladam prototypes a Playground docs workflow (comment 16) | flexseth, dd32, zieladam | [wp-meta 2024-04](https://lists.wordpress.org/pipermail/wp-meta/2024-April/058002.html) |
| **2024-08-30** | On #816, @t-hamano asks for GitHub management and explains the Japanese fork-and-translate workflow. Justin replies "I'd love that too" and links #7520. Justin's #7520 comment 19 (quoted in §1.4) asks specifically for the Theme Handbook. @wildworks (t-hamano) posts the Japanese workflow on #7520. | Justin, t-hamano | [#7520 c19](https://lists.wordpress.org/pipermail/wp-meta/2024-August/059896.html), [wp-meta](https://lists.wordpress.org/pipermail/wp-meta/2024-August/059957.html) |
| 2024-12-25 | Japanese translation paused: "the content and structure of the original have changed significantly" | ja team | [ja handbook](https://ja.wordpress.org/team/handbook/theme-development/) |
| 2024-12-30 | Themes year review: "The Block Theme focus handbook is ready" | KafleG | [post](https://make.wordpress.org/themes/2024/12/30/a-year-in-themes-team-2024/) |
| 2025-04-09 | t-hamano asks whether the structure will change again before the ja team translates. carolinan: no information; depends on Automattic contribution hours. | — | #816 |
| 2025-08-26 | Justin proposes moving old docs into the Classic Themes chapter first, then iterating | Justin | [notes](https://make.wordpress.org/themes/2025/08/27/themes-team-meeting-notes-for-august-26-2025/) |
| 2026-01-27 | @amberhinds offers to write the accessibility section ([#2170](https://github.com/WordPress/Documentation-Issue-Tracker/issues/2170)); Justin notes it was an agreed condition of #816 | — | GitHub |
| 2026-05 to 07 | chekle's fix-up batch (21 issues closed, 18 pages modified) | chekle | §1.3 |

There is no make/themes or make/docs post after August 2024 about GitHub or Markdown for the Theme Handbook (REST search of make/themes posts for "github" and "markdown", 2026-10-12). No issue or post records a decision *against* the move. It stalled because nobody owned the Meta side, and #7520 became a general "all handbooks" debate instead of a scoped request.

---

## 3. Precedent playbooks

### 3.1 Comparison (measured 2026-10-12)

| | **AAH** [WordPress/Advanced-administration-handbook](https://github.com/WordPress/Advanced-administration-handbook) | **SCF docs** [WordPress/secure-custom-fields `docs/`](https://github.com/WordPress/secure-custom-fields/tree/trunk/docs) | **Coding Standards** [WordPress/wpcs-docs](https://github.com/WordPress/wpcs-docs) | **A11y team handbook** [WordPress/accessibility-team-handbook](https://github.com/WordPress/accessibility-team-handbook) (in progress) |
|---|---|---|---|---|
| Owner | Docs + Hosting | SCF plugin maintainers (Automattic) | Core / WPCS | Accessibility team |
| README / CONTRIBUTING | README with style links only; no contribution section; no CONTRIBUTING | `docs/contributing/index.md` + `documentation.md` (generic) | README only | README |
| CODEOWNERS | none | none | none | none **[checked root and .github]** |
| PR template | none | yes, with AI-use disclosure ([template](https://github.com/WordPress/secure-custom-fields/blob/trunk/.github/pull_request_template.md)) | none | — |
| CI for docs | none | `docs-manifest.yml` fails a PR with a stale manifest | `qa.yml` | none |
| Props | none | `props-bot.yml` (WordPress Props Bot) | none | none |
| Branch rules visible to the public | org-wide deletion/force-push rules only; classic protection exists (`protected=true`), required reviews not visible **[unverified]** | same | same | — |
| Labels | `contributorday`, `WCUS26`, `WCAsia2026`, `documentation`, `needs reviewers` … | `[Status] *`, `[Type] *`, `documentation`, `good first issue`, `props-bot` | — | — |
| Issues | repo issues **and** the Doc tracker `advanced administration` label | repo issues | repo issues | repo issues |
| PR volume | 262 PRs: 197 merged, 54 closed, 11 open (oldest 2026-02-06) | 16 docs-only merged PRs, 2025-02-20 to 2026-06-24 (39 PRs touch docs) | — | 20 issues/PRs since 2025 |
| Time to merge | median 0.7 d overall; **34.0 d for last 50; 37.7 d for 2026 (n=33), p75 103 d** | docs-only median **~15 min**, p75 3.6 d; 11 of 16 self-merged | — | — |
| Who merges (2025+) | kittenkamala (Amy Kamala) 21, mindctrl (John Parris) 13, javiercasares 7, chaion07 4, zunaid321 4; self-merge 1 of 58 | kraftbj 10, cbravobernal 3, priethor 2, ockham 1 | — | rianrietveld |
| "Edit" link on live page | `…/edit/main/<path>.md` and `…/commits/main/<path>.md` | `…/edit/trunk/docs/<path>` | `…/edit/master/<path>` | not live yet |

Sources: `gh pr list` and `gh api` pulls of each repo; live page HTML for the edit links (for example [AAH backup](https://developer.wordpress.org/advanced-administration/security/backup/) and [SCF welcome](https://developer.wordpress.org/secure-custom-fields/welcome/)).

### 3.2 What each teaches

- **AAH: the process works, but review decays.** It runs on volunteers who merge other people's PRs, with almost no self-merges, Contributor-Day labels and no written rules. The 2026 median of 38 days is the cost of having no CODEOWNERS, no SLA and no named second reviewer. Its README does not explain how non-GitHub users contribute. The 2023 status post points them to "A GitHub account … connect it to your WordPress account" plus a Markdown quick reference (R05 §5).
- **SCF: the fastest loop, because maintainers self-merge docs.** That fits a plugin repo with a small trusted team. For a community handbook, the Docs team's gatekeeping norm (R05 §1.2) makes unreviewed self-merge by *non*-maintainers unacceptable. Self-merge *by the trusted maintainer* is exactly the "fast path" the owner wants, and SCF shows it is accepted practice. SCF also has the two CI pieces worth copying: the manifest staleness check and Props Bot.
- **Accessibility team handbook: the freshest precedent, still not finished.** The repo was created 2025-08-05 in the `wpaccessibility` org and transferred to `WordPress` around 2026-09-14 (issues #12 and #13). @coffee2code opened ["Prepare manifest for import"](https://github.com/WordPress/accessibility-team-handbook/issues/15) and ["Content considerations before initial import"](https://github.com/WordPress/accessibility-team-handbook/issues/16) on 2026-09-21, with wrong `markdown_source` URLs after the transfer, null parents, a stale page and slug changes needing redirects. The [2026-09-30 update](https://make.wordpress.org/accessibility/2026/09/30/wp-a11y-docs-update-september-2026/) says "@coffee2code is helping … hopefully get the migration … finished" in October. As of 2026-10-12 the live make/accessibility handbook shows no GitHub edit links, so it is not imported yet. This is the AAH lesson again: **the first import fails on manifest details; generate and validate the manifest in CI, and point `markdown_source` at the final org URL from day one.**
- **The plugin handbook mirror** (R03 §9): created 2023-11-12, still merging PRs (latest 2026-10-07 by ernilambar), live site not importing it. R05 cites a 2024 report that syncing "broke"; R03 found no import today. Either way, the outcome is a GitHub copy that contributors edit and readers never see. On [#7361](https://lists.wordpress.org/pipermail/wp-meta/2024-January/056994.html) dd32 suggested the name `plugin-developer-handbook`, and the ticket shows no resolution in the list archive.

### 3.3 Props, credit and the Documentation Contributor badge

- The Docs [profile badge page](https://make.wordpress.org/docs/handbook/get-involved/documentation-team-profile-badge/) (modified 2026-04-23) lists "Fix an article/page (… DevHub …)" and "Create a PR for Gutenberg docs" as qualifying. Recognition is **manual**: "use the Submit Your Contributions form in the right-hand sidebar … Submit the form each time you contribute." Project leads "decide what is the minimum criteria". The Docs team is reconsidering recognition generally ([Rethinking Contributor Recognition](https://make.wordpress.org/docs/2025/11/04/rethinking-contributor-recognition-in-documentation-team/), Estela, 2025-11-04).
- GitHub activity on WordPress-org repos (issues opened/closed, PRs submitted/merged) appears on profiles.wordpress.org once a GitHub account is linked. Sources: [WP Tavern](https://wptavern.com/wordpress-org-profiles-now-show-activity-for-contributions-made-on-github) and [Linking your GitHub and w.org profiles](https://make.wordpress.org/core/handbook/tutorials/linking-your-github-and-w-org-profiles/). That gives visibility, not the badge. **[2020-21 sources; current behaviour not re-verified]**
- Implication: a Theme Handbook repo should (a) run Props Bot as SCF does, (b) say in the README and PR template that contributors should link their GitHub account and submit the Docs form, or have a maintainer batch-submit merged authors monthly, and (c) keep the handbook-wide `credits.md` as a plain `@username` list, which the existing `autolink_credits()` will keep linking provided the slug stays `credits`. Since the Theme Handbook has no per-article changelog, nothing is lost by not adding one.

---

## 4. The proposal path

### 4.1 Steps, owners, and realistic durations

| # | Step | Who | Precedent and timing |
|---|---|---|---|
| 0 | Pre-wire privately: confirm the trusted maintainer (Justin) and the 2026 editor (chekle) want this, and agree CODEOWNERS | project owner | — |
| 1 | **Proposal on make/themes**, tag `#theme-documentation` (the 2023 overhaul tag), x-posted to make/docs and make/meta. State: one-to-one conversion, no structural change, who maintains, how wp-admin is locked, translation impact. Two-week comment window plus an agenda item at a Themes meeting (Tuesdays 15:00 UTC, #themereview / #themes) and a Docs meeting (Tuesdays 14:00 UTC, #docs). | Justin as author or co-author (it should come from the owner, not an outsider) | 2023 overhaul: 24-day comment window ([post](https://make.wordpress.org/themes/2023/04/04/theme-handbook-overhaul-proposal/)). The reverted block.json PR (R05 §4) shows the cost of skipping this. |
| 2 | **Meta Trac ticket**, component *Developer Hub*: "Devhub: Import Theme Handbook from GitHub". Reference #7520 comment 19 and say explicitly that this is the scoped, owner-requested case, not "all handbooks". | Justin or the project owner | SCF [#7917](https://lists.wordpress.org/pipermail/wp-meta/2025-February/061132.html) (kraftbj, 2025-02-20) |
| 3 | **Repo in the WordPress org**: create it directly, or build it in a personal repo and transfer. Needs an org owner. Must meet the [repo criteria](https://make.wordpress.org/project/2025/06/04/criteria-for-creating-or-migrating-repositories-under-the-wordpress-github-organization/) (2025-06-04): maintainer from an established team in README and CODEOWNERS, problem statement, make-blog tag. | org owner (dd32 transferred AAH in 2022, R05 §5) **[current org owners unverified]** | A11y: transfer around 2026-09-14; then the manifest had to be rewritten for the new URL |
| 4 | **Content PR**: the converted 139 files plus the generated manifest, reviewed by the maintainer page by page or by diff report | project owner (conversion); Justin and chekle (review) | — |
| 5 | **Importer PR** to [WordPress/wporg-developer](https://github.com/WordPress/wporg-developer): a `DevHub_Theme_Handbook` subclass like [`import-scf.php`](https://github.com/WordPress/wporg-developer/blob/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-scf.php) (35 lines). The existing CPT is `theme-handbook`, registered through `devhub_handbook_post_types` (`[ 'apis', 'plugin', 'theme' ]`). The importer must target that CPT and base so that existing posts are **adopted** (same IDs, URLs, old-slug redirects) rather than duplicated (R02 row "match by key or slug"; R04 §F/G; TH01 §(e)). Only `publish` posts count as existing, so drafts and private pages need a decision. | project owner writes it; a Meta committer reviews and merges | SCF #547: opened and merged 2025-02-20 by dd32. Playground #569: 2026-06-18 → 2026-07-15, self-merged by akirk. |
| 6 | **Deploy and first import** on a sandbox, then production; verify adoption on a few pages; trash nothing | Meta committer with dotorg deploy rights (R05 §3.2) | AAH first import 2023-03-28 needed dd32 to fix the manifest |
| 7 | **Lock wp-admin editing** for `theme-handbook` (capability filter in `handbooks.php` or the subclass), and update the Feedback page, the Docs role page, the Themes "Projects" page and the tracker bot | Meta committer; Docs and Themes reps for the pages | none: no precedent locks editing (see §5.1) |
| 8 | Announce on make/themes and make/docs; update #816 | Justin | AAH announcement 2023-04-10 |

**Realistic calendar:** if the maintainer co-authors the proposal and a Meta committer is lined up before posting, about 4 to 8 weeks (2 weeks of comments, 1 to 2 weeks of review, a few days for importer review and deploy). Without a named committer, it becomes the AAH/#7520 pattern: months. **[estimate]**

### 4.2 Who must say yes, and who does work

| Person | Role | Why they matter | Signal so far |
|---|---|---|---|
| **Justin Tadlock** (@greenshady / justintadlock) | Themes rep; author of the current handbook | Content owner; proposal author; lead CODEOWNER | Asked for GitHub publicly (2024-01-11, 2024-08) |
| **Cheyne** (@chekle, wp.org slug **[unverified]**) | Automattic; 2026 handbook editor | Second maintainer; most current editing practice | 21 `themes` closures in 2026 |
| @bijayyadav, @fahimmurshed | Themes reps | Team sign-off | Agreed with Justin's 2025-08 classic-docs plan |
| @kafleg (Ganga Kafle) | Docs "Theme Handbook Rep"; Themes posts author; bot-pinged | Docs-side sign-off; reviewer | Reviewed all overhaul posts (2023-24); CC'd on the 2024 GitHub idea |
| @poena (Carolina Nymark, `carolinan`) | Docs "Theme Handbook Rep"; core committer | Reviewer; credibility with core | Active on #816; suggested automation for docs in 2024 (R05 §1.5) |
| @utz119 (`TeBenachi`) | Docs "Theme Handbook Rep"; bot-pinged | Reviewer | 6 issues filed |
| @estelaris, @milana_cap, @atachibana, @kenshino | Docs reps | Docs team acknowledgement; tracker changes; Docs is moving *toward* writing in WordPress for HelpHub (R05 §1.4), so frame this as a developer handbook, like AAH | Milana co-led the AAH move |
| **@dd32** (Dion Hulse) | Meta lead; Meta Janitor; 7 wporg-developer commits since 2025 | Most likely reviewer and deployer; author of the #7520 objection, which he scoped to non-code content. Developer docs are his stated "works great" case. | Merged SCF importer the same day |
| **@coffee2code** (Scott Reilly) | Meta rep; 11 wporg-developer commits since 2025 (most of anyone) | Currently doing the a11y handbook import; knows the manifest pitfalls | Active on exactly this work in 2026-09 |
| @obenland (8 commits), @tellyworth (Meta rep) | Meta | Alternate reviewer and deployer | — |
| @akirk (Alex Kirk) | Wrote the Playground importer and self-merged it in 2026 | Proof that a non-Meta-lead can land an importer; possible reviewer **[Meta commit/deploy rights unverified]** | — |
| Japanese locale team: @t-hamano (wildworks), mkismy, stein2nd, miminari | Translators | Downstream consumers; supporters | Asked for GitHub in 2024 |

**Meta Janitors** ([2026-04-23](https://make.wordpress.org/meta/handbook/about/projects/meta-janitors/), R05 §3.2) includes dd32 and is told to "explore tighter integration between WordPress.org and version-controlled workflows". That is a good fit, but no Janitors-specific posts were found on make/meta in 2026 (REST search, 2026-10-12). Treat it as an argument in the ticket, not as a channel. The Docs team's 2026 priorities are HelpHub issue triage, release docs and recognition (R05 §1.5). The Theme Handbook is not competing for their capacity, which helps; ask them for acknowledgement, not work.

---

## 5. Repo design decisions the proposal must settle

| Decision | Options | Recommendation | Why |
|---|---|---|---|
| **Name and org** | `WordPress/theme-handbook` (matches `jawordpressorg/theme-handbook` and Justin's 2023 repo); `WordPress/theme-developer-handbook` (the landing-page intro and the Themes team page call it the "Theme Developer Handbook", though the page title is "Theme Handbook"; dd32's 2024 naming suggestion for the plugin equivalent was `plugin-developer-handbook`); `developer-themes-handbook` (mirrors `developer-plugins-handbook`) | `WordPress/theme-developer-handbook` as first choice, `theme-handbook` acceptable; let Meta pick in the ticket | Naming has been a Meta comment before (#7361). The ja team's repo name does not depend on ours. |
| **Default branch** | `trunk` / `main` | `trunk` | The importer has supported any branch since 2022-10-13 (Meta #6538; see the [`wporg-markdown` history](https://github.com/WordPress/wordpress.org/commits/trunk/wordpress.org/public_html/wp-content/plugins/wporg-markdown/inc/class-editor.php)); matches Gutenberg, SCF and Playground |
| **Merge rights** | Themes team only; Docs only; a named group | GitHub team `theme-handbook-maintainers` with write access: Justin, chekle, kafleg, carolinan, TeBenachi. The Documentation GitHub team gets triage. | Matches "shared between Themes and Docs" while keeping a small gate, as the Docs team keeps for HelpHub (R05 §1.2) |
| **CODEOWNERS** | none (AAH); per-chapter | `* @justintadlock @chekle` at minimum; optionally `/global-settings-and-styles/ @…` for theme.json experts | Required by the repo criteria; AAH's lack of it correlates with 34-day reviews |
| **Branch protection** | none; 1 review; 2 reviews (Hosting team) | Require 1 approving review from a CODEOWNER, the manifest check passing, no force push. Allow admins (the maintainers) to bypass. | Bypass is the trusted-maintainer fast path. GitHub records bypasses, so it stays auditable. |
| **Maintainer fast path** | self-merge allowed for typos only; for anything | Maintainers may self-merge their own PRs (as SCF does, 11 of 16 docs PRs). Others need one maintainer review. State a **7-day first-response SLA**. | The owner asked for one. It mirrors annezazu's "tiered system" idea (R05 §1.4). |
| **Non-GitHub contributors** | as AAH (GitHub account required); paste text in an issue | Keep the **issue-comment path**: anyone can propose text in an issue, and a maintainer opens the PR with `Co-authored-by` so Props Bot credits them. Also document the "Edit" pencil (web editor, auto-fork). | Keeps today's lowest-barrier path. Answers dd32's "isn't accessible to all". |
| **Issues** | repo issues only; tracker only; both (AAH) | Enable repo issues; **transfer** the 73 open `themes` issues from the tracker in one batch (GitHub issue transfer works within an org for users with write access to both repos and keeps comments). Afterwards, the tracker's `themes` label points to the repo through a pinned notice plus an issue template link. | Splitting intake (AAH has 33 tracker issues and repo issues) is a known source of drift. 17 of the open issues are overhaul tasks that belong next to the content. |
| **Issue transfer caveat** | — | Re-create labels `themes`, `new document`, `tracking issue` in the new repo first so they carry over; keep #816 as the umbrella. **[transfer label behaviour per GitHub docs; not tested here]** | — |
| **CI** | none (AAH) | (1) Regenerate the manifest and fail if stale (SCF `docs-manifest.yml`); (2) slug, duplicate and parent validation (R04 §N, a11y #15); (3) link check; (4) Props Bot | The first import failures in AAH and a11y were all manifest errors |
| **PR template** | none | SCF's, plus "Linked issue", "Pages touched", and the Docs form link for credit | — |
| **Credits** | keep `credits.md`; generate it | Keep `credits.md` with slug `credits`; a maintainer appends merged authors at release time **[or a script from `git shortlog`; optional]** | `autolink_credits()` depends on the slug |
| **Release-gated docs** | branch; merge on release day | Merge on release day (this handbook has no release-day publishing ritual today; only 5 pages have a 2025 `modified` date) | The Block Editor importer tracks trunk only (R05 §4) |
| **Deletions and redirects** | — | A `REDIRECTS.md` or redirect-map file in the repo; removals done by a Meta committer on request | The importer never deletes (R04) |
| **Archiving** | — | Name two maintainers so the 6-month inactivity archiving rule never triggers | Repo criteria |

### 5.1 wp-admin after cutover: the decisive question

What the code does today (`wporg-markdown/inc/class-editor.php`, last change 2026-09-11):
- `render_editor_warning()` shows an admin notice: **"This page is maintained on GitHub. Content, title, and slug edits here will be discarded on next sync."**
- `redirect_edit_link_to_github()` changes front-end "Edit" links to GitHub, but only when not `is_admin()`.
- Nothing removes the capability. The importer skips unchanged files (ETag, R04), so a wp-admin edit **survives until someone next changes that page's Markdown**, and is then silently lost. Divergence can last for months on a handbook where only 5 pages carry a 2025 `modified` date.

Options:

| Option | Effect | Recommendation |
|---|---|---|
| A. Leave editing on, rely on the warning | Same failure mode as the plugin mirror, inverted: hand-fixes vanish later | No |
| B. Remove `edit_posts` for `theme-handbook` from `handbook_editor` and editors (keep it for admins) through a `map_meta_cap` filter in the subclass | wp-admin fixes become impossible; everything goes through Git | **Yes**, announced in the proposal |
| C. B plus a nightly check comparing rendered post content to the last import and alerting #docs | Detects admin edits and failed imports (the Code Reference's two-year silent stall, R05 §3.4) | Yes, if a committer will host it **[no precedent]** |

Cutover order: freeze wp-admin edits (announce a date) → final export and conversion → merge the content PR → first import adopts the posts → apply the lock → transfer issues. Any edit made between export and lock must be re-applied in Git; the freeze window should be days, not weeks.

---

## 6. Translation impact

- **GlotPress:** none. `translate.wordpress.org/projects/meta/` sub-projects are browsehappy, contributor-toolkit, forums, get-involved, learn-wordpress, o2, openverse, p2-breathe, pattern-directory, plugins, rosetta, themes (directory UI), wordcamp, wordpress-org, wp15 and wp20. There is no DevHub or handbook content project (fetched 2026-10-12). developer.wordpress.org has no locale variants.
- **Rosetta:** only **Japanese**, at [ja.wordpress.org/team/handbook/theme-development/](https://ja.wordpress.org/team/handbook/theme-development/), authored by Naoko Takano, first published 2021-09-06. Its landing page says translation is "paused as of 2024-12-25" because the source changed. Source files: [jawordpressorg/theme-handbook](https://github.com/jawordpressorg/theme-handbook) (created 2021-09-05, **139 `.md` files**, mirroring the current English tree including `classic-themes/` and `credits/feedback`). Translators comment out the English paragraph and add Japanese below it, using textlint with `textlint-rule-preset-wp-docs-ja`. Active in 2026: stein2nd (140 commits), miminari (45), t-hamano (12), mkismy (6). Issue #318 "原文の更新" ("updating the source text"), opened 2026-07-25, is open. Spot checks of es, fr, de, it, br, cn, ko, ru, tr, id and nl `/team/handbook` found no Theme Handbook copy. Unofficial personal translations exist (for example `66beta/theme-handbook-zh`, 2025-04) and are out of scope.
- **Impact, stated honestly:**
  - English-only move; no translation tooling promised. Rosetta HelpHub copies (R05 §6) are unaffected, since this is a different handbook.
  - The one active translation benefits. A Git source gives the ja team per-file diffs ("easier to detect differences when merging updates made upstream", t-hamano, #816, 2024-08-30), and a one-to-one conversion **keeps their 139-file mapping valid**. Their paths already match the English URL tree.
  - Risk to them: the converter's Markdown will not be byte-identical to their hand-converted English. Their next "update source" pass will show noise on every file. Mitigation: tell them before cutover, publish the commit that represents "conversion only", and offer a path mapping file.

---

## 7. Risks and mitigations

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| 1 | **Dual source of truth after cutover** (wp-admin edits persist, then vanish) | High if not addressed | Option B or C in §5.1; freeze window; update every "how to contribute" page the same day |
| 2 | **Meta capacity**: no committer picks up the ticket; #7520 has been idle since 2024-08 | Medium | Line up dd32 or coffee2code *before* posting; write the importer PR ourselves (SCF pattern); scope the ticket to one handbook; cite Justin's #7520 comment |
| 3 | **dd32's #7520 objection reused** ("isn't accessible to all", WP as source of truth for multilingual) | Medium | This is developer docs, his "works great" case; keep the issue-comment path for non-GitHub users; show the only translation team *asked* for GitHub |
| 4 | **Maintainer bandwidth** (Automattic-sponsored people; carolinan's 2025-04 remark; AAH's 34 to 38 day reviews) | Medium-high | Two named CODEOWNERS, maintainer bypass, 7-day SLA, Contributor-Day labels, monthly triage note at the Themes meeting |
| 5 | **First import breaks** (manifest slugs, parents, `markdown_source` URLs; duplicate posts if the base or CPT mismatches) | Medium | CI manifest validation; dry run on a sandbox; build in the final org repo from the start (a11y #15 lesson); match the `theme-handbook` CPT base exactly (R04 §152) |
| 6 | **Drafts and private pages lost** (importer only adopts `publish`; e.g. the "Private: Pattern Directory page" in #868) | Low-medium | Inventory non-published `theme-handbook` posts with an admin before conversion **[count unknown without auth]** |
| 7 | **Seen as a structural rewrite** (the ja team paused in 2024 over structure churn; the 2023 overhaul was large) | Medium | Lead the proposal with "no URL, title or order changes"; publish a URL diff showing zero changes |
| 8 | **Intake fragmentation** (tracker, Meta Trac *Handbooks*, repo issues) | Medium | Transfer the open `themes` issues; template pointer in the tracker; close or redirect #8011 and #8012 |
| 9 | **Docs team reads it as Themes taking the handbook** (2025 morale context, R05 §1.1) | Low-medium | Make the Docs Theme Handbook reps maintainers; x-post to make/docs before posting; badge path unchanged |
| 10 | **Silent import stall** (Code Reference precedent) | Low-medium | Show "last imported commit" on pages or alert on stale imports **[needs Meta]** |

---

## 8. Questions to put to the trusted maintainer and the Themes team

**To the maintainer (Justin) and chekle**
1. Do you still want the GitHub move you asked for on #816 (2024-01-11) and #7520 (2024-08)? Will you author or co-author the make/themes proposal?
2. Who are the CODEOWNERS (you, chekle, others)? Do you want a self-merge bypass for all your PRs or only small ones?
3. Who currently holds `handbook_editor` on developer.wordpress.org for this handbook? Are any pages in draft or private status that must survive?
4. Are you comfortable with wp-admin editing being **locked** after cutover, including for yourselves?
5. Repo name: `theme-developer-handbook` or `theme-handbook`?
6. Should the 73 open `themes` issues move to the new repo, and should #816 stay the umbrella?
7. Is a release-day publishing need coming (for example, theme.json changes in 7.x) that requires a release branch?

**To the Themes team (reps @bijayyadav, @fahimmurshed; plus @kafleg)**
8. Does the team agree the handbook stays jointly owned, with merge rights for a named Themes and Docs group?
9. Who besides Justin will commit to reviewing PRs within 7 days?
10. Should the stale make/themes "Projects → Theme Developer Handbook" entry (leads @acalfieri, @aristath, Trello) be replaced by the repo link?

**To the Docs team (Theme Handbook reps @kafleg, @poena, @utz119; reps @estelaris, @milana_cap)**
11. Is moving the `themes` intake from the tracker to the repo acceptable, and will the bot ping the new maintainers?
12. How should merged PRs count for the Documentation Contributor badge: form submission, a monthly maintainer batch, or Props Bot output?

**To Meta (@dd32, @coffee2code)**
13. Will one of you review the importer PR and run the first import? Should it be a new DevHub ticket or a reopened #7520 scope?
14. Is a capability lock on an imported handbook CPT acceptable as a pattern, or is the warning notice considered enough?

**To the Japanese locale team (@t-hamano, @mkismy)**
15. Would a one-time "conversion only" commit plus a path map make the next source sync manageable?
