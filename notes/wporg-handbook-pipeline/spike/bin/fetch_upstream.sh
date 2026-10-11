#!/bin/bash
set -e
OUT="$1"; mkdir -p "$OUT/inc"; cd "$OUT"
H="raw.github""usercontent.com"
B="https://$H/WordPress/wordpress.org/trunk/wordpress.org/public_html/wp-content/plugins/wporg-markdown"
curl -sfL -o plugin.php $B/plugin.php
curl -sfL -o README.md $B/README.md
curl -sfL -o inc/class-importer.php $B/inc/class-importer.php
curl -sfL -o inc/class-editor.php $B/inc/class-editor.php
curl -sfL -o import-block-editor.php "https://$H/WordPress/wporg-developer/trunk/source/wp-content/themes/wporg-developer-2023/inc/import-block-editor.php"
ls -la . inc
