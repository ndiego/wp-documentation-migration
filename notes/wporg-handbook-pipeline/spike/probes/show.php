<?php
// wp eval-file probes/show.php <slug> [raw|render|both]
// Prints title / excerpt / stored post_content and/or the_content-rendered HTML for a helphub_doc.
$slug = $args[0];
$mode = $args[1] ?? 'both';
$p    = get_posts( array( 'post_type' => 'helphub_doc', 'name' => $slug, 'post_status' => 'any', 'numberposts' => 1 ) );
if ( ! $p ) {
	WP_CLI::error( "no post $slug" );
}
$p = $p[0];
echo "ID: {$p->ID}\nTITLE: " . var_export( $p->post_title, true ) . "\nEXCERPT: {$p->post_excerpt}\nMODIFIED: {$p->post_modified}\n";
if ( 'render' !== $mode ) {
	echo "----- STORED post_content -----\n{$p->post_content}\n";
}
if ( 'raw' !== $mode ) {
	global $post;
	$post = $p;
	setup_postdata( $p );
	echo "----- RENDERED the_content -----\n" . apply_filters( 'the_content', $p->post_content ) . "\n";
}
