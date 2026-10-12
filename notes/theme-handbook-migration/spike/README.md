# Theme Handbook import spike: how to rerun

This spike imports all 139 Theme Handbook pages into the local DevHub site, through the same
`wporg-markdown` importer used by the Block Editor, AAH and SCF handbooks. It then compares the
rendered result with production. The findings are in `../research/03-spike.md`.

## Contents

| Path | What |
|---|---|
| `scripts/fetch_prod.py` | Exports the 139 pages from the production REST API. With `--html` it also saves each rendered front-end page. |
| `scripts/convert_theme.py` | Converts HTML to Markdown and writes `manifest.json`. It wraps the repo converter (`scripts/convert.py`) and swaps in the DevHub-specific steps. |
| `scripts/serve.py` | Static server that sends ETags and answers 304, the way raw.githubusercontent.com does. Plain `http.server` sends no ETag, so every re-import would rewrite every post. |
| `scripts/fetch_local.sh` | Saves the local rendering of every production URL. |
| `scripts/compare.py` | Compares local with production for each page and writes `fidelity.json`. |
| `scripts/screenshots.mjs` | Takes side-by-side Playwright screenshots of the post content column. |
| `importer/import-theme.php` | Importer subclass (the final version from the spike branch). |
| `importer/functions.php.diff` | The `require` added to `functions.php`. |
| `manifest.json` | The generated manifest: 139 pages plus 1 private stub parent. |
| `samples/` | 8 of the 139 generated `.md` files. |
| `results/` | `fidelity.json` (final run), `convert-report.json`, and the manifest logs for Run A (vanilla importer) and Run B (fixed importer). |
| `screenshots/` | 5 side-by-sides (production left, local right). |

The code is also on the local-only branch `spike/theme-handbook-import` (commit `233c422`) in
`~/Developer/wordpress-org/wporg-developer`. That branch is cut from `upstream/trunk` and was not pushed.

## Rerun

Use a fresh scratch directory for data. Do not put fetched data next to the scripts.

```sh
SP=~/Developer/wp-documentation-migration/notes/theme-handbook-migration/spike
PY=~/Developer/wp-documentation-migration/.venv/bin/python   # bs4 + markdownify + pyyaml
D=/path/to/scratch/data; mkdir -p $D

# 1. Export production: pages.json and prod-html/ (about 1 minute; 0.3 s between requests)
python3 -I $SP/scripts/fetch_prod.py $D --html

# 2. Convert (about 1 s). Output goes to $D/serve/md/ (Markdown + manifest.json).
$PY -I $SP/scripts/convert_theme.py --pages $D/pages.json --out $D/serve

# 3. Serve it to the container (binds 0.0.0.0:8765)
python3 -I $SP/scripts/serve.py $D/serve 8765 &

# 4. Switch DevHub to the spike branch. Check the container can reach the server.
cd ~/Developer/wordpress-org/wporg-developer
git switch spike/theme-handbook-import
npx wp-env run cli curl -s http://host.docker.internal:8765/md/manifest.json | head

# 5. Import (about 2 s total; each failed fetch adds a 5 s timeout, see 03-spike.md)
npx wp-env run cli wp eval 'do_action("devhub_theme_import_manifest");'
npx wp-env run cli wp eval 'do_action("devhub_theme_import_all_markdown");'
#    Run the markdown step again until it reports 139 of 139 (Docker networking drops the odd request).

# 6. Measure
bash $SP/scripts/fetch_local.sh $D
$PY -I $SP/scripts/compare.py $D            # writes $D/fidelity.json
node $SP/scripts/screenshots.mjs $D/shots   # optional; takes paths below /themes/ as extra args

# 7. Leave the site as you found it
npx wp-env run cli wp post delete $(npx wp-env run cli wp post list --post_type=theme-handbook --post_status=any --format=ids) --force
git switch add/copy-page-sidebar
npx wp-env run cli wp cron event unschedule devhub_theme_import_manifest
npx wp-env run cli wp cron event unschedule devhub_theme_import_all_markdown
```

Notes:

- **Reproducing Run A.** To see the stock importer fail, replace `import-theme.php` with a class that has
  only `init()` (do_init `'theme', 'themes', <manifest url>`), like `import-scf.php`.
- **WP-Cron.** `DISABLE_WP_CRON` is not set locally. While the spike branch is checked out, the two
  `devhub_theme_*` cron events are scheduled every 15 minutes, and any page load can run them.
- **Forcing a re-render.** After changing the importer subclass, clear the stored ETags. Otherwise
  unchanged files return 304 and keep their old HTML:
  `wp eval 'foreach(get_posts(["post_type"=>"theme-handbook","post_status"=>"any","numberposts"=>-1,"fields"=>"ids"]) as $id) delete_post_meta($id,"wporg_markdown_etag");'`
- **Relative sources.** `markdown_source` values in `manifest.json` are relative. The importer resolves
  them against the manifest's directory, and treats anything not starting with `https://` as
  relative, so an absolute `http://` URL would break.
