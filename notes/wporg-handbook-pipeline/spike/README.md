# wporg-markdown importer spike: how to re-run

Findings: `../research/04-importer-spike.md`.

Docker wasn't available on the spike machine, so the spike ran on **native PHP 8.4 + WP-CLI + WordPress
(7.1.3) on SQLite** (sqlite-database-integration drop-in). The importer, Jetpack (16.3, for the
`WPCom_GHF_Markdown_Parser`) and the real WordPress insert, kses and render paths are all used unmodified.
`.wp-env.json` is a Docker equivalent that hasn't been tested.

## Files

| Path | What |
|---|---|
| `helphub-spike-importer/` | Test plugin: hierarchical `helphub_doc` CPT (base `/documentation/`), `HelpHub_Spike_Importer extends WordPressdotorg\Markdown\Importer` (modelled on wporg-developer `DevHub_Docs_Importer`), same cron hooks DevHub uses, `wp spike manifest|markdown|dump|kses` commands, context logging, and an opt-in link/image rewrite proof of concept (option `helphub_spike_rewrite_links`). |
| `bin/fetch_upstream.sh <dir>` | Downloads current trunk wporg-markdown + the wporg-developer import classes. |
| `bin/setup-native.sh <spike-dir>` | wp-config + install on SQLite. |
| `bin/prepare.sh <spike-dir> <project>/docs` | Installs the plugins and copies the docs `.md` files and `manifest.json` into `<spike-dir>/served`. |
| `bin/etag_server.py <dir> <port> [--no-etag]` | Static server that behaves like raw.githubusercontent.com: it sends an ETag and answers 304 on a match. |
| `bin/wpx` | `wp --path=<spike>/wp` wrapper. |
| `bin/make_fixtures.py`, `fixtures/` | Edge-case fixtures (kitchen sink, title/frontmatter cases) added to the served manifest. |
| `bin/mutate_run3.py`, `bin/mutate_run4.py` | Re-run scenarios (edit, retitle, remove, rename slug, move, reorder, index, duplicate slug, ...). |
| `bin/check.py`, `bin/audit.py`, `bin/diffdump.py`, `bin/anchors.py`, `bin/grepctx.py` | Analysis of `wp spike dump --content` output. |
| `probes/show.php`, `probes/kses.php`, `probes/srcurl.php` | `wp eval-file` probes (stored vs rendered HTML, kses state, source URL resolution). |

## Steps

```sh
S=/some/scratch/importer-spike            # copy this folder there
mkdir -p $S/wp $S/dl && cd $S/wp && php -d memory_limit=1G $(which wp) core download
cd $S/dl && curl -LO https://downloads.wordpress.org/plugin/sqlite-database-integration.latest-stable.zip \
         && curl -LO https://downloads.wordpress.org/plugin/jetpack.latest-stable.zip
cd $S/wp/wp-content/plugins && unzip -q $S/dl/sqlite-database-integration.latest-stable.zip && unzip -q $S/dl/jetpack.latest-stable.zip
bash $S/bin/fetch_upstream.sh $S/upstream
bash $S/bin/setup-native.sh $S
bash $S/bin/prepare.sh $S <project>/docs
python3 -I $S/bin/etag_server.py $S/served 8882 &      # manifest at http://127.0.0.1:8882/manifest.json
$S/bin/wpx spike manifest && $S/bin/wpx spike markdown
$S/bin/wpx spike dump --content > $S/out/run1.jsonl
python3 -I $S/bin/check.py $S/served/manifest.json $S/out/run1.jsonl $S/served
python3 -I $S/bin/audit.py $S/served $S/served/manifest.json $S/out/run1.jsonl
$S/bin/wpx eval-file $S/probes/show.php <slug> both     # stored + rendered HTML
```

Real-cron context (kses filters active, unlike WP-CLI): `cd $S/wp && php -S 127.0.0.1:8881 &` then
`curl 'http://127.0.0.1:8881/wp-cron.php?doing_wp_cron'`. The context is logged to option `helphub_spike_context_log`.
Run `wp option update helphub_spike_no_etag 1` to force a full re-fetch.
