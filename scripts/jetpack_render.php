<?php
/**
 * Render docs/ Markdown exactly like the wporg-markdown Importer would (frontmatter strip, H1 title
 * extraction, Jetpack WPCom_GHF_Markdown_Parser), without WordPress. Used for QA.
 *
 * Setup (parser not vendored; fetch into a scratch dir):
 *   mkdir -p $JP/_inc/lib/markdown && for f in markdown.php markdown/extra.php markdown/gfm.php; do
 *     curl -sfL -o $JP/_inc/lib/$f https://raw.githubusercontent.com/Automattic/jetpack/trunk/projects/plugins/jetpack/_inc/lib/$f; done
 * Usage:
 *   php scripts/jetpack_render.php $JP docs/some/file.md          # print HTML
 *   php scripts/jetpack_render.php $JP docs $OUT_DIR              # render all, then:
 *   .venv/bin/python -I scripts/qa_textdiff.py --rendered $OUT_DIR
 */
// Minimal harness: replicate wporg-markdown Importer::update_post_from_markdown_source() steps
// (frontmatter strip, H1 title extraction, WPCom_GHF_Markdown_Parser) without WordPress.
define( 'ABSPATH', '/' );
define( 'JETPACK__PLUGIN_DIR', $argv[1] );
function apply_filters( $tag, $value ) { return $value; }
function esc_html( $s ) { return htmlspecialchars( $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr__( $s ) { return $s; }
function esc_attr( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function __( $s ) { return $s; }
function esc_html__( $s ) { return $s; }
require JETPACK__PLUGIN_DIR . '/_inc/lib/markdown.php';
function render_md( $markdown ) {
$markdown = preg_replace( '#^---(.+)---#Us', '', $markdown );
$markdown = trim( $markdown );
$title = null;
if ( preg_match( '/^#\s(.+)/', $markdown, $m ) ) {
	$title = $m[1];
	$markdown = preg_replace( '/^#\s(.+)/', '', $markdown );
}
$markdown = trim( $markdown );
$parser = new WPCom_GHF_Markdown_Parser();
$parser->preserve_shortcodes = false;
$html = $parser->transform( $markdown );
return "<!-- TITLE: $title -->\n" . $html;
}

if ( is_dir( $argv[2] ) ) {
	$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $argv[2] ) );
	$n = 0;
	foreach ( $it as $f ) {
		if ( substr( $f, -3 ) !== '.md' ) { continue; }
		$rel = substr( $f, strlen( rtrim( $argv[2], '/' ) ) + 1 );
		$out = rtrim( $argv[3], '/' ) . '/' . substr( $rel, 0, -3 ) . '.html';
		@mkdir( dirname( $out ), 0777, true );
		file_put_contents( $out, render_md( file_get_contents( $f ) ) );
		$n++;
	}
	echo "rendered $n files\n";
} else {
	echo render_md( file_get_contents( $argv[2] ) );
}
