# Make front page: team list and "Next meeting" (and why Core AI shows none)

Researched 2026-10-14. Read-only. Live data captured that day from make.wordpress.org; code read from shallow clones of
`WordPress/wporg-make` @ `053e36d` (2026-09-04), `WordPress/meeting-calendar` @ `20c0fa6` (2026-10-13), and the
`WordPress/wordpress.org` Meta mirror @ `cfb6461` (2026-10-14). Raw captures are in the session scratchpad
(`make-meetings/live/`: `front.html`, `all.json` = all 226 meeting posts, `make_site.json`, `meetings.html`, `ai.html`).

## TL;DR

The Core AI meetings **do exist** as meeting posts and are live on <https://make.wordpress.org/meetings/>. They are missing
from the front page because of a **team-name mismatch**: the front-page card asks for meetings whose `team` meta equals
the card's post title, **"Core AI"**, but both AI meeting posts have `team` = **"AI"**. No other cause (expiry, cache,
missing post) applies. Fix: change `team` on meeting posts 5179 and 5244 to `Core AI` (a wp-admin edit, no deploy), or
add a `Core AI` to `AI` alias in the shortcode the way `Documentation` is already aliased to `Docs` (Meta deploy).

## 1. How the front-page team list is produced

- **Theme:** `wporg-make-2024` in [WordPress/wporg-make](https://github.com/WordPress/wporg-make), `source/wp-content/themes/wporg-make-2024/`.
- `patterns/front-page-content.php` holds a core **Query Loop** over the `make_site` post type, sorted by date ascending:
  `<!-- wp:query {"query":{"perPage":100,"postType":"make_site","order":"asc","orderBy":"date"}, "className":"wporg-make-team-list"} -->`
  Each item renders the template part `parts/card-team.html`, which has three columns: `core/post-title` (linked),
  `core/post-content` (the blurb), and the theme's own block `<!-- wp:wporg-make/meeting-time {"fontSize":"extra-small"} /-->`.
- **Data source:** the `make_site` CPT on the make.wordpress.org main site, registered by
  `wordpress.org/public_html/wp-content/plugins/wporg-make-sites-cpt/make_sites_cpt.php` ([mirror](https://github.com/WordPress/wordpress.org/blob/trunk/wordpress.org/public_html/wp-content/plugins/wporg-make-sites-cpt/make_sites_cpt.php)).
  One post per team: title (the team name), content (blurb), and meta `make_site_id` (the network blog ID, used to make the
  permalink in `functions.php` `replace_make_site_permalink()`). The CPT also has legacy meta `weekly_meeting`,
  `weekly_meeting_when`, and `weekly_meeting_where`, which **the current theme doesn't read** (grep finds no use).
- The list is public over REST: `GET https://make.wordpress.org/wp-json/wp/v2/make_site?per_page=100` returns 24 items. The Core AI item is
  **post 5173, title "Core AI"**, slug `core-ai`, created 2025-05-30, link `https://make.wordpress.org/ai/`.
- Adding a team card is a super-admin or Meta task (Meta handbook, [Setting Up New Make Sites → Icons, Home, etc](https://make.wordpress.org/meta/handbook/tutorials-guides/setting-up-new-make-sites/): "add a new 'site' to WordPress.org").

## 2. How "Next meeting" is computed and rendered

**Fully server-rendered PHP.** The page makes no REST or JS fetch for this. The only JS is `time-conversion.js`, which rewrites the
`<time class="date">` text into the visitor's local time zone after load.

### The block (theme): passes the card's post title as the team
`src/meeting-time/index.php`:
```php
$post_id = $block->context['postId'];
$team = get_post_field( 'post_title', $post_id );
$meeting_time = call_user_func( $shortcode_tags['meeting_time'], array( 'team' => $team ), '', 'meeting_time' );
```
So **the team key is the `make_site` post title, verbatim** (e.g. "Core AI", "Core Performance", "Documentation").

### The shortcode (Meta plugin): exact meta match on `team`
Plugin `wporg-meeting-posttype` ("WPORG Make Homepage Meeting Post Type" v2.0) in the Meta mirror
`wordpress.org/public_html/wp-content/plugins/wporg-meeting-posttype/class-meeting-post-type.php`. It's identical to
`includes/class-meeting-post-type.php` in [WordPress/meeting-calendar](https://github.com/WordPress/meeting-calendar), which
supplies the admin UI, the calendar block, REST routes, and the ICS feeds. `meeting_time_shortcode()`:
```php
if ( 'Documentation' === $attr['team'] ) {
    $attr['team'] = 'Docs';                     // the only alias that exists
}
switch_to_blog( get_main_site_id() );           // meetings live on the make.wordpress.org main site
$query = new WP_Query( array(
    'post_type'  => 'meeting',
    'nopaging'   => true,
    'meta_query' => array( 'relation' => 'AND',
        array( 'key' => 'team', 'value' => $attr['team'], 'compare' => 'EQUALS' ),
        $this->meeting_meta_query(),            // "not ended" filter, below
    ),
) );
// limit=1: print the first post (sorted by next occurrence), plus "(+N more)" = found_posts - 1,
// linking to /meetings/#<strtolower(team)>
```
- **Matching rule:** an exact string compare of the meta value. The DB collation makes it **case-insensitive in practice**
  (verified: the Core card shows "Core Privacy office-hour" (+5 more), and its 6 active meetings mix `team` = `Core` and `core`).
  Spacing and wording must match exactly. There is no taxonomy or slug. `team` is a free-text field in the wp-admin meta box
  (`meeting-calendar/includes/class-admin.php`, `<input type="text" id="team" name="team">`).
- **"Not ended" filter**, `meeting_meta_query()`: either non-recurring with `start_date >= today (UTC)`, or recurring
  (`recurring IN (weekly, biweekly, occurrence, monthly, 1)`) with `end_date = ''` or `end_date >= today`.
- **Next occurrence**, `get_next_occurrence()`, runs on the `the_posts` filter (`meeting_set_next_meeting` sets `$post->next_date`;
  `meeting_sort_upcoming_meetings` then usorts by it). Times are UTC. The default `after` is `-30 minutes`, so a meeting in progress still counts.
  - `weekly` / legacy `1`: start + ceil((days+1)/7) weeks
  - `biweekly`: start + 2 weeks until > now
  - `monthly`: start + 1 month until > now
  - `occurrence`: nth (1–4) or last (-1) weekday-of-start-date each month, from the `occurrence` int array, scanning up to 12 months
  - otherwise (one-off): start_date if it's still in the future
- **Cancellations:** `meeting_cancelled` post meta (multiple Y-m-d values). The shortcode then adds "This event is cancelled. The next meeting is…".
  Cancel and uncancel run through `DELETE/PUT /wp-json/wporg/v1/meetings/{id}:{date}`, gated by `current_user_can('edit_post', id)`.
- **Meta fields** (registered with `show_in_rest`, so they're visible at `/wp-json/wp/v2/meeting`): `team, start_date, end_date, time, location,
  link, wptv_url, recurring (''|weekly|biweekly|occurrence|monthly), occurrence (int[])`. The REST field `future_occurrences` covers the next 2 months.
  (The brief's `_meeting_start` / `_meeting_time` style names don't exist. The keys are unprefixed.)
- **Other consumers of the same data:** the `/meetings/` calendar (the block from meeting-calendar is server-preloaded from
  `GET /wp-json/wporg/v1/meetings/from/{Y-m-01}`, and the label is `ucwords(team)`), and the ICS feeds at `/meetings.ics` and `/meetings-{team}.ics`.
- **Caching:** the shortcode has no transient or object-cache code of its own. Core WP_Query caching (6.1+) applies, which is why
  meeting-calendar [#105](https://github.com/WordPress/meeting-calendar/issues/105) was closed as handled by core. The front page HTML is
  edge-cached (`x-nc: HIT dca 2` response header), so an edit to a meeting reaches the front page only after that cache expires. *TTL unverified.*
- I found **no Slack meeting-reminder bot** in the open Meta mirror. `common/includes/slack/*` and `api.wordpress.org/.../dotorg/slack/*`
  contain only Trac, props, announce, and a Calendly webhook. *Whether a private bot exists is unverified.*

## 3. Who can add or edit meetings, and the documented process

- `meeting` CPT has `capability_type => 'post'`, `show_ui => true` on the **make.wordpress.org main site** (not the team P2).
  The Meta handbook ([Setting Up New Make Sites → Meetings](https://make.wordpress.org/meta/handbook/tutorials-guides/setting-up-new-make-sites/)) says:
  *"Team meetings can be added to the Meeting Calendar by adding a new Meeting post on the main Make site. Users will need at least an Author role to access it."*
- [The new meeting calendar](https://make.wordpress.org/meta/2020/03/16/the-new-meeting-calendar/) (Meta, 2020-03-16): "Team reps (and anyone with access to edit meetings in wp-admin) can cancel an upcoming meeting."
- In practice, a team rep with Author+ on make.wordpress.org/ (main site) adds the post. Anyone else asks in #meta. The handbook doesn't
  say that the **Team field must equal the front-page card title** to show on the front page. That gap is the root of the Core AI issue.

## 4. Core AI diagnosis

Evidence from the live site on 2026-10-14:

| | Value |
|---|---|
| Front-page card (`make_site` 5173) title | **`Core AI`** → block calls `meeting_time` with `team="Core AI"` |
| Front-page HTML for that card | `<div class="wp-block-wporg-make-meeting-time has-extra-small-font-size"></div>` (empty) |
| Meeting 5179 "AI Team Office Hours (bi-weekly)" | `team: "AI"`, `start_date 2025-06-12`, `time 17:00`, `recurring biweekly`, `end_date ""`, `location "#core-ai"`, next `2026-10-15` |
| Meeting 5244 "AI Contributor Weekly" | `team: "AI"`, `start_date 2025-08-06`, `time 17:00`, `recurring weekly`, `end_date ""`, `location "core-ai"`, `link` Google Meet, next `2026-10-21`; **modified 2026-10-14 17:05 UTC** (someone edited it today) |
| Meetings with team "Core AI" | **0** of 226 published meeting posts |
| `/meetings/` calendar | shows both under team "AI"; `/meetings-ai.ics` returns 200 with 2 VEVENTs |

So both meetings are published, recurring, not ended, and have future occurrences. They pass every filter except
`team = 'Core AI'`. "AI" ≠ "Core AI" even case-insensitively. The team was renamed on the front-page card ("Core AI", Slack
#core-ai), but the meeting posts kept the short name "AI". Cache isn't the cause: the miss is deterministic.

**Fix options**
1. **Data-only (recommended, takes minutes):** in make.wordpress.org/wp-admin → Meetings, set Team = `Core AI` on posts **5179** and **5244**.
   Needs Author+ on the main Make site (a team rep or Meta). The front page updates after the edge cache expires. Side effects:
   the calendar label changes to "Core AI"; the hardcoded purple `.wporg-meeting-calendar__team-ai` color (meeting-calendar #194) stops
   applying and the generated fallback hue is used instead (cosmetic, unless a `team-core-ai` rule is added); the per-team ICS URL changes from `/meetings-ai.ics` to
   `/meetings-core%20ai.ics` (currently 404), so anyone subscribed to the AI feed loses it; the "+more" anchor becomes `#core%20ai`.
2. **Code alias (Meta deploy):** add `'Core AI' => 'AI'` next to the existing `Documentation` → `Docs` special case in
   `meeting_time_shortcode()` (meeting-calendar repo, and the `wporg-meeting-posttype` copy in Meta SVN). This keeps feeds and colors. A more general
   version would be a `make_site` meta field like `meeting_team` that the theme block passes instead of `post_title`.
3. Rename the `make_site` title to "AI". Not recommended, because it changes the team's public name on the front page.

Minor, also for the AI team: post 5244's `location` is `core-ai` without `#`, so even when it shows, the shortcode won't print
"accessible via #core-ai on Slack". The regex `^#([-\w]+)$` needs the `#`.

## 5. Other notable findings

Front-page cards with **no next meeting** (11 of 24): Design, Mobile, Support, Plugins, Community, Meta, Marketing, CLI,
Openverse, Core AI, Core Program. Of these, Core AI is the only **name mismatch**. The rest have no active post:
- **Community:** all 19 posts ended. The two main Team Meeting posts (3174, 3175) have `end_date 2026-08-05`.
- **Meta:** "Meta Team Biweekly Chat" (1857) ended 2026-01-01.
- **Support:** both posts ended (latest end 2025-09-01).
- **Openverse:** ended 2025-01-11.
- Design, Mobile, Plugins, Marketing, CLI, and Core Program have no meeting posts.

Other observations:
- **Teams with active meetings but no front-page card** (they show only on /meetings/): Core Passwords, DEIB Working Group (stored as both
  `DEIB Working Group` and `DEIB working group`), and GatherPress.
- **Upcoming expiries:** both Hosting posts have `end_date 2026-12-31`, so the Hosting card goes empty on 2027-01-01 unless they're extended.
- **Inconsistent data, all harmless because matching ignores case:** 44 posts use lowercase `core`, plus `themes` and `training`. Hosting 4666 has `time "0900"` (no colon). Docs 5730 is a
  one-off dated 2027-03-30.
- **Known tickets and history:** meeting-calendar [#124](https://github.com/WordPress/meeting-calendar/issues/124) "Make teams a taxonomy" closed not-planned
  in favor of [#194](https://github.com/WordPress/meeting-calendar/pull/194) (team colors). The closing comment argues the free-text team field had "no typos". The Core AI
  mismatch is a counterexample, because it's a mismatch against the *front-page* name, which the meeting plugin never checks. #105 (object caching) closed as handled by core.
  A security fix in the same area changed the theme block to call the handler directly instead of building a shortcode string from the post title
  (`WordPress/wordpress.org-security#3`). meta.trac.wordpress.org was behind a bot challenge, so Trac wasn't searched (*unverified*).
- The Core AI P2 sidebar says "The AI Team meets every other Thursday at 5:00 PM UTC" and links to /meetings/. Its weekly summary posts say "All team meeting schedules
  are published on the WordPress Meeting Calendar". So the team did register its meetings centrally, under a different name.
