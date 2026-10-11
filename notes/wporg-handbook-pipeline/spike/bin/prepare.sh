#!/bin/bash
# Install importer + spike plugin into the native WP, and copy docs (md + manifest only) to a served dir.
# Usage: prepare.sh <spike-dir> <project-docs-dir>
set -euo pipefail
S="$1"; DOCS="$2"
P="$S/wp/wp-content/plugins"
rm -rf "$P/wporg-markdown" "$P/helphub-spike-importer"
mkdir -p "$P/wporg-markdown"
cp -R "$S/upstream/plugin.php" "$S/upstream/inc" "$P/wporg-markdown/"
cp -R "$S/helphub-spike-importer" "$P/helphub-spike-importer"
rm -rf "$S/served"; mkdir -p "$S/served"
rsync -a --include='*/' --include='*.md' --include='manifest.json' --exclude='*' --exclude='assets/' "$DOCS/" "$S/served/"
find "$S/served" -name '*.md' | wc -l
WP="php -d memory_limit=1G /opt/homebrew/bin/wp --path=$S/wp"
$WP plugin activate jetpack wporg-markdown helphub-spike-importer
$WP rewrite flush
