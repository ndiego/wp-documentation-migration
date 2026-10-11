#!/bin/bash
# Native (no Docker) WordPress + SQLite setup for the importer spike.
# Usage: setup-native.sh <spike-dir>   (expects <spike-dir>/wp with core downloaded and plugins unzipped)
set -euo pipefail
S="$1"
WPDIR="$S/wp"
WP="php -d memory_limit=1G /opt/homebrew/bin/wp --path=$WPDIR"
SQ="$WPDIR/wp-content/plugins/sqlite-database-integration"
sed -e "s#{SQLITE_IMPLEMENTATION_FOLDER_PATH}#$SQ#" -e "s#{SQLITE_PLUGIN}#sqlite-database-integration/load.php#" "$SQ/db.copy" > "$WPDIR/wp-content/db.php"
rm -f "$WPDIR/wp-config.php"
$WP config create --dbname=wp --dbuser=x --dbpass=x --skip-check --extra-php <<'EOF'
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', __DIR__ . '/wp-content/debug.log' );
define( 'WP_DEBUG_DISPLAY', true );
define( 'DISABLE_WP_CRON', true );
EOF
$WP core install --url=http://localhost:8881 --title=Spike --admin_user=admin --admin_password=admin --admin_email=a@example.com --skip-email
$WP rewrite structure '/%postname%/'
$WP plugin list
